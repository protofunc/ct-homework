from flask import render_template, request, flash, redirect, url_for
import requests
from app.blueprints.main.forms import PokeForm, TeamForm
from app.blueprints.main import main
from flask_login import login_required, current_user
from ...models import User, Pokemon, poke_team
import random

'''Global attributes'''
poke_db_dict = {}

'''Home route'''
@main.route("/")
@login_required
def home():
    users = User.query.all()
    # Following values
    following_set = set()
    for user in current_user.followed:
        following_set.add(user)
    
    for user in users:
        if user in following_set:
            user.isFollowing = True

    return render_template('home.html', users=users)

'''Catch pokemon route'''
@main.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = PokeForm()
    
    # catch pokemon after they've been searched in the API
    if request.form.get('catch') and request.method == 'POST':       
        # check to see if user exceeds max pokemon amount
        if current_user.poke_count < 5:
            # create new instance of Pokemon and save stats to db
            new_poke = Pokemon()
            new_poke.from_dict(poke_db_dict)
            new_poke.save_to_db()

            # Add to team -- need to work out team_add functionality
            current_user.team_add(new_poke)
            flash(f'Pokemon successuffly caught! {new_poke.poke_name.title()} has been added to your team, {current_user.first_name}.', 'success')
            
            # ---- TEST: See if get_team function works ----
            get_team(current_user.id)
            # ---------------- END TEST -----------------------
        else:
            flash('Max amount of pokemon reached!', 'danger')
            # ---- TEST: See if get_team function works ----
            get_team(current_user.id)
            # ---------------- END TEST -----------------------
            return redirect(url_for('main.pokemon'))
        
    # take user input to search against the pokemon api
    if request.form.get('submit') and request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        response = requests.get(url)        
        
        # display output to tables
        if response.ok:
            poke = response.json()
            poke_data = []
            poke_dict = { 
                'name': poke['forms'][0]['name'],
                'ability': poke['abilities'][0]['ability']['name'],
                'base_experience': poke['base_experience'],
                'sprite URL': poke['sprites']['front_shiny'],
                'attack base_stat': poke['stats'][1]['base_stat'],
                'hp base_stat': poke['stats'][0]['base_stat'],
                'defense base_stat': poke['stats'][3]['base_stat']
            }
            # add dict to list and store dict in global variable 
            poke_data.append(poke_dict)    
            set_dict(poke_dict)
            return render_template('pokemon.html', form=form, poke_data=poke_data)
        
        else:
            error = 'Incorrect pokemon name.'
            flash(error, 'danger')
            return render_template('pokemon.html', form=form) 

    return render_template('pokemon.html', form=form)

'''Display team of pokemon route'''
@main.route('/pokemon/my_team/<int:user_id>', methods=['GET', 'POST'])
@login_required
def my_team(user_id):
    form = TeamForm()
    team_data = get_team(user_id)
    if request.form.get('drop') and request.method == 'POST':
        t_num = request.form.get('team_number')
        drop_poke = get_poke(user_id)
        current_user.team_remove(drop_poke[int(t_num)])
        flash(f'Pokemon dropped.', 'success')
        return redirect(url_for('main.my_team', user_id=current_user.id))
    if team_data:
        return render_template('my_team.html', team_data=team_data, form=form)
    else:
        flash('You do not have any pokemon on your team!', 'warning')
        return render_template('my_team.html', team_data=team_data, form=form)
    

'''Battle route'''
@main.route('/battle/<int:user_id>', methods=['GET', 'POST'])
@login_required
def battle(user_id):
    opps = User.query.get(int(user_id))
    my_team = get_team(current_user.id)
    opps_team = get_team(user_id)
    if request.method == 'POST':
        # get ea team's stats
        my_fight = get_stats(my_team)
        opps_fight = get_stats(opps_team)
        print(my_fight, opps_fight)
        # Battle pokemon!!
        while my_fight['hp'] > 0 and opps_fight['hp'] > 0:
            if random.randint(1,10) <= 5:
                opps_fight['hp'] -= my_fight['atk']
                print(f'You attacked! Opponent HP: {opps_fight["hp"]}.')
            else:
                my_fight['hp'] -= opps_fight['atk']
                print(f'Your opponent attacked! Your HP: {my_fight["hp"]}.')
            if my_fight['hp'] <= 0:
                flash('Your team lost, better luck next time!', 'danger')
            if opps_fight['hp'] <= 0:
                flash('Your team won this pokemon battle!', 'success')
        
    if opps_team and my_team:
        return render_template('arena.html', opps_team=opps_team, my_team=my_team, opps=opps)
    else:
        flash('One of the teams does not have any pokemon!', 'danger')
        return render_template('arena.html', opps_team=opps_team, my_team=my_team, opps=opps)

# ----- GET AND SET FUNCTIONS / NON-ROUTES -----
'''function to capture dictionary values'''
def set_dict(poke_dict):
    global poke_db_dict
    poke_db_dict = {
        'poke_name': poke_dict['name'],
        'ability': poke_dict['ability'],
        'sprite_url': poke_dict['sprite URL'],
        'exp': poke_dict['base_experience'],
        'attack': poke_dict['attack base_stat'],
        'hp': poke_dict['hp base_stat'],
        'defense': poke_dict['defense base_stat']
    }

'''Display user pokemon'''
def get_team(uid):
    # save all the pokemon that belong to the user_id passed
    this_team = get_poke(uid)

    # add pokemon to a list so i can access them individually without calling the db
    full_team_list = []
    poke_in_team = {}
    for i in range(len(this_team)):
        poke_in_team = {
        'poke_name': this_team[i].poke_name,
        'ability': this_team[i].ability,
        'sprite_url': this_team[i].sprite_url,
        'exp': this_team[i].exp,
        'attack': this_team[i].attack,
        'hp': this_team[i].hp,
        'defense': this_team[i].defense,
        'team_num': i
        }
        full_team_list.append(poke_in_team)       
    return(full_team_list)

'''Get pokemon instance'''
def get_poke(uid):
    poke_instance = Pokemon.query\
        .join(poke_team, poke_team.c.poke_id == Pokemon.id)\
        .join(User, User.id == poke_team.c.user_id)\
        .filter(User.id == uid)\
        .all()
    return poke_instance

'''Get a team's battle stats'''
def get_stats(team):
    # get totals of ea respective team stats
    xp = 0
    atk = 0
    defense = 0
    hp = 0
    for stats in team:
        xp += stats['exp']
        atk += stats['attack']
        defense += stats['defense']
        hp += stats['hp']
    
    # use xp and defense as multipliers to atk and hp
    xp = xp * .001
    atk = atk + (atk * xp)
    defense = defense * .01
    hp = hp + (hp * defense)

    # save atk and hp to list
    team_stats = {
            'atk': atk,
            'hp': hp
    }
    return team_stats
    

# # --- TEST: Print output of team list  ---
# print(f'**** START OUTPUT *****\nPrinting: {full_team_list}\n**** END OUTPUT *****')
# # ------------- End Test -----------------
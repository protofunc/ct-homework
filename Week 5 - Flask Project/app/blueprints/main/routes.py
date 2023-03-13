from app import db
from flask import render_template, request, flash, redirect, url_for
import requests
from app.blueprints.main.forms import PokeForm
from app.blueprints.main import main
from flask_login import login_required, current_user
from ...models import User, Pokemon, poke_team

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
        if current_user.poke_count < 6:
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
@main.route('/pokemon/my_team/<int:user_id>', methods=['GET'])
@login_required
def my_team(user_id):
    team_data = get_team(user_id)
    if team_data:
        return render_template('my_team.html', team_data=team_data)
    else:
        flash('You do not have any pokemon on your team!', 'warning')
        return render_template('my_team.html', team_data=team_data)

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
    this_team = Pokemon.query\
        .join(poke_team, poke_team.c.poke_id == Pokemon.id)\
        .join(User, User.id == poke_team.c.user_id)\
        .filter(User.id == uid)\
        .all()

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
        'defense': this_team[i].defense
        }
        full_team_list.append(poke_in_team)       

    # --- TEST: Print output of team list  ---
    print(f'**** START OUTPUT *****\nPrinting: {full_team_list}\n**** END OUTPUT *****')
    # ------------- End Test -----------------
    return(full_team_list)
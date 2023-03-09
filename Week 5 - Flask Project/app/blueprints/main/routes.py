from flask import render_template, request, flash, redirect, url_for
import requests
from app.blueprints.main.forms import PokeForm
from app.blueprints.main import main
from flask_login import login_required, current_user
from ...models import User, Pokemon

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

'''Pokemon API route'''
@main.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = PokeForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        response = requests.get(url)
        
        # Display to tables
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
            poke_data.append(poke_dict)

            '''Save pokemon to pokemon db if catch button selected'''
            # ------- Save Pokemon to DB ------- #
            if poke_dict:
                # Created new db dict instead of using poke_dict because i didn't want to go through the other files and update the name change. Refactor later.
                poke_db_dict = {
                    'poke_name': poke_dict['name'],
                    'ability': poke_dict['ability'],
                    'sprite_url': poke_dict['sprite URL'],
                    'exp': poke_dict['base_experience'],
                    'attack': poke_dict['attack base_stat'],
                    'hp': poke_dict['hp base_stat'],
                    'defense': poke_dict['defense base_stat']
                }

                # Verify dict is same naming convention as pokemon model paramaters

                print(poke_db_dict)

                # # Create instance of pokemon
                # new_poke = Pokemon()

                # # Implementing values from our form data for our instance
                # new_poke.from_dict(poke_db_dict)

                # # Save user to database
                # new_poke.save_to_db()

            return render_template('pokemon.html', form=form, poke_data=poke_data)
        
        else:
            error = 'Incorrect pokemon name.'
            flash(error, 'danger')
            return render_template('pokemon.html', form=form) 
    
    return render_template('pokemon.html', form=form)
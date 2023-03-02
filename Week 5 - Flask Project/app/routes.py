from flask import render_template, request
import requests
from .forms import PokeForm, LoginForm, RegisterForm
from app import app

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        if email in app.config.get('REGISTERED_USERS') and password == app.config.get('REGISTERED_USERS').get(email).get('password'):
            return f"Successfully logged in. Hello, {app.config.get('REGISTERED_USERS').get(email).get('name')}."
        else:
            error = "Invalid email or password."
            return render_template('login.html', error=error, form=form)
    return render_template('login.html', form=form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        return 'Success.'
    return render_template('register.html', form=form)

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    form = PokeForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        response = requests.get(url)
        '''Test input and api accessiblity'''
        print(name)
        print(url)
        print(response.ok)
        '''Test printed to terminal'''
        
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
            return render_template('pokemon.html', form=form, poke_data=poke_data)
        else:
            error = 'Incorrect pokemon name.'
            return render_template('pokemon.html', form=form, error=error) 
    return render_template('pokemon.html', form=form)
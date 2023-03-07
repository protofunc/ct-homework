from flask import render_template, request, flash, redirect, url_for
import requests
from .forms import PokeForm, LoginForm, RegisterForm, EditProfileForm
from app import app
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

'''Home route'''
@app.route("/")
@login_required
def home():
    return render_template('home.html')

'''Login route'''
@app.route('/login', methods = ['GET', 'POST'])
def login():
    # Created from forms.py
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data

        # Query user from db
        queried_user = User.query.filter_by(email=email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Successfully logged in! Welcome back, {queried_user.first_name}!', 'success')            
            return redirect(url_for('home'))
        else:
            error = 'Incorrect Email/Password!'
            flash(f'{error}', 'danger')
            return render_template('login.html', error=error, form=form)
    return render_template('login.html', form=form)

'''Logout route'''
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out!', 'success')
        return redirect(url_for('login'))

'''Registration route'''
@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Grabbing our form data and storing into a dict
        new_user_data = {
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email': form.email.data.lower(),
            'password': form.password.data
        }

        # Create instance of User
        new_user = User()

        # Implementing values from our form data for our instance
        new_user.from_dict(new_user_data)

        # Save user to database
        new_user.save_to_db()

        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

'''Profile edit route'''
@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Grabbing our form data and storing into a dict
        this_user_data = {
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email': form.email.data.lower()
        }

        # Get user from DB to edit
        this_user = User.query.filter_by(email=this_user_data['email']).first()

        if this_user:
            flash('Email already exists', 'danger')
            return redirect(url_for('profile'))
        else:
            current_user.update_dict(this_user_data)
            current_user.save_to_db()
            flash('Profile updated.', 'success')
            return redirect(url_for('home'))
    return render_template('profile.html', form=form)

'''Pokemon API route'''
@app.route('/pokemon', methods=['GET', 'POST'])
@login_required
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
            return render_template('pokemon.html', form=form, poke_data=poke_data)
        else:
            error = 'Incorrect pokemon name.'
            return render_template('pokemon.html', form=form, error=error) 
    return render_template('pokemon.html', form=form)
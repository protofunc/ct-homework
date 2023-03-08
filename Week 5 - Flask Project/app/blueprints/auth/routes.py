from flask import render_template, request, flash, redirect, url_for
from app.blueprints.auth.forms import LoginForm, RegisterForm, EditProfileForm
from app.blueprints.auth import auth
from app.blueprints.main import routes
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

'''Login route'''
@auth.route('/login', methods = ['GET', 'POST'])
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
            return redirect(url_for('main.home'))
        else:
            error = 'Incorrect Email/Password!'
            flash(f'{error}', 'danger')
            return render_template('login.html', error=error, form=form)
    return render_template('login.html', form=form)

'''Logout route'''
@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out!', 'success')
        return redirect(url_for('auth.login'))
    
'''Registration route'''
@auth.route('/register', methods = ['GET', 'POST'])
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
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

'''Profile edit route'''
@auth.route('/profile', methods = ['GET', 'POST'])
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
            return redirect(url_for('auth.profile'))
        else:
            current_user.update_dict(this_user_data)
            current_user.save_to_db()
            flash('Profile updated.', 'success')
            return redirect(url_for('main.home'))
    return render_template('profile.html', form=form)

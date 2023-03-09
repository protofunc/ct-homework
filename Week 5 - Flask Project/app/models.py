from app import db, login
from flask_login import UserMixin # Only use UserMixin for the User Model
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

'''Followers table'''
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
'''Alternate way to do above'''
# class follower(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     follower_id = db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
#     followed_id = db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('User',
        secondary = followers,
        primaryjoin = (followers.columns.follower_id == id),
        secondaryjoin = (followers.columns.followed_id == id),
        backref= db.backref('followers', lazy='dynamic'),
        lazy = 'dynamic')

    # hashes our password
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # checks the hashed password
    def check_hash_password(self, login_password):
        return check_password_hash(self.password, login_password)
    
    # Use this method to register our user attributes
    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    # Update user attributes without prompting for password
    def update_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
    
    # Save the user to database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

'''Pokemon table'''
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poke_name = db.Column(db.String, nullable=False)
    ability = db.Column(db.String)
    sprite_url = db.Column(db.String)
    exp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    
    # Use this method to register our user attributes
    def from_dict(self, data):
        self.poke_name = data['poke_name']
        self.ability = data['ability']
        self.sprite_url = data['sprite_url']
        self.exp = data['exp']
        self.attack = data['attack']
        self.hp = data['hp']
        self.defense = data['defense']
    
    # Save the pokemon to database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

'''Table to bridge user and pokemon'''
poke_team = db.Table(
    'poke_team',
    db.Column('poke_id', db.Integer, db.ForeignKey('pokemon.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

'''Posting to the feed'''
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String, nullable=False)
    title = db.Column(db.String)
    caption = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # FK to User Table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Commit post to db
    def from_dict(self, data):
        self.img_url = data['img_url']
        self.title = data['title']
        self.caption = data['caption']
        self.user_id = data['user_id']

    # Save the user to database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
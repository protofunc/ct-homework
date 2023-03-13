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

'''Table to join user and pokemon'''
poke_team = db.Table(
    'poke_team',
    db.Column('poke_id', db.Integer, db.ForeignKey('pokemon.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

'''Pokemon table'''
class Pokemon(db.Model):
    # Attributes
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

    # Update to db
    def update_to_db(self):
        db.session.commit()

    # Delete from db
    def delete_post(self):
        db.session.delete(self)
        db.session.commit()

'''User table'''
class User(UserMixin, db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    poke_count = db.Column(db.Integer, default=0)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('User',
        secondary = followers,
        primaryjoin = (followers.columns.follower_id == id),
        secondaryjoin = (followers.columns.followed_id == id),
        backref = db.backref('followers', lazy='dynamic'),
        lazy = 'dynamic')
    
    # join User and Pokemon tables
    my_team = db.relationship('Pokemon',
        secondary = poke_team, 
        primaryjoin = (poke_team.columns.user_id == id),
        secondaryjoin = (poke_team.columns.poke_id == Pokemon.id),
        backref='team', 
        lazy='dynamic')

    # hashes our password
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # checks the hashed password
    def check_hash_password(self, login_password):
        return check_password_hash(self.password, login_password)
    
    # register user attributes
    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    # update user attributes without prompting for password
    def update_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
    
    # save the user to db
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Update user in db
    def update_to_db(self):
        db.session.commit()

    # follow user
    def follow_user(self, user):
        self.followed.append(user)
        db.session.commit()
    
    # unfollow user
    def unfollow_user(self, user):
        self.followed.remove(user)
        db.session.commit()

    # add pokemon to team, increase personal poke count by 1
    def team_add(self, new_poke):
        # Add the Pokemon instance to the my_team relationship
        self.my_team.append(new_poke)
        self.poke_count+=1
        db.session.commit()

    # remove pokemon from team
    def team_remove(self, dropped_poke):
        self.my_team.remove(dropped_poke)
        self.poke_count-=1
        db.session.commit()

'''Load user'''
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

'''Posting to the feed'''
class Post(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String, nullable=False)
    title = db.Column(db.String)
    caption = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # FK to User Table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # commit post to db
    def from_dict(self, data):
        self.img_url = data['img_url']
        self.title = data['title']
        self.caption = data['caption']
        self.user_id = data['user_id']

    # save the user to database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # update db
    def update_to_db(self):
        db.session.commit()

    # delete from db
    def delete_post(self):
        db.session.delete(self)
        db.session.commit()
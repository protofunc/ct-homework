from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment

# Init packages
login = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()

# Create app
def create_app():
    # Init app
    app = Flask(__name__)
    
    # Config link
    app.config.from_object(Config)

    # Register packages
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    # Config login
    login.login_view = 'auth.login'
    login.login_message = 'Please log into your account.'
    login.login_message_category = 'warning'

    # Import blueprints
    from app.blueprints.main import main
    from app.blueprints.auth import auth
    from app.blueprints.posts import posts

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(posts)

    return app
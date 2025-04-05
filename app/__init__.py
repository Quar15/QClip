import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from . import models


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Ensure required dirs exist
    upload_dir = app.config['UPLOAD_DIRECTORY']
    if not os.path.isdir(upload_dir):
        os.makedirs(upload_dir)

    thumbnail_dir = app.config['THUMBNAIL_DIRECTORY']
    if not os.path.isdir(thumbnail_dir):
        os.makedirs(thumbnail_dir)

    from .blueprints.main.routes import main
    from .blueprints.users.routes import users
    from .blueprints.videos.routes import videos
    from .blueprints.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(videos)
    app.register_blueprint(errors)

    return app

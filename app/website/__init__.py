from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME= "database.db"


def create_app():
    app = Flask(__name__)
    ref_path = path.dirname(path.realpath(__file__))
    database_path = path.join(ref_path, f'../{DB_NAME}')

    app.config['SECRET_KEY'] = 'shreehari-app-experiment'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from . models import User, Password_store

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))



    return app


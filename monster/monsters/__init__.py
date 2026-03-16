from flask import Flask
import os
from dotenv import load_dotenv
from monster.extensions import db, login_manager, bcrypt

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mhw_iceborne_secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login' 
    bcrypt.init_app(app)

    from monster.models import User, Monsterelement

    from monster.core.routes import core_bp
    from monster.users.routes import users_bp
    from monster.monsters.routes import monster_db

    app.register_blueprint(core_bp)
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(monster_db, url_prefix='/monsters')

    return app
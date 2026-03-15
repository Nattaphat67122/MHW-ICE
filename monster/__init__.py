import os
from flask import Flask 
from monster.extensions import db, login_manager, bcrypt
from dotenv import load_dotenv

load_dotenv() # โหลดไฟล์ .env

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    # 1. เริ่มทำงานกับ Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message = 'Please login to access this page.'
    login_manager.login_message_category = 'warning'

    # 2. นำเข้า Models และ Blueprints ไว้ข้างในนี้
    with app.app_context():
        from monster.models import User, Monsterelement
        from monster.core.routes import core_bp
        from monster.users.routes import users_bp
        from monster.monsters.routes import monster_db

        # 3. จดทะเบียน Blueprints
        app.register_blueprint(core_bp, url_prefix='/')
        app.register_blueprint(users_bp, url_prefix='/users')
        app.register_blueprint(monster_db, url_prefix='/monsters')

    return app
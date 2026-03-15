from flask import Flask
import os
from dotenv import load_dotenv
from monster.extensions import db, login_manager, bcrypt

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mhw_iceborne_secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    # เริ่มทำงานกับ Extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login' 
    bcrypt.init_app(app)

    # นำเข้า models เพื่อให้ Flask รู้จักตาราง
    from monster.models import User, Monsterelement

    # --- เพิ่มส่วนนี้เข้าไปครับ ---
    # 1. นำเข้า Blueprints จากไฟล์ routes ต่างๆ
    from monster.core.routes import core_bp
    from monster.users.routes import users_bp
    from monster.monsters.routes import monster_db

    # 2. จดทะเบียน Blueprints ให้แอป Flask รู้จัก
    app.register_blueprint(core_bp)
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(monster_db, url_prefix='/monsters')
    # --------------------------

    return app
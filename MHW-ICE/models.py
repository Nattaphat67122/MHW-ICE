from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class MonsterElement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    main_element = db.Column(db.String(50))  # ธาตุประจำตัว
    # เก็บจุดอ่อนเป็นตัวเลข 0-3 (แทนจำนวนดาวในเกม)
    fire_weak = db.Column(db.Integer, default=0)
    water_weak = db.Column(db.Integer, default=0)
    thunder_weak = db.Column(db.Integer, default=0)
    ice_weak = db.Column(db.Integer, default=0)
    dragon_weak = db.Column(db.Integer, default=0)
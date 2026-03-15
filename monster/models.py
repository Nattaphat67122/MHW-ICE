from monster.extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) 
    password = db.Column(db.String(200), nullable=False)
    
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    avatar = db.Column(db.String(200), default='default.png')

class Monsterelement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    main_element = db.Column(db.String(50))
    img_url = db.Column(db.String(500))
    description = db.Column(db.Text) 
    fire_weak = db.Column(db.Integer, default=0)
    water_weak = db.Column(db.Integer, default=0)
    thunder_weak = db.Column(db.Integer, default=0)
    ice_weak = db.Column(db.Integer, default=0)
    dragon_weak = db.Column(db.Integer, default=0)
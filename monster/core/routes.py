from flask import Blueprint, render_template, request
from monster.models import Monsterelement
from monster.extensions import db

core_bp = Blueprint('core', 
                    __name__,
                    template_folder='templates')

@core_bp.route('/')
def index():
    
    page = request.args.get('page', 1, type=int) 
    
   
    query = db.select(Monsterelement).order_by(Monsterelement.name)
    monsters_pagination = db.paginate(query, page=page, per_page=4)
    
    return render_template('core/index.html',
                           title='Home Page',
                           monsters=monsters_pagination)


@core_bp.route('/home')
def home():  
    return render_template('home.html')
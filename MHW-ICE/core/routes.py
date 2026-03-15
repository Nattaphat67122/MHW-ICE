from flask import Blueprint, render_template, request
from monster.models import Pokemon, Type, User
from monster.extensions import db

core_bp = Blueprint('core', 
                    __name__,
                    template_folder='templates')

@core_bp.route('/')
def index():
    page = request.args.get('page', type=int)
    query = db.select(monsters)
    monsters = db.paginate(query, page=page,per_page=4)
    return render_template('core/index.html',
                           title='Home Page',
                           monsters=monsters)
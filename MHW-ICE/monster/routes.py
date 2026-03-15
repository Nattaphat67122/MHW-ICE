from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from flask_sqlalchemy import query
from monster.models import Monster, Type, User
from monster.models import db

monster_db = Blueprint('monster_db', __name__, 
                       template_folder='templates')

@monster_db.route('/')
def index():
    query = db.select(Monster).where(Monster.user == current_user)
    monsters = db.session.scalars(query).all()
    return render_template('monsters/index.html',
                           title='Monster Page',
                           monsters=monsters)

@monster_db.route('/new', methods=['GET', 'POST'])
def new_monster():
    query = db.select(Type)
    types = db.session.scalars(query).all()
    if request.method == 'POST':
        name = request.form.get('name')
        height = request.form.get('height')
        weight = request.form.get('weight')
        description = request.form.get('description')
        img_url = request.form.get('img_url')
        user_id = current_user.id
        monster_types = request.form.getlist('monster_types')

        query = db.select(Monster).where(Monster.name==name)
        monster = db.session.scalar(query)
        if monster:
            flash(f'Monster :{monster.name} is already exists!', 'warning')
            return redirect(url_for('monster_db.new_monster'))
        else:
            M_types = []
            for id in monster_types:
                M_types.append(db.session.get(Type, id))
            monster = Monster(
                name = name,
                height = height,
                weight = weight,
                description = description,
                img_url = img_url,
                user_id = user_id,
                types=M_types

            )    
            db.session.add(monster)
            db.session.commit()
            flash('Add new monster successful!', 'success')
            return redirect(url_for('monster_db.index'))

    return render_template('monsters/new_monster.html',
                           title='New monster Page',
                           types=types)

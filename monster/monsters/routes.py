from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
import monster
from monster.models import ElementType, Monsterelement, User
from monster.extensions import db
from monster.models import db

monster_db = Blueprint('monster_db', __name__, 
                       template_folder='templates')

@monster_db.route('/')
def index():
    query = db.select(Monsterelement)
    monsters = db.session.scalars(query).all()
    return render_template('monster/index.html',
                           title='Monster Page',
                           monsters=monsters)


@monster_db.route('/new', methods=['GET', 'POST'])
def new_monster():
    if request.method == 'POST':
        name = request.form.get('name')
        selected_elements = request.form.getlist('main_elements') 

        query = db.select(Monsterelement).where(Monsterelement.name == name)
        monster = db.session.scalar(query)

        if monster:
            flash(f'Monster :{monster.name} is already exists!', 'warning')
            return redirect(url_for('monster_db.new_monster'))
        
        new_mon = Monsterelement(
            name = name,
            img_url = request.form.get('img_url'), 
            description = request.form.get('description'), 
            fire_weak = request.form.get('fire_weak', 0),
            water_weak = request.form.get('water_weak', 0),
            thunder_weak = request.form.get('thunder_weak', 0),
            ice_weak = request.form.get('ice_weak', 0),
            dragon_weak = request.form.get('dragon_weak', 0)
        )

        for ename in selected_elements:
            el = db.session.scalar(db.select(ElementType).where(ElementType.name == ename))
            if el:
                new_mon.elements.append(el)

        db.session.add(new_mon)
        db.session.commit()
        flash('เพิ่มข้อมูลมอนสเตอร์สำเร็จ!', 'success')
        return redirect(url_for('monster_db.index'))

    return render_template('monster/new_monster.html', title='New monster Page')

@monster_db.route('/view/<int:monster_id>', endpoint='view')
@monster_db.route('/detail/<int:monster_id>')
def monster_detail(monster_id):
    res = db.session.get(Monsterelement, monster_id)
    
    if res is None:
        flash('ไม่พบข้อมูลมอนสเตอร์', 'warning')
        return redirect(url_for('monster_db.index'))

    return render_template('monster/monster_detail.html', 
                           monster=res, 
                           title=res.name)

@monster_db.route('/delete/<int:monster_id>', methods=['POST'])
def delete_monster(monster_id):
    monster = db.session.get(Monsterelement, monster_id)
    
    if monster:
        db.session.delete(monster)
        db.session.commit()
        flash(f'ลบข้อมูล {monster.name} เรียบร้อยแล้ว!', 'success')
    else:
        flash('ไม่พบข้อมูลมอนสเตอร์ที่ต้องการลบ', 'danger')
        
    return redirect(url_for('monster_db.index'))

@monster_db.route('/edit/<int:monster_id>', methods=['GET', 'POST'])
def edit_monster(monster_id):
    monster = db.session.get(Monsterelement, monster_id)
    if not monster:
        flash('ไม่พบข้อมูลมอนสเตอร์', 'danger')
        return redirect(url_for('monster_db.index'))

    if request.method == 'POST':
        monster.name = request.form.get('name')
        monster.img_url = request.form.get('img_url')
        monster.description = request.form.get('description')

        monster.fire_weak = request.form.get('fire_weak', 0)
        monster.water_weak = request.form.get('water_weak', 0)
        monster.thunder_weak = request.form.get('thunder_weak', 0)
        monster.ice_weak = request.form.get('ice_weak', 0)
        monster.dragon_weak = request.form.get('dragon_weak', 0)

        monster.elements = []
        selected_elements = request.form.getlist('main_elements')
        for ename in selected_elements:
            el = db.session.scalar(db.select(ElementType).where(ElementType.name == ename))
            if el:
                monster.elements.append(el)

        db.session.commit()
        flash(f'แก้ไขข้อมูล {monster.name} สำเร็จ!', 'success')
        return redirect(url_for('monster_db.index'))

    return render_template('monster/edit_monster.html', monster=monster, title='Edit Monster')
    
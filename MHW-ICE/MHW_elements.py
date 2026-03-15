elements = [ 
    'Fire', 'Water', 'Thunder', 'Ice', 'Dragon'
    
]

from monster.models import Type
from monster.extensions import db
def create_monster_elements():
    for element in elements:
        new_element = Type(name=element)
        db.session.add(new_element)
    db.session.commit()
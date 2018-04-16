import sqlite3

from db import db

class TodoModel(db.Model):
    __tablename__ = 'todos'

    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(80))
    text        = db.Column(db.String(200))
    done        = db.Column(db.Boolean)

    def __init__(self, _id, username, text, done):
        self.id = _id
        self.username = username
        self.text = text
        self.done = done
    
    def json(self):
        return {'id': self.id, 'username': self.username, 'text': self.text, 'done': self.done}

    @classmethod
    def is_valid_id(cls, id):
        try:
            id = int(id)
            return id
        except:
            return False
    
    def check_autherized(self, modifier):
        return self.username == modifier
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

        return 
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

        return
    
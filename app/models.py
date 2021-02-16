from enum import unique
from app import db

class AddNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(120), unique=True)
    img_name = db.Column(db.String(32))
    img = db.Column(db.LargeBinary)

    def __repr__(self):
        return '{}'.format(self.title)
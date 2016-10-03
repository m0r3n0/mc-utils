from app import app, db
from flask_login import LoginManager, UserMixin
from hashlib import md5


class Wsdl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    url = db.Column(db.String(200))

    # printing user for debugging purposes
    def __repr__(self):
        return '<wsdl>' % (self.name)



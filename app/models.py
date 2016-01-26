from app import app, db
from flask_login import LoginManager, UserMixin
from hashlib import md5

# each table a class inherited from Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # printing user for debugging purposes
    def __repr__(self):
        return '<User %r>' % (self.nickname)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % \
               (md5(self.email.encode('utf-8')).hexdigest(), size)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   # FK to users

    def __repr__(self):
        return '<Post %r>' % (self.body)


# login section
lm = LoginManager(app)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


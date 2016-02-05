from app import app, db
from flask_login import LoginManager, UserMixin
from hashlib import md5


# create the N:M relation table for followers using the low-level API as there
# is no data in this table, just foreign keys
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


# each table a class inherited from Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    # printing user for debugging purposes
    def __repr__(self):
        return '<User %r>' % (self.nickname)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % \
               (md5(self.email.encode('utf-8')).hexdigest(), size)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # self follow a new user if not already following
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    # self unfollows an already followed user
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).\
            filter(followers.c.follower_id == self.id).\
            order_by(Post.timestamp.desc())

    def following(self):
        return User.query.join(followers, (followers.c.followed_id == User.id)).filter(followers.c.follower_id == self.id)

    def followed_by(self):
        return User.query.join(followers, (followers.c.follower_id == User.id)).filter(followers.c.followed_id == self.id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   # FK to users

    def __repr__(self):
        return '<Post %r>' % (self.body)


class fordward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)

    def __repr__(self):
        return '<forward: %r>' % (self.name)

# login section
lm = LoginManager(app)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


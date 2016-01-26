import os

basedir = os.path.abspath(os.path.dirname(__file__))

# FORMS Config
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# Auxiliary
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

# SQL Config
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

#OAuth
FCBK = 'facebook'

OAUTH_CREDENTIALS = {
    FCBK: {'id': '925788830810075', 'secret': '3abd1341f0596dcfb75090f27346fb1b'},
    'Twitter': {'id': '', 'secret': ''},
    'Google': {'id': '', 'secret': ''}
}

ROOT = {
    'name': 'root',
    'pwd': 'eloy',
    'email': 'moreno79@gmail.com'
}

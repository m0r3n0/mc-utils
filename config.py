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

INTERNAL = 'internal$'
DEFAULT_EMAIL = '@nodomain.com'


# LOGGING
LOCAL_SMTP = {'SERVER': 'localhost', 'PORT': 25, 'USERNAME': None, 'PASSWORD': None}
GMAIL_SMTP = {'SERVER': 'smtp.gmail.com', 'PORT': 465, 'USE_TLS':False, 'USE_SSL': True,
              'USERNAME': os.environ.get('GMAIL_USER'),'PASSWORD': os.environ.get('GMAIL_PWD')}
ADMINS = ['moreno79@gmail.com']
local_smtp = True
if local_smtp:
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
else:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    USE_TLS = False
    USE_SSL = True
    MAIL_USERNAME = os.environ.get('GMAIL_USER')
    MAIL_PASSWORD = os.environ.get('GMAIL_PWD')


# PAGINATION
POSTS_PER_PAGE = 3
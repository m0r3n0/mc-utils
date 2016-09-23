from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import LOCAL_SMTP, ADMINS
from flask.ext.mail import Mail
from .momentjs import momentjs
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)
app.jinja_env.globals['momentjs']=momentjs
babel = Babel(app)

from app import models, views

###### email log
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if LOCAL_SMTP['USERNAME'] or LOCAL_SMTP['PASSWORD']:
        credentials = (LOCAL_SMTP['USERNAME'], LOCAL_SMTP['PASSWORD'])
    mail_handler = SMTPHandler((LOCAL_SMTP['SERVER'], LOCAL_SMTP['PORT']), 'no-reply@' + LOCAL_SMTP['SERVER'],
                               ADMINS, 'microblog crash', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


###### email log
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import MAIL, ADMINS

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import models, views

###### email log
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL['USERNAME'] or MAIL['PASSWORD']:
        credentials = (MAIL['USERNAME'], MAIL['PASSWORD'])
    mail_handler = SMTPHandler((MAIL['SERVER'], MAIL['PORT']), 'no-reply@' + MAIL['SERVER'],
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



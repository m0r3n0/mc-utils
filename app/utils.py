from .models import User

def users():
    users = User.query.all()
    for u in users:
        print('<User: ' + str(u.nickname) + ' | ' + str(u.social_id) + ' | ' + str(u.email) + ' | ' + str(u.about_me) + '>')
        print(u.avatar(128))



def test_email():

    from flask.ext.mail import Message
    from app import app, mail
    from config import ADMINS

    msg = Message('text subject', sender=ADMINS[0], recipients=ADMINS)
    msg.body = 'text body'
    msg.html = '<b>HTML</b> body'
    with app.app_context():
        mail.send(msg)



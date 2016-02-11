from flask.ext.mail import Message
from app import app, mail
from flask import render_template
from config import ADMINS
from threading import Thread
from .decorators import async


def send_async_email(app, msg):

    '''Because it is a separate thread, the application context required by Flask-Mail will not be
    automatically set for us, so the app instance is passed to the thread, and the application context
    is set up manually, like we did above when we sent an email from the Python console.'''
    with app.app_context():
        mail.send(msg)


@async
def send_async_email2(app, msg):

    '''Because it is a separate thread, the application context required by Flask-Mail will not be
    automatically set for us, so the app instance is passed to the thread, and the application context
    is set up manually, like we did above when we sent an email from the Python console.'''
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_boxy, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_boxy
    msg.html = html_body
    # asyncronous call with threads
    #thr = Thread(target=send_async_email, args=[app, msg])
    #thr.start()
    # syncronous call with no threads
    #mail.send(msg)     syncronous email delivery
    # asyncronous call with decorator @async
    send_async_email2(app, msg)

def follower_notification(followed, follower):
    send_email('[microblog] %s is now following you!' % follower.nickname,
               ADMINS[0], [followed.email],
               render_template("follower_email.txt", user=followed, follower=follower),
               render_template("follower_email.html", user=followed, follower=follower))

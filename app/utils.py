from .models import User

def users():
    users = User.query.all()
    for u in users:
        print('<User: ' + str(u.nickname) + ' | ' + str(u.social_id) + ' | ' + str(u.email) + ' | ' + str(u.about_me) + '>')
        print(u.avatar(128))

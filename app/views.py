from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from .forms import RootLoginForm, UserLoginForm
from .models import User
from .oauth import OAuthSignIn

# root & default path
@app.route('/')
@app.route('/index')
def index():

    # fake contents to test the view
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was cool'
        }
    ]
    return render_template('index.html', title='Home', user=current_user, posts=posts)


############################# Login management
@app.route('/login', methods=['GET', 'POST'])
def login():
    # prepare root login form
    root_form = RootLoginForm()
    if root_form.validate_on_submit():     # root form submitted and validated
        root_login(str(root_form.root_pwd.data))
        return redirect(url_for('index'))
    # prepare user login form
    user_form = UserLoginForm()
    if user_form.validate_on_submit():     # user form submitted and validated
        user_login(str(user_form.username.data), str(user_form.user_pwd.data), user_form.remember_me.data)
        return redirect(url_for('index'))
    # otherwise, render form
    return render_template('login.html', title='Sign in', root_form=root_form, user_form=user_form, user=current_user)

# Login on a 3rd party
@app.route('/autorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

# callback login
@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed. No social_id back')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))

# logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Create new account
@app.route('/new_user')
def new_user():
    pass

# Auxiliary login functions
def root_login(pwd):
    if pwd == app.config['ROOT']['pwd']:    # pwd ok
        user = User.query.filter_by(nickname=app.config['ROOT']['name']).first()
        if not user:
            user = User(
                social_id=app.config['ROOT']['name'],
                nickname=app.config['ROOT']['name'],
                email=app.config['ROOT']['email']
            )
            db.session.add(user)
            db.session.commit()
        login_user(user, True)
    else:
        flash("Wrong password for " + app.config['ROOT']['name'])
        return redirect(url_for('login'))

def user_login(username, pwd, remember_me):
    ''' Validates user (not yet implemented) and logs in
    :param username:
    :param pwd:
    :return:
    '''
    user = User.query.filter_by(nickname=username).first()
    if not user:
        user = User(
            social_id='internal$' + username,
            nickname=username,
            email=username + '@nodomain.com'
        )
        db.session.add(user)
        db.session.commit()
    login_user(user, remember_me)


############################# Profile management
# show user profile page
@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found' % nickname)
        return(redirect('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)



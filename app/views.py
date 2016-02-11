from flask import render_template, flash, redirect, url_for, g, session
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.emails import follower_notification
from app.forms import EditProfileForm
from .forms import RootLoginForm, UserLoginForm, PostForm
from .models import User, Post
from .oauth import OAuthSignIn
from datetime import datetime


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


# root & default path
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page=1):

    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=g.user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))

    # fake contents to test the view
    posts = []
    if g.user is not None and g.user.is_authenticated:
        #posts = g.user.followed_posts().all()
        posts = g.user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    return render_template('index.html', title='Home', user=current_user, posts=posts, form=form)


############################# Login management
@app.route('/login', methods=['GET', 'POST'])
def login():

    # check user is already logged in
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
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
    login_user(user)
    #login_user(user, True)     # remember user
    return redirect(url_for('index'))

# logout
@app.route('/logout')
@login_required
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
            autofollow(user)
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
            social_id=app.config['INTERNAL'] + username,
            nickname=username,
            email=username + app.config['DEFAULT_EMAIL']
        )
        db.session.add(user)
        db.session.commit()
        autofollow(user)
    login_user(user, remember_me)

def autofollow(user):
    user = user.follow(user)
    db.session.add(user)
    db.session.commit()

############################# Profile management
# show user profile page
@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found' % nickname)
        return(redirect('index'))
    posts = g.user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    following = user.following()
    followed_by = user.followed_by()
    return render_template('user.html', user=user, posts=posts, followers=followed_by, following=following)


@app.route('/edit', methods=['GET','POST'])
@login_required
def edit():
    form = EditProfileForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        g.user.email = form.email.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('user', nickname=g.user.nickname))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
        form.email.data = g.user.email
    return render_template('edit.html', form=form)


############################# Error management
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


############################# User relations
@app.route('/profiles')
def profiles():
    users = User.query.all()
    return render_template('profiles.html', users=users)


@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found' % nickname)
        return redirect(url_for('index'))
    if user is g.user:
        flash('You can\'t follow your self')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    follower_notification(user, g.user)
    flash('You are now following ' + nickname + '!')
    return redirect(url_for('user', nickname=nickname))


@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found' % nickname)
        return redirect(url_for('index'))
    if user is g.user:
        flash('You can\'t unfollow yourself')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + nickname + '!')
    return redirect(url_for('user', nickname=nickname))







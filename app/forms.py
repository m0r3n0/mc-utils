from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired

class RootLoginForm(Form):
    root_pwd = PasswordField('root_pwd', validators=[DataRequired()])


class UserLoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    user_pwd = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default = False)


class NewUserForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()]) # validación de confirmación?
    email = StringField('email', validators=[DataRequired()]) # validación de email?

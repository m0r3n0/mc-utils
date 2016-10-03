from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


class NewWsdlForm(Form):
    name = StringField('name', validators=[DataRequired()])
    url = StringField('url', validators=[DataRequired()])

class RetrieveWsdlInfo(Form):
    id = SelectField('id', coerce=int, validators=[DataRequired()])
    use_proxy = BooleanField('use_proxy', default=False)



# OLD FORMS
class RootLoginForm(Form):
    root_pwd = PasswordField('root_pwd', validators=[DataRequired()])


class UserLoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    user_pwd = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default = False)


class NewUserForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()]) # validación de confirmación?
    email = StringField('email', validators=[DataRequired()]) # validación de email? No hay en WTF


class EditProfileForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    email = StringField('email', validators=[DataRequired(), Length(min=6, max=100)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True


class PostForm(Form):
    post = StringField('post', validators=[DataRequired()])


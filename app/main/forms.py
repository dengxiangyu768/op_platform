from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import Required

class NameForm(FlaskForm):
    name = StringField('what is your name?',validators=[Required()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    user = StringField(validators=[Required()])
    password = PasswordField('Password',validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

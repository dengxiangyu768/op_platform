from flask_wtf import FlaskForm
from wtforms import TextAreaField,StringField,SubmitField,PasswordField,BooleanField,SelectField
from wtforms.validators import Required


class NameForm(FlaskForm):
    idc = SelectField('idc',validators=[Required()] , choices=[('0','yg'),('1','bj'),\
                                                               ('3','la'),('4','ea01'),\
                                                               ('5','cs'),('6','hd05')])
    service = SelectField('service',validators=[Required()] , choices=[('0','action'),('1','master'),\
                                                               ('2','access'),('3','proxyaction'),\
                                                               ('4','proxymaster'),('5','downloader')])  
     
    version = SelectField('version',validators=[Required()] , choices=[('0','230'),('1','231'),\
                                                               ('4','232'),('5','233')])  
    ip_list = TextAreaField('ip_list',validators=[Required()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    user = StringField(validators=[Required()])
    password = PasswordField('Password',validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

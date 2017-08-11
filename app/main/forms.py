#coding:utf-8
from flask_wtf import FlaskForm
from wtforms import TextAreaField,StringField,SubmitField,PasswordField,BooleanField,SelectField
from wtforms.validators import Required
from ..models import Role,Idc,Playbook

class DeployForm(FlaskForm):
#    idc = SelectField('idc',validators=[Required()] , choices=[('0','yg'),('1','bj'),\
#                                                               ('3','la'),('4','ea01'),\
#                                                               ('5','cs'),('6','hd05')])
    idc = SelectField('Idc', coerce=int)
    playbook = SelectField('Playbook', coerce=int)
    ip_list = TextAreaField('ip_list',description=u'每行一个ip',validators=[Required()])
    submit = SubmitField("Submit")
    def __init__(self,*args, **kwargs):
        super(DeployForm,self).__init__(*args, **kwargs)
        self.idc.choices = [(idc.id, idc.name) for idc in Idc.query.order_by(Idc.name).all()] 
        self.playbook.choices = [(playbook.id, playbook.name) for playbook in Playbook.query.order_by(Playbook.name).all()] 

class LoginForm(FlaskForm):
    user = StringField(validators=[Required()])
    password = PasswordField('Password',validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

class AddUserForm(FlaskForm):
    user = StringField(validators=[Required()])
    password = PasswordField('Password',validators=[Required()])
    role = SelectField('Role', coerce=int)
    submit = SubmitField('add user')
    def __init__(self,*args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()] 

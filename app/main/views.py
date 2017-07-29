from flask import render_template,session,redirect,url_for,flash
from flask_wtf import FlaskForm
from forms import NameForm,LoginForm
from . import main
from .. import db
from ..models import User
from flask_login import login_user,logout_user,login_required

@main.route('/login',methods=['GET','POST'])
def login():
     form = LoginForm()
     if form.validate_on_submit():
         user = User.query.filter_by(username=form.user.data).first()
         if user is not None and user.verify_password(form.password.data):
             login_user(user,form.remember_me.data)
             return redirect(url_for('main.index'))
         flash('Invalid username or password.')
     return render_template('login.html',form=form)
 
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/',methods=['GET','POST'])
@login_required
def index():
    form = NameForm()
    if form.validate_on_submit() :
        session['name'] = form.name.data
        return redirect(url_for('main.index')) 
    return render_template('index.html',form=form,name=session.get('name'))

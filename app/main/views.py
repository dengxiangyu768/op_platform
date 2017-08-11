from flask import render_template,session,redirect,url_for,flash,current_app,jsonify,request
from flask_wtf import FlaskForm
from forms import DeployForm,LoginForm,AddUserForm
from . import main
from .. import db
from ..models import User,Role,Idc,Playbook
from flask_login import login_user,logout_user,current_user,login_required
from .decorators import permission_required,admin_required

import time
from ..ansible.run import playbook_run
import os

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
    return render_template('index.html')


@main.route('/user',methods=['GET'])
@login_required
@admin_required
def user():
    user_message = [] 
    user_all = User.query.all()
    for i in user_all:
        role_name = Role.query.filter_by(id=i.role_id).first().name
        user_message.append({'id':i.id,'username':i.username,'role':role_name})
    return render_template('user.html',user_message=user_message)



@main.route('/adduser',methods=['GET','POST'])
@login_required
@admin_required
def adduser():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.user.data).first()
        if user is None:
            user = User()
            user.username = form.user.data
            user.password = form.password.data 
            user.role_id = form.role.data
            current_app.logger.info('add user %s role %s',user.username,user.role_id)
            user.save()
            return redirect(url_for('main.user'))
        else:
            flash('user is exist!!')   
            return redirect(url_for('main.user'))
    return render_template('adduser.html',form=form)

@main.route('/deluser/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def deluser(id):
    user = User.query.filter_by(id=id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('main.user')) 
    else:
        flash("user is not exists!!")
        return redirect(url_for('main.user')) 

# add 2017-08-09
@main.route('/deploy',methods=['GET','POST'])
@login_required
@admin_required
def deploy():
    form = DeployForm()
    if form.validate_on_submit():
        timestamp = int(time.time())
        idc = Idc.query.filter_by(id=form.idc.data).first()
        playbook = Playbook.query.filter_by(id=form.playbook.data).first()
        ip_list = form.ip_list.data.encode()
        lists = ip_list.replace('\r','').split('\n')
        playbook_run()
        current_app.logger.info("%s command %s %s %s",current_user.username,idc.name,playbook.name,lists)
        return redirect(url_for("main.deploy"))
    return render_template("deploy.html",form=form)

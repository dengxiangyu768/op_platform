from flask import render_template,redirect,request,url_for,flash
from . import auth
from flask_login import login_user,logout_user,login_required
from ..models import User
from ..forms import LoginForm


@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.user.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

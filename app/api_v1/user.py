from flask_httpauth import HTTPBasicAuth
from ..models import User,Role
from flask import g,jsonify
from .errors import unauthorized, forbidden
from . import api
from flask import request
from .decorators import permission_required,admin_required
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='app.log',
                filemode='a')
    

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token,password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.current_user = user
    return True


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user:
        return forbidder('Unconfirmed account')

@api.route('/user',methods=['GET','POST'])
@auth.login_required
@admin_required
def user():
    if request.method == "POST":    
        user_id = request.form['id']
        password = request.form['password']
        if user_id and password:
             user = User.query.filter_by(id=user_id).first()
             user.password = password
             user.save()
             logging.info("{user} update {password}".format(user=user,password=password))
             return jsonify({'result':'success','code':0})
        else:
             return jsonify({'result':'para error','code':1}) 
    if request.method == 'GET':
        user = g.current_user.username
        
        return jsonify({'result':'success','code':0,'message':user})

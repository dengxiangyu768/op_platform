from flask_httpauth import HTTPBasicAuth
from ..models import User
from flask import g,jsonify
from .errors import unauthorized, forbidden
from . import api

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


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

@api.route('/resource')
@auth.login_required
def resource():
    return jsonify({'version':'1.0','data':'hello'})

@api.before_request
@auth.login_required
def before_request():
    if not g.current_user:
        return forbidder('Unconfirmed account')

@api.route('/token')
def get_token():
    token = g.current_user.generate_auth_token(expiration=3600)
    return jsonify({'token':token.decode('ascii')})

from flask_httpauth import HTTPBasicAuth
from ..models import User
from flask import g,jsonify,current_app
from .errors import unauthorized, forbidden
from . import api

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token,password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            current_app.logger.info("%s verify_password failed",str(user))
            return False
    g.current_user = user
    return True


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user:
        return forbidder('Unconfirmed account')

@api.route('/token')
def get_token():
    token = g.current_user.generate_auth_token(expiration=3600)
    current_app.logger.info("%s get token",g.current_user)   
    return jsonify({'retcode':0,'result':'success','token':token.decode('ascii')})

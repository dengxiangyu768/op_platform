#coding:utf-8

from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,request,url_for



class Permission:
    publish = 0b0000000000000001
    deploy = 0b0000000000000010
    rollback = 0b0000000000000100
    admin = 0b1000000000000000


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    permissions = db.Column(db.Integer)

    @staticmethod
    def insert_roles():
        roles = {
            'user': (Permission.publish | Permission.deploy),
            'deployer': (Permission.publish |Permission.deploy | Permission.rollback),
            'admin': (Permission.admin)
        } 
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r]
            db.session.add(role)
        db.session.commit()


    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    role = db.relationship('Role',backref=db.backref('users_set', lazy='dynamic'))
  

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('password is not a readalbe attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %r>' % self.username

    def can(self,permissions):
        roles = Role.query.filter_by(id=self.role_id).first()
        role_permissions = roles.permissions
        return self.role_id is not None and \
            (role_permissions & permissions) == permissions 

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except: 
            return None # valid token, but expired
        return User.query.get(data['id'])

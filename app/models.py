from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

class Permission:
    publish = 0b0000000000000001
    deploy = 0b0000000000000010
    rollback = 0b0000000000000100
    admin = 0b1000000000000000


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role')
    default = db.Column(db.Boolean,default=False,index=True)
    permission = db.Column(db.Integer)

    @staticmethod
    def insert_roles():
        roles = {
            'user': (Permission.publish | Permission.deploy,True),
            'deployer': (Permission.publish |Permission.deploy | Permission.rollback,False),
            'admin': (0b1000000000000000,False)
        } 
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def can(self,permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions 

    def is_administrator(self):
        return self.can(Permission.admin)

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

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

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

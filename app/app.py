import os
from flask import Flask
from flask import request
from flask import render_template
from flask import session,redirect,url_for 
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
manager = Manager(app)
bootstarp = Bootstrap(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = '0707eb3a-38c9-497e-9d6c-3069bce2e603'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqllite:///' + os.path.join(basedir,'data.sqllite')
app.config['SQLALCHEMY_COMMIT_IN_TEARDOWN'] = True
db = SQLAlchemy(app)

class NameForm(Form):
    name = StringField('what is your name?',validators=[Required()])
    submit = SubmitField("Submit")

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'),500

@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index')) 
    return render_template('index.html',form=form,name=session.get('name'))

@app.route('/get')
def get():
    user_agent = request.headers.get('User-Agent')    
    return '<p>your browser is %s</p>' % user_agent

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

if __name__ == '__main__':
    manager.run()

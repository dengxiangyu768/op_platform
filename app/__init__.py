#!/usr/bin/python
#coding:utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
bootstrap = Bootstrap()


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from .api_v1 import api as api_blueprint
    app.register_blueprint(api_blueprint,url_prefix='/api_v1')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    

    return app

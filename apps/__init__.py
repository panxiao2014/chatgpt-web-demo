# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from logging.handlers import RotatingFileHandler
import logging


from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module


db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home', 'chat', 'webroot'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:////volume1/dev/sqlite/flask/db.sqlite3'

            print('> Fallback to SQLite ')
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

from apps.authentication.oauth import github_blueprint

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    #set logger:
    logPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'backapp.log')

    logging.basicConfig(format='[%(asctime)s]''[%(levelname)s][%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%b-%d %H:%M:%S', level=logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s]''[%(levelname)s][%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%b-%d %H:%M:%S %Z')
    
    fh = RotatingFileHandler(logPath, maxBytes=50 * 1024 * 1024, backupCount=1, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    app.logger.addHandler(fh)

    register_extensions(app)
    register_blueprints(app)

    app.register_blueprint(github_blueprint, url_prefix="/login") 
    
    configure_database(app)
    return app

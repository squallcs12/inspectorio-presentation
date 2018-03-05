import os

from flask import Flask

from auth import extension as auth_extension


def create_app(name):
    app = Flask(name)
    app.config.from_object('config.{}'.format(os.getenv('CONFIG_NAME', 'dev')))

    app.debug = app.config['DEBUG']

    from database import db
    db.init_app(app)

    app.db = db

    auth_extension.init_app(app)

    return app


def init_db():
    pass

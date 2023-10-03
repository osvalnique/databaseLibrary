from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from route import blueprint
from models import db

def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:ernest2210@localhost:5432/databuku'
    db.init_app(app)

    blueprints = app.register_blueprint(blueprint)
    return app

  
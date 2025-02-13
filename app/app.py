from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config


#FIXAR APPEN 
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) #TAR INFO FRÅN CONFIG

    db.init_app(app)

    with app.app_context():
        from . import routes, models
        db.create_all()

    return app

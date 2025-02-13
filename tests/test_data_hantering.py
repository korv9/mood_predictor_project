import sys
import os
from unittest.mock import MagicMock, patch
import pandas as pd
import pytest
from flask import Flask
import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash
from app.data_hantering import extract_data
from app.user_login import register_user, login_user
from app.models import db, User  # ANVÄND GLOBAL DB OCH MODELLER


#OBS BEHÖVAS KÖRAS GENOM TERMINALEN PYTHON -M PYTEST för att få rätt root


# SKAPA APP-FIXTURE OCH INITIERA GLOBAL DB MED APP
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'  # KRÄVS FÖR FLASK SESSIONER
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # INITIERA GLOBAL DB MED APPEN
    db.init_app(app)
    return app

# SKAPA DB-FIXTURE SOM SKAPAR OCH TÖMMER TABELLERNA
@pytest.fixture
def _db(app):
    with app.app_context():
        db.create_all()
    yield db
    with app.app_context():
        db.drop_all()

# SKAPA SESSION-FIXTURE SOM GER TILLGÅNG TILL DB.SESSION
@pytest.fixture
def session(_db, app):
    with app.app_context():
        yield _db.session

def register_user(session, username: str, password: str):   
#registrerar en ny användare, som lägger till det i session, följer samma struktur som i user_login.py, men skriver den här för att inte ha med return /login
    
    hashed_password = werkzeug.security.generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    session.add(new_user)
    session.commit()
    return new_user

def test_register_user(session, app):# testar att registrera en ny användare, via register_user funktionen
    
    username = "newuser"
    password = "newpass"
    with app.app_context():
        user = register_user(session, username, password)
        assert user is not None
        assert user.username == username
        assert user.password != password #verifierar att lösenordet är hashat


# TEST FÖR INLOGGNING MED KORREKT LÖSENORD
def test_login_user_success(session, app):
    
    username = "testuser"
    password = "testpass"
    with app.app_context():
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        session.add(new_user)
        session.commit()
        
        user = login_user(username, password)
        assert user is not None
        assert user.username == username

# TEST FÖR INLOGGNING MED FELAKTIGT LÖSENORD
def test_login_user_failure(session, app):

    username = "testuser"
    password = "testpass"
    wrong_password = "wrongpass"
    with app.app_context():
        # REGISTRERA ANVÄNDARE
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        session.add(new_user)
        session.commit()
        # TESTA INLOGGNING MED FEL LÖSENORD
        user = login_user(username, wrong_password)
        assert user is False

# TEST FÖR INLOGGNING NÄR ANVÄNDAREN INTE FINNS
def test_login_user_not_found(session, app):
    # TESTA INLOGGNING (ANVÄNDAREN FINNS INTE)
    username = "nonexistentuser"
    password = "testpass"
    with app.app_context():
        user = login_user(username, password)
        assert user is False





if __name__ == '__main__':
    pytest.main()
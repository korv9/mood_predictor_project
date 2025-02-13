from sqlalchemy.orm import Session
import werkzeug
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for, flash, session
from app.app import db
from app.models import User

def register_user(db, username: str, password: str):
    hashed_password = werkzeug.security.generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    db.session.refresh(new_user)
    return redirect(url_for('log_in'))


#bekräftar användare vid inlogg
def login_user(username: str, password: str):
    user = User.query.filter_by(username=username).first()
    
    if not user:
        print("User not found")
        return False
    
    if not werkzeug.security.check_password_hash(user.password, password):
        print("Wrong password")
        return False
    print("User logged in")
    return user

def check_user():
    #KONTROLLERAR OM ANVÄNDAREN ÄR INLOGGAD, och finns i databasen
    if 'username' not in session:
        return None
    
    try:
        user = User.query.filter_by(username=session['username']).first()
    except Exception as e:
        print(f"Error querying user: {e}")
        return None
    
    if not user:
        session.pop('username', None)  #säkerställer att gammal/invalid användare inte är kvar i session
        return None
    
    return user

def login_required(f):
    #DECORATOR FÖR ATT KONTROLLERA OM ANVÄNDAREN ÄR INLOGGAD
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page')
            return redirect(url_for('log_in'))
        return f(*args, **kwargs)
    return decorated_function
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
from sqlalchemy import Integer, Float, Date, String
from app.app import db

# klass för användar info, psykologiska profilen ingår också i samma table
class User(db.Model):
    __tablename__ = 'user_info'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # EN ANVÄNDARE KAN HA FLERA DAILY MOODS
    daily_moods = db.relationship('DailyMood', backref='user', lazy=True)

    # psykologiska profilen, används för bias för mood prediction
    depression = db.Column(db.Integer, nullable=False, default=0)
    anxiety = db.Column(db.Integer, nullable=False, default=0)
    stress = db.Column(db.Integer, nullable=False, default=0)
    mania = db.Column(db.Integer, nullable=False, default=0)
    delusion = db.Column(db.Integer, nullable=False, default=0)
    paranoia = db.Column(db.Integer, nullable=False, default=0)
    depressive_episodes = db.Column(db.Integer, nullable=False, default=0)
    manic_episodes = db.Column(db.Integer, nullable=False, default=0)

    
# klass för daglig humördata
class DailyMood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)
    mood = db.Column(db.Integer, nullable=True)
    appetite = db.Column(db.Integer, nullable=True)
    sleep = db.Column(db.Integer, nullable=True)
    stress = db.Column(db.Integer, nullable=True)
    exercise = db.Column(db.Integer, nullable=True)
    social_activity = db.Column(db.Integer, nullable=True)
    productivity = db.Column(db.Integer, nullable=True)
    hobby_time = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0))


    __table_args__ = (
        db.UniqueConstraint('user_id', 'date', name='unique_user_date'),
    )

def get_monday(some_date):
    """Return the Monday for the week of some_date."""
    return some_date - timedelta(days=some_date.weekday())





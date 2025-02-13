import pandas as pd
from app.models import DailyMood, User
from app.app import db
from datetime import datetime, date
from typing import Optional
from flask import session



def extract_data(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return pd.DataFrame()  

    daily_moods = DailyMood.query.filter_by(user_id=user.id).all()
    
    data = []
    for mood in daily_moods:
        # Skapa en dictionary med alla fält
        mood_data = {
            'date': mood.date,
            'mood': mood.mood,
            'appetite': mood.appetite,
            'sleep': mood.sleep,
            'stress': mood.stress,
            'exercise': mood.exercise,
            'social_activity': mood.social_activity,
            'productivity': mood.productivity,
            'hobby_time': mood.hobby_time
        }
        
        # Kontrollera om någon av värdena är None
        if all(v is not None for v in mood_data.values()):
            data.append(mood_data)

    df = pd.DataFrame(data)
    return df



def parse_next_day_date(date_str: Optional[str]) -> Optional[date]:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
    except ValueError:
        return None

def parse_feature_importance(feature_data: Optional[dict]) -> Optional[pd.DataFrame]:
    try:
        return pd.DataFrame(feature_data) if feature_data else None
    except (ValueError, TypeError):
        return None

def parse_prediction_data(prediction_data: dict) -> tuple:
    """Parse prediction data and return tuple of (next_day_date, feature_importance)"""
    if not prediction_data:
        return None, None
        
    next_day_date = datetime.strptime(prediction_data['next_day_date'], "%Y-%m-%d").date() if prediction_data.get('next_day_date') else None
    feature_importance = pd.DataFrame(prediction_data['feature_importance']) if prediction_data.get('feature_importance') else None
    
    return next_day_date, feature_importance

from flask import session
from datetime import datetime
import pandas as pd
from app.training import get_latest_prediction
from app.data_hantering import extract_data

def handle_prediction_data(username: str, fields: list) -> tuple:
#processar prediction data och returnerar prediction, next_day_date, feature_importance, mse, r2
    prediction_data = get_latest_prediction(username, fields)
    if prediction_data:
        session['prediction_data'] = prediction_data
        
        next_day_date = (datetime.strptime(prediction_data['next_day_date'], "%Y-%m-%d").date() 
                        if prediction_data.get('next_day_date') else None)
        feature_importance = (pd.DataFrame(prediction_data['feature_importance']) 
                            if prediction_data.get('feature_importance') else None)
        
        return (
            prediction_data['prediction'],
            next_day_date,
            feature_importance,
            prediction_data['mse'],
            prediction_data['r2']
        )
    
    session.pop('prediction_data', None)
    return None, None, None, None, None
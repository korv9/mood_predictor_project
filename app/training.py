from dataclasses import dataclass
import pandas as pd
import numpy as np
from datetime import timedelta
import threading
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from app.data_hantering import extract_data
from app.app import create_app

#använder constant för columner, kan lägga till mer senare,
FEATURE_COLUMNS = ['mood', 'appetite', 'sleep', 'stress', 
                  'exercise', 'social_activity', 'productivity', 'hobby_time']

@dataclass 
class PredictionResult: #dataklass för att hålla prediction data
    prediction: float = None
    next_day_date: str = None
    feature_importance: dict = None
    mse: float = None
    r2: float = None

class MoodModel: #klass för mood
    def __init__(self, username):
        # Initierar modellen med användarnamn och sätter alla startvärden till None
        self.username = username
        self.model = None
        self.scaler = None
        self.feature_importance = None
        self.mse = None
        self.r2 = None

    def train(self):
        # Huvudfunktion för att träna modellen med användarens data
        df = extract_data(self.username)
        if df.empty or len(df) < 2: #kontrollerar att det finns tillräckligt med data, har satt till 2 för att kunna träna trots litet dataset
            return None

        X, y = self._prepare_data(df)
        X_scaled = self._scale_features(X)
        self._fit_model(X_scaled, y)
        
        return self._get_model_metrics(X, y)

    def predict(self, current_values):
        # Gör en förutsägelse baserad på dagens värden
        if not all([self.model, self.scaler]):
            return None
        
        current_df = pd.DataFrame([current_values], columns=FEATURE_COLUMNS)
        scaled_values = self.scaler.transform(current_df)
        return round(float(self.model.predict(scaled_values)[0]), 2)

    def _prepare_data(self, df):
        # Förbereder data för träning genom att sortera och skapa nästa dags humörvärde
        df = df.sort_values('date')
        df['next_day_mood'] = df['mood'].shift(-1)
        df = df.dropna(subset=['next_day_mood'])
        return df[FEATURE_COLUMNS], df['next_day_mood']

    def _scale_features(self, X):
        # Normaliserar features för bättre träningsresultat
        self.scaler = StandardScaler()
        return self.scaler.fit_transform(X)

    def _fit_model(self, X_scaled, y):
        # Tränar den linjära regressionsmodellen med den normaliserade datan
        self.model = LinearRegression()
        self.model.fit(X_scaled, y)

    def _get_model_metrics(self, X, y):
        # Beräknar modellens prestanda och feature importance
        y_pred = self.model.predict(self.scaler.transform(X))
        self.mse = mean_squared_error(y, y_pred)
        self.r2 = r2_score(y, y_pred)
        
        self.feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': abs(self.model.coef_)
        }).sort_values('importance', ascending=False)

        return self.model, self.scaler, self.feature_importance, self.mse, self.r2

def train_model_in_background(username):
    #funktion för multithreading
    app = create_app()
    with app.app_context():
        model = MoodModel(username)
        return model.train()

def start_training_thread(username):
    #startar en tråd för att träna modellen i bakgrunden
    training_thread = threading.Thread(
        target=train_model_in_background, 
        args=(username,),
        daemon=True
    )
    training_thread.start()

def get_latest_prediction(username, fields):
    #hämtar senaste prediction data och returnerar en PredictionResult
    df = extract_data(username)
    if df.empty:
        return None

    try:
        model = MoodModel(username)
        results = model.train()
        if not results:
            return None

        latest_data = df.iloc[-1][fields].values
        prediction = model.predict(latest_data)
        next_day_date = df.iloc[-1]['date'] + timedelta(days=1)

        return PredictionResult(
            prediction=prediction,
            next_day_date=next_day_date.strftime("%Y-%m-%d"),
            feature_importance=model.feature_importance.to_dict('records'),
            mse=model.mse,
            r2=model.r2
        ).__dict__

    except Exception as e:
        print(f"Error getting prediction: {e}")
        return None
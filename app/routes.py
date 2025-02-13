from flask import (
    flash, 
    request, 
    render_template, 
    redirect, 
    session, 
    url_for, 
    current_app as app
)
from datetime import date, timedelta, datetime
from app.models import DailyMood, User
from app.data_hantering import extract_data
from app.prediction_handler import handle_prediction_data
from app.training import get_latest_prediction, start_training_thread
from app.user_login import register_user, login_user, check_user, login_required
from app.app import db

FORM_FIELDS = ['mood', 'appetite', 'sleep', 'stress', 'exercise', 'social_activity', 'productivity', 'hobby_time']
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


@app.route('/')
def index():
    user = check_user()
    return render_template('log_in.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return register_user(db, request.form['username'], request.form['password'])
    return render_template('register.html')

@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    user = check_user()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = login_user(username, password)
        
        if not user:
            flash("Invalid username or password")
            return render_template('log_in.html')
            
        session.clear()  
        session['username'] = user.username
        session.modified = True  #försäkrad att session är sparad
        
        return redirect(url_for('main_page'))
    
    return render_template('log_in.html')


@app.route('/dashboard', methods=['GET', 'POST']) #dashboard för profil, ska läggas in mer senare
@login_required
def dashboard():
    user = check_user()
    return render_template('dashboard.html', user=user)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        return add_to_profile()
    return render_template('profile.html')

def add_to_profile():
    user = check_user() #query för att matcha användaren med sessionens användare, sedan lägga till psykoligiska profilen i databasen
    
    user.depression = request.form.get('depression')
    user.anxiety = request.form.get('anxiety')
    user.stress = request.form.get('stress')
    user.mania = request.form.get('mania')
    user.delusion = request.form.get('delusion')
    user.paranoia = request.form.get('paranoia')
    user.depressive_episodes = request.form.get('depressive_episodes')
    user.manic_episodes = request.form.get('manic_episodes')
    
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('log_in'))





@app.route('/main', methods=['GET', 'POST'])
@login_required
def main_page():
    user = check_user()

    week_param = request.args.get('week')
    week_start = (datetime.strptime(week_param, "%Y-%m-%d").date() if week_param  
                 else date.today() - timedelta(days=date.today().weekday()))
    
    prev_week = week_start - timedelta(days=7) #för knappar för att gå fram och tillbaka i veckor
    next_week = week_start + timedelta(days=7)

    if request.method == 'POST':
        for day in WEEKDAYS:
            # Itererar över dagarna,day_date indexeras med veckodagar för att få rätt dag i veckan för formuläret
            day_date = week_start + timedelta(days=WEEKDAYS.index(day))
            daily_mood = DailyMood.query.filter_by(user_id=user.id, date=day_date).first()

            # Skapar en ny DailyMood-post om den inte finns
            if not daily_mood:
                daily_mood = DailyMood(user_id=user.id, date=day_date)
                db.session.add(daily_mood)

            # Gettar värdet från formuläret och sätter det i databasen
            for field in FORM_FIELDS:
                field_name = f"{day.lower()}_{field}"
                value = request.form.get(field_name)
                if value:
                    setattr(daily_mood, field, int(value))
                else:
                    setattr(daily_mood, field, None) #gör så att användare kan lämna fältet tomt 
                    
        db.session.commit()
        
        # bakgrund träning multithread
        start_training_thread(user.username)
        
        return redirect(url_for('main_page', week=week_start.strftime("%Y-%m-%d")))

    # Hämtar datan som redan finns i databasen för att displaya i formulären
    data = {}
    for day in WEEKDAYS:
        day_date = week_start + timedelta(days=WEEKDAYS.index(day))
        daily_mood = DailyMood.query.filter_by(user_id=user.id, date=day_date).first()
        
        if daily_mood:
            data[day] = {field: getattr(daily_mood, field) for field in FORM_FIELDS}
        else:
            data[day] = {field: None for field in FORM_FIELDS}

    # hämtar senaste prediction data
    prediction, next_day_date, _, _, _ = handle_prediction_data(user.username, FORM_FIELDS)

    return render_template(
        'main_page.html',
        weekdays=WEEKDAYS,
        data=data,
        week_start=week_start,
        prev_week=prev_week,
        next_week=next_week,
        prediction=prediction,
        next_day_date=next_day_date,
        timedelta=timedelta  
    )

#visar psykologiska profilen med dess weights (behöver lägga in fler)
@app.route('/data_mood', methods=['GET', 'POST'])
@login_required
def data_mood():
    user = check_user() 
    data = extract_data(user.username)
    
    if not data.empty:
        #tar bort indexnamnet för att det inte ska visas i tabellen
        data.index.name = None
    
    return render_template('data_mood.html', data_mood=data)



# predictar kommande dagens mood, alltså dagen efter senaste inskickade data
@app.route('/predict_next_day_mood', methods=['GET'])
@login_required
def predict_next_day_mood_route():
    user = check_user()
    prediction, next_day_date, feature_importance, mse, r2 = handle_prediction_data(user.username, FORM_FIELDS)
    
    if not prediction:
        flash("No prediction available. Please ensure you have entered some data.")
        return redirect(url_for('main_page'))
    
    return render_template('predict_next_day_mood.html', 
                         prediction=prediction,
                         feature_importance=feature_importance,
                         mse=mse,
                         r2=r2,
                         next_day_date=next_day_date)
import sys
import os
import csv
from app.models import User, DailyMood, db
from app.app import create_app
from datetime import datetime

# Ensure the project root is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#python -m app.restore


def safe_int(value):
    #converterar värdet till int om det inte är tomt, annars None, detta behövs för användaren kan lämna fältet tomt
    try:
        value = value.strip()
    except AttributeError:
        pass
    return int(value) if value else None



def restore_data():
    
    users_backup_file = 'backups/users_backup.csv'
    with open(users_backup_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            user = User.query.get(row['id'])  #kollar om användare redan finns i databasen, om inte skapas en ny
            
            if not user:
                user = User(
                    id=int(row['id']),
                    username=row['username'],
                    password=row['password'],
                    depression=int(row['depression']),
                    anxiety=int(row['anxiety']),
                    stress=int(row['stress']),
                    mania=int(row['mania']),
                    delusion=int(row['delusion']),
                    paranoia=int(row['paranoia']),
                    depressive_episodes=int(row['depressive_episodes']),
                    manic_episodes=int(row['manic_episodes'])
                )
                db.session.add(user)
            else:
                # uppdaterar om användaren redan finns
                user.username = row['username']
                user.password = row['password']
                user.depression = int(row['depression'])
                user.anxiety = int(row['anxiety'])
                user.stress = int(row['stress'])
                user.mania = int(row['mania'])
                user.delusion = int(row['delusion'])
                user.paranoia = int(row['paranoia'])
                user.depressive_episodes = int(row['depressive_episodes'])
                user.manic_episodes = int(row['manic_episodes'])
    db.session.commit()


    #restore data från daily mood table
    daily_backup_file = 'backups/daily_moods_backup.csv'
    with open(daily_backup_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        
        for row in reader: #skapar mood column i databasen
           
            daily_mood = DailyMood(
                user_id=safe_int(row['user_id']),
                date=datetime.strptime(row['date'], '%Y-%m-%d').date(),  # Convert to a date
                mood=safe_int(row['mood']),
                appetite=safe_int(row['appetite']),
                sleep=safe_int(row['sleep']),
                stress=safe_int(row['stress']),
                exercise=safe_int(row['exercise']),
                social_activity=safe_int(row['social_activity']),
                productivity=safe_int(row['productivity']),
                hobby_time=safe_int(row['hobby_time'])
            )
            
            db.session.add(daily_mood)
    db.session.commit()
    print("Data restored successfully.")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        restore_data()
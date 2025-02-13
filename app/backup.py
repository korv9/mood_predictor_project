
import sys
from app.models import DailyMood, User, db
import csv 
import os
from app.app import create_app
#VIKTIGT, KÖR IFRÅN ROOT MED ATT SKRIVA python -m app.backup


#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # kanske kan fixa så man inte måste skriva python -m app.backup




def back_up_data():
    backup_file = 'backups/users_backup.csv'
    with open (backup_file, 'w') as csvfile:
        fieldnames = ['id', 'username', 'password', 'depression', 'anxiety', 'stress', 'mania',
                      'delusion', 'paranoia', 'depressive_episodes', 'manic_episodes']  #sorterar data i csv filen efter dessa kategorier
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        users = User.query.all()
        for u in users:
            writer.writerow({  
                'id': u.id,
                'username': u.username,
                'password': u.password,
                'depression': u.depression,
                'anxiety': u.anxiety,
                'stress': u.stress,
                'mania': u.mania,
                'delusion': u.delusion,
                'paranoia': u.paranoia,
                'depressive_episodes': u.depressive_episodes,
                'manic_episodes': u.manic_episodes
            })
    



    moods_backup_file = 'backups/daily_moods_backup.csv' # skapar en separat för mood datan
    with open(moods_backup_file, 'w', newline='') as csvfile:
        
        fieldnames = [ 'user_id', 'date', 'mood', 'appetite', 'sleep', 'stress', 
                      'exercise', 'social_activity', 'productivity', 'hobby_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        daily_moods = DailyMood.query.all()
        
        for mood in daily_moods:
            writer.writerow({
                
                'user_id': mood.user_id,
                'date': mood.date,
                'mood': mood.mood,
                'appetite': mood.appetite,
                'sleep': mood.sleep,
                'stress': mood.stress,
                'exercise': mood.exercise,
                'social_activity': mood.social_activity,
                'productivity': mood.productivity,
                'hobby_time': mood.hobby_time
            })
    print("Data backed up")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        back_up_data()



#schtasks /create /tn "DailyBackup" /tr "python -m app.backup" /sc daily /st 23:00
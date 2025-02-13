"""import sys
import os
import pytest
from flask import Flask
import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash
from app.user_login import register_user, login_user
from app.models import db, User  # ANVÄND GLOBAL DB OCH MODELLER
# FIXA PROJEKTKATALOGEN
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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



@patch('app.data_hantering.User')
@patch('app.data_hantering.DailyMood')
def test_extract_data(MockDailyMood, MockUser):
    with app.app_context():
        # Mock user
        mock_user = MagicMock()
        mock_user.id = 1
        MockUser.query.filter_by.return_value.first.return_value = mock_user

        # Mock daily moods
        mock_mood = MagicMock()
        mock_mood.date = '2023-10-01'
        mock_mood.mood = 5
        mock_mood.appetite = 6
        mock_mood.sleep = 7
        mock_mood.stress = 4
        mock_mood.exercise = 8
        mock_mood.social_activity = 3
        mock_mood.productivity = 9
        mock_mood.hobby_time = 2
        MockDailyMood.query.filter_by.return_value.all.return_value = [mock_mood]

        # Call the function
        df = extract_data('test')

        # Print DataFrame information
        print("\n=== DataFrame Content ===")
        print(df)
        print("\n=== DataFrame Info ===")
        print(df.info())
        print("\n=== DataFrame Description ===")
        print(df.describe())

        # Check the DataFrame
        expected_data = {
            'date': ['2023-10-01'],
            'mood': [5],
            'appetite': [6],
            'sleep': [7],
            'stress': [4],
            'exercise': [8],
            'social_activity': [3],
            'productivity': [9],
            'hobby_time': [2]
        }
        expected_df = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(df, expected_df)

if __name__ == '__main__':
    pytest.main()"""
MOOD TRACKER / PREDICTOR





This is a small Flask-SQLalchemy web app designed to track and predict the mood of a user along with various related metrics.
The primary goal of the project is to accurately predict incoming manic or depressive episodes for users with bipolar disorder.
At its current stage, the app offers only a vague prediction of the next day's mood using a simple machine learning model built with scikit-learn.

Further into development, I plan to enhance the model by adding more variables and metrics, primarily focusing on the users history of manic and depressive episodes. 
By incorporating a user-specific, detailed psychological profile, the aim is to map the correlations between factors such as sleep, appetite, stress, and bipolar episodes. 
The main focus is to try and track what ratio of sleep and appetite that might trigger the hormonal swing which causes the depressive and manic episodes for users with a bipolar disorder. 
 

INSTALLATION -

git clone https://github.com/korv9/mood_predictor_project
cd MOOD_PROJECT

Create a virtual environment:
python -m venv venv

Install the required dependencies:
pip install -r requirements.text

Create a .env file with:
SECRET_KEY=your_secret_key_here
DATABASE_URI=sqlite:///mood_tracker.db

And then run the app:
python run.py


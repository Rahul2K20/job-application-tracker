import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


SECRET_KEY = 'rahul123'  
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

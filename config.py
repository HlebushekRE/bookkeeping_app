import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'YOUR_RANDOM_SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:1qazxsw23edc@localhost/bookkeeping'
    UPLOAD_FOLDER = basedir + '/static/uploads/'

config = Config()


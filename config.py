import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Connect to the database


# TODO IMPLEMENT DATABASE URL
class DatabaseURI:
    # Just change the names of your database and credentials and all to connect to your local system
    DATABASE_NAME = "fyyurdb"
    username = os.getenv('usrname')
    password = os.getenv('passwd')
    url = 'localhost:5432'

    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(
        username, password, url, DATABASE_NAME)

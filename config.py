import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

# SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12Wegba34@localhost:5432/fyyur'
SQLALCHEMY_TRACK_MODIFICATIONS = False

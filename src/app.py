"""
This flask application represents an online car market with CRUD operations and
Google Plus authentication.
It is part of the Udacity Full Stack Developer Nanodegree.

Github repository: https://github.com/riverstorm/car-portal
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from os.path import join, dirname, realpath


# Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = join(dirname(realpath(__file__)), 'static')
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = '5864164198696464869464869'

ADMIN_ID = 'YOUR GPLUS ID HERE'
CLIENT_ID = json.loads(open('client_secrets.json', 'r')
                       .read())['web']['client_id']

# Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Views
import views

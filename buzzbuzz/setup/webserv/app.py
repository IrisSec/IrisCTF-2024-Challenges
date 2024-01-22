import os
import sys

from flask import *
from flask_sqlalchemy import *

# Instantiate the application and define settings.
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.urandom(32)

# Load the database.
db = SQLAlchemy(app)
from model import *
with app.app_context():
	db.create_all()

from route import *
from api import *

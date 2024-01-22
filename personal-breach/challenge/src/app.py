import os

from flask import *

# Instantiate the application and define settings.
app = Flask(__name__)
app.secret_key = os.urandom(32)

from form import *

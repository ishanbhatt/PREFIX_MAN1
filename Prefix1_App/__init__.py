from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from Prefix1_App.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from Prefix1_App import routes
from Prefix1_App import models

db.create_all()

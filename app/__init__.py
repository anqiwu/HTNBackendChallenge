from flask import Flask

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

from app.controllers import get_users, user_by_id

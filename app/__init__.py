from flask import Flask

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

from app.routes.User import get_users
from app.routes.Skill import skill_method
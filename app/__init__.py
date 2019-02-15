from flask import Flask

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

from app.routes.User import get_all_users, user_by_id
from app.routes.Skill import get

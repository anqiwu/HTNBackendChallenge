from app import db

users_skills = db.Table('users_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('skill_with_rating_id', db.Integer, db.ForeignKey('skills_with_rating.skill_with_rating_id'), primary_key=True)
)

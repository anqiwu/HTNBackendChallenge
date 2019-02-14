from app import db


class SkillWithRating(db.Model):
    __tablename__ = 'skills_with_rating'

    skill_with_rating_id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.skill_id'))

    db.UniqueConstraint('skill_name', 'rating')

    def __init__(self, skill_name, rating, skill_id):
        self.skill_name = skill_name
        self.rating = rating
        self.skill_id = skill_id

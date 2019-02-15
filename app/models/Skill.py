from app import db


class Skill(db.Model):
    __tablename__ = 'skills'

    skill_id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(255), nullable=False, unique=True)

    users = db.relationship("UserSkill", back_populates="skill", lazy="dynamic")

    def __init__(self, skill_name):
        self.skill_name = skill_name

from app import db


class UserSkill(db.Model):
    __tablename__ = 'users_skills'
    __table_args__ = (
        db.PrimaryKeyConstraint('user_id', 'skill_id'),
    )

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.skill_id'))
    rating = db.Column(db.Integer, nullable=False)

    db.UniqueConstraint('user_id', 'user_id')
    skill = db.relationship("Skill", back_populates="users")
    user = db.relationship("User", back_populates="skills")

    def __init__(self, rating):
        self.rating = rating

from app import db


class Company(db.Model):
    __tablename__ = 'companies'

    company_id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(255), unique=True)
    users = db.relationship('User', backref='user', lazy=True)

    def __init__(self, company):
        self.company = company


users_skills = db.Table('users_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.skill_id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.Text)
    company = db.Column(db.Integer, db.ForeignKey('companies.company_id'))
    phone = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    skills = db.relationship("Skill", secondary=users_skills, lazy="dynamic", backref=db.backref("users", lazy="dynamic"))

    def __init__(self, email, name, picture, company, phone, latitude, longitude):
        self.email = email
        self.name = name
        self.picture = picture
        self.company = company
        self.phone = phone
        self.latitude = latitude
        self.longitude = longitude


class Skill(db.Model):
    __tablename__ = 'skills'

    skill_id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    db.UniqueConstraint('skill_name', 'rating')

    def __init__(self, skill_name, rating):
        self.skill_name = skill_name
        self.rating = rating

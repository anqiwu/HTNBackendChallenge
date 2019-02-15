from app import db
from app.models.Company import Company

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.Text)
    company = db.Column(db.Integer, db.ForeignKey('companies.company'))
    phone = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    skills = db.relationship("UserSkill", back_populates="user", lazy="dynamic")

    def __init__(self, email, name, picture, company, phone, latitude, longitude):
        self.email = email
        self.name = name
        self.picture = picture
        self.company = company
        self.phone = phone
        self.latitude = latitude
        self.longitude = longitude

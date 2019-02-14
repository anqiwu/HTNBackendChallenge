from app import db


class Company(db.Model):
    __tablename__ = 'companies'

    company_id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(255), unique=True)
    users = db.relationship('User', backref='user', lazy=True)

    def __init__(self, company):
        self.company = company

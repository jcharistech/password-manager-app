from .extensions import db
from flask_login import UserMixin

# Model
class PasswordManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(520), nullable=False)
    site_url = db.Column(db.String(520), nullable=False)
    site_password = db.Column(db.String(520), nullable=False)

    def __repr__(self):
        return '<PasswordManager %r>' % self.email


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(520))
    email = db.Column(db.String(520), nullable=False)
    password = db.Column(db.String(520), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email




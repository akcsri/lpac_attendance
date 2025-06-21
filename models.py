from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin  # ← 追加

db = SQLAlchemy()


from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    participants = db.relationship('Participant', backref='user', lazy=True)

class Participant(db.Model):
    email = db.Column(db.String(120))
    questions = db.Column(db.Text)
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(100))
    name = db.Column(db.String(100))
    status = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所有者ユーザー

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

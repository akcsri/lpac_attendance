from flask import Flask
from werkzeug.security import generate_password_hash
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def create_user(username, password, role='user'):
    with app.app_context():
        db.create_all()  # Ensure tables are created
        password_hash = generate_password_hash(password)
        new_user = User(username=username, password_hash=password_hash, role=role)
        db.session.add(new_user)
        db.session.commit()
        print(f"User {username} created successfully.")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Create a new user.')
    parser.add_argument('username', type=str, help='The username of the new user.')
    parser.add_argument('password', type=str, help='The password of the new user.')
    parser.add_argument('--role', type=str, default='user', help='The role of the new user.')

    args = parser.parse_args()

    create_user(args.username, args.password, args.role)

def create_user(username, password, role='user'):
    with app.app_context():
        db.create_all()

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"ユーザー '{username}' はすでに存在します。")
            return

        password_hash = generate_password_hash(password)
        new_user = User(username=username, password_hash=password_hash, role=role)
        db.session.add(new_user)
        db.session.commit()
        print(f"ユーザー '{username}' を作成しました。")

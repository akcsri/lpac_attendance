from flask import Flask
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def delete_user(username):
    with app.app_context():
        user_to_delete = User.query.filter_by(username=username).first()
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            print(f"ユーザー '{username}' を削除しました。")
        else:
            print(f"ユーザー '{username}' は存在しません。")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Delete a user by username.')
    parser.add_argument('username', type=str, help='The username of the user to delete.')

    args = parser.parse_args()

    delete_user(args.username)

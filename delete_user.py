from flask import Flask
from models import db, User
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')

# app.pyと同じデータベース設定を使用
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def delete_user(username):
    with app.app_context():
        user_to_delete = User.query.filter_by(username=username).first()
        if user_to_delete:
            user_id = user_to_delete.id
            user_role = user_to_delete.role
            
            db.session.delete(user_to_delete)
            db.session.commit()
            
            print(f"✅ ユーザー '{username}' を削除しました。")
            print(f"   削除されたユーザー情報:")
            print(f"   - ID: {user_id}")
            print(f"   - ロール: {user_role}")
            
            # 全ユーザー数を表示
            total_users = User.query.count()
            print(f"   📊 残りのユーザー数: {total_users}")
        else:
            print(f"❌ ユーザー '{username}' は存在しません。")
            
            # 登録されているユーザー一覧を表示
            all_users = User.query.all()
            if all_users:
                print("\n📋 登録されているユーザー:")
                for u in all_users:
                    print(f"   - {u.username} (ロール: {u.role})")
            else:
                print("\n⚠️ ユーザーが1人も登録されていません")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Delete a user by username.')
    parser.add_argument('username', type=str, help='The username of the user to delete.')

    args = parser.parse_args()

    # データベース設定を表示
    print("=" * 60)
    print("🔧 データベース設定")
    print("=" * 60)
    if DATABASE_URL:
        masked_url = DATABASE_URL[:20] + "..." + DATABASE_URL[-20:]
        print(f"DATABASE_URL: {masked_url}")
        if 'postgresql://' in DATABASE_URL:
            print("✅ PostgreSQLを使用")
        else:
            print("⚠️ SQLiteを使用")
    else:
        print("⚠️ DATABASE_URLが設定されていません")
        print("   SQLiteを使用します")
    print("=" * 60)
    print()

    delete_user(args.username)

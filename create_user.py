from flask import Flask
from werkzeug.security import generate_password_hash
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

def create_user(username, password, role='user'):
    with app.app_context():
        # テーブルが存在することを確認
        db.create_all()
        
        # 既存ユーザーをチェック
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"⚠️ ユーザー '{username}' はすでに存在します。")
            print(f"   既存ユーザー情報:")
            print(f"   - ID: {existing_user.id}")
            print(f"   - ユーザー名: {existing_user.username}")
            print(f"   - ロール: {existing_user.role}")
            return

        # 新しいユーザーを作成
        password_hash = generate_password_hash(password)
        new_user = User(username=username, password_hash=password_hash, role=role)
        db.session.add(new_user)
        db.session.commit()
        
        print(f"✅ ユーザー '{username}' を作成しました。")
        print(f"   ログイン情報:")
        print(f"   - ユーザー名: {username}")
        print(f"   - パスワード: {password}")
        print(f"   - ロール: {role}")
        
        # 作成を確認
        created_user = User.query.filter_by(username=username).first()
        if created_user:
            print(f"   ✅ データベースへの保存を確認しました（ID: {created_user.id}）")
        else:
            print(f"   ❌ 警告: データベースへの保存確認に失敗しました")
        
        # 全ユーザー数を表示
        total_users = User.query.count()
        print(f"   📊 現在の登録ユーザー数: {total_users}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Create a new user.')
    parser.add_argument('username', type=str, help='The username of the new user.')
    parser.add_argument('password', type=str, help='The password of the new user.')
    parser.add_argument('--role', type=str, default='user', help='The role of the new user (user or admin).')

    args = parser.parse_args()

    # データベース設定を表示
    print("=" * 60)
    print("🔧 データベース設定")
    print("=" * 60)
    if DATABASE_URL:
        # URLの一部を隠して表示
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

    create_user(args.username, args.password, args.role)

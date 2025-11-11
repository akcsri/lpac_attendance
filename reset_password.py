#!/usr/bin/env python3
"""
パスワードリセットスクリプト

使い方:
  python reset_password.py ユーザー名 新しいパスワード

例:
  python reset_password.py admin NewPassword123
"""

from app import app, db
from models import User
from werkzeug.security import generate_password_hash
import sys

def reset_password(username, new_password):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        
        if not user:
            print(f"❌ ユーザー '{username}' が見つかりません")
            
            # 登録されているユーザー一覧を表示
            all_users = User.query.all()
            if all_users:
                print("\n登録されているユーザー:")
                for u in all_users:
                    print(f"  - {u.username} (ロール: {u.role})")
            else:
                print("\nユーザーが1人も登録されていません")
            return False
        
        # パスワードを更新
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        
        print(f"✅ ユーザー '{username}' のパスワードをリセットしました")
        print(f"新しいパスワード: {new_password}")
        print(f"\nログイン情報:")
        print(f"  ユーザー名: {username}")
        print(f"  パスワード: {new_password}")
        print(f"  ロール: {user.role}")
        return True

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("使い方: python reset_password.py ユーザー名 新しいパスワード")
        print("例: python reset_password.py admin NewPassword123")
        sys.exit(1)
    
    username = sys.argv[1]
    new_password = sys.argv[2]
    
    reset_password(username, new_password)

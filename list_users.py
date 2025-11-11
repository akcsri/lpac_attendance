#!/usr/bin/env python3
"""
ユーザー一覧表示スクリプト

使い方:
  python list_users.py
"""

from app import app, db
from models import User

def list_users():
    with app.app_context():
        print("=" * 60)
        print("👥 登録ユーザー一覧")
        print("=" * 60)
        print()
        
        # データベース接続確認
        try:
            users = User.query.all()
            total_users = User.query.count()
            
            print(f"📊 登録ユーザー数: {total_users}")
            print()
            
            if not users:
                print("⚠️ ユーザーが1人も登録されていません")
                print()
                print("💡 ユーザーを作成するには:")
                print("   python create_user.py ユーザー名 パスワード --role admin")
                print()
                return
            
            # ユーザー一覧を表示
            print("登録されているユーザー:")
            print("-" * 60)
            
            for i, user in enumerate(users, 1):
                print(f"{i}. ユーザー名: {user.username}")
                print(f"   ID: {user.id}")
                print(f"   ロール: {user.role}")
                print(f"   パスワードハッシュ: {user.password_hash[:30]}...")
                
                # 参加者数を表示
                participant_count = len(user.participants) if hasattr(user, 'participants') else 0
                print(f"   登録参加者数: {participant_count}")
                print()
            
            # ロール別の統計
            admin_count = User.query.filter_by(role='admin').count()
            user_count = User.query.filter_by(role='user').count()
            
            print("-" * 60)
            print("📈 統計情報:")
            print(f"   管理者: {admin_count}人")
            print(f"   一般ユーザー: {user_count}人")
            print(f"   合計: {total_users}人")
            
        except Exception as e:
            print(f"❌ データベースエラー: {e}")
            print()
            print("💡 DATABASE_URLを確認してください")
            return
        
        print()
        print("=" * 60)

if __name__ == '__main__':
    list_users()

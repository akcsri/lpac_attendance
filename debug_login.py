#!/usr/bin/env python3
"""
ログイン問題のデバッグスクリプト

使い方:
  Render Shell で実行:
  python debug_login.py

  または特定のユーザーをチェック:
  python debug_login.py admin
"""

from app import app, db
from models import User
from werkzeug.security import check_password_hash
import sys

def debug_login(username=None):
    with app.app_context():
        print("=" * 60)
        print("🔍 ログイン問題デバッグツール")
        print("=" * 60)
        print()
        
        # 1. データベース接続確認
        print("1️⃣ データベース接続確認...")
        try:
            user_count = User.query.count()
            print(f"   ✅ データベース接続成功")
            print(f"   📊 登録ユーザー数: {user_count}")
            print()
        except Exception as e:
            print(f"   ❌ データベース接続エラー: {e}")
            print("   💡 DATABASE_URLを確認してください")
            return
        
        # 2. 全ユーザー一覧
        print("2️⃣ 登録されているユーザー:")
        users = User.query.all()
        if not users:
            print("   ⚠️ ユーザーが1人も登録されていません")
            print("   💡 create_user.py を実行してユーザーを作成してください")
            print()
            return
        
        for user in users:
            print(f"   👤 ユーザー名: {user.username}")
            print(f"      ID: {user.id}")
            print(f"      ロール: {user.role}")
            print(f"      パスワードハッシュ: {user.password_hash[:20]}...")
            print()
        
        # 3. 特定ユーザーの詳細チェック
        if username:
            print(f"3️⃣ ユーザー '{username}' の詳細チェック:")
            user = User.query.filter_by(username=username).first()
            
            if not user:
                print(f"   ❌ ユーザー '{username}' が見つかりません")
                print(f"   💡 正確なユーザー名: {[u.username for u in users]}")
                print()
                return
            
            print(f"   ✅ ユーザーが見つかりました")
            print(f"   ID: {user.id}")
            print(f"   ユーザー名: {user.username}")
            print(f"   ロール: {user.role}")
            print(f"   パスワードハッシュ: {user.password_hash}")
            print()
            
            # パスワードテスト
            print("4️⃣ パスワードテスト:")
            test_password = input("   テスト用パスワードを入力 (Enter でスキップ): ").strip()
            
            if test_password:
                if check_password_hash(user.password_hash, test_password):
                    print(f"   ✅ パスワード '{test_password}' は正しいです！")
                    print()
                    print("   🤔 ログインできない場合の原因:")
                    print("      1. SECRET_KEYが設定されていない")
                    print("      2. ブラウザのCookieが無効")
                    print("      3. セッション管理の問題")
                    print()
                    print("   💡 解決策:")
                    print("      - Renderの環境変数でSECRET_KEYを設定")
                    print("      - ブラウザのシークレットモードで試す")
                    print("      - ブラウザのCookieをクリア")
                else:
                    print(f"   ❌ パスワード '{test_password}' は間違っています")
                    print()
                    print("   💡 パスワードをリセットするには:")
                    print(f"      python reset_password.py {username} 新しいパスワード")
            print()
        
        # 4. SECRET_KEY確認
        print("5️⃣ SECRET_KEY 確認:")
        secret_key = app.config.get('SECRET_KEY')
        if secret_key == 'your_secret_key':
            print("   ⚠️ SECRET_KEYがデフォルト値です")
            print("   💡 Renderの環境変数でSECRET_KEYを設定してください")
            print("   例: SECRET_KEY=ランダムな長い文字列")
        elif secret_key:
            print(f"   ✅ SECRET_KEYが設定されています: {secret_key[:10]}...")
        else:
            print("   ❌ SECRET_KEYが設定されていません")
        print()
        
        # 5. セッション設定確認
        print("6️⃣ セッション設定:")
        print(f"   SESSION_TYPE: {app.config.get('SESSION_TYPE', 'default')}")
        print(f"   PERMANENT_SESSION_LIFETIME: {app.config.get('PERMANENT_SESSION_LIFETIME', 'default')}")
        print()
        
        print("=" * 60)
        print("✅ デバッグ完了")
        print("=" * 60)

if __name__ == '__main__':
    username = sys.argv[1] if len(sys.argv) > 1 else None
    debug_login(username)

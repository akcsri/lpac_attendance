#!/usr/bin/env python3
"""
テーブル再作成スクリプト

⚠️ 警告: このスクリプトは既存のデータをすべて削除します！

使い方:
  python recreate_tables.py
"""

from app import app, db
from models import User, Participant

def recreate_tables():
    with app.app_context():
        print("=" * 60)
        print("⚠️  テーブル再作成")
        print("=" * 60)
        print()
        
        # 確認
        print("⚠️  警告: このスクリプトは既存のデータをすべて削除します！")
        print()
        
        # 既存のユーザー数を確認
        try:
            user_count = User.query.count()
            participant_count = Participant.query.count()
            
            if user_count > 0 or participant_count > 0:
                print(f"📊 現在のデータ:")
                print(f"   ユーザー: {user_count}人")
                print(f"   参加者: {participant_count}人")
                print()
                print("このデータはすべて削除されます。")
                print()
                
                response = input("続行しますか？ (yes/no): ").strip().lower()
                if response != 'yes':
                    print("❌ キャンセルしました")
                    return
                print()
        except:
            # テーブルがない場合はスキップ
            pass
        
        try:
            print("🗑️  既存のテーブルを削除中...")
            db.drop_all()
            print("✅ 削除完了")
            print()
            
            print("🔨 新しいテーブルを作成中...")
            db.create_all()
            print("✅ 作成完了")
            print()
            
            print("📋 作成されたテーブル:")
            print("   - user (password_hash: VARCHAR(255))")
            print("   - participant")
            print()
            
            print("✅ スキーマ更新完了")
            print()
            print("次のステップ:")
            print("  1. 管理者ユーザーを作成:")
            print("     python create_user.py admin password123 --role admin")
            print()
            print("  2. 一般ユーザーを作成:")
            print("     python create_user.py username password123")
            
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
            print()
            print("💡 手動でテーブルを削除してから再試行してください")
        
        print()
        print("=" * 60)

if __name__ == '__main__':
    recreate_tables()

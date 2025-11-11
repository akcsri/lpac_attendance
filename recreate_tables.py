#!/usr/bin/env python3
"""
テーブル再作成スクリプト（改良版）

使い方:
  python recreate_tables_v2.py
"""

from app import app, db
from models import User, Participant
from sqlalchemy import text

def recreate_tables():
    with app.app_context():
        print("=" * 60)
        print("⚠️  テーブル再作成（改良版）")
        print("=" * 60)
        print()
        
        # 既存のユーザー数を確認
        try:
            user_count = User.query.count()
            participant_count = Participant.query.count()
            
            print(f"📊 現在のデータ:")
            print(f"   ユーザー: {user_count}人")
            print(f"   参加者: {participant_count}人")
            print()
            
            if user_count > 0 or participant_count > 0:
                print("⚠️  このデータはすべて削除されます。")
                print()
                response = input("続行しますか？ (yes/no): ").strip().lower()
                if response != 'yes':
                    print("❌ キャンセルしました")
                    return
                print()
        except Exception as e:
            print(f"ℹ️  既存テーブルの確認をスキップ: {e}")
            print()
        
        try:
            print("🗑️  テーブルを手動で削除中...")
            
            # 手動でテーブルを削除（外部キー制約を考慮）
            with db.engine.connect() as conn:
                # トランザクション開始
                trans = conn.begin()
                try:
                    # 参加者テーブルを先に削除（外部キー制約）
                    print("   - participant テーブルを削除中...")
                    conn.execute(text('DROP TABLE IF EXISTS participant CASCADE;'))
                    
                    # ユーザーテーブルを削除
                    print("   - user テーブルを削除中...")
                    conn.execute(text('DROP TABLE IF EXISTS "user" CASCADE;'))
                    
                    # コミット
                    trans.commit()
                    print("✅ 削除完了")
                    print()
                except Exception as e:
                    trans.rollback()
                    raise e
            
            print("🔨 新しいテーブルを作成中...")
            db.create_all()
            print("✅ 作成完了")
            print()
            
            # 作成されたテーブルを確認
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print("📋 作成されたテーブル:")
            for table in tables:
                print(f"   - {table}")
                if table == 'user':
                    columns = inspector.get_columns(table)
                    for col in columns:
                        if col['name'] == 'password_hash':
                            col_type = str(col['type'])
                            print(f"     ✓ password_hash: {col_type}")
            print()
            
            print("✅ スキーマ更新完了")
            print()
            print("次のステップ:")
            print("  1. 管理者ユーザーを作成:")
            print("     python create_user.py admin password123 --role admin")
            print()
            print("  2. ユーザー一覧を確認:")
            print("     python list_users.py")
            
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
            print()
            print("💡 手動でテーブルを削除してください:")
            print()
            print("以下のSQLを実行:")
            print('  DROP TABLE IF EXISTS participant CASCADE;')
            print('  DROP TABLE IF EXISTS "user" CASCADE;')
            print()
            print("その後、テーブルを作成:")
            print("  python init_db.py")
        
        print()
        print("=" * 60)

if __name__ == '__main__':
    recreate_tables()

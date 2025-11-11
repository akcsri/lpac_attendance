#!/usr/bin/env python3
"""
手動でSQLを実行してテーブルを再作成

使い方:
  python manual_recreate.py
"""

from app import app, db
from sqlalchemy import text

def manual_recreate():
    with app.app_context():
        print("=" * 60)
        print("🛠️  手動テーブル再作成")
        print("=" * 60)
        print()
        
        print("以下のSQLを実行します:")
        print()
        
        sqls = [
            'DROP TABLE IF EXISTS participant CASCADE;',
            'DROP TABLE IF EXISTS "user" CASCADE;',
            '''CREATE TABLE "user" (
                id SERIAL PRIMARY KEY,
                username VARCHAR(150) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL
            );''',
            '''CREATE TABLE participant (
                id SERIAL PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                email VARCHAR(150) NOT NULL,
                position VARCHAR(150) NOT NULL,
                questions TEXT,
                status VARCHAR(100),
                user_id INTEGER NOT NULL REFERENCES "user"(id)
            );'''
        ]
        
        for i, sql in enumerate(sqls, 1):
            print(f"{i}. {sql}")
        print()
        
        response = input("実行しますか？ (yes/no): ").strip().lower()
        if response != 'yes':
            print("❌ キャンセルしました")
            return
        
        print()
        print("📊 SQL実行中...")
        print()
        
        try:
            with db.engine.connect() as conn:
                trans = conn.begin()
                try:
                    for i, sql in enumerate(sqls, 1):
                        print(f"  {i}. 実行中: {sql[:50]}...")
                        conn.execute(text(sql))
                        print(f"     ✅ 完了")
                    
                    trans.commit()
                    print()
                    print("✅ すべてのSQLが正常に実行されました")
                    print()
                    print("📋 作成されたテーブル:")
                    print("   - user (password_hash: VARCHAR(255))")
                    print("   - participant")
                    print()
                    print("次のステップ:")
                    print("  python create_user.py admin password123 --role admin")
                    
                except Exception as e:
                    trans.rollback()
                    print(f"     ❌ エラー: {e}")
                    raise
                    
        except Exception as e:
            print()
            print(f"❌ SQLの実行に失敗しました: {e}")
            print()
            print("💡 psqlコマンドで手動実行してください:")
            print()
            print("以下をコピーして実行:")
            print("-" * 60)
            for sql in sqls:
                print(sql)
            print("-" * 60)
        
        print()
        print("=" * 60)

if __name__ == '__main__':
    manual_recreate()

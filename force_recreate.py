#!/usr/bin/env python3
"""
テーブル直接再作成（確認なし）

使い方:
  python force_recreate.py
"""

from app import app, db
from sqlalchemy import text

def force_recreate():
    with app.app_context():
        print("=" * 60)
        print("🛠️  テーブル強制再作成")
        print("=" * 60)
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
        
        print("📊 SQL実行中...")
        print()
        
        try:
            with db.engine.connect() as conn:
                trans = conn.begin()
                try:
                    for i, sql in enumerate(sqls, 1):
                        print(f"  {i}. {sql.split()[0]} {sql.split()[1] if len(sql.split()) > 1 else ''}...")
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
                    print("  python create_user.py admin admin123 --role admin")
                    
                except Exception as e:
                    trans.rollback()
                    print(f"     ❌ エラー: {e}")
                    raise
                    
        except Exception as e:
            print()
            print(f"❌ SQLの実行に失敗しました: {e}")
            print()
            print("💡 データベースへのアクセスに問題がある可能性があります")
            print("   DATABASE_URLを確認してください")
        
        print()
        print("=" * 60)

if __name__ == '__main__':
    print("⚠️  警告: このスクリプトは確認なしでテーブルを削除・再作成します")
    print()
    force_recreate()

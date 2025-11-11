#!/usr/bin/env python3
"""
最もシンプルなテーブル再作成

使い方:
  python simple_recreate.py
"""

import os
import psycopg2

# DATABASE_URLを取得
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URLが設定されていません")
    exit(1)

# postgres:// を postgresql:// に変換
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')

print("=" * 60)
print("🔧 シンプルテーブル再作成")
print("=" * 60)
print()

# SQLリスト
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

try:
    print("📊 データベースに接続中...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    cursor = conn.cursor()
    print("✅ 接続成功")
    print()
    
    print("🗑️ 既存テーブルを削除中...")
    cursor.execute(sqls[0])
    print("   ✅ participant テーブル削除")
    cursor.execute(sqls[1])
    print("   ✅ user テーブル削除")
    print()
    
    print("🔨 新しいテーブルを作成中...")
    cursor.execute(sqls[2])
    print("   ✅ user テーブル作成 (password_hash: VARCHAR(255))")
    cursor.execute(sqls[3])
    print("   ✅ participant テーブル作成")
    print()
    
    conn.commit()
    print("✅ コミット完了")
    print()
    
    # 確認
    cursor.execute("SELECT column_name, data_type, character_maximum_length FROM information_schema.columns WHERE table_name = 'user' AND column_name = 'password_hash';")
    result = cursor.fetchone()
    if result:
        print(f"📋 確認: password_hash = {result[1]}({result[2]})")
    print()
    
    cursor.close()
    conn.close()
    
    print("✅ テーブル再作成完了！")
    print()
    print("次のステップ:")
    print("  python create_user.py admin admin123 --role admin")
    
except Exception as e:
    print(f"❌ エラーが発生しました: {e}")
    print()
    print("💡 トラブルシューティング:")
    print("1. DATABASE_URLが正しいか確認")
    print("2. PostgreSQLが起動しているか確認")
    print("3. ネットワーク接続を確認")
    
    if 'conn' in locals():
        conn.rollback()
        conn.close()

print()
print("=" * 60)

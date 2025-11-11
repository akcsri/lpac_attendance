#!/usr/bin/env python3
"""
データベーススキーマ更新スクリプト

password_hashカラムのサイズを150から255に変更します。

使い方:
  python update_schema.py
"""

from app import app, db
from sqlalchemy import text

def update_schema():
    with app.app_context():
        print("=" * 60)
        print("🔧 データベーススキーマ更新")
        print("=" * 60)
        print()
        
        try:
            # PostgreSQLの場合
            print("📊 password_hashカラムのサイズを255文字に拡張中...")
            
            # ALTER TABLEを実行
            with db.engine.connect() as conn:
                conn.execute(text('ALTER TABLE "user" ALTER COLUMN password_hash TYPE VARCHAR(255);'))
                conn.commit()
            
            print("✅ スキーマ更新完了")
            print()
            print("変更内容:")
            print("  - password_hash: VARCHAR(150) → VARCHAR(255)")
            print()
            print("✅ これでユーザーを作成できます:")
            print("   python create_user.py admin password123 --role admin")
            
        except Exception as e:
            error_msg = str(e)
            
            if "does not exist" in error_msg or "no such table" in error_msg:
                print("⚠️ テーブルがまだ作成されていません")
                print()
                print("💡 まずテーブルを作成してください:")
                print("   python init_db.py")
                print()
                print("その後、ユーザーを作成できます:")
                print("   python create_user.py admin password123 --role admin")
                
            elif "already" in error_msg.lower() or "cannot alter type" in error_msg.lower():
                print("ℹ️ カラムはすでに更新されている可能性があります")
                print()
                print("✅ ユーザー作成を試してください:")
                print("   python create_user.py admin password123 --role admin")
                
            else:
                print(f"❌ エラーが発生しました: {e}")
                print()
                print("💡 代替方法:")
                print("1. テーブルを削除して再作成:")
                print("   python recreate_tables.py")
                print()
                print("2. または手動でSQL実行:")
                print('   ALTER TABLE "user" ALTER COLUMN password_hash TYPE VARCHAR(255);')
        
        print()
        print("=" * 60)

if __name__ == '__main__':
    update_schema()

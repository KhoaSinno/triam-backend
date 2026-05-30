import os
import sys
import argparse
from sqlalchemy import text

# Thêm root path vào SYS_PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import engine
from app.core.logger import log

def clean_db():
    parser = argparse.ArgumentParser(description="Dọn dẹp sạch sẽ database Supabase.")
    parser.add_argument("--force", action="store_true", help="Bỏ qua nhắc nhở xác nhận.")
    args = parser.parse_args()

    print("=" * 60)
    print("          CẢNH BÁO: DỌN DẸP SẠCH SẼ DATABASE SUPABASE")
    print("=" * 60)

    if not args.force:
        confirm = input("⚠️ Hành động này sẽ XÓA TOÀN BỘ BẢNG VÀ DỮ LIỆU của dự án trên Database. Bạn có chắc chắn muốn tiếp tục? (y/N): ")
        if confirm.lower() != 'y':
            print("❌ Hủy bỏ hành động dọn dẹp database.")
            return

    print("[*] Đang kết nối và dọn dẹp cơ sở dữ liệu...")
    try:
        with engine.connect() as connection:
            # Drop schema public để xóa sạch toàn bộ bảng, view, types, trigger cũ
            print("[*] Đang xóa schema 'public'...")
            connection.execute(text("DROP SCHEMA public CASCADE;"))
            
            print("[*] Đang tạo mới schema 'public'...")
            connection.execute(text("CREATE SCHEMA public;"))
            connection.execute(text("GRANT ALL ON SCHEMA public TO postgres;"))
            connection.execute(text("GRANT ALL ON SCHEMA public TO public;"))
            
            print("[*] Đang kích hoạt extension 'vector' (cho pgvector)...")
            connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            
            connection.commit()
            print("✅ DỌN DẸP DATABASE THÀNH CÔNG! Cơ sở dữ liệu hiện đã trống hoàn toàn.")
    except Exception as e:
        print(f"[!] Gặp lỗi khi dọn dẹp database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    clean_db()

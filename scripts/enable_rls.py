import os
import sys
from sqlalchemy import text

# Thêm root path vào SYS_PATH để nhận diện được module "app"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import engine

def enable_rls_on_all_tables():
    print("🔄 Đang kết nối database để thiết lập Row Level Security (RLS)...")
    try:
        with engine.begin() as conn:
            # 1. Lấy danh sách tất cả các bảng trong schema public
            result = conn.execute(text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public' AND table_type = 'BASE TABLE';"
            ))
            tables = [row[0] for row in result.fetchall()]
            
            print(f"📋 Tìm thấy {len(tables)} bảng cần bật RLS: {tables}")
            
            for table in tables:
                print(f"🔒 Thiết lập RLS cho bảng: {table}...")
                
                # Bật RLS
                conn.execute(text(f"ALTER TABLE public.{table} ENABLE ROW LEVEL SECURITY;"))
                
                # Xóa policy cũ nếu có trùng tên
                conn.execute(text(f'DROP POLICY IF EXISTS "Allow service_role full access" ON public.{table};'))
                
                # Tạo policy cho phép service_role có toàn quyền (ALL)
                conn.execute(text(
                    f'CREATE POLICY "Allow service_role full access" ON public.{table} '
                    f'FOR ALL TO service_role USING (true) WITH CHECK (true);'
                ))
                
                print(f"   ✅ Đã bật RLS và cấu hình policy cho service_role.")
                
            print("🎉 Bật RLS và cấu hình bảo mật thành công cho toàn bộ các bảng!")
    except Exception as e:
        print("❌ Lỗi khi thiết lập RLS:")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    enable_rls_on_all_tables()

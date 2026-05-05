import os
import sys

# Thêm root path vào SYS_PATH để nhận diện được module "app"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select

from app.db.database import engine
from app.models.db_models import Book


def test_connection():
    print("🔄 Đang cố gắng kết nối với Supabase...")
    try:
        with Session(engine) as session:
            # Chạy thử 1 truy vấn đơn giản
            statement = select(Book).limit(1)
            result = session.exec(statement).first()
            print("✅ Kết nối Database THÀNH CÔNG!")
            if result:
                print(f"📖 Lấy thành công Book từ DB: {result.title}")
            else:
                print("⚠️ Kết nối thành công, bảng 'books' hiện đang rỗng.")
    except Exception as e:
        print("❌ Lỗi kết nối Database:")
        print(str(e))
        print("\n💡 Gợi ý: Hãy chắc chắn bạn đã điền đúng mât khẩu và chuỗi DATABASE_URL trong file .env")


if __name__ == "__main__":
    test_connection()

# Cấu trúc thư mục

```text
triam-backend/
├── app/
│   ├── api/                # Nơi chứa các route (Endpoints)
│   ├── core/               # Config, bảo mật, biến môi trường
│   ├── crud/               # Logic tương tác DB (Create, Read, Update, Delete)
│   ├── models/             # SQLModel Classes (Table definitions)
│   ├── services/           # Business logic (Xử lý AI, Voice-to-text,...)
│   ├── db.py               # Khởi tạo Engine và Session
│   └── main.py             # File chạy chính
├── .env                    # Chứa DATABASE_URL của Supabase
├── pyproject.toml          # Quản lý bởi uv
└── uv.lock
```

---

### 1. `app/models/audiobook.py` (Lớp Bản thiết kế)

Đây là nơi bạn định nghĩa dữ liệu trông như thế nào. SQLModel cho phép bạn dùng một Class cho cả Database (Table) và API (Pydantic).

```python
from sqlmodel import SQLModel, Field
from typing import Optional

class Audiobook(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str
    description: Optional[str] = None
    file_url: str  # Link file từ Supabase Storage
```

---

### 2. `app/db.py` (Lớp Kết nối)

Nơi duy nhất giữ chìa khóa mở cổng vào Supabase.

```python
import os
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session
```

---

### 3. `app/crud/audiobook.py` (Lớp Thao tác dữ liệu)

Lớp này giống như một "thủ thư". Bạn muốn lấy sách, thêm sách thì gọi ông này. Code ở đây chỉ thuần túy là truy vấn.

```python
from sqlmodel import Session, select
from app.models.audiobook import Audiobook

def get_audiobooks(session: Session):
    # Lấy danh sách tất cả sách
    return session.exec(select(Audiobook)).all()

def create_audiobook(session: Session, book: Audiobook):
    # Lưu một cuốn sách mới vào Supabase
    session.add(book)
    session.commit()
    session.refresh(book)
    return book
```

---

### 4. `app/api/v1/endpoints/audiobooks.py` (Lớp Tiếp tân)

Đây là các Route mà App Flutter của bạn sẽ gọi tới. Nó chỉ nhận yêu cầu và điều phối.

```python
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db import get_session
from app.models.audiobook import Audiobook
from app.crud import audiobook as crud_book

router = APIRouter()

@router.get("/", response_model=list[Audiobook])
def read_all_books(session: Session = Depends(get_session)):
    return crud_book.get_audiobooks(session)

@router.post("/", response_model=Audiobook)
def add_new_book(book: Audiobook, session: Session = Depends(get_session)):
    return crud_book.create_audiobook(session, book)
```

---

### 5. `app/main.py` (Đầu não)

Nơi lắp ghép tất cả các mảnh ghép lại với nhau.

```python
from fastapi import FastAPI
from app.api.v1.endpoints import audiobooks
from app.db import engine, SQLModel

app = FastAPI(title="TRIAM Assistant API")

# Tự động tạo bảng trên Supabase khi khởi chạy (nếu chưa có)
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Gắn các route của audiobook vào ứng dụng chính
app.include_router(audiobooks.router, prefix="/audiobooks", tags=["Audiobooks"])
```

---

### 6. Tại sao chia như vậy lại "Clean"?

1.  **Dễ tìm lỗi:** Nếu app báo lỗi không lưu được dữ liệu -> Vào `crud/` hoặc `db.py`. Nếu link API sai -> Vào `api/`.
2.  **Mở rộng cực nhanh:** Khi TRIAM có thêm tính năng AI Chat, bạn chỉ cần tạo `app/services/ai_service.py` để xử lý logic AI, rồi gọi nó từ Route.
3.  **Tái sử dụng:** Sau này bạn làm module "Gợi ý sách", bạn có thể gọi lại hàm `get_audiobooks` ở lớp CRUD mà không cần viết lại câu lệnh SQL.
# 🚀 Bí Kíp Clean Code & Best Practices (Triam Backend)

Chào mừng bạn đến với thế giới của **Clean Code**! Viết code chạy được là một chuyện, nhưng viết code để 6 tháng sau đọc lại vẫn hiểu, hoặc đưa cho người khác bảo trì dễ dàng lại là một nghệ thuật.

Trong dự án `Triam Backend` (sử dụng FastAPI + SQLModel), chúng ta áp dụng tư tưởng **Clean Architecture** (Kiến trúc Sạch). Dưới đây là những nguyên tắc cốt lõi được đúc kết từ quá trình refactor hệ thống của bạn.

---

## 1. Tư Duy Cốt Lõi: Sự Tách Biệt Trách Nhiệm (Separation of Concerns)

Lỗi phổ biến nhất của người mới là "nhét" mọi thứ vào chung một hàm: Từ xác thực user, kết nối DB, query dữ liệu, xử lý AI, cho đến trả về HTTP Response. Điều này tạo ra "Spaghetti Code" (Code rác rưởi rối rắm).

**Nguyên tắc vàng:** Mỗi file, mỗi lớp (layer) chỉ làm đúng 1 việc.

Trong dự án của chúng ta, các lớp được phân chia nghiêm ngặt:

1. **Layer 1: Routing (API Endpoints)** - `app/api/v1/endpoints/`
   - **Nhiệm vụ:** Nhận request từ User, xác thực (Auth), gọi xuống tầng dưới để lấy dữ liệu, và trả về HTTP Response (200 OK, 404 Not Found).
   - **Cấm kỵ:** Tuyệt đối không viết logic kết nối Database hoặc logic AI phức tạp ở đây.
2. **Layer 2: Business Logic (Services)** - `app/services/`
   - **Nhiệm vụ:** Nơi chứa "não bộ" của ứng dụng. Xử lý logic gọi AI, convert Audio, tính toán,...
3. **Layer 3: Data Access (CRUD)** - `app/crud/`
   - **Nhiệm vụ:** Chỉ nói chuyện với Database. Nhận tham số, thực thi câu lệnh SQL (qua SQLModel) và trả về cục Data.
   - **Cấm kỵ:** Không tự ý lấy thông tin User (như gán cứng `MOCK_USER_ID`), không trả về lỗi HTTP 404 (vì CRUD không biết HTTP là gì).

---

## 2. Case Study Thực Tế: Refactor tính năng Study Context

Hãy nhìn lại chính đoạn code mà chúng ta vừa sửa để thấy rõ sự khác biệt giữa "Bad Code" và "Clean Code".

### ❌ Bad Code (Trước khi sửa)
```python
# Trong file app/crud/study_context.py (Tầng CRUD)
MOCK_USER_ID = "862d7c26-3160-4f76-9e77-07d91f7317cc"

def get_study_contexts(session: Session, user_id: uuid.UUID = MOCK_USER_ID):
    # LỖI 1: Tầng DB không được phép chứa biến "Giả lập User". 
    # Nếu sau này có 1000 users, hàm này sẽ sai hoàn toàn.
    return session.exec(select(StudyContext).where(StudyContext.user_id == user_id)).all()

# Trong file app/api/v1/endpoints/study_context.py (Tầng API)
@router.delete("/study-contexts/documents/{document_id}")
async def delete_study_context_document(document_id: uuid.UUID):
    # LỖI 2: Tự tạo Session Database ngay trong hàm API.
    # Vừa tốn tài nguyên, vừa khó viết Test tự động sau này.
    with Session(engine) as session:
        delete_study_context_document(session, document_id)
    return {"message": "Context document deleted successfully"}
```

### ✅ Clean Code (Sau khi đã sửa)
```python
# Tầng CRUD: app/crud/study_context.py
# -> TRONG SẠCH, CHỈ CÓ LOGIC DATABASE
def get_study_contexts(session: Session, user_id: str) -> list[StudyContext]:
    return session.exec(select(StudyContext).where(StudyContext.user_id == user_id)).all()

# Tầng API: app/api/v1/endpoints/study_context.py
# -> QUẢN LÝ HTTP & AUTHENTICATION
MOCK_USER_ID = "862d7c26-3160-4f76-9e77-07d91f7317cc"

@router.delete("/study-contexts/{context_id}")
async def delete_study_context_api(
    context_id: uuid.UUID, 
    session: Session = Depends(get_session) # XỬ LÝ LỖI 2 BẰNG DEPENDENCY INJECTION
):
    # Tầng API chịu trách nhiệm kiểm tra xem User có quyền xóa hay không
    context = get_study_context(session, context_id)
    if not context or context.user_id != MOCK_USER_ID:
        raise HTTPException(status_code=404, detail="Study context not found")

    # Gọi xuống CRUD để xóa
    delete_study_context(session, context_id)
    return {"message": "Study context deleted successfully"}
```

---

## 3. Top 3 "Vũ Khí" Của FastAPI Cần Thuần Thục

### Vũ khí 1: Dependency Injection (`Depends`)
Thay vì tự mở và đóng kết nối Database (`with Session(engine)`), FastAPI cung cấp cơ chế `Depends`. 
Khi bạn viết `session: Session = Depends(get_session)`, FastAPI sẽ:
- Tự động mở kết nối DB khi request chạy vào.
- Tự động truyền biến `session` đó cho bạn dùng.
- Tự động đóng kết nối (close) khi request kết thúc.
=> Bạn sẽ không bao giờ sợ bị "tràn bộ nhớ" hay "kẹt Database connection".

### Vũ khí 2: Phân biệt rõ Data Model vs Schema Model
- **`app/models/db_models.py` (SQLModel `table=True`):** Là cấu trúc cái bàn/cái ghế lưu dưới ổ cứng (Database).
- **`app/schemas/` (Pydantic `BaseModel` hoặc SQLModel `table=False`):** Là cái "hộp quà" để đóng gói dữ liệu gửi cho Frontend hoặc nhận từ Frontend.
- **Vì sao không dùng chung 1 cái?** Vì đôi khi bạn cần trả về Frontend một thông tin tổng hợp (ví dụ: Tên Sách + Số lượng Chat) nhưng dưới DB thì 2 thông tin này nằm ở 2 bảng khác nhau.

### Vũ khí 3: Type Hinting (Gợi ý kiểu dữ liệu)
Hãy nhìn vào các hàm mới tôi viết:
```python
def get_study_context(...) -> StudyContext | None:
```
Luôn khai báo kiểu dữ liệu trả về (`->`). Nhờ nó, IDE (VSCode/Cursor) sẽ tự động nhắc code, báo lỗi ngay lập tức nếu bạn code sai. Đừng bao giờ viết code Python kiểu "mù mờ" (không có Type Hinting).

---

## 4. Lời Khuyên Dành Cho Bạn 💡

1. **Rule of Thumb (Nguyên tắc Ngón Tay Cái):** Khi viết một hàm ở tầng API, nếu hàm đó dài quá **30 dòng**, chắc chắn bạn đang code sai (chứa quá nhiều logic). Hãy tách nó ra và ném bớt logic xuống tầng `services` hoặc `crud`.
2. **Naming (Đặt tên):** Đặt tên biến/hàm dài cũng không sao, miễn là nó RÕ RÀNG.
   - ❌ Thay vì: `def get_ctx_doc()`
   - ✅ Hãy dùng: `def get_context_documents()`
3. **Đừng sợ tạo ra file mới:** Nếu thấy một file quá dài, hãy cắt nó ra làm nhiều file nhỏ. Cấu trúc thư mục ngăn nắp thì não bộ cũng sẽ ngăn nắp.

Chúc bạn code ngày càng "sạch" và "chất" nhé! Kiến trúc hiện tại của dự án Triam đã rất vững chắc rồi, hãy cứ bám theo flow này để phát triển!

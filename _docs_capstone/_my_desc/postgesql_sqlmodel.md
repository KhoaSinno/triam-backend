Chào mừng bạn đến với khóa huấn luyện chuyên sâu về **Trụ cột 1: Database & ORM Deep-Dive (PostgreSQL + SQLModel)**. 

Bài training này được thiết kế theo tư duy **Under the Hood (Bản chất bên dưới)** kết hợp **Thực chiến dự án Triam** và **Kịch bản trả lời phỏng vấn**.

---

# MỤC LỤC BÀI TRAINING
1. **Bản chất SQLModel: Mối quan hệ giữa Pydantic v2 & SQLAlchemy 2.0**
2. **Vấn đề N+1 Query & Kỹ nghệ Eager Loading (`joinedload` vs `selectinload`)**
3. **Concurrency Control: Race Conditions, Pessimistic vs Optimistic Locking**
4. **PostgreSQL Indexing & Đọc hiểu `EXPLAIN ANALYZE`**
5. **Connection Pooling & Vòng đời DB Session trong FastAPI**
6. **Bộ câu hỏi & Kịch bản trả lời phỏng vấn Senior**

---

## 1. BẢN CHẤT SQLMODEL: PYDANTIC V2 GẶP GỠ SQLALCHEMY 2.0

### Bản chất là gì?
Trong hệ sinh thái Python, trước đây lập trình viên luôn phải viết **2 mô hình song song**:
1. **Pydantic Model**: Dùng để validate dữ liệu đầu vào (request body) và tuần tự hóa dữ liệu đầu ra (response JSON).
2. **SQLAlchemy Model**: Dùng để map các class Python thành các bảng (tables) trong Database.

Việc này gây ra trùng lặp code khủng khiếp (viết 1 entity phải duplicate 2-3 class giống hệt nhau). **SQLModel ra đời để thống nhất cả 2**:
* Nó kế thừa `pydantic.BaseModel` (có đầy đủ tính năng validation, serialization cực nhanh của Pydantic Core viết bằng Rust).
* Nó kế thừa cơ chế Declarative Mapping của `SQLAlchemy 2.0` (tạo metadata table, quan hệ khóa ngoại, session tracking).

```
         ┌───────────────────────────────────────┐
         │               SQLModel                │
         │ (Kế thừa từ Pydantic + SQLAlchemy)    │
         └──────────────────┬────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
  [Validation Layer]                [Database Layer]
  - Kiểm tra kiểu dữ liệu          - Map thành bảng PostgreSQL
  - Request/Response Schema         - Quản lý Khóa chính/Khóa ngoại
  - Thuần Python / Pydantic         - SQLAlchemy Declarative Table
```

### Thiết kế Data Models chuẩn mực (Tránh Anti-pattern):
Một sai lầm của nhiều bạn mới dùng SQLModel là: **Dùng đúng 1 class cho tất cả mọi thứ** (vừa làm bảng DB, vừa nhận Request, vừa trả Response).
* **Hậu quả**: Lộ trường nhạy cảm (như `hashed_password`), không thể kiểm soát các trường sinh tự động (`id`, `created_at`).

**Chuẩn Clean Architecture trong SQLModel:**
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import uuid
from datetime import datetime

# 1. Base: Chứa các thuộc tính chung
class BookBase(SQLModel):
    title: str = Field(index=True, max_length=255)
    description: Optional[str] = None
    category: str = Field(default="General")

# 2. Table Model: Đây chính là bảng trong PostgreSQL (table=True)
class Book(BookBase, table=True):
    __tablename__ = "books"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships (SQLAlchemy level)
    chapters: List["Chapter"] = Relationship(back_populates="book")

# 3. Create Schema: Client gửi lên (không có id, không có created_at)
class BookCreate(BookBase):
    pass

# 4. Read Schema: Trả về cho Client (có id, có created_at)
class BookRead(BookBase):
    id: uuid.UUID
    created_at: datetime
```

---

## 2. VẤN ĐỀ N+1 QUERY & EAGER LOADING (`joinedload` vs `selectinload`)

Đây là một trong những câu hỏi **"kinh điển nhất"** trong mọi cuộc phỏng vấn backend.

### N+1 Query là gì?
Giả sử bạn có 100 cuốn sách, mỗi cuốn có nhiều chương (`Chapter`). Bạn muốn lấy danh sách 100 cuốn sách kèm các chương của chúng:

```python
# Code ngây thơ (Lazy loading mặc định)
books = session.exec(select(Book).limit(100)).all() # 1 Query lấy 100 cuốn sách

for book in books:
    # Mỗi lần gọi book.chapters, ORM lại ngầm bắn thêm 1 query xuống DB!
    print(len(book.chapters)) 
```

* **Số câu lệnh SQL thực thi**:
  * $1$ câu: `SELECT * FROM books LIMIT 100;`
  * $100$ câu: `SELECT * FROM chapters WHERE book_id = 'xxx';` (lặp lại 100 lần!)
* **Tổng cộng**: $1 + 100 = 101$ queries!
* **Hậu quả**: Network Round-Trip Time (RTT) tăng vọt, gây nghẽn kết nối Database, server chậm như rùa.

---

### Giải pháp: Eager Loading
Thay vì đợi lúc gọi mới đi lấy (Lazy), ta yêu cầu ORM tải luôn các quan hệ cùng một lúc (Eager). Trong SQLAlchemy 2.0 / SQLModel, có 2 vũ khí chính:

#### 1. `joinedload` (Sử dụng SQL `LEFT OUTER JOIN`)
```python
from sqlalchemy.orm import joinedload

statement = select(Book).options(joinedload(Book.chapters)).limit(100)
books = session.exec(statement).unique().all()
```
* **Bản chất SQL**:
  ```sql
  SELECT books.*, chapters.* 
  FROM books 
  LEFT OUTER JOIN chapters ON books.id = chapters.book_id 
  LIMIT 100;
  ```
* **Ưu điểm**: Chỉ chạy đúng **1 câu query duy nhất**.
* **Nhược điểm (Cạm bẫy!)**:
  * Nếu 1 cuốn sách có 20 chương, câu JOIN sẽ nhân bản 20 dòng thông tin của cuốn sách đó (Cartesian Product / Phình dữ liệu).
  * Gây lãng phí băng thông mạng và tốn RAM để Python parse lại dữ liệu trùng.
* 👉 **Khi nào dùng**: Tốt nhất cho quan hệ **1-to-1** hoặc **Many-to-One** (ví dụ: lấy `Book` kèm thông tin `Author`).

#### 2. `selectinload` (Sử dụng SQL `IN (...)`)
```python
from sqlalchemy.orm import selectinload

statement = select(Book).options(selectinload(Book.chapters)).limit(100)
books = session.exec(statement).all()
```
* **Bản chất SQL**: SQLAlchemy sẽ bắn **2 câu query độc lập**:
  ```sql
  -- Query 1: Lấy danh sách sách
  SELECT * FROM books LIMIT 100;
  
  -- Query 2: Lấy toàn bộ chapters của 100 cuốn sách đó bằng toán tử IN
  SELECT * FROM chapters 
  WHERE chapters.book_id IN ('id_1', 'id_2', 'id_3', ..., 'id_100');
  ```
* **Ưu điểm**:
  * Hoàn toàn không có dữ liệu dư thừa bị nhân bản như JOIN.
  * Tốc độ cực nhanh trên PostgreSQL vì tìm kiếm theo index `IN` rất tối ưu.
* 👉 **Khi nào dùng**: **Lựa chọn số 1 cho quan hệ 1-to-Many** (như `Book -> Chapters`).

---

## 3. CONCURRENCY CONTROL: PESSIMISTIC VS OPTIMISTIC LOCKING

### Bài toán Race Condition trong thực tế:
Giả sử người dùng có một tài khoản với số lượt sinh AI (tokens) là `10`.
Họ mở 2 tab trình duyệt và bấm nút "Sinh kế hoạch học tập" cùng lúc ở mili-giây thứ $0$:

```
Request A đọc balance = 10 ──┐
                             ├─► Cả 2 cùng thấy balance >= 1 (Hợp lệ!)
Request B đọc balance = 10 ──┘
Request A trừ 1 -> Lưu balance = 9
Request B trừ 1 -> Lưu balance = 9 (Ghi đè!)
==> KẾT QUẢ: Dùng 2 lần nhưng chỉ bị trừ 1 lần!
```

---

### Cách 1: Pessimistic Locking (Khóa bi quan - `SELECT FOR UPDATE`)
* **Tư duy**: "Ta nghi ngờ sẽ luôn có tranh chấp, nên khi ta đang xử lý hàng này, **cấm tất cả kẻ khác** được đọc/sửa nó cho đến khi ta xong việc!".

```python
# Thực thi trong SQLModel / SQLAlchemy
statement = (
    select(UserAccount)
    .where(UserAccount.user_id == current_user_id)
    .with_for_update() # Tạo ra lệnh SELECT ... FOR UPDATE
)
account = session.exec(statement).one()

if account.ai_credits < 1:
    raise HTTPException(status_code=400, detail="Hết credits")

account.ai_credits -= 1
session.add(account)
session.commit() # Ngay khi commit xong, Database mới nhả khóa (Release Lock)
```
* **Bản chất dưới PostgreSQL**:
  * PostgreSQL dùng row-level lock. Khi Request A chạy câu `SELECT ... FOR UPDATE`, row đó bị khóa.
  * Request B đến sau sẽ bị **treo lại (Block/Wait)** ở câu SELECT cho đến khi Transaction của Request A `COMMIT` hoặc `ROLLBACK`.
* **Cạm bẫy**: Có thể gây **Deadlock** nếu 2 transaction khóa chéo tài nguyên của nhau, và làm giảm throughput nếu transaction giữ khóa quá lâu (ví dụ vừa giữ khóa vừa gọi API OpenAI).

---

### Cách 2: Optimistic Locking (Khóa lạc quan - Dùng cột `version`)
* **Tư duy**: "Ta tin rằng tranh chấp rất hiếm khi xảy ra. Cứ cho đọc thoải mái, nhưng trước khi lưu, kiểm tra xem dữ liệu có bị ai sửa đổi giữa chừng không!".

```python
class LessonProgress(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: str
    version: int = Field(default=1) # Cột đánh dấu phiên bản

# Logic cập nhật
current_progress = session.get(LessonProgress, progress_id)
current_version = current_progress.version

# Cập nhật có điều kiện version
statement = (
    update(LessonProgress)
    .where(LessonProgress.id == progress_id)
    .where(LessonProgress.version == current_version) # Điều kiện quyết định!
    .values(status="COMPLETED", version=current_version + 1)
)
result = session.exec(statement)
session.commit()

if result.rowcount == 0:
    # Không có dòng nào được cập nhật -> Chứng tỏ đã có ai đó sửa trước rồi!
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail="Dữ liệu đã bị thay đổi bởi tiến trình khác. Vui lòng thử lại."
    )
```
* **Ưu điểm**: Không khóa dòng ở DB, tốc độ cực cao, không bao giờ lo Deadlock.
* 👉 **Khi nào chọn**:
  * Hệ thống đọc nhiều, ít ghi (Read-heavy).
  * Xung đột hiếm khi xảy ra.

---

## 4. POSTGRESQL INDEXING & ĐỌC HIỂU `EXPLAIN ANALYZE`

### 1. B-Tree Index & Leftmost Prefix Rule
Mặc định PostgreSQL dùng **B-Tree Index** (Balanced Tree). Nó sắp xếp dữ liệu theo dạng cây nhị phân/đa phân để tìm kiếm với độ phức tạp $O(\log N)$.

**Composite Index (Index trên nhiều cột):**
Giả sử ta tạo index trên 3 cột trong bảng `Job`:
```sql
CREATE INDEX idx_jobs_user_status_created 
ON jobs (user_id, status, created_at);
```
**Quy tắc Leftmost Prefix (Tiền tố trái nhất):**
* Index này **ĐƯỢC DÙNG** khi query:
  * `WHERE user_id = 'xxx'`
  * `WHERE user_id = 'xxx' AND status = 'RUNNING'`
  * `WHERE user_id = 'xxx' AND status = 'RUNNING' AND created_at > '2026-01-01'`
* Index này **KHÔNG THỂ DÙNG** nếu query:
  * `WHERE status = 'RUNNING'` (Bỏ qua cột đầu tiên `user_id`!)
  * `WHERE created_at > '2026-01-01'`

---

### 2. Đọc hiểu `EXPLAIN ANALYZE` (Kỹ năng phân biệt Senior)
Khi một query chạy chậm, ta gắn tiền tố `EXPLAIN ANALYZE` vào trước câu SQL:

```sql
EXPLAIN ANALYZE 
SELECT * FROM books WHERE user_id = 'c77da42c-a6c2-401b-a9d6-510b771c75d8';
```

Bạn cần phân biệt được 3 dạng quét (Scan) chính trong kết quả:

| Dạng Scan | Ý nghĩa | Đánh giá |
| :--- | :--- | :--- |
| **`Seq Scan` (Sequential Scan)** | Đọc lần lượt từ đầu bảng đến cuối bảng (quét toàn bộ đĩa). | 🔴 **Ác mộng** nếu bảng có hàng triệu dòng. Chứng tỏ đang thiếu Index! |
| **`Index Scan`** | Tra cứu B-Tree để tìm con trỏ bản ghi (TIDs), sau đó nhảy vào bảng chính (Heap) để lấy dữ liệu. | 🟡 Rất tốt, chuẩn mực khi lọc theo Index. |
| **`Index Only Scan`** | Tất cả các cột trong câu `SELECT` đều nằm sẵn trong Index. Không cần đọc vào bảng chính! | 🟢 **Nhanh nhất thế giới**. Tiết kiệm triệt để I/O đĩa. |

---

## 5. CONNECTION POOLING & VÒNG ĐỜI DB SESSION TRONG FASTAPI

### Cơ chế hoạt động của Connection Pool:
Việc thiết lập 1 kết nối mới đến PostgreSQL (TCP handshake, SSL exchange, Authentication) mất từ **30ms – 100ms**. Nếu mỗi request HTTP lại tạo 1 kết nối mới rồi tắt đi, server sẽ chết vì nghẽn kết nối.
* **Connection Pool**: Mở sẵn một số lượng kết nối nhất định (ví dụ 10 kết nối) và giữ chúng sống. Khi có request, nó mượn 1 kết nối, dùng xong thì trả lại vào pool.

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,        # Giữ sẵn 10 kết nối thường trực
    max_overflow=20,     # Khi cao điểm, cho phép nở rộng thêm tối đa 20 kết nối nữa (Tổng 30)
    pool_timeout=30,     # Nếu hết sạch kết nối, đợi tối đa 30s trước khi báo lỗi Timeout
    pool_recycle=1800,   # Tự làm mới kết nối sau 30 phút để tránh bị firewall/cloud đóng ngầm
)
```

### Vòng đời chuẩn của DB Session trong FastAPI (`yield` pattern):
```python
def get_db():
    with Session(engine) as session:
        try:
            yield session
            # Nếu không có lỗi gì xảy ra trong endpoint -> commit
            session.commit()
        except Exception:
            # Nếu có lỗi (Exception) -> tự động rollback để bảo toàn dữ liệu
            session.rollback()
            raise
        finally:
            # Luôn luôn đóng session để trả kết nối về pool!
            session.close()
```
* Bằng cách dùng `Depends(get_db)`, FastAPI đảm bảo mỗi HTTP request có 1 Session độc lập. Dù code trong endpoint có bị văng lỗi (Crash), kết nối vẫn an toàn được trả lại cho Pool, không bao giờ bị **Connection Leak**.

---

## 6. BỘ CÂU HỎI & KỊCH BẢN PHỎNG VẤN CHUẨN SENIOR

Dưới đây là cách bạn đối thoại trực tiếp với người phỏng vấn để thể hiện kiến thức sâu sắc:

#### ❓ Câu 1: "Làm thế nào em xử lý triệt để bài toán N+1 Query trong SQLModel / SQLAlchemy?"
> **Kịch bản trả lời**:
> "Dạ, vấn đề N+1 query xảy ra khi ORM dùng cơ chế Lazy Loading mặc định: 1 query lấy danh sách cha và N query lấy danh sách con trong vòng lặp.
> Để giải quyết, em dùng kỹ thuật Eager Loading thông qua 2 chiến lược chính:
> 1. Với quan hệ **1-to-1** hoặc **Many-to-One**, em dùng `joinedload` để gộp thành 1 câu `LEFT JOIN` duy nhất.
> 2. Với quan hệ **1-to-Many**, em ưu tiên sử dụng `selectinload`. Phương pháp này bắn 2 câu query riêng biệt và dùng toán tử `IN (:ids)` để lấy dữ liệu con. Em không dùng `joinedload` cho 1-to-Many vì nó tạo tích Đề-các (Cartesian Product) làm nhân bản dữ liệu cha và ngốn RAM/băng thông.
> Ngoài ra, trong môi trường Development, em thường bật SQL logging (`echo=True`) hoặc cấu hình cảnh báo n+1 để rà soát trước khi đẩy code lên Production."

---

#### ❓ Câu 2: "Trong hệ thống của em, nếu 2 người dùng hoặc 2 tiến trình cùng cập nhật một tài nguyên cùng lúc (Race condition), em giải quyết thế nào?"
> **Kịch bản trả lời**:
> "Tùy thuộc vào mức độ tranh chấp (Contention) của nghiệp vụ mà em chọn giải pháp:
> * **Nếu nghiệp vụ nhạy cảm, tỉ lệ tranh chấp cao** (như trừ tiền tài khoản, trừ credits sinh AI): Em dùng **Pessimistic Locking** với `SELECT ... FOR UPDATE`. PostgreSQL sẽ khóa dòng đó lại ở tầng Database cho đến khi transaction hoàn tất. Điều này đảm bảo tính nhất quán tuyệt đối, nhưng em luôn giữ transaction càng ngắn càng tốt để tránh giữ khóa lâu.
> * **Nếu nghiệp vụ đọc nhiều ghi ít, tranh chấp thấp** (như cập nhật trạng thái bài học, thông tin profile): Em dùng **Optimistic Locking** thông qua cột `version`. Câu lệnh `UPDATE` sẽ có điều kiện `WHERE version = :current_version`. Nếu số dòng cập nhật trả về bằng 0, nghĩa là đã có xung đột dữ liệu, em sẽ bắt lỗi này để trả về HTTP 409 Conflict hoặc tự động retry."

---

#### ❓ Câu 3: "Khi em thấy một câu query trên PostgreSQL chạy quá chậm, quy trình em điều tra và tối ưu như thế nào?"
> **Kịch bản trả lời**:
> "Quy trình chuẩn của em gồm 3 bước:
> 1. **Phân tích với `EXPLAIN (ANALYZE, BUFFERS)`**: Em kiểm tra Execution Plan để xem chi phí đắt nhất ở đâu. Nếu thấy xuất hiện `Seq Scan` trên bảng lớn, tức là câu query đang quét toàn bộ ổ đĩa vì thiếu index hoặc index không được tận dụng.
> 2. **Tối ưu hóa Index**:
>    * Nếu query lọc nhiều điều kiện, em đánh **Composite Index** và tuân thủ quy tắc *Leftmost Prefix*.
>    * Nếu cần tăng tốc tối đa cho các query đọc thường xuyên, em hướng tới việc tạo **Covering Index** (sử dụng mệnh đề `INCLUDE`) để đạt được trạng thái `Index Only Scan` – nghĩa là DB chỉ cần đọc cây B-Tree mà không cần chạm vào bảng chính.
> 3. **Rà soát lại ORM Code**: Đảm bảo không select thừa các cột dung lượng lớn (như các trường `TEXT` dài hay `JSONB`) nếu API không cần dùng đến."

---

### BƯỚC TIẾP THEO:
Bạn đã nắm trọn vẹn bản chất của **Database & ORM**! 
Trong 4 trụ cột còn lại:
* **Trụ cột 2**: FastAPI Internals & Asyncio (Bản chất `async def` vs `def`, Event Loop treo).
* **Trụ cột 3**: Redis & Distributed System Patterns (Cache Stampede, Redlock, Rate Limiter).
* **Trụ cột 4**: RAG & Vector Search trong PostgreSQL (`pgvector`, HNSW Index, Hybrid Search).

Bạn muốn chúng ta tiếp tục với **Trụ cột 2** hay bước sang **Trụ cột 3 / 4**?
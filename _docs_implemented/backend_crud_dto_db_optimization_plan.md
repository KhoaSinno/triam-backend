# Backend CRUD, DTO, DB Constraint Optimization Plan

Ngay 2026-05-19.

Tai lieu nay tong hop ke hoach optimize backend theo cac van de da review trong doan chat gan day:

- Book CRUD hien co nhung chua user-scoped.
- DTO chua tach ro create/update/response.
- Router con goi repository truc tiep o vai cho.
- Thread/message API chua validate ownership day du.
- DB nen them unique constraints de chan duplicate.
- `Book` nen co `document_type` thay vi infer tu `file_url`.

Muc tieu: dua backend ve huong clean architecture hon, an toan hon cho multi-user, de debug, va on dinh khi worker retry.

> Ghi chu quan trong ve auth hien tai:
>
> Backend da co auth dependency (`get_current_user`) nhung flow san pham hien tai **chua bat user_id that**. Nhieu endpoint van dang dung `MOCK_USER_ID = 862d7c26-3160-4f76-9e77-07d91f7317cc`.
>
> Vi vay plan nay chia lam 2 muc:
>
> - **Implement ngay:** code service/repository theo dang co `user_id` parameter, nhung router van truyen `MOCK_USER_ID`.
> - **Implement sau khi bat auth:** router doi `MOCK_USER_ID` thanh `current_user.sub`.
>
> Cach lam nay giup minh chuan bi kien truc multi-user ma khong lam vo FE/test hien tai.

---

## 1. Ket Luan Review Hien Tai

### Da co

Book:

- `GET /books`
- `GET /books/{book_id}`
- `GET /books/{book_id}/details`
- `POST /books`
- `PUT /books/{book_id}`
- `DELETE /books/{book_id}`
- `POST /books/{book_id}/switch-mode`

Study Context:

- List/create/get/update/delete context.
- Add/delete document vao context.
- List/create threads trong context.

Thread:

- Get-or-create direct thread cho book.
- Get messages cua thread.
- Update thread title.

Upload:

- Upload PDF/EPUB/DOCX.
- Extract outline/TOC/Heading.
- Create DRAFT Book + Chapters.

### Chua chuan

1. Book APIs chua filter theo `user_id` that; hien tai neu co filter thi nen filter bang `MOCK_USER_ID` truoc.
2. `POST /books` dang nhan DB model `Book` truc tiep.
3. `BookInput` dung chung create/update nen update bat buoc `title`.
4. `ChatThreadUpdate` cho phep `title=None` nhung service dang co nguy co bien thanh string `"None"`.
5. `GET /threads/{thread_id}/messages` chua validate thread thuoc user/context.
6. Router `study_context.py` con goi repository truc tiep.
7. Response DTO co mutable default list.
8. DB chua co unique constraints cho cac index nghiep vu quan trong.
9. `Book` chua co `document_type`, worker dang suy luan tu `file_url`.

---

## 2. Nguyen Tac Implement

### Layering

Dung flow:

```text
router -> service -> repository -> model/database
```

Router:

- Inject `Session`.
- Inject `current_user` khi can ownership.
- Goi service.
- Return response.

Service:

- Validate ownership.
- Dieu phoi nhieu repository.
- Raise `AppException`.

Repository:

- Query/mutate DB.
- Khong biet FastAPI.
- Khong goi LLM/TTS/Supabase Storage tru khi repo hien tai dang la legacy va se refactor sau.

### User ownership

Moi API doc/sua/xoa resource cua user phai check:

```python
resource.user_id == current_user.sub
```

Voi nested resource:

```text
thread -> context -> user_id
chapter -> book -> user_id
segment -> chapter -> book -> user_id
```

### DTO

Khong nhan DB model lam request body.

Can tach:

- Create request.
- Update request.
- Response DTO.

---

## 3. Phase 1 - Chuan Hoa Book DTO va User Scope Bang MOCK_USER_ID

Phase nay **chua bat auth user_id that**. Muc tieu la refactor code de tat ca service/repository da san sang nhan `user_id`, nhung router van truyen `MOCK_USER_ID`.

Sau nay khi auth on dinh, chi can doi:

```python
user_id = MOCK_USER_ID
```

thanh:

```python
user_id = current_user.sub
```

### 3.1 Tao DTO Book

File: `app/schemas/audiobook.py`

De xuat:

```python
from pydantic import BaseModel, Field


class BookCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    author: str | None = Field(default=None, max_length=255)


class BookUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    author: str | None = Field(default=None, max_length=255)
```

Neu can giu compatibility voi ten cu:

```python
BookInput = BookUpdateRequest
```

Nhung tot nhat la doi route sang ten moi.

### 3.2 Sua repository Book

File: `app/repositories/audiobook_repo.py`

Them:

```python
def get_books_by_user(session: Session, user_id: uuid.UUID) -> list[Book]:
    return list(session.exec(select(Book).where(Book.user_id == user_id)).all())


def get_book_by_id_and_user(session: Session, book_id: uuid.UUID, user_id: uuid.UUID) -> Book | None:
    return session.exec(
        select(Book).where(Book.id == book_id, Book.user_id == user_id)
    ).first()
```

Update:

```python
def update_book_by_id(
    session: Session,
    book_id: uuid.UUID,
    user_id: uuid.UUID,
    payload: BookUpdateRequest,
) -> Book:
    book = get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)

    session.add(book)
    session.commit()
    session.refresh(book)
    return book
```

### 3.3 Sua service Book

File: `app/services/audiobook_service.py`

Them service user-scoped:

```python
def list_books_by_user(session: Session, user_id: uuid.UUID) -> list[Book]:
    return audiobook_repo.get_books_by_user(session, user_id)


def get_owned_book(session: Session, user_id: uuid.UUID, book_id: uuid.UUID) -> Book:
    book = audiobook_repo.get_book_by_id_and_user(session, book_id, user_id)
    if not book:
        raise BookNotFoundError()
    return book
```

Sua cac service sau de nhan `user_id`:

- `get_book`
- `update_book_by_id`
- `delete_book_and_assets`
- `get_book_details`
- `switch_book_mode`

### 3.4 Sua router Book Trong Giai Doan MOCK_USER_ID

File: `app/api/v1/routers/audiobooks.py`

Tam thoi chua dung auth dependency trong route book. Dung:

```python
MOCK_USER_ID = uuid.UUID("862d7c26-3160-4f76-9e77-07d91f7317cc")
```

Pattern hien tai nen la:

```python
@router.get("/books", response_model=list[BookResponse])
def read_all_books(session: Annotated[Session, Depends(get_session)]):
    return list_books_by_user(session, MOCK_USER_ID)
```

Sau khi auth san sang, moi doi sang:

```python
from app.api.dependencies.auth import get_current_user
from app.schemas.user import UserTokenPayload
```

Pattern:

```python
@router.get("/books", response_model=list[BookResponse])
def read_all_books(
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[UserTokenPayload, Depends(get_current_user)],
):
    return list_books_by_user(session, current_user.sub)
```

Tat ca endpoint book nen duoc viet service theo dang co `user_id`, nhung router giai doan nay co the truyen `MOCK_USER_ID`.

### 3.5 Phase Sau - Bat Auth User ID That

Khi FE da gui Bearer token on dinh va BE da verify token dung:

1. Import:

```python
from app.api.dependencies.auth import get_current_user
from app.schemas.user import UserTokenPayload
```

2. Them dependency vao route:

```python
current_user: Annotated[UserTokenPayload, Depends(get_current_user)]
```

3. Thay:

```python
MOCK_USER_ID
```

bang:

```python
current_user.sub
```

4. Xoa TODO/comment mock user o router/service.

5. Update tests:

- Unit test service van truyen `user_id` truc tiep.
- API test can override `get_current_user` de khong phu thuoc Supabase real token.

Vi du override:

```python
app.dependency_overrides[get_current_user] = lambda: UserTokenPayload(
    sub=TEST_USER_ID,
    email="test@example.com",
    role="authenticated",
    aud="authenticated",
)
```

### 3.6 Trade-off

Uu diem:

- Multi-user safe.
- Khong lo user A doc/sua/xoa book user B.
- FE contract ro hon.

Trade-off:

- Giai doan mock chua phai security hoan chinh.
- Can discipline: moi service/repo phai nhan `user_id` ngay tu bay gio de sau nay doi sang auth khong phai refactor lon.
- Upload service hien dang `MOCK_USER_ID`; khi bat auth can dong bo upload endpoint nua.

---

## 4. Phase 2 - Chuan Hoa Study Context va Thread Ownership Bang MOCK_USER_ID

### 4.1 Router khong goi repository truc tiep

File: `app/api/v1/routers/study_context.py`

Hien co:

```python
return get_study_contexts(session, MOCK_USER_ID)
```

Nen chuyen:

```python
return study_context_service.list_contexts(session, user_id)
```

Giai doan nay:

```python
user_id = MOCK_USER_ID
```

Giai doan auth:

```python
user_id = current_user.sub
```

Service:

```python
def list_contexts(session: Session, user_id: uuid.UUID) -> list[StudyContext]:
    return get_study_contexts(session, user_id)
```

### 4.2 Thread messages phai validate ownership

File: `app/services/study_context_service.py`

Them:

```python
def get_thread_messages(session: Session, user_id: uuid.UUID, thread_id: uuid.UUID) -> list[ChatMessage]:
    thread = session.get(ChatThread, thread_id)
    if not thread:
        raise ThreadNotFoundError()

    context = _get_owned_context(session, thread.context_id, user_id)
    return get_chat_history_by_thread_id(session, thread.id)
```

Router:

```python
@router.get("/threads/{thread_id}/messages", response_model=list[ChatMessageResponse])
async def get_thread_messages_api(...):
    return study_context_service.get_thread_messages(session, MOCK_USER_ID, thread_id)
```

Sau khi bat auth, doi `MOCK_USER_ID` thanh `current_user.sub`.

### 4.3 Fix ChatThreadUpdate

Hien tai:

```python
title: str | None = None
```

Neu endpoint la `PUT`, nen title bat buoc:

```python
class ChatThreadUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
```

Neu muon partial update thi doi endpoint thanh `PATCH` va validate it nhat co field:

```python
if payload.title is None:
    raise BadRequestError("Thiếu title để cập nhật thread.")
```

Khong duoc dung:

```python
str(payload.title)
```

vi `None` thanh `"None"`.

### 4.4 Delete thread API

Repository da co:

```python
delete_thread(session, thread_id)
```

Nen them service:

```python
def delete_thread_by_id(session: Session, user_id: uuid.UUID, thread_id: uuid.UUID) -> None:
    thread = get_owned_thread(...)
    delete_thread(session, thread.id)
```

Router:

```python
@router.delete("/threads/{thread_id}")
```

### 4.5 Trade-off

Uu diem:

- Thread/message secure hon.
- Route consistent voi clean architecture.
- Chuan bi tot cho auth that.

Trade-off:

- Can them helper get_owned_thread.
- Test can update vi route can auth/current_user.

---

## 5. Phase 3 - Chuan Hoa Response DTO

### 5.1 Mutable default list

File: `app/schemas/responses/audiobook_res.py`

Hien co:

```python
chapter_segments: list[SegmentResponse] = []
chapters: list[ChapterDetailResponse] = []
```

Nen sua:

```python
from pydantic import Field

chapter_segments: list[SegmentResponse] = Field(default_factory=list)
chapters: list[ChapterDetailResponse] = Field(default_factory=list)
```

### 5.2 Mode type

Hien co:

```python
mode: str
```

Neu FE contract chap nhan enum, nen dung:

```python
from app.core.constant import PlanMode

mode: PlanMode
```

Neu FE dang expect string, giu `str` de tranh break.

### 5.3 BookResponse co nen expose `file_url`?

Hien co:

```python
file_url: Optional[str] = None
```

Can can nhac:

- Neu FE can link raw file thi giu.
- Neu raw book file la internal storage, khong nen expose.

Option production:

```python
document_type: str | None = None
```

va bo `file_url` khoi list response, chi expose o detail/admin neu can.

---

## 6. Phase 4 - DB Constraints va `document_type`

### 6.1 Them `document_type` vao Book

File: `app/models/db_models.py`

```python
document_type: str | None = Field(default=None, sa_column=Column(Text))
```

Tot hon nua la enum:

```python
class DocumentType(str, Enum):
    PDF = "pdf"
    EPUB = "epub"
    DOCX = "docx"
```

Nhung neu muon migration don gian, dung `Text` truoc.

### 6.2 Update upload service

File: `app/services/upload_service.py`

Khi create Book:

```python
book = Book(
    ...
    document_type=document_type,
)
```

### 6.3 Update worker

File: `app/services/workers/book_pipeline.py`

Hien dang infer type tu `file_url`. Sau khi co `document_type`:

```python
document_type = book.document_type or infer_document_type_from_url(book.file_url)
```

Giai doan transition nen giu fallback de book cu khong loi.

### 6.4 Unique constraints

File: `app/models/db_models.py`

Can import:

```python
from sqlalchemy import UniqueConstraint
```

Chapter:

```python
__table_args__ = (
    UniqueConstraint("book_id", "chapter_index", name="uq_chapters_book_id_chapter_index"),
)
```

ChapterSegment:

```python
__table_args__ = (
    UniqueConstraint("chapter_id", "mode", "segment_index", name="uq_segments_chapter_mode_segment_index"),
)
```

BookKnowledge:

```python
__table_args__ = (
    UniqueConstraint("chapter_id", "chunk_index", name="uq_book_knowledge_chapter_chunk_index"),
)
```

DirectBookContext da co:

```python
PrimaryKeyConstraint("user_id", "book_id", name="direct_book_context_pk")
```

giu nguyen.

### 6.5 Scan duplicate truoc migration

Truoc khi add unique constraints, chay SQL:

```sql
select book_id, chapter_index, count(*)
from chapters
group by book_id, chapter_index
having count(*) > 1;
```

```sql
select chapter_id, mode, segment_index, count(*)
from chapter_segments
group by chapter_id, mode, segment_index
having count(*) > 1;
```

```sql
select chapter_id, chunk_index, count(*)
from book_knowledge
group by chapter_id, chunk_index
having count(*) > 1;
```

Neu co duplicate, phai cleanup truoc.

### 6.6 Alembic migration

Tao migration:

```powershell
uv run alembic revision --autogenerate -m "add document type and unique constraints"
```

Review migration:

- Khong duoc drop bang/cot ngoai y muon.
- Them column `document_type`.
- Them unique constraints.

Backfill:

```sql
update books
set document_type = case
    when lower(file_url) like '%.pdf%' then 'pdf'
    when lower(file_url) like '%.epub%' then 'epub'
    when lower(file_url) like '%.docx%' then 'docx'
    else null
end
where document_type is null;
```

Neu `document_type` nullable truoc thi an toan hon. Sau khi data sach, migration sau co the set `nullable=False`.

### 6.7 Trade-off

Uu diem:

- DB chan duplicate data.
- Worker retry an toan hon.
- RAG/TTS khong bi duplicate segment/chunk.
- `document_type` ro nghia hon infer tu URL.

Trade-off:

- Migration co the fail neu data hien tai ban.
- Worker retry can chien luoc delete/upsert/skip.
- Them constraint co the lock table trong luc migrate.
- Them `document_type` can backfill data cu.

---

## 7. Phase 5 - Worker Retry Strategy Sau Khi Co Unique Constraints

Khi DB co unique constraint, worker can xu ly retry ro rang.

### Option A - Delete then insert

Truoc khi regenerate chapter/mode:

```python
delete_segments_by_chapter_and_mode(session, chapter_id, mode)
```

Sau do insert moi.

Uu diem:

- Don gian.
- Data moi sach.

Trade-off:

- Neu worker fail giua chung, co the mat segments cu.

### Option B - Upsert

Dung Postgres upsert theo unique constraint.

Uu diem:

- Retry-safe.
- It duplicate.

Trade-off:

- Code phuc tap hon voi SQLModel/SQLAlchemy.

### Khuyen nghi hien tai

Voi do an capstone, chon **Option A** cho mode regeneration, nhung update status ro:

```text
PROCESSING -> delete old mode assets/rows -> insert new -> READY
ERROR neu fail
```

Sau nay production co the nang len upsert.

---

## 8. Phase 6 - Test Plan

### Unit tests

Book service:

- list books by user chi tra sach cua user.
- get book cua user khac -> `BookNotFoundError`.
- update book partial title/author.
- update empty payload -> tuy rule, 400 hoac no-op.

Thread service:

- get messages cua thread thuoc user -> pass.
- get messages cua thread user khac -> `ThreadNotFoundError` hoac `StudyContextNotFoundError`.
- update thread title None -> 400.

DTO:

- `BookCreateRequest` reject empty title.
- `BookUpdateRequest` allow partial.
- `ChatThreadUpdate` reject None/empty neu PUT.

DB constraints:

- Insert duplicate chapter index cung book -> IntegrityError.
- Insert duplicate segment index cung chapter/mode -> IntegrityError.
- Insert duplicate knowledge chunk cung chapter -> IntegrityError.

### Integration/manual tests

Upload:

- PDF no outline -> 422.
- PDF outline -> 200, `document_type=pdf`.
- DOCX heading -> 200, `document_type=docx`.
- EPUB TOC -> 200, `document_type=epub`.

Book API:

- User A list khong thay book user B.
- User A get book user B -> 404.
- User A delete book user B -> 404.

Thread API:

- User A get thread messages user B -> 404.

### Commands

```powershell
uv run ruff check app tests
uv run pytest tests/test_document_parsers.py tests/test_api_study_context.py -q
uv run python -m py_compile app/api/v1/routers/audiobooks.py app/services/audiobook_service.py app/repositories/audiobook_repo.py
```

Chay integration tests can server rieng neu test goi `127.0.0.1:8000`.

---

## 9. Thu Tu Implement De It Rui Ro

1. Fix DTO response mutable defaults.
2. Tach `BookCreateRequest` / `BookUpdateRequest`.
3. Chuyen Book service/repository sang user-scoped, router van truyen `MOCK_USER_ID`.
4. Chuan hoa Study Context router khong goi repo truc tiep, van dung `MOCK_USER_ID`.
5. Them service ownership cho thread messages/update/delete.
6. Fix `ChatThreadUpdate` validation.
7. Them `document_type` nullable vao Book + update upload/worker fallback.
8. Scan duplicate DB.
9. Them unique constraints bang Alembic.
10. Them tests.
11. Chay manual upload/book/thread auth tests.

Ly do thu tu nay:

- Buoc 1-6 la code-level, it rui ro DB.
- Buoc 7 co migration nhe, co fallback.
- Buoc 8-9 moi la DB constraint, can scan data truoc.
- Auth user_id that nen la phase rieng sau khi FE/BE token flow on dinh.

---

## 10. Checklist Done

- [ ] `GET /books` filter theo user.
- [ ] `GET /books/{book_id}` check ownership.
- [ ] `PUT /books/{book_id}` check ownership va partial update dung.
- [ ] `DELETE /books/{book_id}` check ownership.
- [ ] `POST /books` khong nhan DB model truc tiep.
- [ ] Study Context router khong goi repo truc tiep.
- [ ] Thread messages check ownership.
- [ ] Thread update khong bien `None` thanh `"None"`.
- [ ] DTO list dung `Field(default_factory=list)`.
- [ ] `Book.document_type` co trong model/migration/upload/worker.
- [ ] Unique constraints da add va migration pass.
- [ ] Tests pass.
- [ ] FE contract update neu response doi.

### Auth User ID Sau Nay

- [ ] Book routers thay `MOCK_USER_ID` bang `current_user.sub`.
- [ ] Study Context routers thay `MOCK_USER_ID` bang `current_user.sub`.
- [ ] Upload endpoint gan `Book.user_id = current_user.sub`.
- [ ] Live token/thread endpoints validate user co quyen voi book/thread.
- [ ] API tests override `get_current_user`.

---

## 11. Ghi Chu Senior

Dung constraints trong DB khong phai de thay the code validation. No la lop phong thu cuoi cung.

Code service van phai validate ownership, status, input. DB constraint giup khi:

- Worker retry.
- Request concurrent.
- Bug code tao duplicate.
- Manual script insert sai.

Trong backend thuc te, code sach la tot, nhung DB phai biet tu bao ve minh. Day la khac biet lon giua project demo va project co the song lau.

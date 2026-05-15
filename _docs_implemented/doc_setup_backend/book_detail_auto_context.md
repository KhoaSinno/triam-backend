# Auto StudyContext per User per Book (Book-Detail → get-or-create Thread)

Mục tiêu: khi user mở **Book Detail** và bắt đầu chat, backend sẽ đảm bảo có một `StudyContext` tự động (flag `is_auto_generated = True`) và trả về một `ChatThread` duy nhất cho cặp (user, book). Điều này tránh phân mảnh lịch sử chat và là idempotent (get-or-create).

## Tóm tắt behavior

- Rule: mỗi cặp (user_id, book_id) có tối đa một StudyContext auto-generated và một ChatThread canonical do system quản lý.
- Flow khi FE gọi endpoint book-chat:
  1. Backend tìm `auto_context` cho (user_id, book_id).
  2. Nếu không có, backend tạo (StudyContext is_auto_generated=True) + liên kết `StudyContextDocumentLink(book_id)` + tạo `ChatThread` đầu tiên trong context đó, tất cả trong một transaction.
  3. Trả về `{ context_id, thread_id }` cho FE.

## API (idempotent) — đề xuất

- GET /threads/for-book/{book_id}?user_id={user_id}
  - Mục đích: trả về thread canonical cho user+book, tạo nếu chưa tồn tại.
  - Response (200):
    ```json
    { "context_id": "uuid", "thread_id": "uuid", "is_auto_generated": true }
    ```

- POST /books/{book_id}/threads (optional)
  - Body: { "user_id": "...", "title": "..." }
  - Tạo một thread explicit (không auto) dưới auto-context nếu muốn.

FE contract: luôn gọi `GET /threads/for-book/{book_id}` trước khi lấy LiveKit token. Dùng `thread_id` trả về để lấy token và connect.

## DB design notes (đề xuất)

- Giữ `StudyContext`, `StudyContextDocumentLink`, `ChatThread`, `ChatMessage` như hiện tại.
- Thêm bảng mapping nhỏ để đảm bảo unique canonical mapping và dễ enforce constraint:

```sql
CREATE TABLE auto_book_contexts (
  user_id UUID NOT NULL,
  book_id UUID NOT NULL,
  context_id UUID NOT NULL,
  PRIMARY KEY (user_id, book_id)
);
```

Giải thích: `auto_book_contexts` lưu context tự tạo cho từng (user, book). Khuyến nghị dùng khóa chính (user_id, book_id) để đảm bảo atomic uniqueness.

## Atomic get-or-create pseudo-code (SQLModel / FastAPI)

Pseudo (synchronous for clarity):

```py
from sqlmodel import Session
from sqlalchemy import select

def get_or_create_thread_for_book(db: Session, user_id: UUID, book_id: UUID, title: str):
    # 1) try to find mapping
    row = db.exec(select(AutoBookContext).where(AutoBookContext.user_id==user_id, AutoBookContext.book_id==book_id)).first()
    if row:
        ctx_id = row.context_id
        th = db.exec(select(ChatThread).where(ChatThread.context_id==ctx_id)).first()
        return ctx_id, th.id

    # 2) not found -> create inside tx
    with db.begin():
        ctx = StudyContext(user_id=user_id, title=f"Auto: {title}", is_auto_generated=True)
        db.add(ctx)
        db.flush()  # ctx.id available

        link = StudyContextDocumentLink(context_id=ctx.id, book_id=book_id)
        db.add(link)

        thread = ChatThread(context_id=ctx.id, title=f"Chat - {title}")
        db.add(thread)
        db.flush()

        mapping = AutoBookContext(user_id=user_id, book_id=book_id, context_id=ctx.id)
        db.add(mapping)

    return ctx.id, thread.id
```

Notes: use DB transaction and unique pk on `(user_id, book_id)` to avoid race conditions. If insertion fails due to conflict, select the existing row and return it.

## FastAPI route example (async)

```py
from fastapi import APIRouter, Depends
from sqlmodel import Session

router = APIRouter()

@router.get('/threads/for-book/{book_id}')
async def get_thread_for_book(book_id: UUID, user_id: UUID, db: Session = Depends(get_db)):
    try:
        ctx_id, thread_id = get_or_create_thread_for_book(db, user_id, book_id, title='Book Chat')
        return {'context_id': str(ctx_id), 'thread_id': str(thread_id), 'is_auto_generated': True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Migration notes

- Add `auto_book_contexts` table (or equivalent unique constraint) with PRIMARY KEY (user_id, book_id) to enforce uniqueness.
- Ensure `StudyContext.is_auto_generated` exists (it does), and mark created contexts accordingly.

## UX notes

- FE should cache `thread_id` per book to avoid repeated calls, but still call `GET /threads/for-book/{book_id}` as a canonical source when reconnecting.
- Allow manual merge tool in BE/UI if user wants to merge an auto-context thread into a user-created StudyContext.

## Summary

Thiết kế này đảm bảo: khi user chat từ Book Detail, lịch sử chat không bị phân mảnh; idempotent, an toàn race; và FE có contract đơn giản (`GET /threads/for-book/{book_id}` → dùng `thread_id`).

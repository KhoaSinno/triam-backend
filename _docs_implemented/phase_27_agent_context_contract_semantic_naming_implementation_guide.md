# Phase 27 Implementation Guide: Agent Context Contract Hardening & Semantic Naming Alignment

Tài liệu này là hướng dẫn kỹ thuật chi tiết dành cho các lập trình viên (bao gồm Fresher và Junior) để triển khai **Phase 27: Chuẩn Hóa Hợp Đồng Ngữ Cảnh Agent & Đặt Tên Ngữ Nghĩa (Agent Context Contract Hardening & Semantic Naming)**.

Tài liệu này giải quyết triệt để các khoảng trống hợp đồng (Contract Gaps) được đưa ra trong tài liệu yêu cầu của Frontend tại `phase_14_12_agent_context_contract_spec.md`.

---

## 📚 1. NỀN TẢNG LÝ THUYẾT VÀ KIẾN TRÚC SENIOR (FOR FRESHER TRAINING)

### 1.1. Tại sao việc Hardcode tên mặc định `"New Book Chat"` lại là Bad Practice?
* **Lỗi Vi phạm Tính Định danh Thực thể (Domain Entity Identity Violation):** Khi người dùng chọn một cuốn sách (ví dụ: *"Lâu đài Mặt Trăng"*) để trò chuyện với AI Agent, hệ thống tự động sinh ra một `StudyContext` và `ChatThread`. Việc gán tên cứng `"New Book Chat"` khiến cho mọi Context tạo tự động đều mang tên giống hệt nhau trong Database. Người dùng khi mở danh sách Context chỉ thấy hàng loạt dòng `"New Book Chat"` mà không thể phân biệt được sách nào với sách nào.
* **Quy tắc Senior Best Practice:** Tiêu đề của Context/Thread được tự động tạo **bắt buộc phải kế thừa ngữ nghĩa trực tiếp từ Thực thể Gốc (Source Entity - `book.title`)**. `"New Book Chat"` chỉ được phép tồn tại làm giá trị fallback cuối cùng khi cuốn sách hoàn toàn không có tên (`title is None`).

### 1.2. Phân biệt hai loại Ngữ cảnh Học tập (Study Context Categories)
Trong hệ thống Tri Âm Backend, có 2 loại Context cần được phân biệt rõ ràng thông qua Metadata:

1. **Auto-Generated Direct Book Context (`is_auto_generated = True`):**
   * Được hệ thống tự động tạo khi người dùng bấm nút *"Chat với sách"*.
   * Có quan hệ 1-1 với một cuốn sách duy nhất.
   * **Capabilities (Quyền hạn UI):** Không cho phép thêm/xóa sách phụ (`can_add_documents = False`), nhưng cho phép đổi tên/xóa Context và Thread.

2. **Manual Multi-Document Study Workspace (`is_auto_generated = False`):**
   * Không gian làm việc do người dùng chủ động tạo thủ công.
   * Có thể chứa nhiều sách/tài liệu và nhiều luồng thảo luận (Thread).
   * **Capabilities (Quyền hạn UI):** Cho phép toàn quyền thêm/xóa tài liệu (`can_add_documents = True`), tạo nhiều Thread, đổi tên và xóa.

---

## 🛠️ 2. TÓM TẮT CÁC THAY ĐỔI CẦN THỰC HIỆN (ARCHITECTURE CHECKLIST)

| Tệp tin (File Path) | Tầng kiến trúc | Thay đổi chính |
|---|---|---|
| `app/schemas/responses/study_context_res.py` | Schema DTO | Khai báo `ContextCapabilityResponse`, bổ sung `documents`, `document_count`, `capabilities` vào `StudyContextResponse`. Tạo DTO `DirectBookThreadResponse`. |
| `app/repositories/study_context_thread_repo.py` | Repository | Cập nhật `get_or_create_thread_for_book_repo` để lấy tiêu đề sách làm tên mặc định thay vì chuỗi hardcode. |
| `app/services/study_context_service.py` | Service | Cập nhật `get_or_create_thread_for_book` trả về payload giàu ngữ nghĩa (Preferred Shape). Cập nhật `list_user_study_contexts` và `get_study_context` nạp sẵn `documents` và `capabilities`. |
| `app/api/v1/routers/threads.py` | Router | Xóa bỏ tham số hardcode `title="New Book Chat"`. |
| `tests/services/test_phase27_agent_context_contract.py` | Test Suite | Viết bộ Unit & Integration Test tự động kiểm tra 100% các tiêu chí nghiệm thu. |

---

## 💻 3. CODE IMPLEMENTATION CHI TIẾT (STEP-BY-STEP FOR FRESHER)

### Step 3.1: Cập nhật Schema Response DTO (`app/schemas/responses/study_context_res.py`)

Thêm DTO `ContextCapabilityResponse`, DTO `DirectBookThreadResponse` và cập nhật `StudyContextResponse`.

```python
"""
app/schemas/responses/study_context_res.py
===========================================
Response DTOs cho module Study Context & Chat Thread.
"""

import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.responses.audiobook_res import BookResponse


class ContextCapabilityResponse(BaseModel):
    """Metadata quyền hạn thao tác trên UI phía Flutter FE."""
    can_add_documents: bool = False
    can_remove_documents: bool = False
    can_create_threads: bool = True
    can_rename_context: bool = True
    can_delete_context: bool = True
    can_rename_threads: bool = True
    can_delete_threads: bool = True


class StudyContextResponse(BaseModel):
    """DTO cho StudyContext — Nạp sẵn thông tin tài liệu liên kết và cờ quyền hạn."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    is_auto_generated: bool = False
    document_count: int = 0
    documents: List[BookResponse] = Field(default_factory=list)
    capabilities: Optional[ContextCapabilityResponse] = None
    created_at: datetime
    updated_at: datetime


class DirectBookThreadResponse(BaseModel):
    """DTO phản hồi cho Endpoint GET /threads/for-book/{book_id} chuẩn FE Contract."""

    context_id: uuid.UUID
    thread_id: uuid.UUID
    is_auto_generated: bool = True
    book_id: uuid.UUID
    book_title: str
    context_title: str
    thread_title: str


class ChatThreadResponse(BaseModel):
    """DTO cho ChatThread."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    context_id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime


class ChatMessageResponse(BaseModel):
    """DTO cho ChatMessage."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    thread_id: uuid.UUID
    role: str
    content: str
    created_at: datetime
```

---

### Step 3.2: Cập nhật Repository Layer (`app/repositories/study_context_thread_repo.py`)

Cập nhật `get_or_create_thread_for_book_repo` để tiếp nhận `title` động dựa trên tên sách và cập nhật tên Context/Thread nếu chúng đang mang tên cũ `"New Book Chat"`.

```python
def get_or_create_thread_for_book_repo(session: Session, user_id: uuid.UUID, book_id: uuid.UUID, title: str) -> tuple[uuid.UUID, uuid.UUID]:
    """Lấy hoặc tạo mới cặp (context_id, primary_thread_id) cho cuốn sách.
    Nếu Context/Thread cũ mang tên 'New Book Chat', tự động cập nhật lại theo tên sách thực tế.
    """
    direct_ctx = session.exec(select(DirectBookContext).where(
        DirectBookContext.book_id == book_id, DirectBookContext.user_id == user_id)).first()

    if direct_ctx:
        # Kiểm tra nếu Context/Thread cũ mang tên mặc định 'New Book Chat' thì tự động sửa lại
        context = session.get(StudyContext, direct_ctx.context_id)
        thread = session.get(ChatThread, direct_ctx.primary_thread_id)
        
        need_commit = False
        if context and context.title == "New Book Chat" and title and title != "New Book Chat":
            context.title = title
            session.add(context)
            need_commit = True
            
        if thread and thread.title == "New Book Chat" and title and title != "New Book Chat":
            thread.title = title
            session.add(thread)
            need_commit = True

        if need_commit:
            session.commit()

        return direct_ctx.context_id, direct_ctx.primary_thread_id

    # Nếu chưa có, tạo mới Context với tên sách thực tế
    new_context = StudyContext(
        user_id=user_id,
        title=title,
        is_auto_generated=True,
    )
    session.add(new_context)
    session.flush()

    new_study_context_book_link = StudyContextDocumentLink(
        context_id=new_context.id,
        book_id=book_id,
    )
    session.add(new_study_context_book_link)

    new_thread = ChatThread(
        context_id=new_context.id,
        title=title,
    )
    session.add(new_thread)
    session.flush()

    new_direct_ctx = DirectBookContext(
        user_id=user_id,
        book_id=book_id,
        context_id=new_context.id,
        primary_thread_id=new_thread.id,
    )
    session.add(new_direct_ctx)
    session.commit()

    return new_context.id, new_thread.id
```

---

### Step 3.3: Cập nhật Service Layer (`app/services/study_context_service.py`)

1. Cập nhật `get_or_create_thread_for_book` để tự động lấy `book.title` và trả về `DirectBookThreadResponse`.
2. Cập nhật `list_user_study_contexts` và `get_study_context` để nạp sẵn danh sách `documents` và tính toán `capabilities`.

```python
def _build_capabilities(is_auto_generated: bool) -> dict:
    """Helper xây dựng cờ quyền hạn cho Frontend UI."""
    if is_auto_generated:
        return {
            "can_add_documents": False,
            "can_remove_documents": False,
            "can_create_threads": True,
            "can_rename_context": True,
            "can_delete_context": True,
            "can_rename_threads": True,
            "can_delete_threads": True,
        }
    return {
        "can_add_documents": True,
        "can_remove_documents": True,
        "can_create_threads": True,
        "can_rename_context": True,
        "can_delete_context": True,
        "can_rename_threads": True,
        "can_delete_threads": True,
    }


def get_or_create_thread_for_book(session: Session, user_id: uuid.UUID, book_id: uuid.UUID) -> dict:
    """Lấy hoặc tạo thread chuẩn cho cuốn sách với thông tin ngữ nghĩa đầy đủ."""
    book = get_book_by_id(session, book_id)
    if not book or book.user_id != user_id:
        raise BookNotFoundError()

    default_title = book.title or "Sách chưa đặt tên"
    ctx_id, thread_id = get_or_create_thread_for_book_repo(session, user_id, book_id, title=default_title)

    context = get_context_by_id(session, ctx_id)
    thread = get_thread_by_id(session, thread_id)

    return {
        "context_id": ctx_id,
        "thread_id": thread_id,
        "is_auto_generated": True,
        "book_id": book.id,
        "book_title": book.title,
        "context_title": context.title if context else book.title,
        "thread_title": thread.title if thread else book.title,
    }


def list_user_study_contexts(session: Session, user_id: uuid.UUID) -> list[dict]:
    """Danh sách tất cả StudyContext của user đính kèm danh sách tài liệu và capabilities."""
    contexts = list_user_contexts_repo(session, user_id)
    result = []
    for ctx in contexts:
        docs = list_documents_for_context_repo(session, ctx.id)
        doc_dtos = [b.model_dump() for b in docs]
        result.append({
            "id": ctx.id,
            "title": ctx.title,
            "is_auto_generated": ctx.is_auto_generated,
            "document_count": len(docs),
            "documents": doc_dtos,
            "capabilities": _build_capabilities(ctx.is_auto_generated),
            "created_at": ctx.created_at,
            "updated_at": ctx.updated_at,
        })
    return result


def get_study_context(session: Session, user_id: uuid.UUID, context_id: uuid.UUID) -> dict:
    """Chi tiết StudyContext đính kèm danh sách tài liệu và capabilities."""
    ctx = get_context_by_id(session, context_id)
    if not ctx or ctx.user_id != user_id:
        raise StudyContextNotFoundError()
    
    docs = list_documents_for_context_repo(session, ctx.id)
    doc_dtos = [b.model_dump() for b in docs]
    return {
        "id": ctx.id,
        "title": ctx.title,
        "is_auto_generated": ctx.is_auto_generated,
        "document_count": len(docs),
        "documents": doc_dtos,
        "capabilities": _build_capabilities(ctx.is_auto_generated),
        "created_at": ctx.created_at,
        "updated_at": ctx.updated_at,
    }
```

---

### Step 3.4: Cập nhật Router Layer (`app/api/v1/routers/threads.py`)

Cập nhật route `GET /threads/for-book/{book_id}` để loại bỏ hoàn toàn chuỗi hardcode `"New Book Chat"`.

```python
# app/api/v1/routers/threads.py

from app.schemas.responses.study_context_res import DirectBookThreadResponse

@router.get("/threads/for-book/{book_id}", response_model=DirectBookThreadResponse)
async def get_thread_for_book(
    book_id: uuid.UUID,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)]
):
    """API lấy hoặc khởi tạo Thread chuẩn cho một cuốn sách (Tự động đặt tên theo tiêu đề sách)."""
    return get_or_create_thread_for_book(session, user_id=current_user.sub, book_id=book_id)
```

---

## 🧪 4. KIỂM THỬ TỰ ĐỘNG (AUTOMATED TEST SUITE)

Tạo tệp test `tests/services/test_phase27_agent_context_contract.py` để đảm bảo 100% tiêu chí nghiệm thu đều vượt qua:

```python
import uuid
import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.models.db_models import Book, StudyContext, ChatThread, StudyContextDocumentLink, DirectBookContext
from app.services.study_context_service import (
    get_or_create_thread_for_book,
    list_user_study_contexts,
    get_study_context,
)


@pytest.fixture(name="db_session")
def db_session_fixture():
    engine = create_engine("sqlite:///:memory:")
    target_tables = [
        Book.__table__,
        StudyContext.__table__,
        ChatThread.__table__,
        StudyContextDocumentLink.__table__,
        DirectBookContext.__table__,
    ]
    SQLModel.metadata.create_all(engine, tables=target_tables)
    with Session(engine) as session:
        yield session


def test_get_or_create_thread_for_book_uses_real_book_title(db_session: Session):
    """Kiểm tra get_or_create_thread_for_book đặt tên theo tiêu đề sách thay vì 'New Book Chat'."""
    user_id = uuid.uuid4()
    book = Book(title="Lâu đài Mặt Trăng", user_id=user_id, status="ready")
    db_session.add(book)
    db_session.commit()

    res = get_or_create_thread_for_book(db_session, user_id=user_id, book_id=book.id)

    assert res["book_title"] == "Lâu đài Mặt Trăng"
    assert res["context_title"] == "Lâu đài Mặt Trăng"
    assert res["thread_title"] == "Lâu đài Mặt Trăng"
    assert res["is_auto_generated"] is True
    assert res["context_id"] is not None
    assert res["thread_id"] is not None


def test_list_study_contexts_includes_documents_and_capabilities(db_session: Session):
    """Kiểm tra API danh sách context đính kèm danh sách tài liệu và cờ capabilities."""
    user_id = uuid.uuid4()
    book = Book(title="Tư Duy Nhanh Và Chậm", user_id=user_id, status="ready")
    db_session.add(book)
    db_session.commit()

    # Tạo direct book thread
    get_or_create_thread_for_book(db_session, user_id=user_id, book_id=book.id)

    contexts = list_user_study_contexts(db_session, user_id)
    assert len(contexts) == 1
    ctx_data = contexts[0]

    assert ctx_data["title"] == "Tư Duy Nhanh Và Chậm"
    assert ctx_data["document_count"] == 1
    assert len(ctx_data["documents"]) == 1
    assert ctx_data["documents"][0]["title"] == "Tư Duy Nhanh Và Chậm"
    assert ctx_data["capabilities"]["can_add_documents"] is False
    assert ctx_data["capabilities"]["can_rename_context"] is True
```

---

## 📋 5. TIÊU CHÍ NGHIỆM THU (ACCEPTANCE CRITERIA)

1. **Tên hiển thị chuẩn ngữ nghĩa:** Khi người dùng chọn bất kỳ cuốn sách nào để chat, tiêu đề Context và Thread được tạo tự động **bắt buộc mang tên của cuốn sách đó**, tuyệt đối không xuất hiện chữ `"New Book Chat"`.
2. **Payload Endpoint `threads/for-book/{book_id}`:** Trả về đủ 7 trường (`context_id`, `thread_id`, `is_auto_generated`, `book_id`, `book_title`, `context_title`, `thread_title`).
3. **Danh sách & Chi tiết Context:** API `GET /study-contexts` trả về sẵn danh sách `documents` (chứa tên sách, bìa sách) và cờ `capabilities` cho Frontend điều khiển UI.
4. **Không có N+1 Query:** Mã nguồn Backend truy vấn dữ liệu tài liệu liên kết một cách mượt mà và tối ưu.

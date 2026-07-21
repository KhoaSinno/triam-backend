import uuid
import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.models.db_models import Book, StudyContext, ChatThread, StudyContextDocumentLink, DirectBookContext
from app.schemas.study_context import StudyContextInput, StudyContextDocumentInput
from app.services.study_context_service import (
    create_context,
    add_document_to_context,
    get_or_create_thread_for_book,
    list_contexts,
    get_context,
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
    """Kiểm tra get_or_create_thread_for_book lấy tiêu đề sách thực tế thay vì 'New Book Chat'."""
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


def test_get_or_create_thread_for_book_self_heals_legacy_new_book_chat_title(db_session: Session):
    """Kiểm tra cơ chế self-healing tự động sửa các tên legacy 'New Book Chat' thành tên sách."""
    user_id = uuid.uuid4()
    book = Book(title="Tư Duy Nhanh Và Chậm", user_id=user_id, status="ready")
    db_session.add(book)
    db_session.commit()

    old_context = StudyContext(user_id=user_id, title="New Book Chat", is_auto_generated=True)
    db_session.add(old_context)
    db_session.flush()

    link = StudyContextDocumentLink(context_id=old_context.id, book_id=book.id)
    db_session.add(link)

    old_thread = ChatThread(context_id=old_context.id, title="New Book Chat")
    db_session.add(old_thread)
    db_session.flush()

    direct_ctx = DirectBookContext(
        user_id=user_id,
        book_id=book.id,
        context_id=old_context.id,
        primary_thread_id=old_thread.id
    )
    db_session.add(direct_ctx)
    db_session.commit()

    res = get_or_create_thread_for_book(db_session, user_id=user_id, book_id=book.id)

    assert res["context_title"] == "Tư Duy Nhanh Và Chậm"
    assert res["thread_title"] == "Tư Duy Nhanh Và Chậm"


def test_list_study_contexts_includes_documents_and_capabilities(db_session: Session):
    """Kiểm tra API danh sách context đính kèm danh sách tài liệu và cờ capabilities."""
    user_id = uuid.uuid4()
    book = Book(title="Đắc Nhân Tâm", user_id=user_id, status="ready")
    db_session.add(book)
    db_session.commit()

    payload = StudyContextInput(title="Góc Học Tập Đắc Nhân Tâm")
    created_ctx = create_context(db_session, user_id=user_id, payload=payload)

    doc_payload = StudyContextDocumentInput(book_id=book.id)
    add_document_to_context(db_session, user_id=user_id, context_id=created_ctx["id"], payload=doc_payload)

    contexts = list_contexts(db_session, user_id)
    assert len(contexts) == 1
    ctx_data = contexts[0]

    assert ctx_data["title"] == "Góc Học Tập Đắc Nhân Tâm"
    assert ctx_data["document_count"] == 1
    assert len(ctx_data["documents"]) == 1
    assert ctx_data["documents"][0]["title"] == "Đắc Nhân Tâm"
    assert ctx_data["capabilities"]["can_add_documents"] is True
    assert ctx_data["capabilities"]["can_rename_context"] is True

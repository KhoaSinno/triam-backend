import uuid

import pytest

from app.models.db_models import Book, Chapter
from app.services import upload_service


class FakeSession:
    def __init__(self):
        self.added = []
        self.commits = 0
        self.rollbacks = 0

    def add(self, obj):
        self.added.append(obj)

    def add_all(self, objs):
        self.added.extend(objs)

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1


class FakeUploadFile:
    filename = "LogiForce.docx"
    content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    async def read(self):
        return b"fake docx bytes"


@pytest.mark.asyncio
async def test_upload_document_batches_book_and_chapters_in_one_commit(monkeypatch):
    async def fake_extract_chapters_by_type(tmp_filename, document_type):
        assert document_type == "docx"
        return [
            {"title": "Lời mở đầu", "text": "A", "page_start": None},
            {"title": "Chương 1", "text": "B", "page_start": None},
            {"title": "Chương 2", "text": "C", "page_start": None},
        ]

    async def fake_upload_file_to_supabase(*args, **kwargs):
        return "https://storage.example/raw_books/book/original.docx"

    monkeypatch.setattr(upload_service, "_extract_chapters_by_type", fake_extract_chapters_by_type)
    monkeypatch.setattr(upload_service, "upload_file_to_supabase", fake_upload_file_to_supabase)

    session = FakeSession()
    response = await upload_service.handle_upload_document(session, FakeUploadFile(), uuid.uuid4())

    assert response["document_type"] == "docx"
    assert response["total_chapters"] == 3
    assert session.commits == 1
    assert sum(isinstance(item, Book) for item in session.added) == 1
    assert sum(isinstance(item, Chapter) for item in session.added) == 3

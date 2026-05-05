import uuid

from pydantic import BaseModel


class StudyContextInput(BaseModel):
    title: str

class StudyContextUpdate(BaseModel):
    title: str | None = None

class StudyContextDocumentInput(BaseModel):
    book_id: uuid.UUID

class ChatThreadInput(BaseModel):
    title: str

class ChatThreadUpdate(BaseModel):
    title: str | None = None

import uuid

from pydantic import BaseModel, Field


class StudyContextInput(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class StudyContextUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)


class StudyContextDocumentInput(BaseModel):
    book_id: uuid.UUID


class ChatThreadInput(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class ChatThreadUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=255)

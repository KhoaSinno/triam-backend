from pydantic import BaseModel, Field


class BookCreateRequest(BaseModel):
    """DTO cho input khi tạo mới sách thủ công."""

    title: str = Field(min_length=1, max_length=255)
    author: str | None = Field(default=None, max_length=255)


class BookUpdateRequest(BaseModel):
    """DTO cho input khi cập nhật metadata sách."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    author: str | None = Field(default=None, max_length=255)


# Backward-compatible alias while old imports are cleaned up.
BookInput = BookUpdateRequest

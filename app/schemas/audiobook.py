from pydantic import BaseModel, Field, field_validator


class _BookMetadataRequest(BaseModel):
    @field_validator("title", "author", mode="before", check_fields=False)
    @classmethod
    def remove_nul_characters(cls, value: object) -> object:
        if isinstance(value, str):
            return value.replace("\x00", "")
        return value


class BookCreateRequest(_BookMetadataRequest):
    """DTO cho input khi tạo mới sách thủ công."""

    title: str = Field(min_length=1, max_length=255)
    author: str | None = Field(default=None, max_length=255)


class BookUpdateRequest(_BookMetadataRequest):
    """DTO cho input khi cập nhật metadata sách."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    author: str | None = Field(default=None, max_length=255)

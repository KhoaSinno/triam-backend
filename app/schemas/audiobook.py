from typing import Optional

from pydantic import BaseModel


class BookInput(BaseModel):
    """DTO cho input khi tạo mới hoặc cập nhật sách."""

    title: str
    author: Optional[str] = None

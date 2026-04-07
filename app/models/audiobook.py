from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Audiobook(SQLModel, table=True):
    # __tablename__ = "audiobooks"  # Nếu tên bảng trên Supabase là 'audiobooks' (số nhiều)

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    # Nếu cột created_at đã có data, bạn map đúng kiểu dữ liệu là xong
    created_at: Optional[datetime] = None

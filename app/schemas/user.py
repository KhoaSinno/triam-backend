# app/schemas/user.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class UserTokenPayload(BaseModel):
    """
    Schema định nghĩa payload chứa trong JWT token của Supabase trả về
    """
    sub: UUID
    email: Optional[str] = None
    role: Optional[str] = None
    aud: Optional[str] = None
    exp: Optional[int] = None

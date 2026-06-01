from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserTokenPayload(BaseModel):
    """
    Schema định nghĩa payload chứa trong JWT token của Supabase trả về
    """
    sub: UUID
    email: Optional[str] = None
    role: Optional[str] = None
    aud: Optional[str] = None
    exp: Optional[int] = None

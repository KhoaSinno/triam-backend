from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID
from app.core.supabase import supabase
from app.schemas.user import UserTokenPayload

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserTokenPayload:
    """
    Dependency lấy và verify JWT token từ Header sử dụng Supabase Python SDK.
    Dùng Depends(get_current_user) trong mọi endpoint cần bảo mật.
    """
    token = credentials.credentials
    try:
        # Sử dụng SDK chính thức của Supabase để kiểm tra auth qua server
        # Phương pháp này hỗ trợ chuẩn Asymmetric Keys mới nhất (ES256/RS256) một cách mượt mà nhất.
        user_response = supabase.auth.get_user(token)

        if not user_response or not user_response.user:
            raise ValueError("Không thể lấy thông tin người dùng")

        user = user_response.user

        return UserTokenPayload(
            sub=UUID(str(user.id)),
            email=user.email,
            role=user.role,
            aud=user.aud,
        )

    except Exception as e:
        # Bắt mọi lỗi decode, hết hạn auth hoặc token rác
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token không hợp lệ hoặc đã hết hạn: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

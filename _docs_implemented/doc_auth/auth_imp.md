# 🚀 Hướng Dẫn Tích Hợp Supabase Auth Toàn Diện (Triam Backend)

Dựa trên nguyên tắc **Clean Architecture** và việc Frontend (Flutter) đã xử lý Login/Register trực tiếp với Supabase, Backend của chúng ta chỉ làm nhiệm vụ duy nhất: **Xác thực (Verify) JWT Token từ Header và trích xuất thông tin User**.

Lưu ý: Do Supabase đã chuyển sang hệ thống **Asymmetric Keys (ES256/RS256)** thay vì `HS256` tĩnh như cũ nên việc sử dụng JWKS qua PyJWT có thể bị lỗi gateway block hoặc không mượt. Do vậy chúng ta sẽ áp dụng Best Practice cuối cùng và chuẩn nhất từ docs: Dùng `supabase-py` package để xác thực bảo mật! 

---

## Bước 1: Cài đặt thư viện cần thiết

Dự án đã có Supabase Python SDK, bạn chỉ cần import vào là được. Bỏ qua việc cài pyjwt.

```bash
uv pip install supabase
```

---

## Bước 2: Thiết lập biến môi trường (app/core/config.py)

Với cơ chế mới, bạn **KHÔNG CẦN** rò rỉ bất kỳ Secret Key nào để chống lộ key.
File `.env` của bạn chỉ cần:

```env
SUPABASE_URL="https://<project-id>.supabase.co"
SUPABASE_SERVICE_ROLE_KEY="<service-role-key>"
```

---

## Bước 3: Schema cho User Payload (app/schemas/user.py)

Tạo file `user.py` trong thư mục `app/schemas/` để định nghĩa cấu trúc dữ liệu. Nhờ Pydantic, bạn sẽ có auto-complete.

```python
# app/schemas/user.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class UserTokenPayload(BaseModel):
    sub: UUID                # Đây là User ID của Supabase
    email: Optional[str] = None
    role: Optional[str] = None
    aud: Optional[str] = None
```

---

## Bước 4: Tạo Dependency Xác Thực (app/api/dependencies/auth.py)

Đây là "trái tim" của hệ thống. Chúng ta dùng trực tiếp hàm tĩnh `.auth.get_user(token)` của client supabase.

```python
# app/api/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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
        # Sử dụng SDK chính thức của Supabase để kiểm tra auth.
        # Phương pháp này hỗ trợ chuẩn Asymmetric Keys mới nhất (ES256/RS256).
        user_response = supabase.auth.get_user(token)
        
        if not user_response or not user_response.user:
            raise ValueError("Không thể lấy thông tin người dùng")
            
        user = user_response.user
        
        # Parse data thành Pydantic mode để dễ dàng trả về
        return UserTokenPayload(
            sub=user.id,
            email=user.email,
            role=user.role,
            aud=user.aud,
        )

    except Exception as e:
        # Bắt lỗi decode, hết hạn auth hoặc token rác
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token không hợp lệ hoặc đã hết hạn: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

---

## Bước 5: Áp dụng vào Router (Dùng trong các API)

Cơ chế này hoàn toàn khớp với Clean Architecture. Chỉ cần tiêm Dependency `get_current_user` vào router.

```python
# app/api/v1/endpoints/study_context.py
from fastapi import APIRouter, Depends
from app.api.dependencies.auth import get_current_user   
from app.schemas.user import UserTokenPayload 

router = APIRouter()

@router.get("/study-contexts")
async def get_my_study_contexts(
    current_user: UserTokenPayload = Depends(get_current_user) 
):
    # Trích xuất UUID xịn từ token
    user_id = current_user.sub
    
    return {"user_id": str(user_id), "status": "secure"}
```

---

### Ưu điểm vượt trội của kiến trúc mới này:

1. **Chuẩn tài liệu Supabase nhất:** Sử dụng native `get_user` giải quyết 100% thay đổi Asymmetric Key của Supabase vì gói SDK đã bao bọc logic này.
2. **Khóa 100% Session bị thu hồi:** Khác với JWKS decode local cũ (nếu token còn hạn nhưng tài khoản đã bị khóa, JWT nội bộ vẫn pass), bằng việc gọi `get_user`, Supabase kiểm tra nếu tài khoản vừa bị khóa/đăng xuất thì token lập tức vứt bỏ. Dùng kiểu này an toàn tối đa cho bảo mật doanh nghiệp.

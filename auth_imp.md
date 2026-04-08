## 1. Phía Flutter (Frontend - Giao tiếp trực tiếp với Supabase)

Flutter sẽ dùng SDK của Supabase để "tự lo" toàn bộ UI và kết nối:

- **Xử lý Auth:** Đăng ký (Sign up), Đăng nhập (Login bằng Email/Password, Google, Apple v.v...).
- **Nhận Token:** Supabase Server sẽ trả về cho Flutter một **Access Token** (thực chất là một chuỗi JWT - JSON Web Token).
- **Gửi Request:** Bất cứ khi nào Flutter muốn gọi API xuống backend FastAPI của bạn (ví dụ: upload PDF, chat với AI), Flutter sẽ nhét cái JWT này vào Header HTTP (cụ thể là `Authorization: Bearer <JWT_Token>`).

---

## 2. Phía Backend FastAPI (Xác thực lại và cấp phép)

Dù Supabase đã cấp token, Backend của bạn **KHÔNG ĐƯỢC** tin tưởng mù quáng bất cứ ai gọi API tới. Trách nhiệm của Backend là:

### **Verify Token (Giải mã và kiểm tra)**

Khi nhận được request của Flutter, BE sẽ bóc cái Header lấy ra chuỗi JWT. Lúc này dùng một thư viện Python (như `PyJWT`) kết hợp với **khóa bí mật (JWT Secret)** mà Supabase cung cấp cho Project của bạn để kiểm tra xem Token này:

- Có phải là giả mạo không? (Chữ ký chuẩn không).
- Có bị hết hạn không?

### **Trích xuất thông tin người dùng (user_id)**

Vì thông tin Token không bị mã hoá hoàn toàn, bên trong cái Token hợp lệ đó sẽ chứa ID của người dùng (nằm ở trường `sub` - subject). BE dễ dàng lấy được cái `user_id` này ra.

### **Cấp phép và xử lý (Authorization)**

- `User_id` lấy được từ Token sẽ được truyền vào các hàm logic, gán thẳng vào các object như: `book_id = ...`, `user_id = <ID_từ_Token>`.
- Đảm bảo ông User A gọi API tìm kiếm RAG thì Backend chỉ query nội dung học trong bảng `book_knowledge` mà sách của User A sở hữu.

---

## Tóm lại: Backend cần code những gì ở giai đoạn Tương lai?

Về sau, bạn không cần code API tạo tài khoản hay đổi mật khẩu. Bạn chỉ cần code khoảng 1-2 file duy nhất (thường đặt tên là `app/api/deps.py` hoặc `auth.py`):

1.  **Viết 1 hàm Dependency:** Xử lý bắt Header -> Giải mã JWT -> Lấy `user_id` -> Nếu Token hết hạn hoặc sai thì trả về lỗi `401 Unauthorized`.
2.  **Gắn Dependency:** Gắn cái Dependency đó vào các endpoint API.
    - _Ví dụ:_ `@router.post("/upload", dependencies=[Depends(get_current_user)])`.

> **Kết luận:** Nhờ mô hình này, Backend của bạn hoàn toàn **Stateless** (không cần lưu session đăng nhập), rất nhẹ nhàng và cực kỳ dễ scale (mở rộng)! Hiện tại, bạn hoàn toàn có thể yên tâm dùng cách **Mock User** như tôi đề xuất ở trên để tiếp tục làm các logic khác trước đã.

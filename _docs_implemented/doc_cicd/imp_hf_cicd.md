Chào bạn, dựa trên tài liệu từ repo bạn gửi và cấu trúc dự án `triam-backend` hiện tại của bạn, đây là hướng dẫn chi tiết từng bước (step-by-step) để bạn thiết lập tự động đồng bộ từ GitHub sang Hugging Face Spaces bằng GitHub Actions.

### Bước 1: Lấy Token "Write" từ Hugging Face

Bạn cần một "chìa khóa" để GitHub có quyền ghi dữ liệu vào Space của bạn.

1.  Truy cập vào trang [Hugging Face Settings - Tokens](https://huggingface.co/settings/tokens).
2.  Nhấn nút **New token**.
3.  **Token name:** Đặt tên dễ nhớ (ví dụ: `GitHub_Sync_TriAm`).
4.  **Token type:** Bạn **bắt buộc** phải chọn **Write**.
5.  Nhấn **Generate a token**.
6.  **Copy** đoạn mã token vừa tạo (hãy lưu tạm vào đâu đó vì nó sẽ bị ẩn đi sau này).

### Bước 2: Thêm Token vào Secret của GitHub Repository

Bây giờ, bạn cần đưa "chìa khóa" này vào GitHub một cách bảo mật.

1.  Mở trình duyệt, vào repository `triam-backend-main` của bạn trên **GitHub**.
2.  Chọn tab **Settings** (biểu tượng bánh răng trên cùng).
3.  Ở menu bên trái, tìm mục **Secrets and variables** -> chọn **Actions**.
4.  Nhấn nút màu xanh **New repository secret**.
5.  **Name:** Nhập chính xác là `HF_TOKEN`.
6.  **Secret:** Dán đoạn mã token bạn đã copy ở Bước 1 vào.
7.  Nhấn **Add secret**.

### Bước 3: Tạo file cấu hình GitHub Actions (Workflow)

Bạn cần tạo một file để ra lệnh cho GitHub tự động đẩy code sang Hugging Face mỗi khi bạn `push`.

1.  Trên máy tính của bạn, tại thư mục gốc của dự án, hãy tạo thư mục (nếu chưa có): `.github/workflows/`.
2.  Trong thư mục đó, tạo một file mới tên là `sync_to_hf.yml`.
3.  Dán toàn bộ nội dung sau vào file đó:

```yaml
name: Sync to Hugging Face Hub
on:
  push:
    branches: [main] # Hoặc tên nhánh chính của bạn (ví dụ: master)
  workflow_dispatch: # Cho phép bạn bấm nút chạy tay trên GitHub nếu cần

jobs:
  sync-to-hub:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          lfs: true # Hỗ trợ nếu bạn có file lớn (PDF/Audio) dùng Git LFS

      - name: Push to HF
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          # Cấu hình thông tin git tạm thời để push
          git remote add hf https://khoasinoo:$HF_TOKEN@huggingface.co/spaces/khoasinoo/tri-am-backend
          # Push toàn bộ code lên nhánh main của Hugging Face
          git push --force hf main
```

### Bước 4: Đảm bảo Dockerfile và uv.lock đã sẵn sàng

Vì bạn đang dùng `uv`, hãy chắc chắn rằng trong repo GitHub của bạn **đã có** các file sau ở thư mục gốc:

- `Dockerfile` (Sử dụng bản tôi đã viết cho bạn để cài `uv` và chạy port `7860`).
- `pyproject.toml` và `uv.lock` (Để server cài đúng thư viện).
- Thư mục `app/` chứa code chính.

### Bước 5: Push và Kiểm tra

Bây giờ là lúc tận hưởng thành quả:

1.  Mở terminal tại thư mục dự án trên máy bạn và chạy:
    ```bash
    git add .
    git commit -m "Add GitHub Actions sync to HF"
    git push origin main
    ```
2.  **Trên GitHub:** Vào tab **Actions**. Bạn sẽ thấy một workflow đang chạy. Nếu nó hiện dấu tích xanh là code đã được đẩy sang Hugging Face thành công.
3.  **Trên Hugging Face:** Vào tab **App**. Bạn sẽ thấy nó tự động chuyển sang trạng thái **Building**.

---

### 💡 Lưu ý quan trọng cho dự án TRIAM của bạn:

- **Biến môi trường:** Sau khi sync thành công, Hugging Face sẽ build lại. Hãy chắc chắn bạn đã vào **Settings -> Variables and secrets** trên Hugging Face để nhập các Key từ file `.env` (như `GEMINI_API_KEY`, `SUPABASE_URL`...).
- **Link API:** Sau khi build xong, app Flutter của bạn hãy gọi đến link: `https://khoasinoo-tri-am-backend.hf.space/` (nhớ đã sửa lỗi CORS trong `main.py` như tôi đã nhắc nhé).

Giờ bạn hãy thử thực hiện Bước 1 và 2 trước đi, nếu gặp khó khăn ở chỗ nào hãy báo tôi ngay!

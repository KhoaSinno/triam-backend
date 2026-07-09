├── 1. Slide Mở đầu & Đặt vấn đề (~3 Slide)
│   ├── Slide 1: Trang bìa (Tên đề tài, GVHD TS. Nguyễn Trung Việt, Sinh viên thực hiện)
│   ├── Slide 2: Tính cấp thiết (Nghịch lý sách nói cũ: nghe thụ động, không tương tác)
│   └── Slide 3: Mục tiêu hệ thống (Tạo quy trình từ sách chữ sang sách nói theo chế độ, Cơ chế ôn tập giúp user hệ thống ghi nhớ kiến thức hiệu quả, Tương tác voice to voice nhanh chóng hiệu quả)
│
├── 2. Phân tích & Kiến trúc hệ thống (~3 Slide)
│   ├── Slide 4: Sơ đồ kiến trúc tổng quan 5 khối (Tách biệt luồng REST và luồng Realtime LiveKit)
│   ├── Slide 5: Sơ đồ lớp (Class Diagram) và Mô hình dữ liệu cốt lõi (BookSection, LearningUnit)
│   └── Slide 6: Giải pháp bảo mật Database nâng cao (Row Level Security - RLS trên PostgreSQL)
│
├── 3. Các phân hệ giải pháp cốt lõi (~7 Slide) -> *Ăn điểm thuật toán*
│   ├── Slide 7: Phân hệ Ingestion Pipeline (Quy trình đệ quy DFS, cổng lọc lỗi 422 Validation Gate)
│   ├── Slide 8: Bộ hoạch định Pareto Planner (Cơ chế Structured Outputs, luồng dự phòng Heuristic)
│   ├── Slide 9: Luồng phát Audiobook & Chống tua ngược (Logic theo dõi biến listened_ms)
│   ├── Slide 10: Định thời ôn tập Spaced Repetition (Quét lịch tự động qua Celery Beat)
│   ├── Slide 11: Mô hình Transactional Outbox Pattern (Đồng bộ Transaction ghi tiến độ và hàng đợi FCM)
│   ├── Slide 12: Trợ lý Voice Agent hai lớp (Kiến trúc văn bản qua HTTP, kiến trúc giọng nói qua WebRTC)
│   └── Slide 13: Luồng tra cứu Hybrid RAG & Evidence Validation (Tính blended_score và bộ lọc ảo giác)
│
├── 4. Hiện thực & Đánh giá thực nghiệm (~5 Slide) -> *Chứng minh thực chiến*
│   ├── Slide 14: Stack công nghệ triển khai (FastAPI, Celery, Redis, Supabase, Flutter Riverpod)
│   ├── Slide 15: Minh họa giao diện thực tế ứng dụng di động TriÂm
│   ├── Slide 16: Kịch bản kiểm thử tích hợp (Integration Test cases nổi bật)
│   ├── Slide 17: Số liệu thực nghiệm RAG (Độ chính xác và tính bám nguồn tri thức)
│   └── Slide 18: Thống kê hiệu năng thời gian thực (Biểu đồ độ trễ thoại dưới 1.5s và throughput của worker)
│
└── 5. Kết luận & Demo (~2 Slide)
    ├── Slide 19: Kết luận, Hạn chế (Tài liệu OCR chưa cấu trúc) và Hướng phát triển
    └── Slide 20: Lời cảm ơn Hội đồng & Bắt đầu Demo hệ thống
# BÁO CÁO TỔNG HỢP VÀ HƯỚNG DẪN KỊCH BẢN ĐÁNH GIÁ ĐỘ TRỄ THỰC NGHIỆM (LATENCY EVALUATION)

Tệp hướng dẫn này lưu trữ toàn bộ ngữ cảnh, giải thích bản chất kỹ thuật, nguồn dữ liệu và mã nguồn các test script đo đạc phân bổ độ trễ ($P_{50}, P_{90}, P_{95}$) cho hệ thống Trợ lý thoại TRIAM. Các AI Agent trong các phiên làm việc tiếp theo cần đọc tệp này để hiểu rõ xuất xứ số liệu và phương pháp kiểm thử.

---

## 1. VỊ TRÍ VÀ THÔNG SỐ CHÍNH THỨC TRONG LUẬN VĂN LATEX

- **Tệp LaTeX**: `W:\WorkSpace_IT\_CAPSTON_PROJECT\2022DoAnTN_KhoaDat\noidung\c9_xay_dung_he_thong\c9_07_danh_gia_thuc_nghiem.tex`
- **Mục**: `\subsection{Đánh giá hiệu năng và phân bổ độ trễ}` (`\label{sec:9-7-2}`)
- **Bảng đặc tả**: `\label{tab:c9_latency_budget}`

### Bảng kết quả chính thức (Đo đạc thực tế từ thiết bị di động):

| Giai đoạn xử lý | Chỉ số đo lường | $P_{50}$ (ms) | $P_{90}$ (ms) | $P_{95}$ (ms) |
| :--- | :--- | :---: | :---: | :---: |
| Định tuyến ý định | Semantic Grounding Router | 29 | 56 | 295 |
| Chốt chặn câu hỏi | Query Guard Validation | 0 | 0 | 0 |
| Truy xuất tri thức RAG | Retrieval (Hybrid Search + Cohere Reranker) | 1493 | 2966 | 3100 |
| Tìm kiếm Web mở rộng | Tavily Web Search API | 869 | 869 | 869 |
| Tổng hợp công cụ RAG | Total Tool Execution | 1516 | 2987 | 3131 |
| **Tổng lượt thoại** | **Voice Turn Total** | **12279** | **26459** | **41958** |

---

## 2. GIẢI THÍCH BẢN CHẤT KỸ THUẬT VÀ Ý NGHĨA THỐNG KÊ

1. **Khái niệm Phân vị ($P_{50}, P_{90}, P_{95}$)**:
   - **$P_{50}$ (Median / Trung vị 50%)**: 50% số lượt thoại có độ trễ nhỏ hơn hoặc bằng mốc này (trải nghiệm người dùng phổ biến nhất).
   - **$P_{90}$ (Phân vị 90%)**: 90% số lượt thoại có độ trễ nhỏ hơn hoặc bằng mốc này.
   - **$P_{95}$ (Phân vị 95% - Worst Case)**: 95% số lượt thoại có độ trễ nhỏ hơn hoặc bằng mốc này (chỉ 5% lượt thoại phức tạp nhất vượt qua mốc này).

2. **Bản chất của `Query Guard Validation` ($0\text{ ms}$)**:
   - Là bộ lọc từ vựng/trùng lặp chạy trực tiếp in-memory trên RAM Python với độ phức tạp $O(1)$. Thời gian thực tế chỉ tốn $0.1 \rightarrow 0.4\text{ ms}$, khi làm tròn sang số nguyên (`int`) sẽ bằng **$0\text{ ms}$**.

3. **Bản chất của `Voice Turn Total` ($12,2\text{s}$)** vs **`TTFA` ($1,8\text{s} - 2,5\text{s}$)**:
   - **`Voice Turn Total`**: Tính từ lúc người dùng bắt đầu ngắt lời cho đến khi Trợ lý đọc xong chữ cuối cùng của bài giảng dài 150-400 từ ($12,2\text{s}$ là thời lượng phát hoàn chỉnh bài giảng).
   - **`TTFA` (Time-To-First-Audio)**: Nhờ cơ chế **WebRTC Audio Streaming**, người học bắt đầu nghe thấy tiếng Trợ lý cất lời chỉ sau **$1,8\text{s} - 2,5\text{s}$**, đảm bảo đàm thoại mượt mà tự nhiên.

---

## 3. CÁC TEST SCRIPT ĐƯỢC KHỞI TẠO VÀ CÁCH CHẠY

Hệ thống đã xây dựng 2 script kiểm thử độc lập trong thư mục `tests/`:

### Script 1: Kiểm thử dữ liệu di động di động thực tế (`eval_latency_budget.py`)
- **Tệp mã nguồn**: `w:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\tests\eval_latency_budget.py`
- **Nguồn dữ liệu**: Đọc 318 sự kiện `AGENT_TRACE` từ `logs/ragas_eval/parsed_live_logs.json` (bóc tách từ các tệp `log_live_context_*.md`).
- **Lệnh chạy**:
  ```bash
  python tests/eval_latency_budget.py
  ```

### Script 2: Kiểm thử dữ liệu trực tiếp trên Backend Console (`eval_backend_console_latency.py`)
- **Tệp mã nguồn**: `w:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\tests\eval_backend_console_latency.py`
- **Nguồn dữ liệu**: Đọc 237 sự kiện `AGENT_TRACE` từ 11 tệp `logs/agent_eval/voice_console_*.log` (chạy test trực tiếp trên máy chủ BE không qua FE).
- **Kết quả Backend Console**:
  - `Semantic Grounding Router`: $P_{50} = 17\text{ ms}$
  - `Retrieval RAG`: $P_{50} = 3768\text{ ms}$
  - `Voice Turn Total (Console)`: $P_{50} = 9686\text{ ms}$ (nhanh hơn di động 2,6s do không tốn trễ mạng di động).
- **Lệnh chạy**:
  ```bash
  python tests/eval_backend_console_latency.py
  ```

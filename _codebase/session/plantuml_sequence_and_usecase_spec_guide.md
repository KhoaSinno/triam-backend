# QUY CHUẨN ĐẶC TẢ USE-CASE VÀ SƠ ĐỒ TRÌNH TỰ (PLANTUML & LATEX) CHO ĐỒ ÁN TRIAM

Tệp hướng dẫn này tổng hợp toàn bộ quy chuẩn, cấu trúc, phong cách vẽ sơ đồ PlantUML và cách soạn thảo bảng đặc tả Use-Case LaTeX cho hệ thống TRIAM. Mọi AI Agent trong các phiên làm việc sau cần đọc tệp này để tuân thủ chính xác 100%.

---

## 1. CẤU TRÚC THƯ MỤC VÀ ĐẶT TÊN TỆP (FILE NAMING & DIRECTORY STRUCTURE)

1. **Mã nguồn sơ đồ PlantUML (`.puml`)**:
   - Thư mục: `w:\WorkSpace_IT\_CAPSTON_PROJECT\triam-backend\_docs_capstone\_dia\Sequence\`
   - Tên tệp: `UC00X_Name.puml` (Ví dụ: `UC001_UploadAndIngestBook.puml`, `UC005_RealtimeVoiceAgentRAG.puml`).

2. **Tệp xuất PDF phục vụ chèn vào Luận văn LaTeX**:
   - Đường dẫn chèn trong LaTeX: `hinhve/c9_xay_dung_he_thong/sequence_uc_spec/UC00X_Name.pdf`
   - Vị trí vật lý: `W:\WorkSpace_IT\_CAPSTON_PROJECT\2022DoAnTN_KhoaDat\hinhve\c9_xay_dung_he_thong\sequence_uc_spec\`

3. **Nội dung đặc tả trong Luận văn LaTeX**:
   - Tệp Section chính: `W:\WorkSpace_IT\_CAPSTON_PROJECT\2022DoAnTN_KhoaDat\noidung\c9_xay_dung_he_thong\c9_08_xay_dung_chuc_nang.tex`
   - Tệp Index nhúng: `W:\WorkSpace_IT\_CAPSTON_PROJECT\2022DoAnTN_KhoaDat\noidung\c9_xay_dung_he_thong\index_c9.tex` (Dòng `\input{noidung/c9_xay_dung_he_thong/c9_08_xay_dung_chuc_nang}` phải nằm ngay **SAU** `c9_02_thiet_ke_giai_thuat`).

---

## 2. PHONG CÁCH VÀ QUY TẮC VẼ SƠ ĐỒ PLANTUML (PLANTUML SEQUENCE DIAGRAM RULES)

### 2.1. Cấu hình bắt buộc
* **Tắt bóng đổ (No Shadows)**: Luôn khai báo `skinparam shadowing false` ngay bên dưới dòng `@startuml`.

### 2.2. Quy ước đặt tên Đối tượng (Participant Naming)
* **Actor (Người dùng)**: `actor "User" as user`
* **Boundary (Giao diện)**: `boundary "UI: ..." as ui_...` (Ví dụ: `ui_voice`, `ui_app`)
* **Control (Bộ xử lý / Dịch vụ)**: `control "Ctrl: ..." as ctrl_...` hoặc tên dịch vụ (Ví dụ: `LiveKit Voice\nAgent Worker`, `Semantic Grounding\nRouter`, `Hybrid RAG\nService`)
* **Entity (CSDL / Queue / Storage)**: `entity "PostgreSQL" as db`, `entity "Redis Queue" as redis`, `entity "Storage" as storage`
* **External Entity (Dịch vụ bên thứ ba)**: `entity "OpenAI Realtime" as openai`, `entity "Firebase FCM" as fcm`

### 2.3. Quy ước Khối rẽ nhánh (Alt / Else Colors)
* **Luồng chính / Thành công**: `alt#Gold #LightBlue [Tên luồng]`
* **Luồng thứ cấp / Pareto / Cache**: `else #LightGreen [Tên luồng]`
* **Luồng ngoại lệ / Thất bại / Ngoài phạm vi**: `else #Pink [Tên luồng]`

### 2.4. Mô hình Kiến trúc Thực tế trong 5 Use-Case Core của TRIAM
1. **UC001 (Upload & Ingest Book)**: `User` -> `UI upload` -> `Ingestion service` -> `Storage` (Lưu tệp thô) -> `Validator` (Validation Gate) -> `Outline extractor` (Trích xuất `BookSection`) -> `PostgreSQL` (Lưu `Book` ở trạng thái `DRAFT`).
2. **UC002 (Create Study Plan)**: `User` -> `UI Cấu hình` -> `Dịch vụ kế hoạch đọc` -> `Thuật toán lập bài học` (`Full Mode` Heuristic gộp/tách đề mục vs `Pareto Mode` Cosine Similarity + LLM) -> `PostgreSQL` (Lưu `ReadingPlan` & `LearningUnit`) -> `Celery Worker` -> `Redis Queue` ("document" TTS background worker).
3. **UC003 (Track Audio Progress & Monotonic Anti-Rewind)**: `User` -> `UI Trình phát` -> `Dịch vụ tiến độ` -> `Throttling Filter` (Tiết giảm CSDL) -> `PostgreSQL` (Cập nhật tiến độ tích lũy & tiến độ cao nhất). Nếu $P_{\text{max}} \ge 80\% \rightarrow$ đánh dấu `COMPLETED`. Khi tua ngược: $P_{\text{current}}$ giảm nhưng $P_{\text{max}}$ giữ nguyên, bảo toàn trạng thái hoàn thành.
4. **UC004 (Spaced Repetition & FCM Notification Outbox)**: `Dịch vụ ôn tập` sinh 5 mốc SRS ($1, 3, 7, 14, 30$ ngày) khi bài học hoàn thành $\rightarrow$ Lưu `notification_outbox` (Transactional Outbox) -> `Celery Beat` quét định kỳ 60s -> `Redis Queue` -> `Notification Worker` -> `Firebase FCM` -> `UI Thông báo di động`.
5. **UC005 (Realtime Voice Agent & RAG)**:
   - **SFU WebRTC Relay**: `UI` kết nối phòng WebRTC của `LiveKit WebRTC Server`. `UI` publish Audio Stream vào `LiveKit WebRTC Server` $\rightarrow$ Server relay cho `LiveKit Voice Agent Worker`.
   - **Semantic Grounding Router**: Phân loại ý định.
     - **Nằm trong sách**: Gọi `Hybrid RAG Service` (`RRF Fusion` + `Cohere Reranker`) $\rightarrow$ Truyền context tới `OpenAI Realtime API` (`gpt-4o-mini-realtime`).
     - **Nằm ngoài sách**: `Semantic Grounding Router` yêu cầu `Internet Search` $\rightarrow$ Xin cấp quyền người dùng $\rightarrow$ Gọi `Internet Search Service` $\rightarrow$ Truyền kết quả tới `OpenAI Realtime API`.
   - **Phát âm thanh**: `Agent Worker` publish Audio Stream phản hồi vào `LiveKit WebRTC Server` $\rightarrow$ Server relay trực tiếp về `UI` thiết bị.

---

## 3. PHONG CÁCH VÀ CẤU TRÚC BẢNG ĐẶC TẢ USE-CASE LATEX

### 3.1. Cấu trúc Khối Bảng chuẩn hóa
Mỗi Use-Case trong `c9_08_xay_dung_chuc_nang.tex` được bao bọc trong khối `\begingroup ... \endgroup` để giữ độ rộng cột và khoảng cách hàng chuẩn:

```latex
\subsection{Chức năng: [Tên chức năng] (UC00X)}

\begingroup
\renewcommand{\arraystretch}{1.1}
\small
\centering
\noindent
\begin{minipage}{\textwidth}
    \centering
    \captionof{table}{Bảng đặc tả usecase: [Tên chức năng]}
    \begin{tabular}{|m{3cm}|m{9cm}|}
        \hline
        \textbf{Mã số}  & UC00X \\
        \hline
        \textbf{Tên}  & [Tên Use-Case] \\
        \hline
        \textbf{Mô tả}  & [Mô tả ngắn gọn, chính xác các công nghệ và quy trình cốt lõi] \\
        \hline
        \textbf{Tác nhân}  & [Người dùng / Hệ thống (tự động)] \\
        \hline
        \textbf{Mức độ ưu tiên}  & Bắt buộc \\
        \hline
        \textbf{Tác động}  & [Tác động dữ liệu CSDL hoặc hệ thống] \\
        \hline
        \textbf{Tiền điều kiện}  & [Tiền điều kiện thực hiện] \\
        \hline
        \textbf{Hậu điều kiện}  & [Kết quả đầu ra sau khi xử lý thành công] \\
        \hline
        \multirow{N}{*}{\textbf{Luồng xử lý chính}}
            & 1. Bước 1... \\
            & 2. Bước 2... \\
            ...
        \hline
        \multirow{2}{*}{\textbf{Xử lý ngoại lệ}}
            & - Trường hợp ngoại lệ 1... \\
            & - Trường hợp ngoại lệ 2... \\
        \hline
    \end{tabular}
\end{minipage}
\end{group}

\begin{figure}[H]
    \centering
    \includegraphics[width=1\textwidth]{hinhve/c9_xay_dung_he_thong/sequence_uc_spec/UC00X_Name.pdf}
    \caption{Sơ đồ trình tự: [Tên chức năng]}
    \label{fig:UC00X_Name}
\end{figure}
```

---

## 4. TÓM TẮT NGUYÊN TẮC VĂN PHONG VÀ TRÁNH LỖI

1. **Văn phong ngắn gọn, chuẩn academic**: Viết súc tích, đi thẳng vào bản chất kỹ thuật (ví dụ: dùng `PostgreSQL` thay cho `PostgreSQL DB`, dùng `Internet Search` thay cho `Web Search`).
2. **Không lạm dụng `\texttt{...}`**: Chỉ dùng `\texttt{...}` cho tên hàm/API/mô hình thật sự cần thiết, tránh tạo cảm giác rối rắt trên văn bản LaTeX.
3. **Đúng mô hình thực tế**: Luôn đối chiếu với mã nguồn Python backend (`app/`) để đảm bảo không bị nhầm lẫn giữa các mô hình (ví dụ: đàm thoại giọng nói Realtime dùng `OpenAI Realtime gpt-4o-mini-realtime`, không dùng `Google Gemini`).

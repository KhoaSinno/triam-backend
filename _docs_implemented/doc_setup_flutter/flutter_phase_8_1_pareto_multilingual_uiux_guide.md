# TRIAM Flutter Phase 8.1 Pareto Multilingual UI/UX Guide

Ngày cập nhật: 2026-06-02  
Audience: Flutter team, backend maintainer, capstone reviewer  
Backend scope: Phase 8.1 Pareto signal optimizer for Vietnamese/English documents  
Mục tiêu: Gợi ý FE cải thiện UI/UX cho mode Pareto sau khi backend đã tối ưu chọn bài học trọng tâm đa ngôn ngữ.

---

## 1. Đọc File Này Khi Nào?

FE đã implement theo contract chính:

```text
_docs_implemented/doc_setup_flutter/flutter_phase_6_backend_contract_uiux_refactor_guide.md
```

File Phase 8.1 này là tài liệu bổ sung cho UI/UX của `pareto` mode. Nếu hai file mâu thuẫn về API, ưu tiên file Phase 6 vì Phase 8.1 **không đổi API contract**.

Phase 8.1 chỉ cải thiện cách backend tạo `learning_units` Pareto:

```text
Trước:
  Pareto chủ yếu dựa vào prompt và vài keyword tiếng Việt.

Sau:
  Pareto hiểu tốt hơn outline tiếng Việt, tiếng Anh, song ngữ;
  gom các đề mục nhỏ thành bài học trọng tâm;
  fallback sạch hơn nếu LLM planner lỗi.
```

---

## 2. Điều FE Cần Biết

### 2.1 API Không Đổi

FE vẫn dùng các endpoint hiện tại:

```http
POST /api/v1/generate-plan
POST /api/v1/books/{book_id}/switch-mode
GET  /api/v1/books/{book_id}/learning-units?mode=pareto
GET  /api/v1/books/{book_id}/details?mode=pareto
GET  /api/v1/jobs/{job_id}
```

Không cần thêm API mới cho Phase 8.1.

### 2.2 Ý Nghĩa Pareto Mode Đã Rõ Hơn

FE không nên mô tả Pareto là:

```text
Tóm tắt mục lục
```

Nên mô tả là:

```text
Bản tinh gọn các ý cốt lõi
```

Hoặc:

```text
Nghe nhanh những phần quan trọng nhất
```

Với tiếng Anh:

```text
Focused version of the core ideas
```

### 2.3 Pareto Units Không Bằng Số Đề Mục

Backend có thể nhận một sách có rất nhiều đề mục, nhưng Pareto chỉ tạo vài bài nghe trọng tâm.

Ví dụ:

```text
122 đề mục gốc
4 bài nghe Pareto
```

FE không được hiển thị:

```text
122 chương Pareto
```

Nên hiển thị:

```text
122 đề mục
4 bài nghe trọng tâm
```

---

## 3. UI/UX Nên Cải Thiện

### 3.1 Mode Selector

Khi user chọn mode, nên có giải thích ngắn:

| Mode | Label gợi ý | Mô tả ngắn |
| --- | --- | --- |
| `full` | Đầy đủ | Nghe nhiều nội dung hơn theo cấu trúc tài liệu |
| `pareto` | Tinh gọn | Nghe nhanh các ý cốt lõi và phần quan trọng nhất |

Không nên dùng text quá dài trong button mode. Dùng tooltip, bottom sheet hoặc helper text bên dưới.

### 3.2 Generate Plan Bottom Sheet

Trước khi user bấm tạo plan/audio, FE nên hiển thị:

```text
Mode: Tinh gọn
Số đề mục gốc: 122
Dự kiến tạo: một số bài nghe trọng tâm
Ghi chú: Bản tinh gọn sẽ gom các mục liên quan để nghe nhanh hơn.
```

Nếu sách tiếng Anh:

```text
Mode: Focused
Original sections: 122
Output: focused learning units
```

FE không cần tự tính số unit Pareto trước khi gọi API. Backend mới là nơi quyết định.

### 3.3 Book Detail Screen

Nên tách rõ 2 lớp:

```text
Mục lục gốc:
  hiển thị outline/book_sections.

Bài nghe:
  hiển thị learning_units.
```

Gợi ý layout:

```text
[Tab] Mục lục
[Tab] Bài nghe
```

Trong tab Bài nghe khi mode là Pareto:

```text
4 bài nghe trọng tâm
Được tạo từ 122 đề mục gốc
```

Nếu title là tiếng Anh thì giữ nguyên tiếng Anh. Không tự dịch title ở FE.

### 3.4 Learning Unit Card

Một card bài nghe Pareto nên hiển thị:

```text
Tên bài nghe
Thời lượng dự kiến hoặc số đoạn nghe
Badge: Tinh gọn
Trạng thái: Đang xử lý / Có thể nghe / Hoàn tất
```

Ví dụ tiếng Việt:

```text
Nền tảng logic mệnh đề
Tinh gọn · 12 phút · Có thể nghe
```

Ví dụ tiếng Anh:

```text
Core Concepts and Logical Operators
Focused · 10 min · Ready
```

Lưu ý:

- Title có thể dài, phải wrap tối đa 2 dòng.
- Không ép lowercase/uppercase toàn bộ title, vì title tiếng Anh và tiếng Việt đều cần giữ ngữ nghĩa.
- Nếu title quá dài, dùng ellipsis sau 2 dòng.

### 3.5 Empty And Loading States

Khi Pareto đang generate:

```text
Đang chuẩn bị bản tinh gọn...
```

Không nên ghi:

```text
Đang tóm tắt chương...
```

Vì backend không còn xử lý theo chương cũ nữa.

Khi chưa có Pareto mode:

```text
Bạn có thể tạo bản tinh gọn để nghe nhanh các ý chính.
```

Khi `switch-mode` từ full sang pareto:

```text
Đang chuẩn bị bản tinh gọn. Bạn vẫn có thể nghe bản đầy đủ trong lúc chờ.
```

---

## 4. Multilingual UX Rules

### 4.1 Giữ Ngôn Ngữ Gốc Của Tài Liệu

Backend Phase 8.1 giữ title theo ngôn ngữ nguồn. FE không nên tự dịch title.

Ví dụ:

```text
Book tiếng Việt:
  "Khái niệm mệnh đề và phép toán logic"

Book tiếng Anh:
  "Rules of Inference and Proof Methods"
```

Lý do:

- User dễ đối chiếu với mục lục gốc.
- Tránh dịch sai thuật ngữ chuyên ngành.
- Giảm mismatch giữa outline và bài nghe.

### 4.2 UI Text Có Thể Theo Ngôn Ngữ App

Nếu app đang dùng tiếng Việt, label UI vẫn tiếng Việt:

```text
Tinh gọn
Đầy đủ
Mục lục
Bài nghe
Đang xử lý
```

Nhưng title bài học giữ nguyên từ backend.

### 4.3 Font Và Layout

FE cần đảm bảo:

- hỗ trợ dấu tiếng Việt;
- hỗ trợ title tiếng Anh dài;
- title wrap đẹp trong card;
- không dùng font size scale theo viewport quá mạnh;
- không để badge/status chen vào title.

Gợi ý card:

```text
[Unit index]  Title, max 2 lines
              Badge + duration + status
```

Không đặt status badge ngay sát title nếu title có thể dài.

---

## 5. Progress UX

Phase 8.1 không đổi progress API. FE vẫn poll:

```http
GET /api/v1/jobs/{job_id}
```

Gợi ý hiển thị:

```text
Đang tạo bản tinh gọn
Đã có thể nghe một phần
Hoàn tất bản tinh gọn
```

Khi trạng thái `partial_ready`, FE nên unlock audio có sẵn:

```text
Bạn có thể bắt đầu nghe trong khi hệ thống xử lý phần còn lại.
```

Không chờ `ready` mới cho nghe nếu backend đã trả trạng thái nghe được.

---

## 6. UX Copy Gợi Ý

### 6.1 Vietnamese

```text
Mode đầy đủ:
Nghe nội dung chi tiết theo cấu trúc tài liệu.

Mode tinh gọn:
Nghe nhanh các ý cốt lõi, khái niệm, quy tắc và phương pháp quan trọng.

Đang xử lý:
Đang chuẩn bị bản tinh gọn...

Partial ready:
Bản tinh gọn đã có thể nghe một phần.

Switch mode:
Đang chuẩn bị bản tinh gọn. Bạn vẫn có thể nghe bản hiện tại trong lúc chờ.
```

### 6.2 English

```text
Full:
Listen to a more detailed version following the document structure.

Focused:
Listen to the core ideas, rules, methods, and key concepts.

Processing:
Preparing focused version...

Partial ready:
Focused version is partially ready.
```

---

## 7. Không Nên Làm

FE không nên:

- tự detect Pareto bằng keyword;
- tự gom mục lục thành bài nghe;
- tự dịch title learning unit;
- hiển thị `total_sections` thành số chương;
- render `book_sections` như danh sách audio;
- gọi lại generate plan liên tục nếu chỉ muốn refresh progress;
- chờ toàn bộ sách ready mới cho nghe khi backend đã có `partial_ready`;
- hard-code giả định Pareto luôn có 3 hoặc 4 bài nghe.

---

## 8. Checklist Cho FE

- [ ] Mode selector có label `Đầy đủ` và `Tinh gọn`.
- [ ] Có mô tả ngắn để user hiểu Pareto là bản tinh gọn, không phải mất dữ liệu.
- [ ] Book detail tách `Mục lục` và `Bài nghe`.
- [ ] Không hiển thị số đề mục thành số chương.
- [ ] Learning unit card wrap title tốt cho tiếng Việt và tiếng Anh.
- [ ] Không tự dịch title từ backend.
- [ ] Khi `switch-mode` sang Pareto, giữ bản cũ đang nghe cho tới khi Pareto có thể nghe.
- [ ] Poll job progress và unlock khi `partial_ready`.
- [ ] Empty/loading/error state dùng từ "bản tinh gọn" thay vì "tóm tắt chương".
- [ ] FE không cần đổi API cho Phase 8.1.

---

## 9. Manual Test Gợi Ý Cho FE

### 9.1 Sách tiếng Việt

Flow:

```text
Upload sách tiếng Việt
Generate plan mode pareto
Vào Book Detail
Kiểm tra Mục lục và Bài nghe
Play bài nghe đầu tiên
Update progress
Switch full/pareto
```

Expected:

```text
Title tiếng Việt hiển thị đúng dấu.
Số bài nghe Pareto ít hơn số đề mục.
UI không gọi nhầm là chương.
```

### 9.2 Sách tiếng Anh

Flow:

```text
Upload English document with headings
Generate plan mode pareto
Open learning units
Play focused units
```

Expected:

```text
English titles preserved.
Long title wraps cleanly.
Badge/status không che title.
No broken Vietnamese-only label in title area.
```

### 9.3 Sách song ngữ

Flow:

```text
Upload mixed Vietnamese-English document
Generate plan mode pareto
Check unit titles and outline
```

Expected:

```text
Title không bị FE tự dịch.
UI vẫn dùng label theo ngôn ngữ app.
```

---

## 10. Tóm Tắt Cho Agent FE

Phase 8.1 không yêu cầu đổi API. FE cần cải thiện UI/UX để diễn giải đúng `pareto` mode:

```text
Pareto = bản tinh gọn các ý cốt lõi,
không phải danh sách chương,
không phải tóm tắt từng đề mục,
và có thể hoạt động với sách tiếng Việt, tiếng Anh hoặc song ngữ.
```

Việc chính của FE:

- render đúng `learning_units`;
- phân biệt `book_sections` với `learning_units`;
- giữ title theo backend;
- hiển thị mode Pareto bằng ngôn ngữ dễ hiểu;
- hỗ trợ title đa ngôn ngữ và trạng thái processing/partial_ready/ready.


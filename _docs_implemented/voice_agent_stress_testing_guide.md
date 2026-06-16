# TRIAM Voice Agent - Stress Testing Guide

Tài liệu này cung cấp các kịch bản kiểm thử khó (Stress Test Cases) giúp bạn tự kiểm tra toàn diện hoạt động của Voice Agent sau khi tối ưu hóa.

---

## 1. Case 1: Chỉ định chương không tồn tại
* **Câu hỏi bạn nói**: *"Tóm tắt chương 99"* hoặc *"Nội dung chương 150 có gì?"*
* **Kỳ vọng hành vi của Agent**: 
  * Agent sẽ phát âm câu trả lời làm rõ: *"Tôi không tìm thấy chương hoặc đề mục đó trong sách hiện tại. Bạn vui lòng kiểm tra lại số hoặc tên mục."* (LLM có thể diễn đạt lại câu này cho tự nhiên hơn).
* **Quy trình hoạt động bên dưới**:
  ```mermaid
  sequenceDiagram
      User->>Agent: "Tóm tắt chương 99"
      Agent->>intent_router: detect_section_intent()
      Note over intent_router: Nhận diện chỉ chỉ định chương (explicit target = 99)
      intent_router->>section_resolver: resolve_section()
      Note over section_resolver: Tra mục lục sách trong DB, không thấy mục 99
      section_resolver-->>Agent: SectionResolution(NOT_FOUND, "section_not_found")
      Agent-->>User: Trả về CLARIFICATION_REQUIRED & Agent đọc câu hỏi làm rõ
  ```

---

## 2. Case 2: Hỏi câu hỏi ngữ nghĩa nhưng chứa từ khóa chương
* **Câu hỏi bạn nói**: *"Nhân vật Lennie trong chương này như thế nào?"* hoặc *"Tóm tắt nhân vật George trong chương"* (Không có số chương cụ thể).
* **Kỳ vọng hành vi của Agent**:
  * Agent **không được hỏi ngược lại đòi số chương**.
  * Agent tự động tìm kiếm RAG toàn cuốn sách và trả lời trực tiếp về tính cách của Lennie/George dựa trên ngữ cảnh lấy được.
* **Quy trình hoạt động bên dưới**:
  ```mermaid
  sequenceDiagram
      User->>Agent: "Nhân vật Lennie trong chương này thế nào?"
      Agent->>intent_router: detect_section_intent()
      Note over intent_router: marker_present=True nhưng has_target=False.<br/>Trả về None (Không yêu cầu làm rõ cứng).
      Agent->>search_book_knowledge: Kích hoạt RAG tìm kiếm ngữ nghĩa toàn cuốn sách
      search_book_knowledge-->>Agent: Trả về các chunks nội dung liên quan đến Lennie
      Agent-->>User: LLM tổng hợp câu trả lời trực tiếp mà không vặn hỏi chương
  ```

---

## 3. Case 3: Hỏi thông tin thời sự / ngoài lề (Yêu cầu Web Search)
* **Câu hỏi bạn nói**: *"Giá Bitcoin hôm nay là bao nhiêu?"* hoặc *"Thời tiết Hà Nội hôm nay thế nào?"*
* **Kỳ vọng hành vi của Agent**:
  * Agent sẽ gọi Tool Web Search ngầm định, tự động cấp quyền vì ý định rõ ràng (`mode=implicit`, `intent=grant`).
  * Agent thực hiện tìm kiếm internet và trả lời trực tiếp thông tin thời sự mới nhất.
* **Quy trình hoạt động bên dưới**:
  ```mermaid
  sequenceDiagram
      User->>Agent: "Giá Bitcoin hôm nay là bao nhiêu?"
      Agent->>query_guard: Phân loại ý định tìm web
      Note over query_guard: classify_web_permission_intent_fast_path() -> implicit grant
      Agent->>execute_web_search: Gọi tìm kiếm Google/Bing ngoài internet
      execute_web_search-->>Agent: Trả về kết quả giá cả/thời tiết mới nhất
      Agent-->>User: Trả lời thông tin trực tiếp từ web
  ```

---

## 4. Case 4: Hỏi câu hỏi ngoài sách mơ hồ (Quy trình Hỏi xin quyền Web)
* **Câu hỏi bạn nói**: *"Ai là tổng thống Mỹ hiện tại?"* hoặc *"Cho tôi biết tin tức về AI hôm nay."*
* **Kỳ vọng hành vi của Agent**:
  * Agent sẽ hỏi xin quyền của bạn: *"Tôi cần tìm kiếm internet để trả lời câu hỏi này. Bạn có đồng ý cho tôi tìm web không?"* (Agent không được tự ý tìm nếu quyền chưa rõ ràng).
* **Quy trình hoạt động bên dưới**:
  1. Router phát hiện thông tin không nằm trong sách $\rightarrow$ Trả về `EXTERNAL_INFO_REQUIRED`.
  2. Agent gọi hàm `ask_web_search_permission` để ghi nhận trạng thái chờ duyệt (`waiting_for_web_permission`).
  3. LLM phát âm câu hỏi xin quyền và dừng lại chờ bạn trả lời.

---

## 5. Case 5: Từ chối cấp quyền Web (Sau khi Agent hỏi ở Case 4)
* **Câu nói tiếp theo của bạn**: *"Không được"* hoặc *"Khỏi đi"* hoặc *"Không"*
* **Kỳ vọng hành vi của Agent**:
  * Agent nhận biết được lời từ chối, hủy lệnh tìm kiếm và đáp lại nhẹ nhàng: *"Được rồi, tôi sẽ không tìm kiếm internet. Bạn có câu hỏi nào khác trong sách không?"*
* **Quy trình hoạt động bên dưới**:
  1. Trạng thái thoại đang là `waiting_for_web_permission`.
  2. Bạn nói từ chối $\rightarrow$ `classify_voice_reply_intent` phân loại là `deny`.
  3. Agent chặn không gọi tool tìm kiếm web, xóa trạng thái chờ và trả lời xác nhận từ chối.

---

## 6. Case 6: Đồng ý cấp quyền Web (Sau khi Agent hỏi ở Case 4)
* **Câu nói tiếp theo của bạn**: *"Đồng ý"* hoặc *"Tìm đi"* hoặc *"Ừ"*
* **Kỳ vọng hành vi của Agent**:
  * Agent nhận biết sự đồng ý, ngay lập tức gọi web search ngầm, lấy kết quả và trả lời cho câu hỏi gốc của bạn ở Case 4.
* **Quy trình hoạt động bên dưới**:
  1. Bạn nói đồng ý $\rightarrow$ Phân loại là `grant`.
  2. Agent gọi `execute_web_search` với câu hỏi gốc được lưu trong bộ nhớ tạm.
  3. Trả về kết quả và trả lời trực tiếp.

---

## 7. Case 7: Hỏi thông tin cấu trúc sách (Metadata)
* **Câu hỏi bạn nói**: *"Sách này có bao nhiêu chương?"* hoặc *"Tác giả quyển sách này là ai?"*
* **Kỳ vọng hành vi của Agent**:
  * Agent trả lời ngay lập tức bằng dữ liệu cứng (ví dụ: *"Sách Of Mice and Men có tổng cộng 6 chương chính"* hoặc *"Tác giả là John Steinbeck"*).
  * **Không chạy RAG** (Không gọi vector search tốn tài nguyên).
* **Quy trình hoạt động bên dưới**:
  1. `detect_metadata_intent` nhận diện từ khóa `bao nhiêu chương` $\rightarrow$ `BOOK_METADATA_ROOT_SECTION_COUNT`.
  2. Router đọc thẳng trường `root_section_count` từ bảng sách đã tải sẵn trong RAM.
  3. Trả về kết quả ngay lập tức dưới dạng trả lời tĩnh (`BOOK_METADATA_FOUND`).

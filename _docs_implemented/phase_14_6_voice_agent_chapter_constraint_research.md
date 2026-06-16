# Báo cáo Nghiên cứu và Thực hiện: Khắc phục hiện tượng Trợ lý Ràng buộc Người dùng Nhập Chương/Đề mục cụ thể

Báo cáo này tập trung vào nguyên nhân gốc rễ và giải pháp thực tế đã triển khai để khắc phục triệt để hành vi trợ lý tự động hỏi ngược lại yêu cầu người dùng chỉ định số chương (ví dụ: *"Bạn muốn tóm tắt chương nào?"* hoặc *"Bạn muốn hỏi nhân vật này trong chương nào?"*) đối với các câu hỏi chung hoặc câu hỏi ngữ nghĩa.

---

## 1. Phân tích Nguyên nhân Gốc rễ (2 Con đường Kích hoạt)

Hiện tượng này trước đây được kích hoạt qua 2 con đường (pathways) độc lập trong hệ thống:

### Con đường A: Bộ định tuyến Grounding Router lọc quá chặt chẽ (Python Code)
Khi câu hỏi của người dùng có chứa từ khóa liên quan đến phân đoạn như *"chương"*, *"phần"*, *"mục"* (nhưng không đi kèm số chương cụ thể, ví dụ: *"tóm tắt chương"*), hệ thống Python lập tức chặn câu hỏi và chuyển sang luồng hội thoại làm rõ bối cảnh (`CLARIFICATION`).

*   **Điểm chính xác 1 (Intent Detection)**: Hàm `detect_section_intent` (tại [intent_router.py:L84-L88](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_grounding/intent_router.py#L84-L88))
    Trước đây, nếu người dùng nói từ *"chương"* hoặc *"phần"* (có `marker_present`) mà không chỉ định số cụ thể, hệ thống trả về `CLARIFICATION_REQUIRED`. Phiên bản cũ hiện tại đã được comment lại tại [intent_router.py:L91-L98](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_grounding/intent_router.py#L91-L98) để đối chiếu.
*   **Điểm chính xác 2 (Section Resolver)**: [section_resolver.py:L183-L190](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_grounding/section_resolver.py#L183-L190)
    Khi `reference.has_target` là `False` (không tìm thấy số chương đi kèm), hàm này ngay lập tức trả về mã lỗi `missing_section_reference` đi kèm câu thoại làm rõ tĩnh: *"Bạn muốn hỏi chương hoặc đề mục nào?"*.
*   **Điểm chính xác 3 (LLM Rephrasing)**: Khi LLM nhận marker `CLARIFICATION_REQUIRED` từ tool, theo chỉ thị hệ thống, nó sẽ chuyển tiếp câu hỏi làm rõ này đến người dùng. LLM tự động diễn đạt lại câu thoại tĩnh thành câu nói tự nhiên hơn: *"Bạn muốn biết tính cách nhân vật này trong chương nào, bạn cho tôi chương cụ thể..."*

### Con đường B: LLM Tự quyết định từ chối do thiếu bối cảnh hoặc chỉ thị (LLM Decision)
Trong trường hợp người dùng hỏi một câu chung chung **không chứa từ khóa phân đoạn** (ví dụ: *"tóm tắt tính cách nhân vật lenie"*):
1.  Hệ thống Python không lọc `CLARIFICATION` mà sẽ fallback thành công về `GroundingRoute.BOOK_RAG` (Semantic RAG).
2.  Hệ thống chạy vector search và nạp các đoạn văn bản (chunks) từ các chương khác nhau.
3.  Do thiếu chỉ thị rõ ràng trong các prompt hệ thống (`VOICE_AGENT_INSTRUCTIONS` và `TEXT_AGENTIC_SYSTEM_INSTRUCTIONS`), mô hình lo ngại về tính chính xác và tự động chọn cách an toàn nhất là: Hỏi ngược lại người dùng xem họ có muốn thu hẹp phạm vi vào một chương cụ thể nào không.

---

## 2. Giải pháp Thực tế đã Triển khai (Đơn giản hóa & Tối ưu hóa)

Thay vì tạo thêm module phức tạp và hardcode danh sách từ khóa tiếng Việt (tránh thêm phiền phức và rủi ro sai lệch hành vi), chúng ta đã triển khai phương án tối ưu và triệt để nhất:

### Bước 1: Loại bỏ logic lọc cứng trong Python Code
Cập nhật [intent_router.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_grounding/intent_router.py) tại hàm `detect_section_intent` (ở dòng 84-88) để loại bỏ hoàn toàn việc trả về `CLARIFICATION_REQUIRED` khi thiếu mục tiêu số chương, đồng thời comment lại đoạn code cũ (ở dòng 91-98) để lưu vết tham chiếu:
```python
def detect_section_intent(query: NormalizedQuery, reference: SectionReference) -> GroundingIntent | None:
    summary_requested = contains_any_phrase(query, SUMMARY_MARKERS)
    if reference.has_target:
        return GroundingIntent.BOOK_SECTION_SUMMARY if summary_requested else GroundingIntent.BOOK_SECTION_CONTENT
    return None
```
*Hiệu quả*: Nếu câu hỏi không chỉ định rõ số chương (ví dụ: *"Tóm tắt chương"*, *"Kể về nhân vật Lennie trong chương"*), bộ định tuyến sẽ trả về `None`, hệ thống tự động fallback về luồng `GroundingRoute.BOOK_RAG` để tìm kiếm ngữ nghĩa toàn bộ sách.

### Bước 2: Cập nhật System Prompt (LLM Instructions Tuning)
Bổ sung quy tắc rõ ràng vào các prompt hệ thống trong [agent_voice_gpt_realtime.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py) để cấm LLM tự ý yêu cầu người dùng chọn chương đối với các câu hỏi khái quát.

*   **Prompt Voice Chat (`VOICE_AGENT_INSTRUCTIONS`)**:
    > `- If the user asks a general/conceptual book question or requests a character/concept summary without specifying a chapter, do not ask them to specify a chapter. Answer directly using the provided context (e.g. from BOOK_CONTEXT_FOUND).`
*   **Prompt Text Chat (`TEXT_AGENTIC_SYSTEM_INSTRUCTIONS`)**:
    > `- If the user asks a general/conceptual book question or requests a character/concept summary without specifying a chapter, do not ask them to specify a chapter. Answer directly using the provided context.`

---

## 3. Kết quả Xác minh và Thử nghiệm
*   **Chạy thử nghiệm Console thoại**:
    *   Hỏi: *"Những nhân vật trong 'Of Mice and Men' là ai?"* $\rightarrow$ Trả lời trực tiếp ngay lập tức bằng dữ liệu RAG.
    *   Hỏi: *"Quan hệ giữa Candy và George là gì?"* $\rightarrow$ Tìm kiếm RAG toàn sách và trả lời trực tiếp không hỏi vặn.
    *   Hỏi: *"Tóm tắt chương 2"* $\rightarrow$ [section_resolver.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_grounding/section_resolver.py) hoạt động bình thường, định vị trúng chương 2 để tóm tắt.
    *   Hỏi: *"Tóm tắt chương 99"* $\rightarrow$ Agent thông báo rõ không tìm thấy chương 99 trong sách hiện tại.
*   **Đồng bộ hóa Unit Test**:
    Định cấu hình lại và đồng bộ hóa các bộ kiểm thử tự động để phù hợp với cơ chế định tuyến thông minh mới (bỏ chặn `CLARIFICATION` không đáng có và tự động fallback về `BOOK_RAG`):
    *   [test_intent_router.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/tests/services/agent_grounding/test_intent_router.py): Cập nhật `test_detects_section_summary_and_missing_reference` để mong đợi `detect_section_intent` trả về `None` khi thiếu reference cụ thể.
    *   [test_grounding_router.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/tests/services/agent_grounding/test_grounding_router.py): Cập nhật `test_ambiguous_section_falls_back_to_rag_without_section_load` kiểm thử việc tự động định vị lại về `BOOK_RAG` (`GroundingIntent.BOOK_SEMANTIC_QUESTION`) thay vì `CLARIFICATION`.
    *   [test_shared_policy.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/tests/services/agent_policy/test_shared_policy.py): Cập nhật `test_missing_section_target_falls_back_to_rag` để xác nhận kết quả phân tích sinh ra hành động `ANSWER_WITH_RAG_CONTEXT` và nạp context `BOOK_CONTEXT_FOUND` bình thường.
    *   [test_query_guard.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/tests/services/voice_agent/test_query_guard.py): Thay đổi `test_section_question_without_target_is_valid` để cho phép các câu hỏi dạng *"Tóm tắt chương"* hợp lệ và đi tiếp.
    *   [test_agent_voice_query_guard.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/tests/services/voice_agent/test_agent_voice_query_guard.py): Thay đổi `test_voice_clarification_marker_sets_pending_state` sử dụng từ khóa gợi ý trung lập `"abc"` nhằm kích hoạt lỗi `too_short_or_ack_only` thay vì `missing_section_reference` (do quy tắc cũ đã bị gỡ bỏ).
*   **Kết quả Test Suite**: Toàn bộ **306/306 test cases** chạy thành công 100%.

# Hướng dẫn Kỹ thuật Phase 19 - Context-Aware ASR Correction for Realtime Voice Agent

## 1. Tại sao Phase này tồn tại (Bối cảnh & Nghiệp vụ)

Trong quá trình sử dụng Trợ lý thoại tương tác thời gian thực (LiveKit Realtime Agent), người học thường xuyên gặp lỗi nhận dạng giọng nói từ Whisper STT do các đặc trưng đặc thù của tiếng Việt:
1.  **Lỗi đồng âm/lệch dấu (Acoustic Homophones)**: Nhầm lẫn dấu hỏi/ngã/nặng hoặc các phụ âm đầu gần âm (`"Sách có mấy"` bị nhận diện thành `"Sạch co máy"`, `"Hậu quả"` bị nhận diện thành `"Câu hỏi"`).
2.  **Lỗi thuật ngữ chuyên ngành (Code-Switching)**: Whisper phiên âm sai các từ tiếng Anh chuyên ngành công nghệ hoặc lập trình khi trộn lẫn trong câu tiếng Việt (`"webrtc"` -> `"web r t c"`, `"int"` -> `"em"`).

### Hướng tiếp cận SOTA tối ưu (Không hard-code)
Thay vì sử dụng một mô hình sửa lỗi chính tả trung gian chạy ngoài (tốn thêm 0.5s - 1.5s độ trễ) hoặc hard-code các bộ từ điển tĩnh trong code, Phase 19 triển khai **Cơ chế sửa lỗi lai hai tầng tích hợp ngữ cảnh động (Context-Aware ASR Correction)**:

*   **Tầng 1 (Whisper Style Prompting)**: Thay đổi cách gửi prompt định hướng cho Whisper. Thay vì gửi danh sách từ khóa thô (glossary), chúng ta gửi một **câu thoại giả định (mock conversation)**. Whisper học văn phong và cách viết hoa các thuật ngữ từ câu thoại này tốt hơn rất nhiều.
*   **Tầng 2 (Context-Aware LLM Agent Policy)**: Tận dụng khả năng ghi nhớ ngữ cảnh (Stateful Session) của OpenAI Realtime API. Chúng ta nạp danh mục chương sách hiện tại một cách động từ cơ sở dữ liệu vào `instructions` của Agent. Khi người dùng nói sai âm học, Agent sẽ tự động đối chiếu âm thanh/văn bản bị lỗi đó với ngữ cảnh chương mục và lịch sử thoại gần nhất để gọi đúng công cụ RAG với tham số đã được hiệu chỉnh chính xác.

---

## 2. Hướng dẫn sửa đổi mã nguồn chi tiết

Chúng ta sẽ sửa đổi 2 tệp tin chính:
1.  `app/services/voice_agent/transcription_prompt.py`: Chuẩn hóa Whisper Prompt từ danh sách từ khóa sang câu thoại giả định.
2.  `app/services/agent_voice_gpt_realtime.py`: Tích hợp luật sửa lỗi ASR và nạp động tiêu đề chương vào System Instructions của Trợ lý thoại.

---

### 2.1 Cập nhật [app/services/voice_agent/transcription_prompt.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/voice_agent/transcription_prompt.py)

Tìm hàm `_build_prompt` (khoảng dòng 162) và thay thế logic nối từ khóa thô thành cấu trúc câu thoại giả định.

#### Mã nguồn thay đổi (Diff):
```diff
-def _build_prompt(base: str, terms: list[str], *, max_chars: int) -> str:
-    dynamic_suffix = " Session-specific expected terms: " + ", ".join(terms) + "." if terms else ""
-    prompt = (
-        base
-        + " The user may mix Vietnamese with English book titles, author names, character names, AI terms, and short app commands."
-        + " Prefer the exact expected terms when acoustically plausible; do not force them when the audio clearly says something else."
-        + dynamic_suffix
-    ).strip()
-    return _trim_prompt(prompt, max_chars=max_chars)

+def _build_prompt(base: str, terms: list[str], *, max_chars: int) -> str:
+    # Xây dựng câu thoại giả định (Mock Conversation) giúp Whisper học văn phong và thuật ngữ tốt hơn
+    mock_dialogue = ""
+    if terms:
+        mock_dialogue = " Chào bạn! Hôm nay chúng ta sẽ cùng thảo luận về các thuật ngữ " + ", ".join(terms[:12]) + " nhé. Bạn muốn hỏi gì?"
+    
+    prompt = (
+        base
+        + " The user may mix Vietnamese with English book titles, author names, character names, AI terms, and short app commands."
+        + " Prefer the exact expected terms when acoustically plausible; do not force them when the audio clearly says something else."
+        + mock_dialogue
+    ).strip()
+    return _trim_prompt(prompt, max_chars=max_chars)
```

---

### 2.2 Cập nhật [app/services/agent_voice_gpt_realtime.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py)

#### Bước A: Bổ sung Quy tắc sửa lỗi ASR vào `VOICE_AGENT_INSTRUCTIONS`
Tìm chuỗi khai báo `VOICE_AGENT_INSTRUCTIONS` (khoảng dòng 68) và bổ sung thêm chỉ dẫn sửa lỗi chính tả âm học cho Agent:

```diff
 VOICE_AGENT_INSTRUCTIONS = """
 You are TRIAM, a Vietnamese audiobook study assistant.
 
 Core rules:
 - Answer in Vietnamese only.
 - Keep replies natural and short: 2-3 sentences.
 - You are encouraged to use Markdown formatting (including headings, bold text, bullet/numbered lists, and tables) in your transcript text to make the on-screen display rich and structured. However, speak in a natural, conversational manner.
 - If audio is unclear, partial, noisy, silent, or unintelligible, ask the user to repeat in Vietnamese.
 - If the user asks a general/conceptual book question or requests a character/concept summary without specifying a chapter, do not ask them to specify a chapter. Answer directly using the provided context (e.g. from BOOK_CONTEXT_FOUND).
 
+ASR spelling and homophone correction rules:
+- The user's voice inputs are transcribed using Speech-to-Text (ASR) and may contain spelling mistakes, missing diacritics, or homophone errors (e.g., "sạch co máy chương" instead of "sách có mấy chương", "câu hỏi bi thảm" instead of "hậu quả bi thảm").
+- You must dynamically map acoustically similar speech to the correct terms from the "Ngữ cảnh học tập hiện tại" or the recent conversation history.
+- When calling functions like `search_book_knowledge`, always use the corrected spelling of the query (e.g., pass "sách có mấy chương" instead of "sạch co máy chương", and "hậu quả bi thảm" instead of "câu hỏi bi thảm").
+
 Tool rules:
 - For any question about book content, concepts, chapters, learning topics, or study context, ALWAYS call `search_book_knowledge` first.
...
 """
```

#### Bước B: Nạp động Tiêu đề Chương vào Instructions trong hàm khởi tạo `TriamAssistant`
Tìm hàm khởi tạo `__init__` của lớp `TriamAssistant` (khoảng dòng 264) và cập nhật logic để duyệt cây đề mục và nạp tiêu đề chương cấp 1 (level 1) vào prompt hướng dẫn:

```diff
     def __init__(
         self,
         document_ids: list[str],
         web_search_policy: WebSearchPermissionPolicy,
         tracer: AgentTurnTracer,
         grounding_router: GroundingRouter | None = None,
         voice_turn_state: VoiceTurnState | None = None,
         shared_policy: SharedAgentPolicy | None = None,
     ) -> None:
         books_str = ""
         if grounding_router and grounding_router.scope.books:
             books_list = []
             for b in grounding_router.scope.books:
                 book_desc = f"- Sách: '{b.title}'"
                 if b.author:
                     book_desc += f" của tác giả {b.author}"
                 books_list.append(book_desc)
             books_str = "\n\nNgữ cảnh học tập hiện tại:\n" + "\n".join(books_list)
 
+            # Trích xuất và nạp danh sách chương cấp 1 động từ GroundingScope để LLM làm điểm tựa sửa lỗi
+            headings_list = []
+            for s in grounding_router.scope.sections:
+                if s.level == 1:  # Chỉ lấy tiêu đề chương chính để tránh quá tải prompt
+                    headings_list.append(f"  + Chương {s.path}: {s.title}")
+            if headings_list:
+                books_str += "\n\nDanh sách các chương trong sách:\n" + "\n".join(headings_list)
+
         super().__init__(instructions=VOICE_AGENT_INSTRUCTIONS + books_str)
```

---

## 3. Giải thích Kỹ thuật dành cho Fresher (Training & Concepts)

### 3.1 Tại sao Whisper cần Continuation Prompt thay vì Glossary?
*   **Glossary**: Gửi dạng `[từ 1, từ 2, từ 3]`. Whisper thường bỏ qua danh sách này vì nó không biết các từ này dùng trong ngữ cảnh nào và có thể dẫn đến việc ghép sai từ ghép.
*   **Continuation (Mock Dialogue)**: Gửi dạng `"Hôm nay chúng ta sẽ thảo luận về A, B, C nhé."`. Whisper sử dụng cơ chế chú ý (attention mechanism) để tiếp tục hội thoại theo phong cách mẫu này. Khi nghe thấy âm thanh tương tự âm học của `A`, `B`, hoặc `C`, Whisper sẽ ưu tiên chọn từ có chính tả chính xác như câu mẫu.

### 3.2 Cơ chế sửa lỗi Stateful của OpenAI Realtime API
*   Khi sử dụng API truyền thống (Stateless), mỗi lượt thoại là độc lập. Để sửa lỗi chính tả ngữ cảnh (như nhầm `"câu hỏi"` thành `"hậu quả"`), bạn bắt buộc phải truy vấn lại cơ sở dữ liệu lịch sử chat để so khớp.
*   Với LiveKit Realtime Agent sử dụng **OpenAI Realtime API**, phiên kết nối là liên tục (Stateful). Toàn bộ lịch sử trao đổi của người dùng và Agent được mô hình ghi nhớ trực tiếp trong session memory. Khi người dùng hỏi *"Hậu quả bi thảm là sao?"* bị nhận diện sai thành *"Câu hỏi bi thảm là sao?"*, mô hình sẽ tự liên kết với câu trả lời trước đó của nó chứa từ *"hậu quả bi thảm"* để hiểu đúng và gọi công cụ RAG với tham số chính xác.

---

## 4. Kịch bản kiểm thử (Verification Plan)

### 4.1 Chạy Unit Test tự động
Fresher chạy bộ unit test để đảm bảo các thay đổi cú pháp không phá vỡ ứng dụng:
```powershell
uv run pytest tests/services/voice_agent -q
```

### 4.2 Kiểm thử thủ công (Integration/Manual Test)
1.  Khởi động môi trường ảo của backend.
2.  Mở ứng dụng client hoặc trang console LiveKit.
3.  Chọn sách `"Of Mice and Men"`.
4.  Nói vào micro bằng giọng cố ý sai lệch hoặc nhầm dấu:
    *   Nói nhanh: *"Sạch co máy chương"* $\rightarrow$ Kiểm tra logs xem tham số `query` truyền vào `search_book_knowledge` có được Agent tự động sửa thành `"sách có mấy chương"` hay không.
    *   Nói thuật ngữ: *"webrtc là gì"* $\rightarrow$ Kiểm tra xem tham số truyền vào RAG có được viết hoa chuẩn `"WebRTC"` không.
5.  Đảm bảo không phát sinh bất kỳ lỗi ngoại lệ nào (`Exception`) trong logs của LiveKit worker.

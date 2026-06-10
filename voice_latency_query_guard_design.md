# Tài liệu thiết kế: Khắc phục lỗi trễ (Latency/Deadlock) của Voice Agent khi hội thoại làm rõ

Tài liệu này phân tích chi tiết lỗi treo và mô tả thiết kế giải pháp **Option 3 (Hybrid: Trạng thái + Độ dài câu)** để Codex có thể hiện thực hóa (implement) một cách tối ưu và triệt để nhất.

---

## 1. Mô tả vấn đề (Problem Description)

Khi sử dụng Voice Agent trong môi trường học tập, người dùng gặp phải hiện tượng treo/trễ nghiêm trọng (turn latency kéo dài từ **55 - 66 giây**) trong luồng hội thoại làm rõ:

1. **Người dùng**: *"Chương 5 xảy ra chuyện gì?"*
2. **Agent**: *"Bạn muốn tóm tắt chương 5 đúng không?"* (Hỏi xác nhận/làm rõ)
3. **Người dùng**: *"đúng rồi"*
4. **Hệ thống**: Treo cực kỳ lâu (gần 1 phút), không phản hồi giọng nói. Nếu người dùng không chủ động nói một câu hỏi mới khác thì Agent sẽ im lặng hoặc lỗi.

---

## 2. Phân tích nguyên nhân gốc rễ (Root Cause Analysis)

### Nguyên nhân A: Bộ lọc từ khóa của Voice Query Guard quá khắt khe
Trong lượt thoại xác nhận, mô hình (LLM) sinh ra câu lệnh gọi tool:
```python
search_book_knowledge(query="tóm tắt chương 5")
```
Nhưng transcript thực tế của người dùng ở lượt thoại này chỉ là `"đúng rồi"`.
`VoiceQueryGuard` so sánh câu truy vấn `"tóm tắt chương 5"` với transcript `"đúng rồi"`. Do không có bất kỳ từ khóa trùng khớp nào (overlap ratio = 0.0), Query Guard chặn lệnh gọi tool với mã lỗi `tool_query_important_token_mismatch` hoặc `tool_query_transcript_mismatch`.

### Nguyên nhân B: Vòng lặp bối rối (LLM Deadlock) và Race Condition
* Khi tool bị chặn và trả về `CLARIFICATION_REQUIRED`, LLM rơi vào vòng lặp cố gắng gọi lại tool hoặc chờ đợi phản hồi trong vô vọng vì nó nghĩ nó đã hỏi làm rõ rồi. Điều này dẫn tới hết hạn turn timeout (gần 60 giây).
* **Race Condition (Bất đồng bộ sự kiện)**: Khi người dùng ngắt lời bằng câu nói mới (ví dụ: *"Crooks làm gì..."*), sự kiện `user_input_transcribed` cập nhật transcript mới của người dùng nhanh hơn. Nhưng ngay sau đó, sự kiện `conversation_item_added` của câu thoại cũ (`"đúng rồi"`) được commit trễ, đè lên transcript khiến Query Guard tiếp tục chặn sai lượt thoại tiếp theo.

---

## 3. Giải pháp thiết kế triệt để: Option 3 (Hybrid: Trạng thái + Độ dài câu)

Giải pháp này sử dụng **Dialogue State Tracking (Theo dõi trạng thái hội thoại)** kết hợp với **Kiểm tra độ dài văn bản cục bộ** để tự động cho phép chạy tool (Bypass) khi người dùng trả lời xác nhận ngắn.

### Cơ chế hoạt động:
1. **Lưu trạng thái**: Khi Agent phản hồi một câu hỏi làm rõ (`CLARIFICATION_REQUIRED`), hệ thống đặt cờ `waiting_for_clarification = True`.
2. **Quyết định Bypass**: Ở lượt thoại tiếp theo, nếu LLM gọi tool:
   * Nếu `waiting_for_clarification == True` **VÀ** transcript của người dùng ngắn (ví dụ: $\le$ 3 từ), hệ thống hiểu đây là câu xác nhận/phủ định ngắn $\rightarrow$ **Tự động Bypass (cho phép chạy RAG luôn)**.
   * Nếu không thỏa mãn (ví dụ người dùng hỏi sang câu dài khác), hệ thống vẫn so khớp từ khóa bình thường để bảo vệ tính chính xác.
3. **Dọn dẹp trạng thái**: Cờ `waiting_for_clarification` sẽ được trả về `False` ngay khi một lượt thoại thành công hoặc Agent hoàn thành câu trả lời bình thường (không phải clarification).

---

## 4. Hướng dẫn hiện thực hóa Code (Implementation Details)

Codex hãy thực hiện thay đổi tại các file sau:

### Bước 1: Thêm cờ trạng thái vào `VoiceTurnState`
File: [turn_state.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/voice_agent/turn_state.py)

Thêm thuộc tính `waiting_for_clarification` vào khởi tạo của class `VoiceTurnState`:
```python
class VoiceTurnState:
    def __init__(self, *, clock=time.monotonic) -> None:
        self._clock = clock
        self._final_transcript: VoiceTranscriptSnapshot | None = None
        self._committed_user_text: VoiceTranscriptSnapshot | None = None
        # Cờ đánh dấu đang chờ câu trả lời làm rõ từ người dùng
        self.waiting_for_clarification: bool = False
```

---

### Bước 2: Cập nhật logic `VoiceQueryGuard` để nhận cờ và thực hiện Bypass
File: [query_guard.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/voice_agent/query_guard.py)

1. Cập nhật hàm `guard_voice_book_query` và `compare_query_with_transcript` để nhận thêm tham số `waiting_for_clarification: bool = False`.
2. Trong hàm `compare_query_with_transcript`, thêm logic kiểm tra độ dài từ của transcript khi cờ đang bật:

```python
def guard_voice_book_query(
    query: str,
    transcript: VoiceTranscriptSnapshot | None,
    *,
    config: VoiceQueryGuardConfig | None = None,
    waiting_for_clarification: bool = False,
) -> VoiceQueryGuardResult:
    return compare_query_with_transcript(
        query,
        transcript,
        config=config,
        waiting_for_clarification=waiting_for_clarification,
    )

def compare_query_with_transcript(
    query: str,
    transcript: VoiceTranscriptSnapshot | None,
    *,
    config: VoiceQueryGuardConfig | None = None,
    waiting_for_clarification: bool = False,
) -> VoiceQueryGuardResult:
    resolved_config = config or VoiceQueryGuardConfig()
    base_result = assess_voice_query(query, config=resolved_config)
    if not base_result.valid:
        return base_result
    if transcript is None:
        return base_result

    # --- ĐOẠN CODE THAY ĐỔI: LAI (HYBRID) BYPASS ---
    if waiting_for_clarification:
        # Chuẩn hóa transcript để đếm từ chính xác
        from app.services.voice_agent.web_permission_intent_classifier import normalize_intent_text
        normalized_text = normalize_intent_text(transcript.text)
        words = normalized_text.split()
        
        # Nếu câu thoại rất ngắn (<= 3 từ), coi như là câu trả lời khẳng định/phủ định (vd: "đúng rồi", "dạ phải")
        if len(words) <= 3:
            return VoiceQueryGuardResult(
                valid=True,
                reason_code="valid",
                token_count=base_result.token_count,
                important_token_count=base_result.important_token_count,
                overlap_ratio=1.0,
                important_overlap_ratio=1.0,
                transcript_source=transcript.source,
            )
    # -----------------------------------------------

    # Logic so khớp từ khóa mặc định bên dưới giữ nguyên...
    query_tokens = _content_tokens(query)
    ...
```

---

### Bước 3: Cập nhật luồng xử lý chính trong Realtime Assistant
File: [agent_voice_gpt_realtime.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py)

#### 1. Cập nhật `resolve_book_query`:
Truyền cờ `waiting_for_clarification` vào Query Guard, sau đó thiết lập cờ dựa trên kết quả chặn:

```python
    async def resolve_book_query(self, query: str, input_mode: AgentInputMode) -> str:
        if input_mode == AgentInputMode.VOICE and settings.VOICE_AGENT_QUERY_GUARD_ENABLED:
            transcript = self.voice_turn_state.recent_transcript(settings.VOICE_AGENT_QUERY_GUARD_TRANSCRIPT_TTL_SECONDS)
            
            # Truyền trạng thái waiting_for_clarification hiện tại vào
            guard_result = guard_voice_book_query(
                query,
                transcript,
                config=self._voice_query_guard_config(),
                waiting_for_clarification=self.voice_turn_state.waiting_for_clarification,
            )
            
            # Tiêu thụ cờ ngay sau khi kiểm tra để tránh rò rỉ trạng thái
            self.voice_turn_state.waiting_for_clarification = False
            
            if not guard_result.valid:
                self.tracer.record_answer_source(input_mode, AgentAnswerSource.CLARIFICATION)
                
                # Nếu bị chặn vì cần làm rõ thông tin, bật cờ cho lượt thoại tiếp theo
                if guard_result.reason_code in (
                    "missing_section_reference", 
                    "too_short_or_ack_only", 
                    "tool_query_transcript_mismatch", 
                    "tool_query_important_token_mismatch"
                ):
                    self.voice_turn_state.waiting_for_clarification = True
                
                # Phần trả về thông báo lỗi giữ nguyên...
                ...
```

#### 2. Dọn dẹp cờ trạng thái khi Assistant trả lời bình thường:
Trong hàm `_handle_conversation_item_added`, khi Agent hoàn thành câu trả lời dạng thoại mà **không** phải là yêu cầu làm rõ, hãy tắt cờ:

```python
        elif item.role == "assistant":
            tracer.record_assistant(AgentInputMode.VOICE, char_count=len(text))
            tracer.complete_turn(AgentInputMode.VOICE)
            log.info(f"Assistant voice speech saved | text_len={len(text)} | thread_id={thread_uuid}")
            asyncio.create_task(transcript_store.save_and_publish_assistant(text))
            
            # Nếu lượt thoại của Agent kết thúc bình thường (không phải clarification), reset cờ
            if tracer.get_last_answer_source(AgentInputMode.VOICE) != AgentAnswerSource.CLARIFICATION:
                voice_turn_state.waiting_for_clarification = False
```
*(Lưu ý: Có thể cần viết thêm một helper method `get_last_answer_source` trong Tracer nếu chưa có, hoặc đọc trực tiếp từ thuộc tính lưu trữ lượt thoại của tracer).*

---

## 5. Kịch bản kiểm thử đề xuất (Suggested Tests)

Codex cần viết test case trong [test_query_guard.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/tests/services/voice_agent/test_query_guard.py) để đảm bảo không bị lỗi hồi quy (regression):

```python
def test_query_guard_bypasses_overlap_checks_during_clarification_mode() -> None:
    # Giả lập trạng thái đang chờ làm rõ (waiting_for_clarification = True)
    transcript = _snapshot("đúng rồi")
    
    result = guard_voice_book_query(
        query="tóm tắt chương năm của cuốn sách chuột và người",
        transcript=transcript,
        waiting_for_clarification=True
    )
    
    # Kết quả mong muốn: Phải hợp lệ (valid = True) dù không có từ khóa nào khớp
    assert result.valid is True
    assert result.reason_code == "valid"
```

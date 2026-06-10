# TRIAM Voice Agent Root-cause Fix Plan

Ngày tạo: 2026-06-10  
Phạm vi chính: `app/services/agent_voice_gpt_realtime.py`, `app/services/agent_grounding/*`, `app/services/agent_policy/*`, `app/services/voice_agent/tool_reply_watchdog.py`

## 0. Kết luận kỹ thuật

Sau khi đối chiếu log gần nhất với source code hiện tại, lỗi không còn nằm ở dynamic transcription prompt. Dynamic prompt đã start thành công, ví dụ log có dạng:

```text
Realtime transcription prompt ready | dynamic=True | terms=45 | chars=768
Starting realtime session with model: gpt-realtime-mini, voice: cedar
```

Root cause hiện tại gồm 2 nhóm:

1. **GroundingRouter / SharedPolicy đang route quá sớm sang clarification**, khiến nhiều câu hỏi semantic về sách không được chạy RAG thật. Ví dụ các câu như “mối quan hệ giữa George và Lennie”, “vai trò của Candy”, “Curley xuất hiện trong chương nào” đáng lẽ nên fallback RAG, nhưng log cho thấy `grounding_route=clarification`, `section_not_found`, `retrieval_result_count=0`, `tool_total=1-2ms`.

2. **Tool reply lifecycle sau khi tool hoàn thành vẫn chưa đủ chắc**, đặc biệt web/RAG tool result xong nhưng Realtime model không tự nói ngay. Watchdog hiện phát hiện đúng `no_speech_after_tool`, nhưng fallback hiện chỉ gọi `session.generate_reply()` chung chung, đôi khi vẫn trễ.

Vì vậy kế hoạch fix phải làm theo thứ tự ưu tiên:

```text
P0. Fix router/policy để semantic book query fallback RAG thay vì clarification.
P1. Tăng độ chắc của watchdog sau tool bằng forced reply instructions + optional direct say fallback.
P2. Sửa watchdog thinking counter để không coi thinking là speech generation.
P3. Giữ dynamic transcription prompt, chỉ thêm log và rollback flag.
P4. Thêm test scenario để tránh regression.
```

---

## 1. Nguyên tắc trước khi sửa

Không rollback dynamic prompt vội.

Không hard-code nhân vật như `George`, `Lennie`, `Candy` vào router.

Không tắt Watchdog.

Không tắt SharedAgentPolicy.

Không bật lại transcript overlap hard-block.

Tất cả dòng code mới hoặc vùng code sửa cần có comment dạng:

```py
# TRIAM_FIX_ROOT_CAUSE: ...
```

để sau này bạn dễ search/revert.

---

## 2. P0 — Fix semantic book query bị route sai thành clarification

### 2.1 Vấn đề trong code hiện tại

Trong `app/services/agent_grounding/grounding_router.py`, flow hiện tại:

```py
reference = parse_section_reference(normalized)
section_intent = detect_section_intent(normalized, reference)
if section_intent == GroundingIntent.CLARIFICATION_REQUIRED:
    result = self._clarification("missing_section_reference", "Bạn muốn hỏi chương hoặc đề mục nào?")
elif section_intent is not None:
    result = await self._resolve_section(normalized, reference, section_intent)
elif detect_external_current_info(normalized):
    ...
else:
    result = GroundingResult(... BOOK_RAG ...)
```

Khi câu hỏi có dấu hiệu liên quan “chương/mục/section” nhưng không resolve được section, router trả clarification. Điều này đúng với câu như:

```text
Tóm tắt chương 99.
Nội dung mục 3.2 là gì?
```

Nhưng không đúng với câu semantic như:

```text
Curley xuất hiện trong chương nào?
Vai trò của Candy là gì?
Mối quan hệ giữa George và Lennie là gì?
```

Với các câu này, RAG có khả năng tìm câu trả lời trong toàn bộ sách. Không nên bắt user chỉ định chương.

### 2.2 Thêm config để kiểm soát fallback

File: `app/core/config.py`

Thêm các biến:

```py
# TRIAM_FIX_ROOT_CAUSE: Allow semantic book questions to fall back to RAG when deterministic section resolution fails.
AGENT_GROUNDING_RAG_ON_SECTION_NOT_FOUND: bool = True

# TRIAM_FIX_ROOT_CAUSE: Limit fallback only to queries that look semantic, not explicit chapter/path requests.
AGENT_GROUNDING_SEMANTIC_FALLBACK_ENABLED: bool = True
```

`.env` gợi ý:

```env
AGENT_GROUNDING_RAG_ON_SECTION_NOT_FOUND=true
AGENT_GROUNDING_SEMANTIC_FALLBACK_ENABLED=true
```

### 2.3 Tạo helper nhận diện semantic book query

File mới khuyến nghị:

```text
app/services/agent_grounding/semantic_query_detector.py
```

Code:

```py
from __future__ import annotations

from app.services.agent_grounding.contracts import NormalizedQuery
from app.services.agent_grounding.query_normalizer import contains_any_phrase


# TRIAM_FIX_ROOT_CAUSE: Semantic book questions should not require a specific section/chapter.
SEMANTIC_BOOK_QUESTION_MARKERS = (
    "mối quan hệ",
    "quan hệ",
    "vai trò",
    "nhân vật",
    "là ai",
    "ai là",
    "tại sao",
    "vì sao",
    "ý nghĩa",
    "chủ đề",
    "phân tích",
    "so sánh",
    "đặc điểm",
    "tính cách",
    "xuất hiện",
    "liên quan",
    "ảnh hưởng",
    "nguyên nhân",
    "kết quả",
    "bài học",
    "symbol",
    "theme",
    "character",
    "relationship",
    "role",
    "why",
    "meaning",
    "compare",
    "appears",
)


# TRIAM_FIX_ROOT_CAUSE: Explicit section targets should remain deterministic and ask clarification when missing.
EXPLICIT_SECTION_TARGET_MARKERS = (
    "chương 1",
    "chương 2",
    "chương 3",
    "chapter 1",
    "chapter 2",
    "chapter 3",
    "mục 1",
    "mục 2",
    "section 1",
    "section 2",
)


def looks_like_semantic_book_question(query: NormalizedQuery) -> bool:
    """Return True for book-level semantic questions that should be handled by RAG.

    This intentionally does not mention concrete book characters like George/Candy/Lennie.
    It detects question shape, not hard-coded content.
    """
    # TRIAM_FIX_ROOT_CAUSE: Route semantic book questions to RAG instead of asking for chapter clarification.
    return contains_any_phrase(query, SEMANTIC_BOOK_QUESTION_MARKERS)
```

Lưu ý: `contains_any_phrase` đang được import trong `intent_router.py`. Nếu function này chưa export được từ `query_normalizer.py`, bạn có 2 lựa chọn:

- move helper `contains_any_phrase` ra module common, hoặc
- implement local simple version trong file mới.

Nếu hiện tại `contains_any_phrase` nằm trong `intent_router.py`, có thể import từ đó để ít sửa hơn:

```py
from app.services.agent_grounding.intent_router import contains_any_phrase
```

Nhưng cách sạch hơn là đặt helper phrase matching ở module chung sau này.

### 2.4 Sửa `GroundingRouter.resolve()` để fallback RAG đúng

File: `app/services/agent_grounding/grounding_router.py`

Thêm import:

```py
# TRIAM_FIX_ROOT_CAUSE: Detect semantic book-level questions and avoid over-clarification.
from app.core.config import settings
from app.services.agent_grounding.semantic_query_detector import looks_like_semantic_book_question
```

Trong `resolve()`, sửa đoạn:

```py
if section_intent == GroundingIntent.CLARIFICATION_REQUIRED:
    result = self._clarification("missing_section_reference", "Bạn muốn hỏi chương hoặc đề mục nào?")
elif section_intent is not None:
    result = await self._resolve_section(normalized, reference, section_intent)
```

thành:

```py
if section_intent == GroundingIntent.CLARIFICATION_REQUIRED:
    # TRIAM_FIX_ROOT_CAUSE: Do not force chapter clarification for semantic book questions.
    if (
        settings.AGENT_GROUNDING_SEMANTIC_FALLBACK_ENABLED
        and looks_like_semantic_book_question(normalized)
    ):
        result = self._book_rag_result("semantic_query_with_section_marker_fallback")
    else:
        result = self._clarification("missing_section_reference", "Bạn muốn hỏi chương hoặc đề mục nào?")
elif section_intent is not None:
    # TRIAM_FIX_ROOT_CAUSE: Resolve explicit section first, but allow semantic fallback if section resolution fails.
    result = await self._resolve_section_or_rag_fallback(normalized, reference, section_intent)
```

Thêm 2 method vào `GroundingRouter`:

```py
    # TRIAM_FIX_ROOT_CAUSE: Centralized BOOK_RAG decision for deterministic router fallback.
    @staticmethod
    def _book_rag_result(reason_code: str) -> GroundingResult:
        return GroundingResult(
            GroundingDecision(
                GroundingIntent.BOOK_SEMANTIC_QUESTION,
                GroundingRoute.BOOK_RAG,
                ResolutionQuality.NOT_FOUND,
                reason_code,
            )
        )

    async def _resolve_section_or_rag_fallback(self, query, reference, intent: GroundingIntent) -> GroundingResult:
        # TRIAM_FIX_ROOT_CAUSE: Keep exact section behavior, but avoid dead-ending semantic queries in clarification.
        result = await self._resolve_section(query, reference, intent)
        decision = result.decision

        if (
            settings.AGENT_GROUNDING_RAG_ON_SECTION_NOT_FOUND
            and decision.route == GroundingRoute.CLARIFICATION
            and decision.reason_code in {"section_not_found", "missing_section_reference"}
            and looks_like_semantic_book_question(query)
        ):
            return self._book_rag_result("section_not_found_semantic_rag_fallback")

        return result
```

### 2.5 Sửa đoạn fallback cuối trong `resolve()` dùng helper mới

Hiện cuối router có:

```py
result = GroundingResult(
    GroundingDecision(
        GroundingIntent.BOOK_SEMANTIC_QUESTION,
        GroundingRoute.BOOK_RAG,
        ResolutionQuality.NOT_FOUND,
        "semantic_rag_fallback",
    )
)
```

Đổi thành:

```py
# TRIAM_FIX_ROOT_CAUSE: Use one helper for all RAG fallback decisions to keep tracing consistent.
result = self._book_rag_result("semantic_rag_fallback")
```

### 2.6 Kỳ vọng sau P0

Log cho câu:

```text
mối quan hệ giữa George và Lennie trong Of Mice and Men
```

không được là:

```text
grounding_route=clarification
retrieval_result_count=0
```

Mà nên là một trong hai:

```text
grounding_route=book_rag
retrieval_result_count>0
action=answer_with_rag_context
```

hoặc nếu RAG không tìm thấy:

```text
grounding_route=book_rag
retrieval_result_count=0
action=ask_web_permission hoặc book_context_not_found
```

Quan trọng: `tool_total` không còn chỉ 1-2ms cho semantic query, vì RAG thật phải chạy.

---

## 3. P1 — Fix Watchdog fallback sau tool không nói

### 3.1 Vấn đề trong code hiện tại

File: `app/services/voice_agent/tool_reply_watchdog.py`

Hiện khi tool xong mà không có speech:

```py
self.session.generate_reply(**kwargs)
```

với kwargs chỉ có:

```py
{
    "allow_interruptions": True,
    "tool_choice": "none",
}
```

Điểm yếu:

- Không có instruction rõ “Tool đã xong, trả lời ngay”.
- `allow_interruptions=True` dễ bị user/mic interrupt khi agent đang cố trả lời.
- Không có fallback cấp 2 nếu `generate_reply()` vẫn im.
- Watchdog không phân biệt tool web, tool book, permission.

### 3.2 Thêm config cho forced reply instructions và fallback cấp 2

File: `app/core/config.py`

Thêm:

```py
# TRIAM_FIX_ROOT_CAUSE: Add explicit forced reply instruction after a tool result if Realtime does not resume.
VOICE_AGENT_TOOL_REPLY_WATCHDOG_FORCE_INSTRUCTIONS: str = (
    "Tool vừa trả kết quả. Hãy trả lời ngay cho người dùng bằng tiếng Việt, ngắn gọn, "
    "dựa trên kết quả tool mới nhất. Không gọi thêm tool."
)

# TRIAM_FIX_ROOT_CAUSE: Avoid user/mic interruption while the forced post-tool answer is starting.
VOICE_AGENT_TOOL_REPLY_WATCHDOG_ALLOW_INTERRUPTION_ON_FORCE: bool = False

# TRIAM_FIX_ROOT_CAUSE: Optional direct speech fallback when generate_reply still does not create speech.
VOICE_AGENT_TOOL_REPLY_WATCHDOG_DIRECT_SAY_FALLBACK_ENABLED: bool = False
VOICE_AGENT_TOOL_REPLY_WATCHDOG_DIRECT_SAY_DELAY_SECONDS: float = 2.0
VOICE_AGENT_TOOL_REPLY_WATCHDOG_DIRECT_SAY_TEXT: str = "Mình đã có kết quả rồi. Để mình trả lời ngay nhé."
```

`.env` gợi ý ban đầu:

```env
VOICE_AGENT_TOOL_REPLY_WATCHDOG_ALLOW_INTERRUPTION_ON_FORCE=false
VOICE_AGENT_TOOL_REPLY_WATCHDOG_DIRECT_SAY_FALLBACK_ENABLED=false
VOICE_AGENT_TOOL_REPLY_WATCHDOG_DIRECT_SAY_DELAY_SECONDS=2.0
```

Chưa bật direct say fallback ngay. Chỉ bật khi `generate_reply` vẫn im sau P1.

### 3.3 Sửa config dataclass

File: `app/services/voice_agent/tool_reply_watchdog.py`

Hiện:

```py
class VoiceToolReplyWatchdogConfig:
    enabled: bool
    grace_seconds: float
    thinking_grace_seconds: float
    monitored_tools: set[str]
    allow_error_outputs: bool = False
    force_tool_choice_none: bool = True
```

Đổi thành:

```py
class VoiceToolReplyWatchdogConfig:
    enabled: bool
    grace_seconds: float
    thinking_grace_seconds: float
    monitored_tools: set[str]
    allow_error_outputs: bool = False
    force_tool_choice_none: bool = True
    # TRIAM_FIX_ROOT_CAUSE: Explicit instructions make post-tool resume more deterministic.
    force_instructions: str | None = None
    # TRIAM_FIX_ROOT_CAUSE: Prevent mic/user interruptions while forced reply is starting.
    allow_interruption_on_force: bool = False
    # TRIAM_FIX_ROOT_CAUSE: Optional second-level fallback for Realtime sessions that still do not speak.
    direct_say_fallback_enabled: bool = False
    direct_say_delay_seconds: float = 2.0
    direct_say_text: str = "Mình đã có kết quả rồi. Để mình trả lời ngay nhé."
```

### 3.4 Sửa `_tool_reply_watchdog_config()`

File: `app/services/agent_voice_gpt_realtime.py`

Hiện:

```py
def _tool_reply_watchdog_config() -> VoiceToolReplyWatchdogConfig:
    return VoiceToolReplyWatchdogConfig(
        enabled=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_ENABLED,
        grace_seconds=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_GRACE_SECONDS,
        thinking_grace_seconds=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_THINKING_GRACE_SECONDS,
        monitored_tools={...},
        allow_error_outputs=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_ALLOW_ERROR_OUTPUTS,
        force_tool_choice_none=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_FORCE_TOOL_CHOICE_NONE,
    )
```

Thêm config mới:

```py
def _tool_reply_watchdog_config() -> VoiceToolReplyWatchdogConfig:
    return VoiceToolReplyWatchdogConfig(
        enabled=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_ENABLED,
        grace_seconds=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_GRACE_SECONDS,
        thinking_grace_seconds=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_THINKING_GRACE_SECONDS,
        monitored_tools={
            item.strip()
            for item in settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_TOOLS.split(",")
            if item.strip()
        },
        allow_error_outputs=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_ALLOW_ERROR_OUTPUTS,
        force_tool_choice_none=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_FORCE_TOOL_CHOICE_NONE,
        # TRIAM_FIX_ROOT_CAUSE: Pass forced reply instructions to watchdog fallback.
        force_instructions=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_FORCE_INSTRUCTIONS,
        # TRIAM_FIX_ROOT_CAUSE: Make post-tool fallback less likely to be cancelled by user/mic noise.
        allow_interruption_on_force=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_ALLOW_INTERRUPTION_ON_FORCE,
        # TRIAM_FIX_ROOT_CAUSE: Optional direct speech fallback if generate_reply remains silent.
        direct_say_fallback_enabled=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_DIRECT_SAY_FALLBACK_ENABLED,
        direct_say_delay_seconds=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_DIRECT_SAY_DELAY_SECONDS,
        direct_say_text=settings.VOICE_AGENT_TOOL_REPLY_WATCHDOG_DIRECT_SAY_TEXT,
    )
```

### 3.5 Sửa `_generate_reply_after_tool()`

File: `app/services/voice_agent/tool_reply_watchdog.py`

Hiện:

```py
def _generate_reply_after_tool(self) -> None:
    if not hasattr(self.session, "room") or not self.session.room.isconnected():
        log.info("[Watchdog] Session room is disconnected. Aborting force reply.")
        return

    kwargs: dict[str, Any] = {
        "allow_interruptions": True,
    }
    if self.config.force_tool_choice_none:
        kwargs["tool_choice"] = "none"
    self.session.generate_reply(**kwargs)
```

Đổi thành:

```py
def _generate_reply_after_tool(self) -> None:
    if not hasattr(self.session, "room") or not self.session.room.isconnected():
        log.info("[Watchdog] Session room is disconnected. Aborting force reply.")
        return

    kwargs: dict[str, Any] = {
        # TRIAM_FIX_ROOT_CAUSE: Avoid cancelling forced post-tool reply due to mic/user noise.
        "allow_interruptions": self.config.allow_interruption_on_force,
    }
    if self.config.force_tool_choice_none:
        kwargs["tool_choice"] = "none"
    if self.config.force_instructions:
        # TRIAM_FIX_ROOT_CAUSE: Tell Realtime exactly what to do after a completed tool.
        kwargs["instructions"] = self.config.force_instructions

    log.info(
        "Voice tool reply watchdog forcing generate_reply | "
        f"tool_choice_none={self.config.force_tool_choice_none} | "
        f"allow_interruptions={self.config.allow_interruption_on_force} | "
        f"has_instructions={bool(self.config.force_instructions)}"
    )
    self.session.generate_reply(**kwargs)

    if self.config.direct_say_fallback_enabled:
        # TRIAM_FIX_ROOT_CAUSE: Schedule second-level fallback only when explicitly enabled.
        asyncio.create_task(self._direct_say_fallback_after_force())
```

Thêm method:

```py
async def _direct_say_fallback_after_force(self) -> None:
    await asyncio.sleep(self.config.direct_say_delay_seconds)

    if not hasattr(self.session, "room") or not self.session.room.isconnected():
        return

    if not hasattr(self.session, "say"):
        log.info("Voice tool reply watchdog direct say fallback skipped: session.say is unavailable.")
        return

    try:
        # TRIAM_FIX_ROOT_CAUSE: Last-resort direct speech to avoid silent UX after tool completion.
        await self.session.say(
            self.config.direct_say_text,
            allow_interruptions=False,
        )
    except Exception as exc:
        self.tracer.record_error(AgentInputMode.VOICE, "tool_reply_watchdog_direct_say_error")
        log.warning(
            "Voice tool reply watchdog direct say fallback failed | "
            f"error_type={type(exc).__name__}"
        )
```

### 3.6 Kỳ vọng sau P1

Log khi tool xong mà Realtime không tự nói:

```text
watchdog_fired | no_speech_after_tool
Voice tool reply watchdog forcing generate_reply | tool_choice_none=True | allow_interruptions=False | has_instructions=True
speech_created trong 1-4s sau watchdog_fired
```

Nếu vẫn có case im lâu, bật:

```env
VOICE_AGENT_TOOL_REPLY_WATCHDOG_DIRECT_SAY_FALLBACK_ENABLED=true
```

và test lại. Nếu `session.say()` nói được ngay, audio pipeline ổn, lỗi nằm ở Realtime generate_reply lifecycle. Nếu `session.say()` cũng im, phải debug LiveKit session/audio output.

---

## 4. P2 — Sửa Watchdog không coi `thinking` là speech generation

### 4.1 Vấn đề

Trong `VoiceToolReplyWatchdog._extend_grace_for_thinking()` hiện có:

```py
self._speech_generation_counter += 1
generation_marker = self._speech_generation_counter
```

`thinking` không phải `speech_created` và cũng không phải `speaking`. Việc tăng `_speech_generation_counter` ở trạng thái `thinking` có thể làm các watcher khác hiểu nhầm là đã có generation mới.

### 4.2 Sửa code

File: `app/services/voice_agent/tool_reply_watchdog.py`

Đổi:

```py
def _extend_grace_for_thinking(self) -> None:
    active_event_ids = [eid for eid, task in self._watch_tasks.items() if not task.done()]
    if not active_event_ids:
        return

    self._speech_generation_counter += 1
    generation_marker = self._speech_generation_counter
```

thành:

```py
def _extend_grace_for_thinking(self) -> None:
    active_event_ids = [eid for eid, task in self._watch_tasks.items() if not task.done()]
    if not active_event_ids:
        return

    # TRIAM_FIX_ROOT_CAUSE: Do not count "thinking" as speech generation.
    # Only speech_created or agent_speaking should advance _speech_generation_counter.
    generation_marker = self._speech_generation_counter
```

Giữ nguyên phần schedule lại grace.

### 4.3 Kỳ vọng

Watchdog không bypass sai vì `thinking`.

`watchdog_fired` phản ánh đúng hơn việc tool xong nhưng chưa có speech.

---

## 5. P3 — Giữ dynamic transcription prompt nhưng bổ sung kiểm soát

### 5.1 Không rollback dynamic prompt

Dynamic prompt không phải nguyên nhân trực tiếp của lỗi tool xong im. Nó chỉ ảnh hưởng transcript.

Giữ:

```env
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED=true
```

### 5.2 Chỉ cần đảm bảo có rollback flag

Bạn đã có hoặc cần có:

```env
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED=false
```

để test A/B nếu cần.

### 5.3 Log không được in full prompt

Chỉ log:

```text
Realtime transcription prompt ready | dynamic=True | terms=45 | chars=768
```

Không log full prompt để tránh leak nội dung sách/session.

---

## 6. P4 — Test plan theo thứ tự ưu tiên

### 6.1 Test sau P0

Chạy console với cùng `thread_id` và `book_id` mock.

Test câu section cụ thể:

```text
Tóm tắt chương 1 của Of Mice and Men.
```

Kỳ vọng:

```text
grounding_route=book_section
grounding_reason_code=exact_section_path
retrieval_result_count=0 hoặc không cần RAG
assistant nói được
```

Test câu semantic:

```text
Mối quan hệ giữa George và Lennie là gì?
Candy trong truyện có vai trò gì?
Curley xuất hiện trong chương nào?
```

Kỳ vọng:

```text
Không còn grounding_route=clarification + retrieval_result_count=0 cho semantic query.
Phải fallback BOOK_RAG.
Nếu RAG found: BOOK_CONTEXT_FOUND.
Nếu RAG not found: mới ask_web_permission hoặc book_context_not_found.
```

### 6.2 Test sau P1/P2

Test web:

```text
Giá vàng SJC hôm nay ở Việt Nam là bao nhiêu?
```

Flow kỳ vọng:

```text
ask_web_search_permission
user: đồng ý
execute_web_search
web_search latency có giá trị
nếu Realtime tự nói: watchdog_cancelled reason=agent_speaking hoặc speech_created
nếu Realtime không tự nói: watchdog_fired rồi forced generate_reply có instructions
không còn im 20-30s
```

### 6.3 Metric cần xem

```text
tool_total
web_search
grounding_route
grounding_reason_code
retrieval_result_count
watchdog_scheduled
watchdog_fired
forced_reply_reason
speech_created elapsed_ms
turn_total
assistant_char_count
```

### 6.4 Tiêu chí pass

```text
- Semantic book question không bị clarification quá sớm.
- Web search không còn im quá 5-8s sau tool completion.
- Watchdog nếu fire thì phải tạo speech nhanh hơn trước.
- Section exact query vẫn hoạt động.
- Dynamic prompt vẫn log ready, không crash.
```

---

## 7. Thứ tự commit đề xuất

### Commit 1 — Grounding semantic fallback

Files:

```text
app/core/config.py
app/services/agent_grounding/semantic_query_detector.py
app/services/agent_grounding/grounding_router.py
```

Message:

```text
fix(voice): fallback semantic book questions to RAG when section resolution fails
```

### Commit 2 — Watchdog forced reply instructions

Files:

```text
app/core/config.py
app/services/voice_agent/tool_reply_watchdog.py
app/services/agent_voice_gpt_realtime.py
```

Message:

```text
fix(voice): strengthen post-tool watchdog forced reply
```

### Commit 3 — Watchdog thinking counter

Files:

```text
app/services/voice_agent/tool_reply_watchdog.py
```

Message:

```text
fix(voice): do not treat thinking as speech generation in watchdog
```

### Commit 4 — Tests/log polish

Files tùy test structure của bạn.

Message:

```text
test(voice): add grounding fallback and tool watchdog scenarios
```

---

## 8. Rollback plan

Nếu P0 gây route sai quá nhiều:

```env
AGENT_GROUNDING_RAG_ON_SECTION_NOT_FOUND=false
AGENT_GROUNDING_SEMANTIC_FALLBACK_ENABLED=false
```

Nếu P1 làm agent nói đè hoặc phản hồi kép:

```env
VOICE_AGENT_TOOL_REPLY_WATCHDOG_ALLOW_INTERRUPTION_ON_FORCE=true
VOICE_AGENT_TOOL_REPLY_WATCHDOG_DIRECT_SAY_FALLBACK_ENABLED=false
```

Nếu dynamic prompt nghi gây nhiễu:

```env
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED=false
```

---

## 9. Checklist cuối cùng trước khi test

```text
[ ] .env không còn lỗi parse python-dotenv.
[ ] VOICE_AGENT_QUERY_GUARD_ENFORCE_TRANSCRIPT_OVERLAP=false.
[ ] VOICE_AGENT_TOOL_REPLY_WATCHDOG_ENABLED=true.
[ ] AGENT_SHARED_POLICY_ENABLED=true.
[ ] AGENT_GROUNDING_ROUTER_ENABLED=true.
[ ] Dynamic transcription prompt log dynamic=True.
[ ] Semantic query fallback RAG có log reason_code mới.
[ ] Watchdog forced reply log has_instructions=True.
```


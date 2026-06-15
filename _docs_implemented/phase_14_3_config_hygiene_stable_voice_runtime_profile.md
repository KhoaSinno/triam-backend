# Phase 14.3 Implementation Guide - Config Hygiene And Stable Voice Runtime Profile

## 1. Mục tiêu

Phase 14.3 tập trung làm gọn cấu hình runtime sau các phase voice/RAG/learning đã ổn định.

Mục tiêu chính:

- Xóa hoặc deprecate các biến config không còn tác dụng.
- Làm rõ `VOICE_AGENT_CONSOLE_BOOK_ID` và `VOICE_AGENT_CONSOLE_THREAD_ID` là cấu hình local console test hợp lệ, không phải production metadata.
- Đồng bộ `.env.example` theo default trong `app/core/config.py`.
- Xem `app/core/config.py` là source of truth cho default runtime.
- Chốt một profile voice agent ổn định dưới dạng env overlay cho local, Hugging Face Free Space và production demo.
- Cho phép tắt dynamic transcription prompt bằng env overlay khi cần A/B test STT.
- Giữ rollback rõ ràng khi cần A/B test voice.
- Không đổi FE contract.
- Không đổi business logic học sách, plan, notification, RAG schema.

## 2. Vấn đề hiện tại

## 2.1 `config.py` đang phình theo nhiều phase

`app/core/config.py` hiện chứa quá nhiều nhóm cấu hình trong một class lớn:

- Database.
- Supabase.
- TTS.
- LiveKit.
- Realtime voice.
- Web permission.
- Query guard.
- Grounding router.
- Hybrid RAG.
- Celery.
- Pareto planner.
- Notification.
- Learning progress.

Điều này chưa gây lỗi ngay, nhưng làm dev khó biết biến nào còn dùng, biến nào là rollback cũ, biến nào chỉ phục vụ test.

## 2.2 Console IDs là local test config, không phải production config

Console mode đang cần hai biến:

```python
VOICE_AGENT_CONSOLE_BOOK_ID = "..."
VOICE_AGENT_CONSOLE_THREAD_ID = "..."
```

Đây không phải biến thừa. Khi chạy:

```powershell
uv run python -m app.services.agent_voice_gpt_realtime console
```

hai biến này giúp agent biết đang test với sách nào và thread nào. Nếu thiếu hai biến này, local console chỉ còn test được microphone/STT/realtime rất nông, không test được luồng quan trọng hơn là book-grounded RAG, lưu hội thoại và đồng bộ transcript.

Rủi ro thật sự không nằm ở việc hai biến này tồn tại, mà nằm ở việc không ghi rõ phạm vi:

- Dev đổi database nhưng vẫn dùng book/thread ID cũ, dẫn tới test sai dữ liệu hoặc ghi hội thoại vào thread không mong muốn.
- Người đọc code hiểu nhầm console fallback là cấu hình production.
- Production LiveKit room có thể bị vô tình phụ thuộc fallback console nếu metadata parsing không được test rõ.

Hướng xử lý:

- Không xóa hai biến khỏi `config.py`.
- Giữ theo baseline hiện tại trong `config.py` hoặc override bằng `.env` local khi muốn đổi book/thread test.
- Trong `.env.example`, ghi placeholder và chú thích rõ: chỉ dùng cho full local console voice test.
- Production LiveKit room phải lấy `thread_id` và `document_ids` từ metadata do backend cấp token truyền vào, không phụ thuộc hai biến console.

## 2.3 `.env.example` và `config.py` đang lệch default

Một số lệch đáng chú ý:

| Biến | `config.py` | `.env.example` | Vấn đề |
| --- | --- | --- | --- |
| `AGENT_GROUNDING_ROUTER_ENABLED` | `False` | `true` | Dễ deploy lệch hành vi nếu thiếu env |
| `AGENT_SECTION_CONTEXT_MAX_CHARS` | `16000` | `24000` | Khó benchmark latency/token |
| `TTS_GENERATION_CONCURRENCY` | `4` | `2` | Worker local và deploy chạy khác nhau |
| `VOICE_AGENT_TOOL_REPLY_WATCHDOG_THINKING_GRACE_SECONDS` | `4.0` | `6.0` | Khó giải thích vì sao watchdog khác |

Hướng xử lý:

- Ưu tiên `app/core/config.py` làm baseline vì đây là nơi code thật load default khi thiếu env.
- `.env.example` phải phản ánh đúng baseline trong `config.py`.
- Nếu có profile vận hành khác baseline, ví dụ profile Hugging Face ổn định hơn, ghi thành env overlay riêng trong doc; không để `.env.example` lệch âm thầm.
- Không copy ngược `.env.example` vào `config.py` khi chưa có lý do kỹ thuật rõ ràng và test A/B.

## 2.4 Dynamic transcription prompt có thể gây bias STT

`OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED=true` giúp STT biết trước tên sách, tác giả, mục lục, thuật ngữ.

Nhưng trong test thực tế:

- Khi user hỏi tự nhiên, STT vẫn có thể sai.
- Prompt động có thể kéo transcript về các từ trong sách dù người dùng nói khác.
- Nếu STT sai, downstream RAG/turn guard/web permission đều sai theo.

Recommendation Phase 14.3:

```env
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED=false
```

Đây là env overlay để A/B test hoặc chạy profile voice ít bias hơn, không phải default bắt buộc trong `config.py`.

Lý do:

- Ưu tiên transcript trung lập trước.
- Sau khi có benchmark rõ, mới quyết định giữ baseline `true` hay promote overlay `false` thành default.
- Không xóa tính năng để còn rollback nhanh.

## 2.5 Clarification state nên giữ nhưng giảm quyền

`VOICE_AGENT_CLARIFICATION_STATE_ENABLED=true` không trực tiếp ảnh hưởng STT.

Nó dùng để nhớ rằng agent vừa hỏi lại, ví dụ:

```text
Bạn muốn hỏi chương hoặc đề mục nào?
```

Sau đó nếu user nói:

```text
Có.
```

Agent có thể hiểu đây là câu xác nhận, không phải câu hỏi mới.

Vấn đề:

- Nếu TTL quá dài, câu trả lời ngắn vài lượt sau có thể bị dính trạng thái cũ.
- Nếu STT sai thành một câu xác nhận ngắn, agent có thể đi nhầm luồng.

Overlay recommendation khi cần test profile voice ít stale state hơn:

```env
VOICE_AGENT_CLARIFICATION_STATE_ENABLED=true
VOICE_AGENT_CLARIFICATION_STATE_TTL_SECONDS=15
VOICE_AGENT_ASSISTANT_CLARIFICATION_HEURISTIC_ENABLED=false
```

Giữ baseline trong `config.py` theo giá trị hiện tại nếu chưa có benchmark. Khi cần test, dùng env overlay TTL ngắn hơn để giảm stale turn.

## 2.6 Voice history limit hơi cao cho realtime

Hiện tại:

```env
VOICE_AGENT_HISTORY_LIMIT=24
```

Rủi ro:

- Context dài hơn, tăng token/latency.
- Các câu hỏi cũ dễ làm agent lẫn topic.
- Voice cần phản hồi nhanh hơn typed chat.

Overlay recommendation khi cần giảm latency voice:

```env
VOICE_AGENT_HISTORY_LIMIT=12
```

Trade-off:

- Agent nhớ ít hơn.
- Nhưng với book-grounded agent, kiến thức chính phải đến từ RAG, không phải hội thoại cũ.
- Không đổi baseline `VOICE_AGENT_HISTORY_LIMIT=24` trong `config.py` nếu chưa có benchmark chứng minh overlay tốt hơn.

## 2.7 LiveKit concurrency cần ưu tiên ổn định

Hugging Face Free Space đang co-host:

- FastAPI.
- Celery worker.
- Notification worker/Beat.
- LiveKit realtime voice agent.

Overlay recommendation cho Hugging Face Free Space nếu ưu tiên ổn định hơn concurrency:

```env
LIVEKIT_AGENT_JOB_EXECUTOR_TYPE=thread
LIVEKIT_AGENT_NUM_IDLE_PROCESSES=1
LIVEKIT_AGENT_MAX_CONCURRENT_JOBS=1
LIVEKIT_AGENT_LOAD_THRESHOLD=0.95
```

Giải thích:

- `thread` nhẹ hơn `process` trên runtime nhỏ.
- `MAX_CONCURRENT_JOBS=1` giúp demo ổn định hơn.
- Khi cần test 2 user voice cùng lúc mới tăng lên `2`.
- Baseline `config.py` có thể giữ `LIVEKIT_AGENT_MAX_CONCURRENT_JOBS=2`; overlay `1` chỉ dùng khi muốn giảm tranh tài nguyên.

## 3. Scope implement

## 3.1 Được làm

- Sửa `app/core/config.py`.
- Sửa `.env.example`.
- Sửa comment config cho rõ mục đích.
- Xóa biến config thật sự không được dùng.
- Xóa biến config bị duplicate hoặc gây hiểu nhầm về runtime behavior.
- Cập nhật test liên quan config/voice.
- Thêm test đảm bảo console IDs vẫn là config có thể override cho local console full test.
- Thêm test đảm bảo production metadata path không phụ thuộc console fallback.
- Thêm test đảm bảo `.env.example` không còn biến dead.
- Cập nhật doc vận hành local/deploy nếu cần.

## 3.2 Không làm trong Phase 14.3

- Không refactor toàn bộ `Settings` thành nhiều class nhỏ.
- Không đổi DB schema.
- Không đổi API contract cho FE.
- Không đổi RAG scoring.
- Không đổi prompt trả lời chính của agent ngoài cấu hình bật/tắt dynamic transcription prompt.
- Không xóa dynamic transcription prompt builder.
- Không xóa clarification state.

Lý do:

- Phase này là hygiene và ổn định runtime, không phải phase tối ưu RAG/DB lớn.

## 4. Stable voice runtime profile đề xuất

Các profile trong mục này là env overlay khi chạy local/deploy, không phải toàn bộ default bắt buộc phải ghi cứng vào `config.py`.

Nguyên tắc:

- `config.py` giữ baseline chuẩn của code.
- `.env.example` mirror baseline trong `config.py`.
- Khi muốn test profile ổn định hơn, set các biến override trong `.env` local hoặc platform secrets.

## 4.1 Profile local dev

```env
ENABLE_VOICE_AGENT=true
LIVEKIT_AGENT_JOB_EXECUTOR_TYPE=thread
LIVEKIT_AGENT_MAX_CONCURRENT_JOBS=1
VOICE_AGENT_HISTORY_LIMIT=12
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED=false
VOICE_AGENT_CLARIFICATION_STATE_ENABLED=true
VOICE_AGENT_CLARIFICATION_STATE_TTL_SECONDS=15
VOICE_AGENT_ASSISTANT_CLARIFICATION_HEURISTIC_ENABLED=false
AGENT_GROUNDING_ROUTER_ENABLED=true
AGENT_SHARED_POLICY_ENABLED=true
AGENT_HYBRID_RAG_ENABLED=true
AGENT_TRACE_ENABLED=true
VOICE_AGENT_LOG_TRANSCRIPT_TEXT=false

# Required for full local console voice test only.
# Use IDs that exist in the current local/dev database.
VOICE_AGENT_CONSOLE_BOOK_ID=<local-test-book-id>
VOICE_AGENT_CONSOLE_THREAD_ID=<local-test-thread-id>
```

## 4.2 Profile Hugging Face Free Space

```env
ENABLE_VOICE_AGENT=true
LIVEKIT_AGENT_JOB_EXECUTOR_TYPE=thread
LIVEKIT_AGENT_NUM_IDLE_PROCESSES=1
LIVEKIT_AGENT_MAX_CONCURRENT_JOBS=1
CELERY_DOCUMENT_CONCURRENCY=1
CELERY_NOTIFICATION_CONCURRENCY=1
TTS_GENERATION_CONCURRENCY=2
LEARNING_UNIT_PROCESSING_CONCURRENCY=2
LLM_NORMALIZE_CONCURRENCY=1
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED=false
VOICE_AGENT_HISTORY_LIMIT=12
VOICE_AGENT_CLARIFICATION_STATE_TTL_SECONDS=15
```

## 4.3 Profile voice A/B test

Dùng khi muốn đo dynamic prompt có thật sự cải thiện STT hay không.

```env
AGENT_MODEL_PROFILE=voice-dynamic-transcription-on
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED=true
OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_CHARS=900
OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_TERMS=45
OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_SECTION_TERMS=20
```

Khi test xong, so sánh:

- Transcript có đúng hơn không.
- Query guard có block ít hơn không.
- Agent có chọn đúng book/section hơn không.
- Latency tăng bao nhiêu.
- Có xuất hiện hallucination theo tên đề mục không.

## 5. Code changes chi tiết

## 5.1 Clean `app/core/config.py`

### 5.1.1 Console IDs

Giữ:

```python
VOICE_AGENT_CONSOLE_BOOK_ID: str = "..."
VOICE_AGENT_CONSOLE_THREAD_ID: str = "..."
```

Quy ước:

- Đây là fallback chỉ dành cho `uv run python -m app.services.agent_voice_gpt_realtime console`.
- Full local console voice test phải có cả `VOICE_AGENT_CONSOLE_BOOK_ID` và `VOICE_AGENT_CONSOLE_THREAD_ID`.
- Nếu dev đổi DB local/dev, phải đổi hai ID này theo dữ liệu hiện tại.
- Production room không được dùng hai biến này; production phải nhận `thread_id` và `document_ids` từ LiveKit metadata.
- Không log raw metadata, transcript, token hoặc nội dung sách khi validate hai biến này.

### 5.1.2 Remove dead config

Xóa các biến không có runtime usage sau khi đã verify bằng `rg`.

Nhóm clarification cũ:

```python
VOICE_AGENT_CLARIFICATION_LLM_FALLBACK_ENABLED: bool = False
VOICE_AGENT_CLARIFICATION_CLASSIFIER_TIMEOUT_SECONDS: float = 1.2
```

Nhóm embedding/reminder cũ:

```python
EMBEDDING_BATCH_SIZE: int = 64
BOOK_SECTION_EMBEDDING_DIMENSION: int = 1536
PLAN_REMINDER_STUDIED_TODAY_WINDOW_HOURS: int = 24
```

Lý do:

- `EMBEDDING_BATCH_SIZE` bị trùng ý nghĩa với `BOOK_SECTION_EMBEDDING_BATCH_SIZE`; runtime indexing đang dùng biến chuyên biệt.
- `BOOK_SECTION_EMBEDDING_DIMENSION` không được dùng ở runtime. Dimension hiện đã được cố định tại schema vector và model embedding.
- `PLAN_REMINDER_STUDIED_TODAY_WINDOW_HOURS` không còn nằm trong logic reminder mới; calendar/session/reminder hiện dựa trên session schedule và local date.
- Hai biến clarification LLM/classifier timeout không được gọi trong query guard hiện tại.

Trước khi xóa phải chạy:

```powershell
rg -n "VOICE_AGENT_CLARIFICATION_LLM_FALLBACK_ENABLED|VOICE_AGENT_CLARIFICATION_CLASSIFIER_TIMEOUT_SECONDS|EMBEDDING_BATCH_SIZE|BOOK_SECTION_EMBEDDING_DIMENSION|PLAN_REMINDER_STUDIED_TODAY_WINDOW_HOURS" app tests scripts .env.example pyproject.toml
```

Expected sau khi xóa:

```text
No matches
```

Không xóa:

```python
BOOK_SECTION_EMBEDDING_BATCH_SIZE: int = 64
```

Vì `book_section_knowledge_indexer` đang dùng biến này để batch embedding.

### 5.1.3 Preserve `config.py` as baseline defaults

Phase 14.3 không nên đổi hàng loạt runtime defaults trong `config.py` chỉ vì `.env.example` đang lệch.

Baseline hiện tại nên giữ theo `config.py`, ngoại trừ các thay đổi cleanup đã được nêu rõ:

- Ghi rõ phạm vi của console IDs là local console full test.
- Xóa dead config không còn runtime usage.
- Sửa comment/grouping để dễ đọc hơn.

Các default baseline cần `.env.example` mirror theo `config.py`:

```python
VOICE_AGENT_HISTORY_LIMIT: int = 24
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED: bool = True
VOICE_AGENT_CLARIFICATION_STATE_TTL_SECONDS: float = 30.0
AGENT_GROUNDING_ROUTER_ENABLED: bool = False
AGENT_SECTION_CONTEXT_MAX_CHARS: int = 16000
VOICE_AGENT_TOOL_REPLY_WATCHDOG_THINKING_GRACE_SECONDS: float = 4.0
LIVEKIT_AGENT_MAX_CONCURRENT_JOBS: int = 2
TTS_GENERATION_CONCURRENCY: int = 4
```

Ghi chú:

- `config.py` mới là source of truth.
- Stable voice profile ở mục 4 là env overlay để test/deploy, không phải thay đổi default code bắt buộc.
- Nếu sau A/B test chứng minh profile ổn định hơn, lúc đó mới promote một số overlay thành default trong `config.py`.

## 5.2 Update `.env.example`

Thêm local console block:

```env
# Required for full local console voice test only.
# Do not use these values for production LiveKit rooms.
VOICE_AGENT_CONSOLE_BOOK_ID=<local-test-book-id>
VOICE_AGENT_CONSOLE_THREAD_ID=<local-test-thread-id>
```

Xóa khỏi `.env.example`:

```env
VOICE_AGENT_CLARIFICATION_LLM_FALLBACK_ENABLED=false
VOICE_AGENT_CLARIFICATION_CLASSIFIER_TIMEOUT_SECONDS=1.2
EMBEDDING_BATCH_SIZE=64
BOOK_SECTION_EMBEDDING_DIMENSION=1536
PLAN_REMINDER_STUDIED_TODAY_WINDOW_HOURS=24
```

Đồng bộ `.env.example` theo baseline trong `config.py`:

```env
LIVEKIT_AGENT_MAX_CONCURRENT_JOBS=2
VOICE_AGENT_HISTORY_LIMIT=24
VOICE_AGENT_CLARIFICATION_STATE_TTL_SECONDS=30
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED=true
AGENT_GROUNDING_ROUTER_ENABLED=false
AGENT_SECTION_CONTEXT_MAX_CHARS=16000
VOICE_AGENT_TOOL_REPLY_WATCHDOG_THINKING_GRACE_SECONDS=4.0
TTS_GENERATION_CONCURRENCY=4
```

Nếu muốn chạy profile ổn định hơn trên Hugging Face Free Space, override các biến đó bằng platform secrets theo mục 4.2 thay vì làm `.env.example` lệch baseline.

## 5.3 Update console metadata behavior

File:

```text
app/services/agent_voice_gpt_realtime.py
```

Hiện tại console mode fallback lấy từ config. Cách này đúng cho local test, miễn là phạm vi được tách rõ:

- Console mode cần `VOICE_AGENT_CONSOLE_BOOK_ID` và `VOICE_AGENT_CONSOLE_THREAD_ID` để test full voice/RAG/persistence.
- Nếu thiếu hai biến này, chỉ xem đó là limited console run để test microphone/STT/realtime thô, không phải full successful smoke test.
- Non-console mode vẫn phải thoát sớm nếu thiếu `document_ids`, vì production LiveKit room cần metadata từ BE.
- Production room không được tự fallback sang `VOICE_AGENT_CONSOLE_BOOK_ID`.
- Nên log warning ngắn gọn để dev biết đang chạy limited mode.

Ví dụ behavior mong muốn:

```text
Voice console started without VOICE_AGENT_CONSOLE_BOOK_ID; this is a limited STT-only run.
```

Không log raw token, metadata đầy đủ, transcript hay nội dung sách.

Pseudo implementation:

```python
if not document_ids:
    if ctx.room.name == "console":
        log.warning(
            "Voice console started without VOICE_AGENT_CONSOLE_BOOK_ID; "
            "limited STT-only run; full local console test requires a book ID."
        )
    else:
        log.info("No document_ids found in LiveKit metadata; closing voice job.")
        return

if not thread_id and ctx.room.name == "console":
    log.warning(
        "Voice console started without VOICE_AGENT_CONSOLE_THREAD_ID; "
        "chat persistence disabled; full local console test requires a thread ID."
    )
```

`load_grounding_scope([])` hiện an toàn: repository trả về `GroundingScope((), (), ())` khi danh sách book rỗng. Vì vậy limited console run không cần crash, nhưng không được dùng kết quả limited run để kết luận chất lượng RAG/grounding.

Acceptance criteria:

- `uv run python -m app.services.agent_voice_gpt_realtime console` với hai biến console hợp lệ chạy được full local smoke test.
- Console full test dùng đúng book/thread trong current local/dev DB.
- Nếu thiếu book/thread ID, log phải nói rõ đây là limited STT-only run, không phải full smoke test.
- Production room thiếu `document_ids` vẫn bị reject sớm.
- Production room không fallback sang `VOICE_AGENT_CONSOLE_BOOK_ID`.

## 6. Test plan

## 6.1 Static checks

```powershell
uv run ruff check app/core/config.py app/services/agent_voice_gpt_realtime.py app/services/voice_agent
uv run python -m py_compile app/core/config.py app/services/agent_voice_gpt_realtime.py
```

## 6.2 Unit tests

Chạy voice-focused tests:

```powershell
uv run pytest tests/services/voice_agent tests/test_agent_voice_realtime.py tests/test_agent_chat_text_only.py -q
```

Nếu test file nào hiện đã đổi tên sau cleanup, chạy nhóm còn tồn tại:

```powershell
uv run pytest tests/services/voice_agent -q
```

## 6.3 Config regression tests nên thêm

Tạo test nhỏ, ví dụ:

```text
tests/test_config_runtime_profile.py
```

Các case:

- `VOICE_AGENT_CONSOLE_BOOK_ID` và `VOICE_AGENT_CONSOLE_THREAD_ID` là settings hợp lệ, có thể override cho local console full test.
- `.env.example` không chứa UUID thật cho console IDs, chỉ chứa placeholder.
- Production metadata path không phụ thuộc console fallback.
- Dead clarification config không còn trong `Settings`.
- Dead embedding/reminder config không còn trong `Settings`.
- Default stable profile khớp `.env.example` cho các biến quan trọng.

Lưu ý quan trọng:

`Settings(_env_file=None)` vẫn cần các field required như `OPENAI_API_KEY`, `DATABASE_URL`, `SUPABASE_URL`, `LIVEKIT_API_KEY`. Vì vậy test không nên instantiate trống nếu CI không có env đầy đủ.

Pseudo helper:

```python
from app.core.config import Settings


REQUIRED_SETTINGS = {
    "OPENAI_API_KEY": "test",
    "TAVILY_API_KEY": "test",
    "GEMINI_BASE_URL": "https://example.test",
    "GEMINI_API_KEY": "test",
    "DATABASE_URL": "sqlite:///test.db",
    "SUPABASE_URL": "https://example.supabase.co",
    "SUPABASE_KEY": "test",
    "SUPABASE_SERVICE_ROLE_KEY": "test",
    "LIVEKIT_API_KEY": "test",
    "LIVEKIT_API_SECRET": "test",
    "LIVEKIT_AGENT_NAME": "triam-test-agent",
}


def build_clean_settings(**overrides):
    return Settings(_env_file=None, **REQUIRED_SETTINGS, **overrides)


def test_voice_console_ids_are_configurable_for_local_full_test():
    clean_settings = build_clean_settings(
        VOICE_AGENT_CONSOLE_BOOK_ID="195d9623-03d0-483a-ac09-52d9137f2471",
        VOICE_AGENT_CONSOLE_THREAD_ID="07be00b9-c6da-4801-8ba2-7558205b92b2",
    )

    assert clean_settings.VOICE_AGENT_CONSOLE_BOOK_ID
    assert clean_settings.VOICE_AGENT_CONSOLE_THREAD_ID
```

Dead config test:

```python
def test_dead_configs_are_removed():
    clean_settings = build_clean_settings()

    assert not hasattr(clean_settings, "VOICE_AGENT_CLARIFICATION_LLM_FALLBACK_ENABLED")
    assert not hasattr(clean_settings, "VOICE_AGENT_CLARIFICATION_CLASSIFIER_TIMEOUT_SECONDS")
    assert not hasattr(clean_settings, "EMBEDDING_BATCH_SIZE")
    assert not hasattr(clean_settings, "BOOK_SECTION_EMBEDDING_DIMENSION")
    assert not hasattr(clean_settings, "PLAN_REMINDER_STUDIED_TODAY_WINDOW_HOURS")
```

Nếu test settings bị ảnh hưởng bởi `.env` local, luôn dùng `_env_file=None` và truyền required settings bằng helper ở trên.

Không thêm test bắt buộc console IDs default phải rỗng. Với dự án này, console full test cần hai ID hợp lệ; điều cần bảo vệ là production metadata path không dùng fallback console.

## 6.4 Manual voice A/B test

Chạy profile stable:

```powershell
make t5c
```

Hoặc:

```powershell
uv run python -m app.services.agent_voice_gpt_realtime console
```

Trước khi chạy console full test, kiểm tra:

```env
VOICE_AGENT_CONSOLE_BOOK_ID=<book-id tồn tại trong DB local/dev>
VOICE_AGENT_CONSOLE_THREAD_ID=<thread-id tồn tại trong DB local/dev>
```

Nếu thiếu hai biến này, chỉ được xem là limited STT/realtime test; không dùng để đánh giá RAG, grounding, transcript persistence hoặc chất lượng trả lời theo sách.

Test tối thiểu:

```text
1. Hỏi metadata: "Tác giả của sách là ai?"
2. Hỏi section rõ: "Tóm tắt chương 4."
3. Hỏi câu ngắn dễ nhầm: "Có."
4. Hỏi câu mới sau clarification: "Các nhân vật chính nào trong sách này?"
5. Hỏi web permission: "Tìm trên internet đi."
```

Ghi nhận:

- final transcript;
- tool flow;
- query guard reason;
- source selected;
- answer source;
- latency;
- DB message count delta.

Không paste access token hoặc raw secret vào log/report.

## 6.5 Deploy smoke

Sau deploy:

```text
FastAPI startup complete.
Celery connected and ready if enabled.
LiveKit worker registered.
No runtime dependency downloads.
No visible bearer token/api key in traceback.
```

Voice logs expected:

```text
Realtime transcription prompt ready | dynamic=<matches env> | ...
Voice agent config | profile=baseline | ...
registered worker
```

## 7. Rollback plan

Nếu voice trở nên kém hơn sau Phase 14.3:

### 7.1 Bật lại dynamic transcription prompt nếu đang dùng stable overlay

```env
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED=true
AGENT_MODEL_PROFILE=voice-dynamic-transcription-on
```

### 7.2 Tăng history limit

```env
VOICE_AGENT_HISTORY_LIMIT=24
```

### 7.3 Tăng concurrency cho dedicated runtime

Chỉ làm khi API/Celery/Voice không còn co-host trên một HF Free Space:

```env
LIVEKIT_AGENT_MAX_CONCURRENT_JOBS=2
```

### 7.4 Tắt clarification state để test

```env
VOICE_AGENT_CLARIFICATION_STATE_ENABLED=false
```

Lưu ý:

- Tắt clarification state làm voice ít hiểu các câu trả lời ngắn sau khi agent hỏi lại.
- Đây là rollback/debug, không phải recommendation mặc định.

## 8. Trade-off

## 8.1 Tắt dynamic prompt

Ưu điểm:

- STT trung lập hơn.
- Ít bị kéo nhầm theo tên sách/đề mục.
- Dễ debug hơn khi transcript sai.

Đánh đổi:

- Một số thuật ngữ sách/tên riêng có thể được nhận diện kém hơn.
- Cần benchmark lại nếu sách có nhiều thuật ngữ tiếng Anh/viết tắt.

## 8.2 Giảm history limit

Ưu điểm:

- Giảm token và latency.
- Giảm nhiễu topic cũ.
- Voice agent phản hồi gọn hơn.

Đánh đổi:

- Agent nhớ ít hơn về các lượt chat trước.
- Cần rely vào RAG/book context nhiều hơn.

## 8.3 Giảm LiveKit concurrent jobs

Ưu điểm:

- Ổn định hơn trên Hugging Face Free.
- Ít tranh CPU với FastAPI/Celery.

Đánh đổi:

- Chỉ phục vụ tốt một room voice realtime tại một thời điểm trên cùng runtime.
- Muốn nhiều người dùng realtime cần tách runtime hoặc nâng tài nguyên.

## 8.4 Giữ clarification state nhưng TTL ngắn

Ưu điểm:

- Vẫn hỗ trợ voice tự nhiên.
- Giảm stale state.

Đánh đổi:

- Nếu user phản hồi quá chậm sau câu hỏi làm rõ, agent có thể coi là câu hỏi mới.

## 9. Definition of Done

Phase 14.3 hoàn thành khi:

- `VOICE_AGENT_CONSOLE_BOOK_ID` và `VOICE_AGENT_CONSOLE_THREAD_ID` được giữ và document rõ là local console full-test config.
- `.env.example` khớp baseline default trong `config.py`.
- Dead config đã được xóa hoặc được chứng minh là còn dùng.
- Console full test chạy được khi có book/thread ID hợp lệ trong local/dev DB.
- Limited console run thiếu book/thread ID có warning rõ ràng và không được xem là RAG smoke test thành công.
- Non-console room thiếu `document_ids` vẫn bị reject sớm.
- Production room không phụ thuộc console fallback IDs.
- Voice stable profile được document rõ.
- Focused voice/config tests pass.
- Ruff/py_compile pass.
- Manual voice smoke cho thấy transcript/tool flow dễ đọc hơn, không phát sinh loop xác nhận bất thường.
- Không có thay đổi API FE.

## 10. Phase tiếp theo sau 14.3

Sau Phase 14.3, nên làm:

```text
Phase 14.4 - Read Path DB Optimization
```

Mục tiêu Phase 14.4:

- Tối ưu `GET /api/v1/books` tránh N+1 query.
- Tách read-only learning summary khỏi sync/write summary.
- Đổi review count sang SQL `COUNT(*)`.
- Thêm composite indexes cho notification, review, progress, session list.
- Benchmark endpoint latency trước và sau.

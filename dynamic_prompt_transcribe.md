# Hướng dẫn implement Dynamic Transcription Prompt cho TRIAM Voice Agent

## 1. Mục tiêu

Mục tiêu của thay đổi này là cải thiện chất lượng transcript tiếng Việt trong Realtime Voice Agent mà không hard-code từng lỗi STT như `SCC -> SJC` hoặc `Cỏ -> Có`.

Hiện tại hệ thống đã dùng:

```py
input_audio_transcription=AudioTranscription(
    model=settings.OPENAI_REALTIME_TRANSCRIPTION_MODEL,
    language=settings.OPENAI_REALTIME_TRANSCRIPTION_LANGUAGE,
    prompt=settings.OPENAI_REALTIME_TRANSCRIPTION_PROMPT,
)
```

Vấn đề là `OPENAI_REALTIME_TRANSCRIPTION_PROMPT` đang là prompt tĩnh. Nó chỉ chứa một số term chung như `Tri Âm`, `chương`, `sách`, `GPT`, `Gemini`, nhưng không có term cụ thể theo từng phiên học như:

```text
Of Mice and Men
John Steinbeck
George
Lennie
Candy
Curley
Curley's wife
Chapter 1
Chapter 2
giá vàng SJC
tìm trên internet
```

Dynamic prompt sẽ lấy dữ liệu từ session hiện tại, đặc biệt là `grounding_scope`, để build prompt giàu ngữ cảnh hơn cho `gpt-4o-transcribe`.

## 2. Nguyên tắc thiết kế

Không hard-code từng lỗi STT.

Không gọi thêm LLM để sửa transcript ở mọi turn.

Không thay đổi DataChannel hiện có.

Không làm tăng latency runtime theo từng turn, vì prompt được build một lần khi agent session start.

Không đưa nội dung sách quá dài vào prompt. Chỉ đưa metadata và vocabulary ngắn: title, author, section title, section path, app commands, domain terms.

Không log toàn bộ prompt nếu có thể chứa dữ liệu sách/user. Chỉ log số lượng term và độ dài prompt.

## 3. File cần chỉnh

Các file nên thêm/chỉnh:

```text
app/core/config.py
app/services/voice_agent/transcription_prompt.py
app/services/agent_voice_gpt_realtime.py
```

Không cần sửa frontend.

Không cần sửa database.

Không cần đổi model.

## 4. Thêm config mới trong `app/core/config.py`

Tìm đoạn config hiện có:

```py
OPENAI_REALTIME_TRANSCRIPTION_MODEL: str = "gpt-4o-transcribe"
OPENAI_REALTIME_TRANSCRIPTION_LANGUAGE: str = "vi"
OPENAI_REALTIME_TRANSCRIPTION_PROMPT: str = "Vietnamese audio in the TRIAM audiobook study app. Expect terms: Tri Âm, chương, sách, định lý, phương pháp, GPT, Gemini."
```

Thêm các biến mới ngay bên dưới:

```py
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED: bool = True
OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_CHARS: int = 1800
OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_TERMS: int = 80
OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_SECTION_TERMS: int = 40
OPENAI_REALTIME_INPUT_AUDIO_NOISE_REDUCTION: str = "near_field"
```

Ý nghĩa:

```text
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED
→ bật/tắt dynamic prompt.

OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_CHARS
→ giới hạn prompt cuối cùng để tránh quá dài.

OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_TERMS
→ giới hạn tổng số terms đưa vào prompt.

OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_SECTION_TERMS
→ giới hạn số section/path lấy từ sách.

OPENAI_REALTIME_INPUT_AUDIO_NOISE_REDUCTION
→ đưa "near_field" ra config thay vì hard-code trong RealtimeModel.
```

Gợi ý `.env`:

```env
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED=true
OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_CHARS=1800
OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_TERMS=80
OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_SECTION_TERMS=40
OPENAI_REALTIME_INPUT_AUDIO_NOISE_REDUCTION=near_field
```

Lưu ý quan trọng: không viết khoảng trắng quanh dấu `=` trong `.env`.

Đúng:

```env
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED=true
```

Không nên:

```env
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED = true
```

## 5. Tạo file mới `app/services/voice_agent/transcription_prompt.py`

Tạo file:

```text
app/services/voice_agent/transcription_prompt.py
```

Nội dung đề xuất:

```py
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from app.services.agent_grounding.contracts import GroundingScope


_WHITESPACE_RE = re.compile(r"\s+")
_SECTION_NUMBER_RE = re.compile(r"^\s*(chapter|chương|part|phần|section|mục)\s+\d+", re.IGNORECASE)


@dataclass(frozen=True)
class TranscriptionPromptBuildResult:
    prompt: str
    term_count: int
    prompt_chars: int
    dynamic_enabled: bool


def _normalize_term(value: object) -> str:
    text = str(value or "").strip()
    text = _WHITESPACE_RE.sub(" ", text)
    text = text.strip(" -–—|,.;:")
    return text


def _add_unique(terms: list[str], seen: set[str], value: object, *, max_len: int = 80) -> None:
    term = _normalize_term(value)
    if not term:
        return

    if len(term) > max_len:
        term = term[:max_len].rstrip()

    key = term.casefold()
    if key in seen:
        return

    seen.add(key)
    terms.append(term)


def _split_path_terms(path: str | None) -> list[str]:
    if not path:
        return []

    raw = _normalize_term(path)
    if not raw:
        return []

    parts = re.split(r"\s*(?:>|/|\\|»|›)\s*", raw)
    result: list[str] = []

    for part in parts:
        part = _normalize_term(part)
        if part:
            result.append(part)

    if raw and raw not in result:
        result.append(raw)

    return result


def _base_domain_terms() -> tuple[str, ...]:
    return (
        "Tri Âm",
        "TRIAM",
        "chương",
        "sách",
        "tóm tắt",
        "nội dung chính",
        "nhân vật",
        "tác giả",
        "mục lục",
        "bài học",
        "đề mục",
        "định lý",
        "phương pháp",
        "khái niệm",
        "ví dụ",
        "giải thích",
        "so sánh",
        "tìm web",
        "tìm trên internet",
        "tra cứu web",
        "đồng ý",
        "không đồng ý",
        "có",
        "không",
        "tiếp tục",
        "dừng lại",
        "GPT",
        "Gemini",
        "OpenAI",
        "RAG",
    )


def build_realtime_transcription_prompt(
    *,
    base_prompt: str,
    grounding_scope: GroundingScope | None,
    enabled: bool,
    max_chars: int,
    max_terms: int,
    max_section_terms: int,
    extra_terms: Iterable[str] | None = None,
) -> TranscriptionPromptBuildResult:
    base = _normalize_term(base_prompt)

    if not enabled:
        return TranscriptionPromptBuildResult(
            prompt=base,
            term_count=0,
            prompt_chars=len(base),
            dynamic_enabled=False,
        )

    terms: list[str] = []
    seen: set[str] = set()

    for term in _base_domain_terms():
        _add_unique(terms, seen, term)

    if extra_terms:
        for term in extra_terms:
            _add_unique(terms, seen, term)

    if grounding_scope is not None:
        for book in grounding_scope.books:
            _add_unique(terms, seen, book.title)
            _add_unique(terms, seen, book.author)
            if book.document_type:
                _add_unique(terms, seen, str(book.document_type))

        section_added = 0
        for section in grounding_scope.sections:
            if section_added >= max_section_terms:
                break

            title = _normalize_term(section.title)
            path = _normalize_term(section.path)

            if title:
                _add_unique(terms, seen, title)
                section_added += 1

            for path_term in _split_path_terms(path):
                if section_added >= max_section_terms:
                    break
                _add_unique(terms, seen, path_term)
                section_added += 1

    terms = terms[: max(0, max_terms)]

    dynamic_suffix = ""
    if terms:
        dynamic_suffix = (
            " Session-specific expected terms: "
            + ", ".join(terms)
            + "."
        )

    prompt = (
        base
        + " The user may mix Vietnamese with English book titles, author names, character names, AI terms, and short app commands."
        + " Prefer the exact expected terms when acoustically plausible; do not force them when the audio clearly says something else."
        + dynamic_suffix
    ).strip()

    if max_chars > 0 and len(prompt) > max_chars:
        prompt = prompt[:max_chars].rstrip()
        if not prompt.endswith("."):
            prompt += "."

    return TranscriptionPromptBuildResult(
        prompt=prompt,
        term_count=len(terms),
        prompt_chars=len(prompt),
        dynamic_enabled=True,
    )
```

## 6. Vì sao thiết kế này không hard-code

File này không sửa lỗi kiểu:

```py
text = text.replace("SCC", "SJC")
```

Nó chỉ cung cấp vocabulary có xác suất xuất hiện trong phiên hiện tại. Ví dụ nếu sách hiện tại là `Of Mice and Men`, prompt sẽ có:

```text
Of Mice and Men, John Steinbeck, Chapter 1, Chapter 2, George, Lennie...
```

Nếu phiên khác là sách khác, prompt tự đổi theo `grounding_scope`.

## 7. Sửa `app/services/agent_voice_gpt_realtime.py`

### 7.1 Thêm import

Ở đầu file, thêm:

```py
from app.services.voice_agent.transcription_prompt import build_realtime_transcription_prompt
```

File hiện đã import nhiều module voice agent như `query_guard`, `rag_context`, `tool_reply_watchdog`, `transcript_store`, `turn_state`, `web_permission_policy`, nên import mới này đặt cùng nhóm đó là hợp lý.

### 7.2 Build prompt sau khi load `grounding_scope`

Trong `entrypoint`, hiện flow đang là:

```py
grounding_router: GroundingRouter | None = None
if settings.AGENT_GROUNDING_ROUTER_ENABLED:
    try:
        grounding_started = time.perf_counter()
        grounding_scope = await asyncio.to_thread(load_grounding_scope, document_ids)

        async def _load_section_texts(...):
            ...

        grounding_router = GroundingRouter(...)
        log.info(...)
    except Exception:
        ...
```

Vấn đề: `grounding_scope` đang được tạo trong block `try`, nhưng bạn cần dùng nó lúc tạo `RealtimeModel`.

Hãy khai báo `grounding_scope` trước block:

```py
grounding_scope = None
grounding_router: GroundingRouter | None = None
```

Sau đó giữ logic load cũ.

Ví dụ:

```py
grounding_scope = None
grounding_router: GroundingRouter | None = None

if settings.AGENT_GROUNDING_ROUTER_ENABLED:
    try:
        grounding_started = time.perf_counter()
        grounding_scope = await asyncio.to_thread(load_grounding_scope, document_ids)

        async def _load_section_texts(book_id: uuid.UUID, section_ids: tuple[uuid.UUID, ...]):
            return await asyncio.to_thread(
                load_scoped_section_texts,
                book_id,
                section_ids,
                grounding_scope.allowed_book_ids,
            )

        grounding_router = GroundingRouter(
            grounding_scope,
            _load_section_texts,
            section_context_max_chars=settings.AGENT_SECTION_CONTEXT_MAX_CHARS,
        )
        log.info(
            "Grounding router ready | "
            f"books={len(grounding_scope.books)} | sections={len(grounding_scope.sections)} | "
            f"load_ms={int((time.perf_counter() - grounding_started) * 1000)}"
        )
    except Exception:
        log.exception("Failed to initialize grounding router")
        grounding_scope = None
        grounding_router = None
```

### 7.3 Build transcription prompt trước vòng start model

Trước đoạn:

```py
for model_name in model_candidates:
    try:
        log.info(f"Starting realtime session with model: {model_name}, voice: {settings.OPENAI_REALTIME_VOICE}")
        model = RealtimeModel(...)
```

thêm:

```py
transcription_prompt_result = build_realtime_transcription_prompt(
    base_prompt=settings.OPENAI_REALTIME_TRANSCRIPTION_PROMPT,
    grounding_scope=grounding_scope,
    enabled=settings.OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED,
    max_chars=settings.OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_CHARS,
    max_terms=settings.OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_TERMS,
    max_section_terms=settings.OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_SECTION_TERMS,
)

log.info(
    "Realtime transcription prompt ready | "
    f"dynamic={transcription_prompt_result.dynamic_enabled} | "
    f"terms={transcription_prompt_result.term_count} | "
    f"chars={transcription_prompt_result.prompt_chars}"
)
```

Không log toàn bộ prompt.

### 7.4 Thay prompt static trong `RealtimeModel`

Đoạn cũ:

```py
model = RealtimeModel(
    model=model_name,
    voice=settings.OPENAI_REALTIME_VOICE,
    modalities=["audio"],
    input_audio_transcription=AudioTranscription(
        model=settings.OPENAI_REALTIME_TRANSCRIPTION_MODEL,
        language=settings.OPENAI_REALTIME_TRANSCRIPTION_LANGUAGE,
        prompt=settings.OPENAI_REALTIME_TRANSCRIPTION_PROMPT,
    ),
    input_audio_noise_reduction="near_field",
)
```

Đổi thành:

```py
model = RealtimeModel(
    model=model_name,
    voice=settings.OPENAI_REALTIME_VOICE,
    modalities=["audio"],
    input_audio_transcription=AudioTranscription(
        model=settings.OPENAI_REALTIME_TRANSCRIPTION_MODEL,
        language=settings.OPENAI_REALTIME_TRANSCRIPTION_LANGUAGE,
        prompt=transcription_prompt_result.prompt,
    ),
    input_audio_noise_reduction=settings.OPENAI_REALTIME_INPUT_AUDIO_NOISE_REDUCTION,
)
```

## 8. Cập nhật base prompt trong `.env`

Base prompt nên rộng hơn một chút, nhưng vẫn không quá dài.

Gợi ý:

```env
OPENAI_REALTIME_TRANSCRIPTION_PROMPT="Vietnamese audio in the TRIAM audiobook study app. The user may ask about books, chapters, authors, characters, learning concepts, and web lookup permission. Expect Vietnamese mixed with English names and technical terms."
```

Không nên đưa toàn bộ glossary vào `.env`. Glossary sẽ được build động từ DB/session.

## 9. Kiểm thử nhanh bằng console

Chạy:

```bash
uv run python -m app.services.agent_voice_gpt_realtime console
```

Khi start, log kỳ vọng:

```text
Grounding router ready | books=1 | sections=6 | load_ms=...
Realtime transcription prompt ready | dynamic=True | terms=... | chars=...
Starting realtime session with model: gpt-realtime-mini, voice: cedar
```

Nếu thấy:

```text
python-dotenv could not parse statement starting at line ...
```

thì sửa `.env` trước. Nếu `.env` parse lỗi, config mới có thể không load.

## 10. Bộ câu test đề xuất

Test theo 3 nhóm.

### Nhóm A: tên sách và nhân vật

Nói:

```text
Tóm tắt chương 1 của Of Mice and Men.
George và Lennie có mối quan hệ như thế nào?
Candy trong truyện có vai trò gì?
Curley xuất hiện trong chương nào?
```

Kỳ vọng:

```text
Of Mice and Men không bị transcribe quá sai.
George, Lennie, Candy, Curley ổn hơn.
Tool query vẫn đi được vào search_book_knowledge.
```

### Nhóm B: lệnh app ngắn

Nói:

```text
Có.
Đồng ý.
Tìm trên internet đi.
Không cần.
Tiếp tục.
Dừng lại.
```

Kỳ vọng:

```text
Transcript ngắn ít sai hơn.
Permission flow không hiểu nhầm grant thành deny.
```

### Nhóm C: câu ngoài sách

Nói:

```text
Giá vàng SJC hôm nay là bao nhiêu?
Thời tiết Cần Thơ Ninh Kiều hôm nay có mưa không?
```

Kỳ vọng:

```text
Agent xin quyền web nếu cần.
Nếu user đồng ý, execute_web_search chạy.
Transcript không còn sai quá nhiều ở entity phổ biến.
```

## 11. Log cần theo dõi

Theo dõi các log:

```text
Realtime transcription prompt ready
user_input_transcribed received | final=True | chars=...
AGENT_TRACE late_transcript
query_guard_reason_code
grounding_route
detected_intent
tool_names
```

Quan trọng nhất:

```text
query_guard_reason_code không quay lại tool_query_transcript_mismatch
grounding_route nhận đúng book_section hoặc book_rag
web permission không hiểu nhầm câu xác nhận ngắn
```

## 12. Rollback

Nếu dynamic prompt gây vấn đề, chỉ cần set:

```env
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED=false
```

Khi đó hệ thống quay lại prompt static:

```py
settings.OPENAI_REALTIME_TRANSCRIPTION_PROMPT
```

Không cần revert code.

## 13. Tiêu chí đánh giá thành công

Chạy ít nhất 30 lượt voice test:

```text
10 câu hỏi sách có tên nhân vật/tên chương
10 câu permission ngắn
10 câu ngoài sách cần web
```

Đạt nếu:

```text
- Tỷ lệ transcript sai entity giảm rõ.
- Không tăng turn_total đáng kể.
- Không tăng số lần watchdog_fired bất thường.
- Không làm web permission bị lặp/hỏi sai nhiều hơn.
- Không xuất hiện lỗi parse env.
```

## 14. Patch tóm tắt

Tạo file:

```text
app/services/voice_agent/transcription_prompt.py
```

Thêm config:

```py
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED: bool = True
OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_CHARS: int = 1800
OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_TERMS: int = 80
OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_SECTION_TERMS: int = 40
OPENAI_REALTIME_INPUT_AUDIO_NOISE_REDUCTION: str = "near_field"
```

Sửa `agent_voice_gpt_realtime.py`:

```py
from app.services.voice_agent.transcription_prompt import build_realtime_transcription_prompt
```

Build prompt sau khi load `grounding_scope`:

```py
transcription_prompt_result = build_realtime_transcription_prompt(
    base_prompt=settings.OPENAI_REALTIME_TRANSCRIPTION_PROMPT,
    grounding_scope=grounding_scope,
    enabled=settings.OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED,
    max_chars=settings.OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_CHARS,
    max_terms=settings.OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_TERMS,
    max_section_terms=settings.OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_SECTION_TERMS,
)
```

Dùng prompt mới:

```py
input_audio_transcription=AudioTranscription(
    model=settings.OPENAI_REALTIME_TRANSCRIPTION_MODEL,
    language=settings.OPENAI_REALTIME_TRANSCRIPTION_LANGUAGE,
    prompt=transcription_prompt_result.prompt,
),
```

Đưa noise reduction ra config:

```py
input_audio_noise_reduction=settings.OPENAI_REALTIME_INPUT_AUDIO_NOISE_REDUCTION,
```

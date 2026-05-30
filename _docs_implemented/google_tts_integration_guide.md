# Google Cloud Text-to-Speech Chirp 3 HD Integration Guide

Tài liệu này mô tả cách tích hợp **Google Cloud Text-to-Speech Chirp 3 HD** vào TRIAM Backend để tạo audio tiếng Việt chất lượng cao cho audiobook học tập.

Mục tiêu của lần implement này:

- Giữ nguyên public API đang được worker dùng: `generate_audio_and_get_duration(text, filename, voice=None, max_retries=6)`.
- Thêm Google Chirp 3 HD như provider production.
- Giữ Edge TTS làm provider dev/fallback khi cấu hình `TTS_PROVIDER=edge`.
- Không làm vỡ flow hiện tại của `app/services/workers/learning_unit_tts_worker.py`.
- Không log text đầy đủ, credential, token hoặc service account.

Ngày kiểm tra tài liệu chính thức: 2026-05-30.

Nguồn chính thức:

- Google TTS pricing: https://cloud.google.com/text-to-speech/pricing
- Chirp 3 HD docs: https://docs.cloud.google.com/text-to-speech/docs/chirp3-hd
- Quotas and limits: https://docs.cloud.google.com/text-to-speech/quotas
- Voice list: https://docs.cloud.google.com/text-to-speech/docs/list-voices-and-types

---

## 1. Chốt Quyết Định

TRIAM nên dùng:

```env
TTS_PROVIDER=google
GOOGLE_TTS_VOICE=vi-VN-Chirp3-HD-Iapetus
```

Lý do:

- Google Chirp 3 HD có giọng tiếng Việt tự nhiên hơn Edge TTS, phù hợp audiobook học tập.
- Google có quota miễn phí theo **ký tự**, không phải token.
- Chirp 3 HD có khoảng **1 triệu ký tự miễn phí mỗi tháng** theo pricing hiện tại, sau đó tính phí theo ký tự.
- So với ElevenLabs, Google phù hợp hơn cho long-form audiobook vì chi phí dễ kiểm soát hơn.
- So với Vbee, Google có lợi thế là có free tier trước khi phải thanh toán.

Điểm cần nhớ:

- Vẫn phải bật billing trong Google Cloud.
- Google tính theo **character/ký tự**, không tính theo token.
- Không gửi nguyên learning unit quá dài vào một TTS request.
- Không tự động fallback từ Google sang Edge khi Google lỗi trong production, vì sẽ làm giọng đọc không nhất quán và che lỗi vận hành.

---

## 2. Cấu Hình Google Cloud

### 2.1. Bật API

Trong Google Cloud Console:

1. Tạo hoặc chọn project.
2. Bật **Cloud Text-to-Speech API**.
3. Bật billing.
4. Tạo service account cho backend.
5. Gán quyền tối thiểu: **Cloud Text-to-Speech User**.
6. Tạo JSON key cho service account.

### 2.2. Local credential

Local có thể dùng file JSON:

```env
GOOGLE_APPLICATION_CREDENTIALS=./secrets/google-tts-service-account.json
```

Không commit file JSON vào git. Nên thêm vào `.gitignore`:

```gitignore
secrets/
*.service-account.json
google-tts-service-account*.json
```

### 2.3. Hugging Face credential

Trên Hugging Face Space, không nên upload file JSON vào repo. Dùng secret env:

```env
GOOGLE_TTS_CREDENTIALS_JSON=<base64-json-service-account>
```

Tạo base64 trên Windows PowerShell:

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes(".\secrets\google-tts-service-account.json"))
```

Backend sẽ decode env này ra file tạm trong runtime và set `GOOGLE_APPLICATION_CREDENTIALS`.

---

## 3. Dependency

Repo đang dùng `pyproject.toml` chuẩn `[project].dependencies`, không dùng Poetry syntax.

Thêm dependency:

```toml
"google-cloud-texttospeech>=2.36.0",
```

Hoặc dùng lệnh:

```powershell
uv add google-cloud-texttospeech
```

Không dùng:

```toml
google-cloud-texttospeech = "^2.36.0"
```

---

## 4. Config Cần Thêm

File: `app/core/config.py`

Thêm các field vào class `Settings`:

```python
    # Text-to-Speech provider
    TTS_PROVIDER: str = "edge"  # "edge" for local/dev, "google" for production
    TTS_RECEIVE_TIMEOUT_SECONDS: int = 300
    TTS_RETRY_BASE_SECONDS: int = 3

    # Google Cloud Text-to-Speech
    GOOGLE_APPLICATION_CREDENTIALS: str | None = None
    GOOGLE_TTS_CREDENTIALS_JSON: str | None = None
    GOOGLE_TTS_LANGUAGE_CODE: str = "vi-VN"
    GOOGLE_TTS_VOICE: str = "vi-VN-Chirp3-HD-Iapetus"
    GOOGLE_TTS_MAX_BYTES_PER_REQUEST: int = 4500
    GOOGLE_TTS_MONTHLY_FREE_CHAR_LIMIT: int = 1_000_000
    GOOGLE_TTS_ENABLE_COST_LOG: bool = True
```

Gợi ý `.env.example`:

```env
# Text-to-Speech
TTS_PROVIDER=edge
TTS_GENERATION_CONCURRENCY=2
TTS_RECEIVE_TIMEOUT_SECONDS=300
TTS_RETRY_BASE_SECONDS=3

# Google Cloud TTS, only required when TTS_PROVIDER=google
GOOGLE_APPLICATION_CREDENTIALS=
GOOGLE_TTS_CREDENTIALS_JSON=
GOOGLE_TTS_LANGUAGE_CODE=vi-VN
GOOGLE_TTS_VOICE=vi-VN-Chirp3-HD-Iapetus
GOOGLE_TTS_MAX_BYTES_PER_REQUEST=4500
GOOGLE_TTS_MONTHLY_FREE_CHAR_LIMIT=1000000
GOOGLE_TTS_ENABLE_COST_LOG=true
```

Gợi ý production `.env`:

```env
TTS_PROVIDER=google
GOOGLE_TTS_VOICE=vi-VN-Chirp3-HD-Iapetus
GOOGLE_TTS_CREDENTIALS_JSON=<base64-json-service-account>
TTS_GENERATION_CONCURRENCY=1
```

Vì Chirp 3 HD là paid provider sau free quota, production nên bắt đầu với `TTS_GENERATION_CONCURRENCY=1`. Sau khi đo chi phí và rate limit ổn định thì mới tăng.

---

## 5. Implement Trong `app/services/tts_service.py`

### 5.1. Nguyên tắc clean code

Không nên nhồi toàn bộ logic vào `generate_audio_and_get_duration()`. Hàm này nên chỉ làm orchestration:

```text
clean text -> validate -> select provider -> retry -> generate file -> measure duration
```

Các việc nhỏ nên tách thành helper:

- `_clean_text_for_tts`
- `_validate_tts_text`
- `_selected_tts_provider`
- `_prepare_google_credentials`
- `_get_google_tts_client`
- `_generate_audio_file_google_sync`
- `_generate_audio_file_edge`
- `_measure_mp3_duration_ms`
- `_retry_wait_seconds`

### 5.2. Import cần thêm

File hiện tại đã có `asyncio`, `edge_tts`, `settings`, `TTSInputTooShortError`, `log`, `get_loop_semaphore`.

Cần mở rộng import:

```python
import base64
import os
import re
import tempfile
from pathlib import Path

from app.core.exceptions import ExternalServiceError, TTSInputTooShortError
```

Không import Google SDK ở top-level nếu muốn Edge vẫn chạy được trong môi trường chưa bật Google. Import lazy bên trong `_get_google_tts_client()`.

### 5.3. Constants và cache client

Thêm gần đầu file:

```python
SUPPORTED_TTS_PROVIDERS = {"edge", "google"}
MIN_TTS_TEXT_CHARS = 10

_STAGE_TAG_RE = re.compile(r"\[(?:[A-Za-zÀ-ỹ_ -]{2,40})\]")
_google_tts_client = None
```

Vì sao regex không dùng `r"\[.*?\]"`:

- Regex quá rộng có thể xóa nhầm citation hoặc nội dung học tập như `[1]`, `[a, b]`.
- TTS chỉ cần bỏ các stage tag dạng `[smile]`, `[sigh]`, `[pause]`.

### 5.4. Helper làm sạch và validate text

```python
def _clean_text_for_tts(text: str) -> str:
    cleaned = _STAGE_TAG_RE.sub("", text or "")
    return " ".join(cleaned.split()).strip()


def _utf8_size(text: str) -> int:
    return len(text.encode("utf-8"))


def _validate_tts_text(text: str) -> None:
    if len(text) < MIN_TTS_TEXT_CHARS:
        raise TTSInputTooShortError(f"Nội dung quá ngắn để tạo audio ({len(text)} ký tự).")
```

### 5.5. Helper chọn provider

```python
def _selected_tts_provider() -> str:
    provider = settings.TTS_PROVIDER.strip().lower()
    if provider not in SUPPORTED_TTS_PROVIDERS:
        raise ExternalServiceError(f"TTS_PROVIDER không hợp lệ: {settings.TTS_PROVIDER}")
    return provider
```

Không silently fallback khi config sai. Config sai phải fail rõ để dễ debug.

### 5.6. Helper credential cho Google

```python
def _prepare_google_credentials() -> None:
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        return

    raw_credentials = settings.GOOGLE_TTS_CREDENTIALS_JSON
    if not raw_credentials:
        raise ExternalServiceError(
            "Thiếu Google TTS credentials. Cấu hình GOOGLE_APPLICATION_CREDENTIALS "
            "hoặc GOOGLE_TTS_CREDENTIALS_JSON."
        )

    try:
        stripped = raw_credentials.strip()
        if stripped.startswith("{"):
            credentials_json = stripped
        else:
            credentials_json = base64.b64decode(stripped).decode("utf-8")
    except Exception as exc:
        raise ExternalServiceError("GOOGLE_TTS_CREDENTIALS_JSON không hợp lệ.") from exc

    credentials_path = Path(tempfile.gettempdir()) / "triam-google-tts-service-account.json"
    credentials_path.write_text(credentials_json, encoding="utf-8")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_path)
```

Không log nội dung credential. Nếu cần debug, chỉ log provider và voice.

### 5.7. Helper lấy Google client

```python
def _get_google_tts_client():
    global _google_tts_client

    if _google_tts_client is None:
        try:
            from google.cloud import texttospeech
        except ImportError as exc:
            raise ExternalServiceError(
                "Thiếu dependency google-cloud-texttospeech. Chạy: uv add google-cloud-texttospeech"
            ) from exc

        _prepare_google_credentials()
        _google_tts_client = texttospeech.TextToSpeechClient()

    return _google_tts_client
```

Lý do cache client:

- Tránh tạo client mới cho mỗi segment.
- Giảm overhead trong worker khi sách có nhiều audio segment.

### 5.8. Google TTS sync function

Google SDK là sync client, nên viết hàm sync riêng, sau đó gọi bằng `asyncio.to_thread()` trong async function.

```python
def _generate_audio_file_google_sync(text: str, filename: str, voice_name: str) -> int:
    from google.cloud import texttospeech

    byte_count = _utf8_size(text)
    if byte_count > settings.GOOGLE_TTS_MAX_BYTES_PER_REQUEST:
        raise ExternalServiceError(
            "Google TTS input quá dài cho một request "
            f"({byte_count} bytes > {settings.GOOGLE_TTS_MAX_BYTES_PER_REQUEST} bytes). "
            "Cần giảm độ dài từng main_script trong normalize_text_for_speech."
        )

    client = _get_google_tts_client()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=settings.GOOGLE_TTS_LANGUAGE_CODE,
        name=voice_name,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    Path(filename).write_bytes(response.audio_content)
    return len(response.audio_content)
```

Tại sao không tự split và nối MP3 trong `tts_service.py`:

- Một input script hiện đang tương ứng với một row `LearningUnitSegment`.
- Nếu service tự split thành nhiều file rồi nối thô MP3, duration và seek có thể không ổn định.
- Dùng thư viện nối audio chuẩn thường cần FFmpeg, làm deploy Hugging Face nặng hơn.
- Clean hơn là bắt `normalize_text_for_speech()` tạo `main_scripts` đủ nhỏ ngay từ đầu.

Nếu sau này cần xử lý script dài hơn 4,500 bytes, hướng đúng là tách ở tầng `llm_service.py` hoặc worker để tạo nhiều `LearningUnitSegment`, không nối file âm thanh trong TTS service.

### 5.9. Edge TTS helper

```python
async def _generate_audio_file_edge(text: str, filename: str, voice_name: str) -> None:
    communicate = edge_tts.Communicate(
        text,
        voice_name,
        receive_timeout=settings.TTS_RECEIVE_TIMEOUT_SECONDS,
    )
    await communicate.save(filename)
```

### 5.10. Measure duration helper

```python
def _measure_mp3_duration_ms(filename: str) -> int:
    from mutagen.mp3 import MP3

    try:
        audio = MP3(filename)
        return int(audio.info.length * 1000)
    except Exception:
        return 0
```

### 5.11. Retry helper

```python
def _retry_wait_seconds(attempt: int) -> int:
    return settings.TTS_RETRY_BASE_SECONDS * (2**attempt)
```

### 5.12. Hàm chính sau refactor

Giữ tên hàm cũ để worker không cần đổi:

```python
async def generate_audio_and_get_duration(
    text: str,
    filename: str,
    voice: str | None = None,
    max_retries: int = 6,
) -> int:
    """
    Generate one MP3 file and return duration in milliseconds.

    Public function used by learning_unit_tts_worker.
    Keep this signature stable unless worker contract is updated.
    """
    cleaned = _clean_text_for_tts(text)
    _validate_tts_text(cleaned)

    provider = _selected_tts_provider()
    target_voice = voice or (
        settings.GOOGLE_TTS_VOICE if provider == "google" else settings.EDGE_TTS_VOICE
    )

    async with get_loop_semaphore("tts_generation", settings.TTS_GENERATION_CONCURRENCY):
        for attempt in range(max_retries):
            try:
                if provider == "google":
                    audio_bytes = await asyncio.to_thread(
                        _generate_audio_file_google_sync,
                        cleaned,
                        filename,
                        target_voice,
                    )
                    if settings.GOOGLE_TTS_ENABLE_COST_LOG:
                        log.info(
                            "Google TTS generated | chars={} | bytes={} | audio_bytes={} | voice={}",
                            len(cleaned),
                            _utf8_size(cleaned),
                            audio_bytes,
                            target_voice,
                        )
                else:
                    await _generate_audio_file_edge(cleaned, filename, target_voice)
                    log.info(
                        "Edge TTS generated | chars={} | bytes={} | voice={}",
                        len(cleaned),
                        _utf8_size(cleaned),
                        target_voice,
                    )

                return _measure_mp3_duration_ms(filename)

            except Exception as exc:
                if attempt < max_retries - 1:
                    wait = _retry_wait_seconds(attempt)
                    log.warning(
                        "TTS attempt failed | provider={} | attempt={}/{} | chars={} | wait_seconds={} | error={}",
                        provider,
                        attempt + 1,
                        max_retries,
                        len(cleaned),
                        wait,
                        exc,
                    )
                    await asyncio.sleep(wait)
                    continue

                log.error(
                    "TTS failed | provider={} | attempts={} | chars={} | voice={} | error={}",
                    provider,
                    max_retries,
                    len(cleaned),
                    target_voice,
                    exc,
                )
                raise

    return 0
```

Lưu ý logging:

- Log `chars`, `bytes`, `voice`, `provider`.
- Không log full `text`.
- Không log credential path nếu không cần.
- Không log response payload từ Google.

---

## 6. Những Hàm Cũ Nên Giữ Hay Xóa

Hiện `app/services/tts_service.py` có:

- `stream_text_to_speech()` dùng OpenAI TTS stream.
- `stream_text_to_speech_edge()` dùng Edge TTS stream.
- `generate_audio_file_edge()`.
- `generate_audio_and_get_duration()`.

Khuyến nghị phase này:

- Giữ `stream_text_to_speech()` nếu vẫn có API dùng streaming TTS.
- Giữ `stream_text_to_speech_edge()` nếu còn route/dev tool dùng.
- Có thể đổi `generate_audio_file_edge()` thành wrapper gọi `_generate_audio_file_edge()` để không phá import cũ.
- Không thêm Google streaming trong phase này, vì audiobook pipeline cần file MP3 ổn định để upload Supabase.

Wrapper tương thích:

```python
async def generate_audio_file_edge(text: str, filename: str, voice: str = settings.EDGE_TTS_VOICE):
    await _generate_audio_file_edge(_clean_text_for_tts(text), filename, voice)
```

---

## 7. Cần Chỉnh Prompt LLM Để Tránh Vượt Limit

Google quota giới hạn theo bytes/request, tiếng Việt có dấu thường tốn nhiều byte hơn số ký tự hiển thị. Vì vậy `normalize_text_for_speech()` nên đảm bảo mỗi item trong `main_scripts` đủ ngắn.

Trong `app/services/llm_service.py`, bổ sung rule vào prompt:

```text
- Mỗi phần tử trong main_scripts không vượt quá 3,500 ký tự tiếng Việt.
- Nếu nội dung dài, chia thành nhiều phần tử main_scripts.
- Mỗi phần tử phải kết thúc ở ranh giới câu hoàn chỉnh.
```

Vì sao 3,500 ký tự mà không phải 4,500:

- Google limit tính theo bytes, không phải ký tự.
- Tiếng Việt UTF-8 có thể dùng nhiều byte cho một ký tự.
- Chừa buffer giúp tránh request fail.

Nếu muốn chắc hơn, thêm validator trong `NormalizedUnitPayload.validate_main_scripts()`:

```python
MAX_TTS_SCRIPT_BYTES = 4500

for script in scripts:
    if len(script.encode("utf-8")) > MAX_TTS_SCRIPT_BYTES:
        raise ValueError("main_scripts item exceeds Google TTS byte budget")
```

Trade-off:

- Validator giúp fail sớm.
- Nhưng nếu LLM thường tạo script dài, worker sẽ fail nhiều hơn cho tới khi prompt/chunking được chỉnh tốt.
- Nên implement prompt trước, validator sau khi đã test vài sách thật.

---

## 8. Test Plan

### 8.1. Static checks

```powershell
uv run ruff check app/services/tts_service.py app/core/config.py
uv run python -m py_compile app/services/tts_service.py app/core/config.py
```

### 8.2. Local Edge regression

Set:

```env
TTS_PROVIDER=edge
```

Run một đoạn nhỏ:

```powershell
@'
import asyncio
from pathlib import Path
from app.services.tts_service import generate_audio_and_get_duration

async def main():
    output = "uploads/test_edge_tts.mp3"
    Path("uploads").mkdir(exist_ok=True)
    duration = await generate_audio_and_get_duration("Đây là bài kiểm thử tạo giọng đọc tiếng Việt cho TRIAM.", output)
    print({"duration_ms": duration, "exists": Path(output).exists(), "size": Path(output).stat().st_size})

asyncio.run(main())
'@ | uv run python -
```

### 8.3. Local Google smoke test

Set:

```env
TTS_PROVIDER=google
GOOGLE_APPLICATION_CREDENTIALS=./secrets/google-tts-service-account.json
GOOGLE_TTS_VOICE=vi-VN-Chirp3-HD-Iapetus
TTS_GENERATION_CONCURRENCY=1
```

Run:

```powershell
@'
import asyncio
from pathlib import Path
from app.services.tts_service import generate_audio_and_get_duration

async def main():
    output = "uploads/test_google_chirp3.mp3"
    Path("uploads").mkdir(exist_ok=True)
    duration = await generate_audio_and_get_duration(
        "Chào mừng bạn đến với TRIAM. Đây là kiểm thử Google Chirp ba HD tiếng Việt.",
        output,
    )
    print({"duration_ms": duration, "exists": Path(output).exists(), "size": Path(output).stat().st_size})

asyncio.run(main())
'@ | uv run python -
```

Expected:

- File MP3 được tạo.
- `duration_ms > 0`.
- Log có provider, chars, bytes, voice.
- Log không có text đầy đủ hoặc credential.

### 8.4. Worker integration test

Chạy local 2 terminal:

```powershell
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

```powershell
uv run celery -A app.core.celery_app.celery_app worker -Q document -l info --pool=solo --concurrency 1
```

Flow test:

```text
POST /api/v1/upload
POST /api/v1/generate-plan
GET /api/v1/jobs/{job_id}
GET /api/v1/books/{book_id}/learning-units
```

Expected:

- Job đi từ queued/processing sang partial_ready hoặc ready.
- Segment audio URL được tạo.
- Không có lỗi Google input quá dài.
- Nếu có lỗi input quá dài, xử lý tiếp ở `llm_service.py` để giảm độ dài từng `main_scripts`.

---

## 9. Production Checklist

Trước khi deploy:

- `TTS_PROVIDER=google`
- `GOOGLE_TTS_CREDENTIALS_JSON` đã set trong Hugging Face Secrets.
- `GOOGLE_TTS_VOICE` đã chọn đúng giọng.
- `TTS_GENERATION_CONCURRENCY=1` cho giai đoạn đầu.
- Không commit service account JSON.
- Log production không chứa credential.
- Google Cloud billing đã bật.
- Cloud Text-to-Speech API đã enable.
- Worker document queue chạy ổn.
- Test một sách nhỏ trước khi test sách dài.

---

## 10. Trade-off Và Lựa Chọn Không Làm Ở Phase Này

### Không dùng Vbee ngay

Vbee có thể tốt cho tiếng Việt, nhưng cần thanh toán trước. Dự án hiện cần triển khai nhanh, có free tier, dễ test production, nên Google phù hợp hơn.

### Không dùng ElevenLabs cho audiobook mặc định

ElevenLabs mạnh về giọng biểu cảm và voice clone, nhưng chi phí long-form audiobook cao hơn. Có thể để làm premium voice sau.

### Không dùng Google Long Audio Synthesis ngay

Long Audio Synthesis phù hợp nội dung rất dài và có workflow GCS riêng. Hiện pipeline TRIAM đã chia theo `LearningUnitSegment`, upload Supabase và track progress theo DB. Dùng sync TTS theo segment đơn giản hơn, dễ debug hơn.

### Không tự nối MP3 trong TTS service

Tự nối MP3 làm tăng rủi ro seek/duration sai. Nếu một script quá dài, cách đúng là tách script thành nhiều segment ở tầng LLM/worker.

### Không auto fallback Google sang Edge trong production

Auto fallback giúp job dễ hoàn thành hơn, nhưng làm chất lượng giọng lẫn lộn và khiến lỗi Google khó phát hiện. Production nên fail rõ, FE hiển thị lỗi/retry.

---

## 11. Kết Luận Implement

Thay đổi nên làm theo thứ tự:

1. Thêm dependency `google-cloud-texttospeech`.
2. Thêm config trong `app/core/config.py` và `.env.example`.
3. Refactor `app/services/tts_service.py` theo provider-based helper nhỏ.
4. Test Edge regression.
5. Test Google smoke test bằng một câu ngắn.
6. Test worker với một sách thật nhỏ.
7. Nếu gặp lỗi script quá dài, chỉnh prompt/validator trong `app/services/llm_service.py`.

Sau phase này, `tts_service.py` vẫn là một file nhỏ, dễ đọc, dễ debug:

```text
worker -> generate_audio_and_get_duration()
       -> provider edge/google
       -> tạo mp3 local
       -> đo duration
       -> worker upload Supabase
```

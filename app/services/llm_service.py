import json
from dataclasses import dataclass

from openai import AsyncOpenAI
from pydantic import BaseModel, Field, ValidationError, field_validator

from app.core.config import settings
from app.core.constant import PlanMode
from app.core.exceptions import ChapterTooLargeError, LLMResponseFormatError
from app.core.logger import log as logger
from app.services.async_limiter import get_loop_semaphore
from app.services.chapter_chunking_service import split_text_for_llm
from app.services.token_budget_service import estimate_text_budget, exceeds_hard_limit, should_chunk

# Sử dụng Gemini qua OpenAI-compatible API
client = AsyncOpenAI(api_key=settings.GEMINI_API_KEY, base_url=settings.GEMINI_BASE_URL)


@dataclass(frozen=True)
class NormalizedChapter:
    main_scripts: list[str]
    review_script: str


class NormalizedChapterPayload(BaseModel):
    main_scripts: list[str] = Field(min_length=1, description="Các đoạn kịch bản nói nối tiếp nhau.")
    review_script: str = Field(min_length=1, description="Nội dung tóm tắt để người học ôn tập.")

    @field_validator("main_scripts")
    @classmethod
    def validate_main_scripts(cls, value: list[str]) -> list[str]:
        scripts = [item.strip() for item in value if isinstance(item, str) and item.strip()]
        if not scripts:
            raise ValueError("main_scripts must contain at least one non-empty string")
        return scripts

    @field_validator("review_script")
    @classmethod
    def validate_review_script(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("review_script must be non-empty")
        return stripped


SYSTEM_PROMPT_REWRITE_FULL = """
Bạn là một Biên tập viên Sách nói & Chuyên gia Giáo dục (TRIAM AI).
Nhiệm vụ: Chuyển đổi văn bản thô thành kịch bản nói (TTS Script) và trích xuất nội dung ôn tập.

QUY TẮC BIÊN TẬP VĂN BẢN (TTS):
1. Mở rộng từ viết tắt: "CNTT" -> "Công nghệ thông tin", "VN" -> "Việt Nam".
2. Xử lý số liệu/Ký hiệu: "5%" -> "Năm phần trăm", "1990" -> "năm một ngàn chín trăm chín mươi", "Tp.HCM" -> "Thành phố Hồ Chí Minh".
3. Tự nhiên hóa: Thêm các từ nối để câu văn mượt mà. Giữ nguyên thuật ngữ tiếng Anh phổ biến (AI, Marketing) hoặc phiên âm nếu quá khó.
4. Sửa lỗi format: Nối các dòng bị ngắt sai do lỗi PDF. Loại bỏ số trang, header/footer thừa.
5. Văn phong: Thêm các từ nối nhẹ nhàng để câu văn mượt mà, không bị cụt. Giữ nguyên ý nghĩa gốc, không bịa thêm nội dung sai lệch.

YÊU CẦU ĐỊNH DẠNG OUTPUT (JSON BẮT BUỘC):
Bạn phải trả về một JSON object hợp lệ (không markdown) với cấu trúc sau:
{
  "main_scripts": [
    "Đoạn văn bản 1 đã biên tập...",
    "Đoạn văn bản 2 đã biên tập..."
  ],
  "review_script": "Nội dung tóm tắt để ôn tập..."
}

HƯỚNG DẪN CHI TIẾT CÁC TRƯỜNG:
1. "main_scripts" (Mảng các chuỗi):
   - Chia văn bản đã biên tập thành các đoạn nhỏ nối tiếp nhau.
   - Độ dài mỗi đoạn: Khoảng 3-5 câu hoặc 1 ý trọn vẹn (tương đương 30s - 1 phút đọc).
   - QUAN TRỌNG: Đảm bảo tính liền mạch (Coherence). Khi ghép các đoạn lại phải thành một bài nói hoàn chỉnh. KHÔNG thêm các từ như "Đoạn 1", "Phần tiếp" vào đầu mỗi đoạn.
   - Ngắt đoạn đúng dấu chấm câu.

2. "review_script" (Chuỗi):
   - Tóm tắt lại 3-5 ý tưởng cốt lõi nhất của phần văn bản này (khoảng 100-150 từ).
   - Viết dưới dạng văn nói gợi nhớ: "Trong phần này, chúng ta đã tìm hiểu về... Điểm mấu chốt là...".
   - Mục đích: Dùng để phát lại cho người dùng nghe để ôn bài sau 1, 3, 7 ngày.

Input: Văn bản gốc.
Output: Chỉ trả về JSON thuần.
"""

SYSTEM_PROMPT_REWRITE_PARETO = """
Bạn là một Chuyên gia Đọc nhanh & Giáo dục (TRIAM AI) áp dụng nguyên lý Pareto (80/20).
Nhiệm vụ: Chắt lọc 20% nội dung quan trọng nhất (ý chính, công thức, keyword) để mang lại 80% giá trị của văn bản gốc, sau đó chuyển thành kịch bản nói (TTS Script).

QUY TẮC BIÊN TẬP VĂN BẢN (TTS):
1. LƯỢC BỎ: Cắt bỏ hoàn toàn các ví dụ dài dòng, câu chuyện phụ, câu từ lan man "tốt thì biết".
2. TẬP TRUNG CỐT LÕI: Giữ lại định nghĩa, luận điểm chính, keyword (in đậm/in nghiêng trong ý đồ tác giả).
3. VĂN PHONG TTS: Nội dung chắt lọc phải được nối lại thành câu văn nói mượt mà, dễ hiểu, súc tích. Xử lý số liệu, chữ viết tắt như bình thường.
4. Mở rộng từ viết tắt: "CNTT" -> "Công nghệ thông tin", "VN" -> "Việt Nam".
5. Xử lý số liệu/Ký hiệu: "5%" -> "Năm phần trăm", "1990" -> "năm một ngàn chín trăm chín mươi", "Tp.HCM" -> "Thành phố Hồ Chí Minh".
6. Tự nhiên hóa: Thêm các từ nối để câu văn mượt mà. Giữ nguyên thuật ngữ tiếng Anh phổ biến (AI, Marketing) hoặc phiên âm nếu quá khó.
7. Sửa lỗi format: Nối các dòng bị ngắt sai do lỗi PDF. Loại bỏ số trang, header/footer thừa.
8. Văn phong: Thêm các từ nối nhẹ nhàng để câu văn mượt mà, không bị cụt. Giữ nguyên ý nghĩa gốc, không bịa thêm nội dung sai lệch.

YÊU CẦU ĐỊNH DẠNG OUTPUT (JSON BẮT BUỘC):
Bạn phải trả về một JSON object hợp lệ (không markdown) với cấu trúc sau:
{
  "main_scripts": [
    "Đoạn văn bản 1 đã biên tập...",
    "Đoạn văn bản 2 đã biên tập..."
  ],
  "review_script": "Tóm tắt cốt lõi để ôn tập nhanh (100 từ)..."
}

HƯỚNG DẪN CHI TIẾT CÁC TRƯỜNG:
1. "main_scripts" (Mảng các chuỗi):
   - Chia văn bản đã biên tập thành các đoạn nhỏ nối tiếp nhau.
   - Độ dài mỗi đoạn: Khoảng 3-5 câu hoặc 1 ý trọn vẹn (tương đương 30s - 1 phút đọc).
   - QUAN TRỌNG: Đảm bảo tính liền mạch (Coherence). Khi ghép các đoạn lại phải thành một bài nói hoàn chỉnh. KHÔNG thêm các từ như "Đoạn 1", "Phần tiếp" vào đầu mỗi đoạn.
   - Ngắt đoạn đúng dấu chấm câu.

2. "review_script" (Chuỗi):
   - Tóm tắt lại 3-5 ý tưởng cốt lõi nhất của phần văn bản này (khoảng 100-150 từ).
   - Viết dưới dạng văn nói gợi nhớ: "Trong phần này, chúng ta đã tìm hiểu về... Điểm mấu chốt là...".
   - Mục đích: Dùng để phát lại cho người dùng nghe để ôn bài sau 1, 3, 7 ngày.

Input: Văn bản gốc.
Output: Chỉ trả về JSON thuần.
"""


# ---------------------------------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------------------------------


def _prompt_for_mode(mode: str) -> str:
    if mode.lower() == PlanMode.PARETO.value:
        return SYSTEM_PROMPT_REWRITE_PARETO
    return SYSTEM_PROMPT_REWRITE_FULL


def _validate_normalized_payload(payload: dict) -> NormalizedChapter:
    try:
        parsed = NormalizedChapterPayload.model_validate(payload)
    except ValidationError as exc:
        raise LLMResponseFormatError("LLM response không khớp schema JSON yêu cầu.") from exc
    return NormalizedChapter(
        main_scripts=parsed.main_scripts,
        review_script=parsed.review_script,
    )


def _extract_json_object(content: str) -> dict:
    raw = content.strip()
    if raw.startswith("```"):
        raw = raw.strip("`").strip()
        if raw.lower().startswith("json"):
            raw = raw[4:].strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        return json.loads(raw[start : end + 1])


def _coerce_normalized_response(parsed_payload: NormalizedChapterPayload | None, content: str | None) -> NormalizedChapter:
    if parsed_payload is not None:
        return NormalizedChapter(
            main_scripts=parsed_payload.main_scripts,
            review_script=parsed_payload.review_script,
        )

    if not content:
        raise LLMResponseFormatError("LLM response rỗng.")

    try:
        parsed_data = _extract_json_object(content)
    except json.JSONDecodeError as exc:
        raise LLMResponseFormatError("LLM response không phải JSON hợp lệ.") from exc
    return _validate_normalized_payload(parsed_data)


async def _call_normalize_llm(text: str, mode: str, *, context_hint: str | None = None) -> NormalizedChapter:
    mode_prompt = _prompt_for_mode(mode)
    user_content = text if not context_hint else f"{context_hint}\n\n--- INPUT ---\n{text}"
    request_chars = len(user_content)
    request_context = "chunk" if context_hint else "single"

    last_format_error: Exception | None = None
    max_attempts = 2
    for attempt in range(1, max_attempts + 1):
        async with get_loop_semaphore("llm_normalize", settings.LLM_NORMALIZE_CONCURRENCY):
            logger.info(f"LLM normalize start | mode={mode} | context={request_context} | chars={request_chars} | attempt={attempt}/{max_attempts}")
            try:
                response = await client.beta.chat.completions.parse(
                    model=settings.GEMINI_MODEL_LLM,
                    messages=[
                        {"role": "system", "content": mode_prompt},
                        {"role": "user", "content": user_content},
                    ],
                    temperature=0.2,
                    response_format=NormalizedChapterPayload,
                )
                message = response.choices[0].message
                normalized = _coerce_normalized_response(message.parsed, message.content)
                logger.info(f"LLM normalize done | mode={mode} | context={request_context} | scripts={len(normalized.main_scripts)} | review_chars={len(normalized.review_script)}")
                return normalized
            except LLMResponseFormatError as exc:
                last_format_error = exc
                logger.warning(f"LLM normalize returned invalid structured output | mode={mode} | context={request_context} | attempt={attempt}/{max_attempts}")
            except (ValidationError, ValueError, json.JSONDecodeError) as exc:
                last_format_error = exc
                logger.warning(f"LLM normalize schema validation failed | mode={mode} | context={request_context} | attempt={attempt}/{max_attempts}")

    raise LLMResponseFormatError("LLM response không phải JSON hợp lệ sau khi thử lại.") from last_format_error


async def normalize_text_for_speech(raw_text: str, mode: str, *, chapter_title: str | None = None) -> dict:
    """
    Gửi text thô cho Gemini để biên tập và cấu trúc lại thành TTS script.

    Returns:
        {"main_scripts": [...], "review_script": "..."}

    Raises:
        Exception: Nếu LLM call thất bại hoặc response không parse được —
                   caller (tts_worker) chịu trách nhiệm rollback chapter.
    """
    budget = estimate_text_budget(raw_text)
    logger.info(
        f"Normalize preflight | mode={mode} | title={chapter_title or '(unknown)'} | "
        f"chars={budget.char_count} | estimated_tokens={budget.estimated_tokens} | "
        f"estimated_audio_seconds={budget.estimated_audio_seconds}"
    )
    if exceeds_hard_limit(budget):
        raise ChapterTooLargeError(f"Chương quá lớn: khoảng {budget.estimated_tokens} tokens, vượt giới hạn {settings.LLM_INPUT_HARD_TOKEN_LIMIT} tokens.")

    if not should_chunk(budget):
        logger.info(f"Normalize strategy | mode={mode} | strategy=single_call | title={chapter_title or '(unknown)'}")
        normalized = await _call_normalize_llm(raw_text, mode)
        return {
            "main_scripts": normalized.main_scripts,
            "review_script": normalized.review_script,
        }

    chunks = split_text_for_llm(raw_text)
    logger.info(f"Normalize long chapter with {len(chunks)} chunks | mode={mode} | title={chapter_title or '(unknown)'} | estimated_tokens={budget.estimated_tokens}")

    all_scripts: list[str] = []
    review_parts: list[str] = []
    previous_tail = ""

    for chunk in chunks:
        logger.info(f"Normalize chunk start | mode={mode} | title={chapter_title or '(unknown)'} | chunk={chunk.index + 1}/{len(chunks)} | estimated_tokens={chunk.estimated_tokens}")
        context_hint = (
            f"Chương: {chapter_title or 'Không rõ'}.\n"
            f"Đây là phần {chunk.index + 1}/{len(chunks)} của cùng một chương.\n"
            "Giữ mạch văn nối tiếp với phần trước. Không tự nhắc 'phần' hoặc 'chunk' trong câu trả lời.\n"
            f"Đoạn cuối phần trước để nối ngữ cảnh: {previous_tail[-600:]}"
        )
        normalized = await _call_normalize_llm(chunk.text, mode, context_hint=context_hint)
        all_scripts.extend(normalized.main_scripts)
        if normalized.review_script:
            review_parts.append(normalized.review_script)
        previous_tail = chunk.text[-1000:]
        logger.info(f"Normalize chunk done | mode={mode} | title={chapter_title or '(unknown)'} | chunk={chunk.index + 1}/{len(chunks)} | cumulative_scripts={len(all_scripts)}")

    return {
        "main_scripts": all_scripts,
        "review_script": " ".join(review_parts).strip(),
    }

import json
from dataclasses import dataclass

from openai import AsyncOpenAI
from pydantic import BaseModel, Field, ValidationError, field_validator

from app.core.config import settings
from app.core.constant import PlanMode
from app.core.exceptions import LearningUnitTooLargeError, LLMResponseFormatError
from app.core.logger import log as logger
from app.services.async_limiter import get_loop_semaphore
from app.services.chapter_chunking_service import split_text_for_llm
from app.services.token_budget_service import estimate_text_budget, exceeds_hard_limit, should_chunk
from app.services.tts_script_quality_service import inspect_tts_script_quality, sanitize_tts_script_list, sanitize_tts_script_text

# Sử dụng Gemini qua OpenAI-compatible API
client = AsyncOpenAI(
    api_key=settings.GEMINI_API_KEY, 
    base_url=settings.GEMINI_BASE_URL,
    timeout=60.0
)


@dataclass(frozen=True)
class NormalizedUnit:
    main_scripts: list[str]
    review_script: str


class NormalizedUnitPayload(BaseModel):
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


COMMON_TTS_REWRITE_RULES = """
You are TRIAM's audiobook editor. Convert raw textbook text into clean Vietnamese spoken scripts for Text-to-Speech.

Global rules:
- Preserve the source meaning. Do not invent facts, scores, definitions, citations, or claims.
- Write natural Vietnamese speech for listeners, not visual text for readers.
- Every string value must be plain spoken text. Never output Markdown, headings, bullets, tables, inline code marks, visual emphasis, citation markers, page numbers, headers, or footers.
- Convert visual emphasis into normal speech. For example, a visually highlighted concept should become ordinary words in the sentence, with no symbols.
- Repair PDF/DOCX extraction noise: broken lines, repeated headers, footers, page numbers, table separators, and stray formatting symbols.
- Convert numbers, years, percentages, currencies, and common symbols into Vietnamese spoken form when this improves listening.
- First-use terminology rule: for any acronym, initialism, symbol, benchmark, method name, or domain-specific abbreviation, briefly explain it the first time it appears in the same learning unit.
- Prefer the source's own parenthetical explanation or expansion when available.
- If the exact expansion is uncertain, explain the term's role neutrally instead of guessing.
- After a term has been explained once in the same learning unit, you may use the short form to keep audio concise.
- The review script may be heard separately later, so explain essential abbreviations again there.
- Split main_scripts into coherent spoken paragraphs of about 3-5 sentences or one complete idea each. Do not prefix them with labels such as "Segment", "Part", or "Next".
- Ensure the scripts sound continuous when played in order.

Return only a valid JSON object:
{
  "main_scripts": ["spoken paragraph 1", "spoken paragraph 2"],
  "review_script": "spoken review summary"
}
"""

SYSTEM_PROMPT_REWRITE_FULL = (
    COMMON_TTS_REWRITE_RULES
    + """

Mode: FULL.
- Keep the learning unit's content complete and faithful.
- Do not over-summarize. Preserve definitions, arguments, conditions, examples that explain the concept, and important transitions.
- You may make dense textbook prose easier to hear, but keep the author's logic and scope.
- review_script: 100-150 Vietnamese words, summarizing 3-5 core ideas in spoken form.

Input: raw textbook text.
Output: valid JSON only.
"""
)

SYSTEM_PROMPT_REWRITE_PARETO = (
    COMMON_TTS_REWRITE_RULES
    + """

Mode: PARETO.
- Select the smallest set of ideas that gives the learner the highest understanding value.
- Keep definitions, central claims, formulas, rules, methods, causal relationships, and important comparison criteria.
- Remove side stories, long examples, repeated evidence, and low-value details unless they are needed to understand a retained idea.
- Do not keep a dense list of names, benchmarks, acronyms, or scores only because they appear in the source. Group them into a broader spoken idea when the exact items are not essential.
- If a benchmark, acronym, score, or technical name is retained because it is important, explain it at first use using the global first-use terminology rule.
- review_script: about 100 Vietnamese words, focused on the most useful recall points.

Input: raw textbook text.
Output: valid JSON only.
"""
)


# ---------------------------------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------------------------------


def _prompt_for_mode(mode: str) -> str:
    if mode.lower() == PlanMode.PARETO.value:
        return SYSTEM_PROMPT_REWRITE_PARETO
    return SYSTEM_PROMPT_REWRITE_FULL


def _validate_normalized_payload(payload: dict) -> NormalizedUnit:
    try:
        parsed = NormalizedUnitPayload.model_validate(payload)
    except ValidationError as exc:
        raise LLMResponseFormatError("LLM response không khớp schema JSON yêu cầu.") from exc
    return NormalizedUnit(
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


def _coerce_normalized_response(parsed_payload: NormalizedUnitPayload | None, content: str | None) -> NormalizedUnit:
    if parsed_payload is not None:
        return NormalizedUnit(
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


def _sanitize_normalized_unit(unit: NormalizedUnit) -> NormalizedUnit:
    return NormalizedUnit(
        main_scripts=sanitize_tts_script_list(unit.main_scripts),
        review_script=sanitize_tts_script_text(unit.review_script),
    )


def _log_tts_quality_report(unit: NormalizedUnit, *, mode: str, request_context: str, request_chars: int) -> None:
    report = inspect_tts_script_quality([*unit.main_scripts, unit.review_script])
    if not report.has_warnings:
        return

    log_message = (
        "LLM normalize quality warnings | "
        f"mode={mode} | context={request_context} | chars={request_chars} | "
        f"markdown_artifacts={report.markdown_artifacts} | "
        f"unexplained_acronyms={list(report.unexplained_acronyms)}"
    )
    if report.markdown_artifacts:
        logger.warning(log_message)
    else:
        logger.info(log_message)


async def _call_normalize_llm(text: str, mode: str, *, context_hint: str | None = None) -> NormalizedUnit:
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
                    response_format=NormalizedUnitPayload,
                )
                message = response.choices[0].message
                normalized = _coerce_normalized_response(message.parsed, message.content)
                _log_tts_quality_report(normalized, mode=mode, request_context=request_context, request_chars=request_chars)
                normalized = _sanitize_normalized_unit(normalized)
                logger.info(f"LLM normalize done | mode={mode} | context={request_context} | scripts={len(normalized.main_scripts)} | review_chars={len(normalized.review_script)}")
                return normalized
            except LLMResponseFormatError as exc:
                last_format_error = exc
                logger.warning(f"LLM normalize returned invalid structured output | mode={mode} | context={request_context} | attempt={attempt}/{max_attempts}")
            except (ValidationError, ValueError, json.JSONDecodeError) as exc:
                last_format_error = exc
                logger.warning(f"LLM normalize schema validation failed | mode={mode} | context={request_context} | attempt={attempt}/{max_attempts}")

    raise LLMResponseFormatError("LLM response không phải JSON hợp lệ sau khi thử lại.") from last_format_error


async def normalize_text_for_speech(raw_text: str, mode: str, *, unit_title: str | None = None, chapter_title: str | None = None) -> dict:
    """
    Gửi text thô cho Gemini để biên tập và cấu trúc lại thành TTS script.

    Returns:
        {"main_scripts": [...], "review_script": "..."}

    Raises:
        Exception: Nếu LLM call thất bại hoặc response không parse được —
                   caller (learning_unit_tts_worker) chịu trách nhiệm rollback unit.
    """
    title = unit_title or chapter_title
    budget = estimate_text_budget(raw_text)
    logger.info(
        f"Normalize preflight | mode={mode} | title={title or '(unknown)'} | "
        f"chars={budget.char_count} | estimated_tokens={budget.estimated_tokens} | "
        f"estimated_audio_seconds={budget.estimated_audio_seconds}"
    )
    if exceeds_hard_limit(budget):
        raise LearningUnitTooLargeError(f"Bài học quá lớn: khoảng {budget.estimated_tokens} tokens, vượt giới hạn {settings.LLM_INPUT_HARD_TOKEN_LIMIT} tokens.")

    if not should_chunk(budget):
        logger.info(f"Normalize strategy | mode={mode} | strategy=single_call | title={title or '(unknown)'}")
        normalized = await _call_normalize_llm(raw_text, mode)
        return {
            "main_scripts": normalized.main_scripts,
            "review_script": normalized.review_script,
        }

    chunks = split_text_for_llm(raw_text)
    logger.info(f"Normalize long unit with {len(chunks)} chunks | mode={mode} | title={title or '(unknown)'} | estimated_tokens={budget.estimated_tokens}")

    all_scripts: list[str] = []
    review_parts: list[str] = []
    previous_tail = ""

    for chunk in chunks:
        logger.info(f"Normalize chunk start | mode={mode} | title={title or '(unknown)'} | chunk={chunk.index + 1}/{len(chunks)} | estimated_tokens={chunk.estimated_tokens}")
        context_hint = (
            f"Bài học: {title or 'Không rõ'}.\n"
            f"Đây là phần {chunk.index + 1}/{len(chunks)} của cùng một bài học.\n"
            "Giữ mạch văn nối tiếp với phần trước. Không tự nhắc 'phần' hoặc 'chunk' trong câu trả lời.\n"
            f"Đoạn cuối phần trước để nối ngữ cảnh: {previous_tail[-600:]}"
        )
        normalized = await _call_normalize_llm(chunk.text, mode, context_hint=context_hint)
        all_scripts.extend(normalized.main_scripts)
        if normalized.review_script:
            review_parts.append(normalized.review_script)
        previous_tail = chunk.text[-1000:]
        logger.info(f"Normalize chunk done | mode={mode} | title={title or '(unknown)'} | chunk={chunk.index + 1}/{len(chunks)} | cumulative_scripts={len(all_scripts)}")

    return {
        "main_scripts": all_scripts,
        "review_script": " ".join(review_parts).strip(),
    }

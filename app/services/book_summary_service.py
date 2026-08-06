import json
import time
from typing import List, Optional
import uuid

from openai import AsyncOpenAI
from pydantic import BaseModel, Field, ValidationError
from sqlmodel import Session, select, col

from app.core.config import settings
from app.core.constant import SummaryStatus
from app.core.exceptions import LLMResponseFormatError
from app.core.logger import log
from app.models.db_models import Book, BookSection, BookSectionKnowledge


class BookSummarySchema(BaseModel):
    key_idea: str = Field(description="Ý tưởng chính tổng quan nhất của cuốn sách (Khớp FE 'Ý tưởng chính').")
    target_audience: str = Field(description="Đối tượng độc giả phù hợp nhất để đọc cuốn sách này (Khớp FE 'Đối tượng phù hợp').")
    estimated_read_minutes: int = Field(description="Thời gian đọc ước tính tính bằng phút (Khớp FE 'Thời gian đọc ước tính').")
    key_takeaways: List[str] = Field(description="Top 5-7 bài học / đánh giá cốt lõi đắt giá nhất (Khớp FE 'Đánh giá tổng quan').")
    summary: str = Field(description="Bản tóm tắt tổng quan toàn bộ cốt truyện và thông điệp của cuốn sách.")
    main_characters: List[str] = Field(description="Danh sách các nhân vật chính.")


def _normalize_raw_summary_dict(raw_dict: dict, word_count: int) -> dict:
    """Helper bóc tách và chuẩn hóa dữ liệu từ Gemini về đúng Schema trước khi validate Pydantic."""
    if not isinstance(raw_dict, dict):
        return {}

    normalized = {}

    # 1. key_idea
    normalized["key_idea"] = str(
        raw_dict.get("key_idea") or raw_dict.get("title") or raw_dict.get("main_idea") or "Chưa có thông tin"
    )

    # 2. target_audience
    normalized["target_audience"] = str(
        raw_dict.get("target_audience") or raw_dict.get("audience") or "Chưa có thông tin"
    )

    # 3. estimated_read_minutes
    raw_minutes = raw_dict.get("estimated_read_minutes") or raw_dict.get("read_time_minutes")
    if isinstance(raw_minutes, (int, float)):
        normalized["estimated_read_minutes"] = int(raw_minutes)
    else:
        normalized["estimated_read_minutes"] = max(1, int(word_count / 200)) if word_count else 60

    # 4. key_takeaways
    raw_takeaways = raw_dict.get("key_takeaways") or raw_dict.get("takeaways") or raw_dict.get("themes") or raw_dict.get("plot_points")
    if isinstance(raw_takeaways, list):
        items = []
        for item in raw_takeaways:
            if isinstance(item, str):
                items.append(item)
            elif isinstance(item, dict):
                val = item.get("description") or item.get("title") or item.get("name")
                if val:
                    items.append(str(val))
        normalized["key_takeaways"] = items if items else ["Chưa có thông tin"]
    else:
        normalized["key_takeaways"] = ["Chưa có thông tin"]

    # 5. summary
    normalized["summary"] = str(raw_dict.get("summary") or raw_dict.get("description") or "Chưa có thông tin")

    # 6. main_characters
    raw_chars = raw_dict.get("main_characters") or raw_dict.get("characters")
    if isinstance(raw_chars, list):
        char_list = []
        for char in raw_chars:
            if isinstance(char, str):
                char_list.append(char)
            elif isinstance(char, dict):
                name = char.get("name") or char.get("title") or "Nhân vật"
                desc = char.get("description") or char.get("role") or char.get("desc")
                if desc:
                    char_list.append(f"{name}: {desc}")
                else:
                    char_list.append(str(name))
        normalized["main_characters"] = char_list
    else:
        normalized["main_characters"] = []

    return normalized


async def generate_ai_book_summary(session: Session, book_id: uuid.UUID) -> dict:
    """Hàm xử lý nghiệp vụ chính: Kiểm tra token budget, gọi Gemini 3.5 Flash Lite, kiểm duyệt Pydantic và lưu DB."""
    book = session.get(Book, book_id)
    if not book:
        raise ValueError(f"Book not found | book_id={book_id}")

    # Lấy toàn bộ các đoạn kiến thức / chương của sách theo đúng thứ tự
    statement = (
        select(BookSectionKnowledge)
        .join(BookSection, BookSectionKnowledge.section_id == BookSection.id)
        .where(BookSectionKnowledge.book_id == book_id)
        .order_by(col(BookSection.section_index).asc(), col(BookSectionKnowledge.chunk_index).asc())
    )
    chunks = session.exec(statement).all()

    if not chunks:
        sections = session.exec(
            select(BookSection).where(BookSection.book_id == book_id).order_by(col(BookSection.section_index).asc())
        ).all()
        full_text = "\n\n".join([f"[{s.title}]\n{s.text_content or ''}" for s in sections if s.text_content])
    else:
        full_text = "\n\n".join([c.content for c in chunks if c.content])

    word_count = len(full_text.split())
    estimated_tokens = int(word_count * 1.3)
    log.info(f"Book summary generation started | book_id={book_id} | estimated_tokens={estimated_tokens:,}")

    if estimated_tokens > settings.TOTAL_TOKEN_LIMIT:
        log.warning(f"Tokens exceed ceiling ({estimated_tokens:,} > {settings.TOTAL_TOKEN_LIMIT:,}). Fallback to Section Outlines.")
        sections = session.exec(
            select(BookSection).where(BookSection.book_id == book_id).order_by(col(BookSection.section_index).asc())
        ).all()
        full_text = "\n\n".join([f"[{s.title}]\n{(s.text_content or '')[:400]}" for s in sections])

    client = AsyncOpenAI(
        api_key=settings.GEMINI_API_KEY,
        base_url=settings.GEMINI_BASE_URL,
        timeout=120.0,
    )

    prompt_messages = [
        {
            "role": "system",
            "content": (
                "You are an expert literary analyst and executive book summarizer.\n"
                "Your task is to read the provided text of the book and extract a structured executive summary in raw JSON format.\n\n"
                "REQUIRED JSON SCHEMA:\n"
                "Your JSON output MUST contain EXACTLY these keys:\n"
                "{\n"
                '  "key_idea": "String - Main core idea/message of the book in 2-3 sentences.",\n'
                '  "target_audience": "String - Intended target audience (e.g. Độc giả yêu thích...)",\n'
                '  "estimated_read_minutes": Integer - Estimated reading time in minutes (e.g. 180),\n'
                '  "key_takeaways": ["String", "String"] - List of 5-7 key takeaways or main reviews,\n'
                '  "summary": "String - Comprehensive summary of the book plot/content.",\n'
                '  "main_characters": ["String", "String"] - List of main character names as strings (e.g. ["George Milton: Anh nông dân nhân hậu", "Lennie Small: Người bạn trung thành"])\n'
                "}\n\n"
                "CRITICAL GROUNDING CONSTRAINTS:\n"
                "1. Base your summary STRICTLY AND EXCLUSIVELY on the provided book text.\n"
                "2. DO NOT hallucinate, infer, or fabricate any details, facts, plot points, or character traits not explicitly mentioned in the text.\n"
                "3. If any field cannot be explicitly determined from the text, set its string value to 'Chưa có thông tin' (or an empty array [] for list fields).\n"
                "4. Write all string values in fluent, natural Vietnamese for direct display on the mobile app UI.\n"
                "5. Output ONLY valid raw JSON matching the required schema without Markdown code blocks."
            ),
        },
        {"role": "user", "content": f"Here is the complete content of the book:\n\n{full_text}\n\nProvide the executive summary in valid JSON format matching the schema."},
    ]

    start_time = time.perf_counter()
    completion = await client.chat.completions.create(
        model=settings.GEMINI_MODEL_LLM,
        messages=prompt_messages,
        response_format={"type": "json_object"},
        temperature=0.3,
    )
    elapsed_seconds = time.perf_counter() - start_time
    log.info(f"Gemini 3.5 Flash Lite summary complete | book_id={book_id} | elapsed={elapsed_seconds:.2f}s")

    raw_output = completion.choices[0].message.content.strip()

    if raw_output.startswith("```"):
        raw_output = raw_output.strip("`").strip()
        if raw_output.lower().startswith("json"):
            raw_output = raw_output[4:].strip()

    try:
        raw_dict = json.loads(raw_output)
    except json.JSONDecodeError as exc:
        log.error(f"Failed to parse LLM response JSON | book_id={book_id} | raw={raw_output[:200]}")
        raise LLMResponseFormatError("Kết quả trả về từ Gemini không phải là chuỗi JSON hợp lệ.") from exc

    # Chuẩn hóa dữ liệu về đúng schema trước khi validate
    normalized_dict = _normalize_raw_summary_dict(raw_dict, word_count)

    try:
        validated_summary = BookSummarySchema.model_validate(normalized_dict)
        result_dict = validated_summary.model_dump()
    except ValidationError as val_err:
        log.error(f"LLM JSON schema validation failed | book_id={book_id} | error={val_err}")
        raise LLMResponseFormatError("Dữ liệu tóm tắt AI từ Gemini thiếu các trường bắt buộc.") from val_err

    # Cập nhật DB khi dữ liệu đã qua kiểm duyệt chuẩn 100%
    book.ai_summary = result_dict
    book.ai_summary_status = SummaryStatus.COMPLETED.value
    book.ai_summary_error = None
    session.add(book)
    session.commit()
    session.refresh(book)

    return result_dict

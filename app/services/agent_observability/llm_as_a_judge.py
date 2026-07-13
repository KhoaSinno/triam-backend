from __future__ import annotations

import uuid

from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from app.core.config import settings
from app.db.database import engine
from app.models.db_models import BookSectionKnowledge


class LLMJudgeScore(BaseModel):
    faithfulness: float = Field(
        ...,
        description="Điểm trung thực của câu trả lời sinh ra so với phần ngữ cảnh được truy xuất (từ 0.0 đến 1.0). "
                    "Điểm 1.0 nghĩa là toàn bộ thông tin trong câu trả lời đều được hỗ trợ bởi ngữ cảnh. "
                    "Điểm 0.0 nghĩa là câu trả lời chứa các khẳng định sai lệch hoàn toàn so với ngữ cảnh."
    )
    answer_relevance: float = Field(
        ...,
        description="Điểm độ liên quan của câu trả lời đối với câu hỏi gốc của người học (từ 0.0 đến 1.0). "
                    "Điểm 1.0 nghĩa là câu trả lời đi thẳng vào trọng tâm câu hỏi và giải đáp chính xác. "
                    "Điểm 0.0 nghĩa là câu trả lời hoàn toàn lạc đề hoặc không liên quan gì đến câu hỏi."
    )
    verdict: bool = Field(
        ...,
        description="True nếu câu trả lời đạt yêu cầu chất lượng (Faithfulness >= 0.8 và Answer Relevance >= 0.8), "
                    "ngược lại nhận giá trị False nếu bị ảo giác thông tin hoặc trả lời không đúng trọng tâm."
    )
    reasoning: str = Field(
        ...,
        description="Lập luận chi tiết bằng tiếng Việt giải thích cho điểm số trên, chỉ rõ các luận điểm đúng hoặc sai lệch."
    )


def get_retrieved_context(chunk_ids: list[str]) -> str:
    """
    Truy vấn nội dung văn bản gốc của các đoạn tri thức RAG từ PostgreSQL dựa trên danh sách chunk_ids.
    """
    if not chunk_ids:
        return ""

    # Chuyển đổi chuỗi UUID sang đối tượng UUID nếu cần
    uuids = []
    for cid in chunk_ids:
        try:
            uuids.append(uuid.UUID(cid))
        except (ValueError, TypeError):
            continue

    if not uuids:
        return ""

    with Session(engine) as db_session:
        statement = select(BookSectionKnowledge).where(BookSectionKnowledge.id.in_(uuids))
        chunks = db_session.exec(statement).all()
        # Sắp xếp các đoạn văn bản theo thứ tự xuất hiện ban đầu của chunk_ids nhận được từ trace
        chunk_map = {c.id: c.content for c in chunks}
        ordered_contents = [chunk_map[uid] for uid in uuids if uid in chunk_map]
        return "\n\n".join(ordered_contents)


async def judge_answer(
    query: str,
    context: str,
    answer: str,
    *,
    model: str = "gpt-4o-mini",
) -> LLMJudgeScore:
    """
    Gọi API OpenAI để đóng vai trò làm trọng tài (LLM-as-a-Judge) chấm điểm
    độ trung thực (faithfulness) và độ liên quan (answer_relevance) của câu trả lời.
    """
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    system_prompt = (
        "Bạn là một chuyên gia kiểm định chất lượng học liệu số trong hệ thống trợ lý học tập TRIAM.\n"
        "Nhiệm vụ của bạn là đánh giá chất lượng câu trả lời của trợ lý ảo dựa trên câu hỏi của người học "
        "và phần ngữ cảnh sách (context) đã được truy xuất.\n"
        "Bạn cần phân tích kỹ lường xem câu trả lời có bám sát ngữ cảnh không (Faithfulness) "
        "và có trả lời trực tiếp câu hỏi không (Answer Relevance).\n"
        "Hãy cực kỳ nghiêm khắc với hiện tượng ảo giác (hallucination) — bất kỳ tuyên bố nào không có bằng chứng "
        "rõ ràng trong ngữ cảnh đều phải bị trừ điểm trung thực nặng."
    )

    user_prompt = (
        f"--- CÂU HỎI NGƯỜI HỌC ---\n{query}\n\n"
        f"--- NGỮ CẢNH TRÍ THỨC TRUY XUẤT ---\n{context}\n\n"
        f"--- CÂU TRẢ LỜI CỦA TRỢ LÝ ---\n{answer}\n"
    )

    # Sử dụng tính năng Structured Outputs của OpenAI SDK
    completion = await client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format=LLMJudgeScore,
        temperature=0.0
    )

    return completion.choices[0].message.parsed

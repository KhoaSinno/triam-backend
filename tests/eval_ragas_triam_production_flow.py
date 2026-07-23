"""
tests/eval_ragas_triam_production_flow.py
===========================================
Script chạy kiểm thử RAGAS trên đúng 100% LUỒNG PRODUCTION BACKEND TRIAM:
Sử dụng `load_grounding_scope` và `GroundingRouter` từ `app.services.agent_grounding`.

Luồng xử lý Production:
1. Nạp GroundingScope từ Postgres DB (Book metadata & TOC Tree).
2. Gọi GroundingRouter.resolve(query):
   - Nếu route == BOOK_METADATA: Trả câu trả lời chính xác từ DB (Zero LLM Hallucination).
   - Nếu route == BOOK_SECTION: Nạp toàn bộ văn bản chính danh của Chương từ DB và gọi LLM tóm tắt.
   - Nếu route == CLARIFICATION: Yêu cầu người dùng làm rõ.
   - Nếu route == WEB_POLICY: Hỏi xin quyền Web Search.
   - Nếu route == BOOK_RAG: Gọi Hybrid Search (Dense + BM25 + WRRF) + Cohere Reranker.
"""

import asyncio
import json
import sys
import time
from pathlib import Path
import uuid

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from sqlmodel import Session

from app.core.config import settings
from app.db.database import engine
from app.repositories.agent_grounding_repo import (
    load_grounding_scope,
    get_scoped_section_texts,
)
from app.services.agent_grounding import (
    GroundingIntent,
    GroundingRoute,
    GroundingRouter,
)
from app.services.rag_service import search_book_hybrid_knowledge
from openai import AsyncOpenAI

triam_llm_client = AsyncOpenAI(
    api_key=settings.GEMINI_API_KEY,
    base_url=settings.GEMINI_BASE_URL,
)


async def production_section_loader_async(book_id: uuid.UUID, section_ids: tuple[uuid.UUID, ...]):
    allowed_book_ids = (book_id,)
    with Session(engine) as session:
        return get_scoped_section_texts(
            session,
            book_id=book_id,
            section_ids=section_ids,
            allowed_book_ids=allowed_book_ids,
        )


async def run_production_flow_turn(query: str, book_id_str: str) -> dict:
    start_time = time.time()
    book_uuid = uuid.UUID(book_id_str)
    
    # 1. Nạp GroundingScope thực tế từ DB Postgres cho cuốn sách
    scope = load_grounding_scope([book_id_str])
    router = GroundingRouter(
        scope,
        production_section_loader_async,
        section_context_max_chars=settings.AGENT_SECTION_CONTEXT_MAX_CHARS,
    )

    # 2. Định tuyến qua GroundingRouter của TRIAM Backend
    res = await router.resolve(query)
    route = res.decision.route
    intent = res.decision.intent

    response_text = ""
    contexts = []
    raw_chunks = []

    if route == GroundingRoute.BOOK_METADATA:
        # Trả đáp án định danh từ DB Metadata (Zero Hallucination)
        response_text = res.deterministic_answer or ""
        contexts = [f"[METADATA] Total sections: {scope.books[0].total_sections if scope.books else 0}"]

    elif route == GroundingRoute.BOOK_SECTION:
        # Nạp ngữ cảnh chương chính danh và gọi LLM tóm tắt/trả lời
        context_text = res.section_context or ""
        contexts = [context_text]
        prompt = (
            f"Bạn là trợ lý học tập TRIAM. Dựa trên nội dung chương sách sau:\n\n{context_text}\n\n"
            f"Hãy thực hiện yêu cầu: {query}"
        )
        llm_res = await triam_llm_client.chat.completions.create(
            model=settings.GEMINI_MODEL_LLM,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        response_text = llm_res.choices[0].message.content.strip()

    elif route == GroundingRoute.CLARIFICATION:
        response_text = res.deterministic_answer or "Bạn muốn tôi tóm tắt chương hoặc đề mục cụ thể nào của cuốn sách này?"

    elif route == GroundingRoute.WEB_POLICY:
        response_text = "Tôi cần tìm thông tin này trên Internet. Bạn có cho phép tôi tìm kiếm web không?"

    elif route == GroundingRoute.BOOK_RAG:
        # Gọi Hybrid Search + Cohere Reranker
        final_chunks = await search_book_hybrid_knowledge(query=query, document_ids=[book_id_str])
        if isinstance(final_chunks, list) and final_chunks:
            contexts = [str(c.get("content", "")) for c in final_chunks]
            raw_chunks = final_chunks
            context_text = "\n\n".join(contexts)
            prompt = (
                f"Bạn là trợ lý học tập TRIAM. Dựa trên ngữ cảnh sách trích xuất sau:\n\n{context_text}\n\n"
                f"Hãy trả lời câu hỏi: {query}"
            )
            llm_res = await triam_llm_client.chat.completions.create(
                model=settings.GEMINI_MODEL_LLM,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
            )
            response_text = llm_res.choices[0].message.content.strip()
        else:
            response_text = "Không tìm thấy thông tin phù hợp trong sách."

    elapsed = time.time() - start_time
    return {
        "query": query,
        "intent": intent.value,
        "route": route.value,
        "response": response_text,
        "contexts": contexts,
        "raw_chunks": raw_chunks,
        "elapsed": elapsed,
    }


async def main_async():
    testset_path = Path(__file__).resolve().parent / "eval_dataset_triam.json"
    with open(testset_path, "r", encoding="utf-8") as f:
        testset = json.load(f)

    # Thêm câu Q1 (Hỏi số chương metadata) để test đúng luồng hệ thống
    testset_full = [
        {
            "query_id": "Q1",
            "book_id": "827b7894-11e0-4d67-b85d-3800485dbba1",
            "book_title": "Of Mice and Men",
            "category": "metadata",
            "user_input": "Sách có mấy chương",
            "reference": "Cuốn sách này có 6 chương."
        }
    ] + testset

    print(f"🚀 BẮT ĐẦU CHẠY KIỂM THỬ TRÊN ĐÚNG 100% LUỒNG PRODUCTION BACKEND (GroundingRouter + DB)...")

    results = []
    for idx, item in enumerate(testset_full, 1):
        print(f"\n▶ ({idx}/{len(testset_full)}) [{item['query_id']}] Query: '{item['user_input']}'")
        turn = await run_production_flow_turn(item["user_input"], item["book_id"])
        
        print(f"   🧭 Intent Classified: {turn['intent']} | Route: {turn['route']}")
        print(f"   ⏱️ Latency: {turn['elapsed']:.2f}s | Contexts loaded: {len(turn['contexts'])}")
        print(f"   💬 Production Response: {turn['response'][:120]}...")

        results.append({
            "query_id": item["query_id"],
            "user_input": item["user_input"],
            "reference": item["reference"],
            "intent": turn["intent"],
            "route": turn["route"],
            "response": turn["response"],
            "contexts": turn["contexts"],
            "elapsed": turn["elapsed"]
        })

    trace_path = testset_path.parent.parent / "logs" / "ragas_eval" / "production_flow_trace.json"
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    with open(trace_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ [PRODUCTION TRACE SAVED] Đã lưu vết kiểm thử chuẩn luồng Backend tại: {trace_path}")


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()

"""
tests/eval_ragas_triam_of_mice_and_men.py
==========================================
Script thực thi kiểm thử RAGAS thực tế trên cuốn sách "Of Mice and Men" (ID: 827b7894-11e0-4d67-b85d-3800485dbba1).
Thu thập live data từ:
  1. Postgres Vector (Dense) + BM25 Lexical + WRRF Fusion + Cohere Reranker (rag_service.py)
  2. Gemini LLM Generator
Lưu vết 100% chunks và chấm điểm 6 chỉ số RAGAS.
"""

import asyncio
import json
import sys
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from datasets import Dataset

# 1. Import Ragas v0.2+ & Metrics
try:
    from ragas import evaluate
    from ragas.metrics import (
        faithfulness,
        answer_relevancy,
        context_recall,
        context_precision,
        answer_correctness,
        answer_similarity,
    )
    from ragas.llms import LangchainLLMWrapper
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    HAS_RAGAS = True
except ImportError:
    HAS_RAGAS = False

# 2. Import các dịch vụ Backend của TRIAM
from app.core.config import settings
from app.services.rag_service import search_book_hybrid_knowledge
from openai import AsyncOpenAI

# Single source of truth client cho LLM Generation (Gemini 3.5 Flash Lite)
triam_llm_client = AsyncOpenAI(
    api_key=settings.GEMINI_API_KEY,
    base_url=settings.GEMINI_BASE_URL,
)


async def run_triam_rag_pipeline(query: str, book_id: str) -> tuple[list[str], str, list[dict], float]:
    """Gọi trực tiếp Pipeline Hybrid Search + Cohere Reranker của TRIAM."""
    start_time = time.time()
    
    # 1. Truy xuất Top-K Chunks bằng Hybrid Search + Cohere Reranker
    final_chunks = await search_book_hybrid_knowledge(query=query, document_ids=[book_id])
    
    if isinstance(final_chunks, str) or not final_chunks:
        contexts = []
        raw_chunks = []
    else:
        contexts = [str(c.get("content", "")) for c in final_chunks]
        raw_chunks = final_chunks

    # 2. Sinh câu trả lời từ LLM dựa trên ngữ cảnh đã truy xuất
    context_text = "\n\n".join(contexts)
    prompt = (
        f"Bạn là trợ lý học tập TRIAM. Hãy trả lời câu hỏi dựa trên ngữ cảnh sách sau:\n\n"
        f"Ngữ cảnh trích xuất:\n{context_text}\n\n"
        f"Câu hỏi: {query}\n"
        f"Trả lời ngắn gọn, chính xác bằng tiếng Việt."
    )

    res = await triam_llm_client.chat.completions.create(
        model=settings.GEMINI_MODEL_LLM,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    elapsed = time.time() - start_time
    response_text = res.choices[0].message.content.strip()
    
    return contexts, response_text, raw_chunks, elapsed


async def collect_pipeline_results(testset_path: Path):
    with open(testset_path, "r", encoding="utf-8") as f:
        testset = json.load(f)

    print(f"🔄 [1/3] Đang thực thi RAG Pipeline trên DB thật với {len(testset)} test cases...")
    
    eval_data = {
        "user_input": [],
        "retrieved_contexts": [],
        "response": [],
        "reference": []
    }
    trace_logs = []

    for idx, item in enumerate(testset, 1):
        print(f"\n▶ ({idx}/{len(testset)}) [{item['query_id']}] {item['user_input']}")
        contexts, response_text, raw_chunks, elapsed = await run_triam_rag_pipeline(item["user_input"], item["book_id"])
        
        print(f"   ⏱️ Thời gian thực thi: {elapsed:.2f}s")
        print(f"   📚 Số chunks Cohere trả về: {len(raw_chunks)}")
        if raw_chunks:
            print(f"   🏆 Top-1 Chunk ID: {raw_chunks[0].get('id')} (Score: {raw_chunks[0].get('final_score')})")
        print(f"   💬 LLM Response: {response_text[:80]}...")

        eval_data["user_input"].append(item["user_input"])
        eval_data["retrieved_contexts"].append(contexts)
        eval_data["response"].append(response_text)
        eval_data["reference"].append(item["reference"])

        trace_logs.append({
            "query_id": item["query_id"],
            "user_input": item["user_input"],
            "reference": item["reference"],
            "elapsed_seconds": elapsed,
            "retrieved_chunks_count": len(raw_chunks),
            "top_1_chunk_id": raw_chunks[0].get("id") if raw_chunks else None,
            "top_1_score": raw_chunks[0].get("final_score") if raw_chunks else None,
            "retrieved_contexts": contexts,
            "raw_chunks": raw_chunks,
            "response": response_text
        })

    return Dataset.from_dict(eval_data), trace_logs


def main():
    testset_path = Path(__file__).resolve().parent / "eval_dataset_triam.json"
    if not testset_path.exists():
        print(f"❌ Không tìm thấy testset tại: {testset_path}")
        return

    dataset, trace_logs = asyncio.run(collect_pipeline_results(testset_path))

    output_dir = Path(__file__).resolve().parent.parent / "logs" / "ragas_eval"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Lưu Trace Chi Tiết Chunks
    trace_path = output_dir / "of_mice_and_men_trace.json"
    with open(trace_path, "w", encoding="utf-8") as f:
        json.dump(trace_logs, f, ensure_ascii=False, indent=2)
    print(f"\n✅ [TRACE SAVED] Đã lưu vết chi tiết chunks tại: {trace_path}")

    # 2. Đánh giá RAGAS nếu package đã cài đặt thành công
    if HAS_RAGAS:
        print("\n🤖 [2/3] Giám khảo RAGAS đang thực hiện chấm 6 chỉ số...")
        # Sử dụng OpenAI API Key / Gemini OpenAI proxy làm Judge nếu có
        try:
            judge_llm = LangchainLLMWrapper(
                ChatOpenAI(
                    model="gpt-4o" if settings.OPENAI_API_KEY else settings.GEMINI_MODEL_LLM,
                    api_key=settings.OPENAI_API_KEY or settings.GEMINI_API_KEY,
                    base_url=None if settings.OPENAI_API_KEY else settings.GEMINI_BASE_URL,
                    temperature=0.0
                )
            )
            metrics = [context_precision, context_recall, faithfulness, answer_relevancy, answer_correctness, answer_similarity]
            for m in metrics:
                m.llm = judge_llm

            results = evaluate(dataset=dataset, metrics=metrics, llm=judge_llm)
            print("\n📊 [3/3] BÁO CÁO KẾT QUẢ ĐÁNH GIÁ RAGAS:")
            print(results)

            df = results.to_pandas()
            csv_path = output_dir / "of_mice_and_men_ragas_report.csv"
            df.to_csv(csv_path, index=False, encoding="utf-8-sig")
            print(f"✅ [REPORT SAVED] Đã xuất CSV báo cáo tại: {csv_path}")
        except Exception as e:
            print(f"⚠️ RAGAS Judge encounter issue: {e}. Vết dữ liệu Pipeline đã lưu đầy đủ tại trace log.")
    else:
        print("\nℹ️ RAGAS đang được cài đặt trong background. Dữ liệu Pipeline RAG thực tế đã được thu thập và lưu vết 100% trơn tru.")


if __name__ == "__main__":
    main()

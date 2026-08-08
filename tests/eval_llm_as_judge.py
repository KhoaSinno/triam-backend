"""Evaluate historical responses with an LLM judge after offline provenance checks.

This is a custom LLM-as-a-Judge implementation informed by RAGAS concepts; it
is not the RAGAS package.  Retrieval metrics are only requested for cases whose
saved contexts can be tied to the exact ``turn_completed`` retrieval trace.
"""

import asyncio
import hashlib
import json
import math
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd  # noqa: E402
from openai import AsyncOpenAI  # noqa: E402

from app.core.config import settings  # noqa: E402
from scripts.ragas_dataset_validation import (  # noqa: E402
    DEFAULT_OUTPUT_PATH,
    load_provenance_checked_cases,
    print_summary,
)

judge_client = AsyncOpenAI(
    api_key=settings.GEMINI_API_KEY,
    base_url=settings.GEMINI_BASE_URL,
)
JUDGE_MODEL = "gemini-3.5-flash-lite"


@dataclass(frozen=True)
class MetricResult:
    score: float | None
    error: str | None = None


async def call_judge_llm(prompt: str) -> str:
    """Call the judge and surface failures instead of inventing a score."""
    max_retries = 5
    last_error: Exception | None = None
    for attempt in range(max_retries):
        try:
            res = await judge_client.chat.completions.create(
                model=JUDGE_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            return res.choices[0].message.content
        except Exception as exc:
            last_error = exc
            if attempt == max_retries - 1:
                break
            await asyncio.sleep(2.0 * (attempt + 1))
    raise RuntimeError(f"judge_request_failed:{type(last_error).__name__ if last_error else 'unknown'}") from last_error


def clamp(val: float) -> float:
    """Đảm bảo điểm số luôn nằm trong khoảng [0.0, 1.0]."""
    score = float(val)
    if not math.isfinite(score):
        raise ValueError("score_must_be_finite")
    return max(0.0, min(1.0, score))


def _metric_error(exc: Exception) -> MetricResult:
    return MetricResult(score=None, error=f"{type(exc).__name__}:{str(exc)[:160]}")


def _load_json_object(content: str) -> dict:
    payload = json.loads(content)
    if not isinstance(payload, dict):
        raise ValueError("judge_response_is_not_a_json_object")
    return payload


async def evaluate_context_precision(question: str, reference: str, contexts: list[str]) -> MetricResult:
    """Calculate MAP@K from LLM relevance verdicts against the reference answer."""
    if not contexts:
        return MetricResult(score=None, error="missing_contexts")

    formatted_contexts = "\n".join([f"Chunk [{i+1}]: {ctx}" for i, ctx in enumerate(contexts)])
    prompt = (
        f"Câu hỏi: {question}\n\n"
        f"Đáp án chuẩn: {reference}\n\n"
        f"Danh sách các đoạn ngữ cảnh trích xuất theo thứ tự xếp hạng (từ Top 1 đến Top K):\n"
        f"{formatted_contexts}\n\n"
        f"Nhiệm vụ: Kiểm tra từng Chunk xem nó có thông tin liên quan để hỗ trợ đáp án chuẩn hay không.\n"
        f"Trả về kết quả dưới định dạng JSON duy nhất:\n"
        f"{{\"verdicts\": [true/false cho Chunk 1, true/false cho Chunk 2, ...]}}"
    )

    try:
        data = _load_json_object(await call_judge_llm(prompt))
        raw_verdicts = data.get("verdicts", [])
        if not isinstance(raw_verdicts, list) or len(raw_verdicts) != len(contexts):
            raise ValueError("invalid_verdict_count")

        verdicts = [
            v in (True, 1) or str(v).lower() in ("true", "1")
            for v in raw_verdicts
        ]

        sum_precision = 0.0
        relevant_count = 0

        for k, is_rel in enumerate(verdicts, start=1):
            if is_rel:
                relevant_count += 1
                precision_at_k = relevant_count / k
                sum_precision += precision_at_k

        if relevant_count == 0:
            return MetricResult(score=0.0)

        return MetricResult(score=clamp(sum_precision / relevant_count))
    except Exception as exc:
        return _metric_error(exc)


async def evaluate_faithfulness(question: str, contexts: list[str], response: str) -> MetricResult:
    """Tính Faithfulness: Phân rã mệnh đề và dùng Python tự tính tỷ lệ bám ngữ cảnh."""
    if not response or not contexts:
        return MetricResult(score=None, error="missing_response_or_contexts")

    context_text = "\n---\n".join(contexts)
    prompt = (
        f"Ngữ cảnh nguồn:\n{context_text}\n\n"
        f"Câu trả lời:\n{response}\n\n"
        f"Nhiệm vụ:\n"
        f"1. Phân rã câu trả lời thành các mệnh đề khẳng định nhỏ (atomic claims).\n"
        f"2. Kiểm tra xem từng mệnh đề có được suy ra trực tiếp từ ngữ cảnh nguồn hay không.\n"
        f"Trả về định dạng JSON duy nhất:\n"
        f"{{\"claims\": [{{\"claim\": \"...\", \"is_supported\": true/false}}]}}"
    )

    try:
        data = _load_json_object(await call_judge_llm(prompt))
        claims = data.get("claims", [])
        if not isinstance(claims, list) or not claims:
            raise ValueError("missing_claims")

        supported_count = sum(
            1
            for c in claims
            if c.get("is_supported") in (True, 1) or str(c.get("is_supported")).lower() in ("true", "1")
        )
        return MetricResult(score=clamp(supported_count / len(claims)))
    except Exception as exc:
        return _metric_error(exc)


async def evaluate_answer_relevancy(question: str, response: str) -> MetricResult:
    """Tính Answer Relevancy: Đánh giá câu trả lời có đi thẳng vào trọng tâm câu hỏi không."""
    if not response:
        return MetricResult(score=None, error="missing_response")

    prompt = (
        f"Câu hỏi: {question}\n"
        f"Câu trả lời: {response}\n\n"
        f"Đánh giá xem câu trả lời có trực tiếp giải quyết đúng và đầy đủ trọng tâm câu hỏi hay không. "
        f"Không phạt nếu câu trả lời ngắn gọn.\n"
        f"Trả về JSON duy nhất: {{\"relevancy_score\": 0.0-1.0, \"reason\": \"...\"}}"
    )
    try:
        data = _load_json_object(await call_judge_llm(prompt))
        if "relevancy_score" not in data:
            raise ValueError("missing_relevancy_score")
        return MetricResult(score=clamp(data["relevancy_score"]))
    except Exception as exc:
        return _metric_error(exc)


async def evaluate_context_recall(question: str, reference: str, contexts: list[str]) -> MetricResult:
    """Estimate reference-claim coverage by verified retrieved contexts."""
    if not contexts or not reference:
        return MetricResult(score=None, error="missing_reference_or_contexts")

    context_text = "\n---\n".join(contexts)
    prompt = (
        f"Đáp án chuẩn (Reference): {reference}\n\n"
        f"Các đoạn ngữ cảnh trích xuất (Retrieved Contexts):\n{context_text}\n\n"
        f"Đánh giá xem bao nhiêu % thông tin và ý chính trong Đáp án chuẩn có mặt trong các đoạn ngữ cảnh trích xuất.\n"
        f"Trả về JSON duy nhất: {{\"recall_score\": 0.0-1.0, \"reason\": \"...\"}}"
    )
    try:
        data = _load_json_object(await call_judge_llm(prompt))
        if "recall_score" not in data:
            raise ValueError("missing_recall_score")
        return MetricResult(score=clamp(data["recall_score"]))
    except Exception as exc:
        return _metric_error(exc)


async def evaluate_answer_correctness(question: str, reference: str, response: str) -> MetricResult:
    """Tính Answer Correctness: Đánh giá độ chính xác thực tế so với Đáp án chuẩn."""
    if not response or not reference:
        return MetricResult(score=None, error="missing_response_or_reference")

    prompt = (
        f"Câu hỏi: {question}\n"
        f"Đáp án chuẩn (Reference): {reference}\n"
        f"Câu trả lời thực tế (Response): {response}\n\n"
        f"So sánh độ chính xác về mặt sự thật và thông tin giữa Câu trả lời thực tế và Đáp án chuẩn.\n"
        f"Trả về JSON duy nhất: {{\"correctness_score\": 0.0-1.0, \"reason\": \"...\"}}"
    )
    try:
        data = _load_json_object(await call_judge_llm(prompt))
        if "correctness_score" not in data:
            raise ValueError("missing_correctness_score")
        return MetricResult(score=clamp(data["correctness_score"]))
    except Exception as exc:
        return _metric_error(exc)


async def evaluate_item(item: dict, sem: asyncio.Semaphore) -> dict:
    async with sem:
        q = item["user_input"]
        ref = item["reference"]
        ctx = item.get("contexts") or item.get("retrieved_contexts") or []
        resp = item.get("response", "")

        retrieval_eligible = bool(item.get("retrieval_metrics_eligible"))
        relevancy_result, correctness_result = await asyncio.gather(
            evaluate_answer_relevancy(q, resp),
            evaluate_answer_correctness(q, ref, resp),
        )
        if retrieval_eligible:
            faithfulness_result, recall_result, precision_result = await asyncio.gather(
                evaluate_faithfulness(q, ctx, resp),
                evaluate_context_recall(q, ref, ctx),
                evaluate_context_precision(q, ref, ctx),
            )
        else:
            faithfulness_result = MetricResult(score=None, error="not_applicable_unverified_retrieval")
            recall_result = MetricResult(score=None, error="not_applicable_unverified_retrieval")
            precision_result = MetricResult(score=None, error="not_applicable_unverified_retrieval")

        metric_results = {
            "context_precision": precision_result,
            "context_recall": recall_result,
            "faithfulness": faithfulness_result,
            "answer_relevancy": relevancy_result,
            "answer_correctness": correctness_result,
        }
        result = {
            "query_id": item.get("query_id"),
            "user_input": q,
            "evaluation_group": item.get("evaluation_group"),
            "verification_reason": item.get("verification_reason"),
            "verified_trace_id": item.get("verified_trace_id"),
            "retrieval_metrics_eligible": retrieval_eligible,
        }
        result.update({metric: outcome.score for metric, outcome in metric_results.items()})
        result.update({f"{metric}_status": "scored" if outcome.error is None else outcome.error for metric, outcome in metric_results.items()})
        return result


def summarize_metrics(df: pd.DataFrame) -> dict[str, dict[str, float | int | None]]:
    metrics = (
        "context_precision",
        "context_recall",
        "faithfulness",
        "answer_relevancy",
        "answer_correctness",
    )
    summary: dict[str, dict[str, float | int | None]] = {}
    for metric in metrics:
        scores = pd.to_numeric(df[metric], errors="coerce")
        statuses = df[f"{metric}_status"].fillna("")
        summary[metric] = {
            "mean": round(float(scores.mean()), 4) if scores.notna().any() else None,
            "evaluated": int(scores.notna().sum()),
            "not_applicable": int(statuses.eq("not_applicable_unverified_retrieval").sum()),
            "judge_errors": int(statuses.str.contains(":", regex=False).sum()),
        }
    return summary


async def run_evaluation():
    trace_path = DEFAULT_OUTPUT_PATH
    if not trace_path.exists():
        print(f"❌ Không tìm thấy tập dữ liệu đã kiểm tra provenance tại: {trace_path}")
        print("Hãy chạy scripts/ragas_dataset_validation.py trước khi chấm bằng LLM.")
        return

    trace_data = load_provenance_checked_cases(trace_path)

    print(f"🚀 BẮT ĐẦU ĐÁNH GIÁ LLM-AS-A-JUDGE ({JUDGE_MODEL}) CHO {len(trace_data)} TEST CASES...")
    print_summary(trace_data)

    sem = asyncio.Semaphore(5)
    results = await asyncio.gather(*[evaluate_item(item, sem) for item in trace_data])
    df = pd.DataFrame(results)

    print("\n📊 BÁO CÁO KẾT QUẢ ĐÁNH GIÁ CHI TIẾT PRODUCTION FLOW:")
    print(df.to_string(index=False))

    summary = summarize_metrics(df)

    print("\n=====================================================================")
    print("🏆 BẢNG TỔNG HỢP ĐIỂM SỐ LLM-AS-A-JUDGE:")
    print("=====================================================================")
    for metric, values in summary.items():
        mean = values["mean"]
        display_mean = f"{mean:.4f}" if mean is not None else "N/A"
        print(
            f"   • {metric:<25}: {display_mean} / 1.0000 "
            f"(n={values['evaluated']}, N/A={values['not_applicable']}, judge_errors={values['judge_errors']})"
        )
    print("=====================================================================")

    # Tạo timestamp cho lịch sử chạy để không ghi đè kết quả judge cũ.
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    history_csv = trace_path.parent / f"production_flow_llm_judge_report_{now_str}.csv"
    latest_csv = trace_path.parent / "production_flow_llm_judge_report_latest.csv"

    # Lưu file lịch sử và đồng thời cập nhật file latest chính
    df.to_csv(history_csv, index=False, encoding="utf-8-sig")
    df.to_csv(latest_csv, index=False, encoding="utf-8-sig")
    summary_path = trace_path.parent / f"production_flow_llm_judge_summary_{now_str}.json"
    summary_path.write_text(
        json.dumps(
            {
                "judge_model": JUDGE_MODEL,
                "input_dataset": str(trace_path),
                "input_dataset_sha256": hashlib.sha256(trace_path.read_bytes()).hexdigest(),
                "total_cases": len(trace_data),
                "evaluation_groups": {key: int(value) for key, value in df["evaluation_group"].value_counts().items()},
                "metrics": summary,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"\n💾 Đã lưu lịch sử chạy tại : {history_csv}")
    print(f"🔄 Đã cập nhật file latest tại : {latest_csv}")
    print(f"📋 Đã lưu thống kê metric tại : {summary_path}")


def main():
    asyncio.run(run_evaluation())


if __name__ == "__main__":
    main()

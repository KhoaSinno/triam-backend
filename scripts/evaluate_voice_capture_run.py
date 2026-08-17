"""Evaluate verified RAG turns captured from local voice sessions.

This script intentionally evaluates only Faithfulness, Context Recall and
Context Precision. It never treats metadata, policy, or incomplete captures as
RAG retrieval evidence. The metrics are custom LLM-as-a-Judge implementations
that follow the corresponding RAGAS metric principles; this is not a call to
the RAGAS package.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import math
import os
import re
import statistics
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import AsyncOpenAI

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REFERENCE_LATEX = (
    PROJECT_ROOT.parent / "2022DoAnTN_KhoaDat" / "noidung" / "phuluc" / "pl_kich_ban_ragas.tex"
)
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "logs" / "ragas_eval" / "voice_capture_evaluations"
DEFAULT_CASE_SCOPE_MANIFEST = PROJECT_ROOT / "tests" / "fixtures" / "agent_eval" / "voice_capture_case_scopes.json"
JUDGE_MODEL = "gemini-3.5-flash-lite"


def clean_latex_text(value: str) -> str:
    text = value.replace("\\newline", " ").replace("\\&", "&").replace("~", " ")
    for _ in range(3):
        text = re.sub(r"\\(?:textbf|textit|texttt|emph)\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+", " ", text)
    text = text.replace("{", "").replace("}", "").replace("\\", " ")
    return " ".join(text.split())


def load_references_from_latex(path: Path) -> dict[int, str]:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"\\textbf\{Q\s*(?P<number>\d+)\s*:\s*User hỏi.*?"
        r"\\textbf\{Đáp Án\}\s*&\s*(?P<answer>.*?)\\\\\s*\\hline",
        flags=re.DOTALL,
    )
    references: dict[int, str] = {}
    for match in pattern.finditer(text):
        answer = clean_latex_text(match.group("answer"))
        if answer:
            references[int(match.group("number"))] = answer
    return references


def case_number(case_id: object) -> int | None:
    match = re.search(r"Q(\d+)$", str(case_id or "").strip(), flags=re.IGNORECASE)
    return int(match.group(1)) if match else None


def split_rendered_context(value: object) -> list[str]:
    text = str(value or "")
    chunks = [part.strip() for part in re.split(r"(?=--- Source \d+)", text)]
    return [chunk for chunk in chunks if chunk.startswith("--- Source")]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_case_scopes(path: Path) -> dict[str, dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    cases = payload.get("cases") if isinstance(payload, dict) else None
    if not isinstance(cases, dict):
        raise ValueError("invalid_case_scope_manifest")
    scopes: dict[str, dict[str, str]] = {}
    for case_id, value in cases.items():
        if not isinstance(value, dict):
            raise ValueError(f"invalid_case_scope:{case_id}")
        scope = str(value.get("scope") or "").strip()
        reason = str(value.get("reason") or "").strip()
        if not scope or not reason:
            raise ValueError(f"missing_case_scope_fields:{case_id}")
        scopes[str(case_id)] = {"scope": scope, "reason": reason}
    return scopes


def build_verified_case(
    payload: dict[str, Any],
    *,
    path: Path,
    run_dir: Path,
    references: dict[int, str],
    seen_case_ids: set[str],
    case_scopes: dict[str, dict[str, str]],
) -> tuple[dict[str, Any] | None, str]:
    trace = payload.get("trace") if isinstance(payload.get("trace"), dict) else {}
    user = payload.get("user") if isinstance(payload.get("user"), dict) else {}
    assistant = payload.get("assistant") if isinstance(payload.get("assistant"), dict) else {}
    retrieved = payload.get("retrieved_context") if isinstance(payload.get("retrieved_context"), dict) else {}
    case_id = str(payload.get("case_id") or "").strip()
    contexts = split_rendered_context(retrieved.get("rendered_context"))
    question_number = case_number(case_id)
    reference = references.get(question_number) if question_number is not None else None
    scope = case_scopes.get(case_id)
    checks = (
        (payload.get("evaluation_status") != "accepted", "not_accepted"),
        (trace.get("answer_source") != "book_rag", f"answer_source_{trace.get('answer_source') or 'missing'}"),
        (bool(trace.get("error_code")), "trace_error"),
        (not trace.get("transcript_final_seen"), "missing_final_transcript"),
        (not case_id, "missing_case_id"),
        (not str(user.get("text") or "").strip() or not str(assistant.get("text") or "").strip(), "missing_user_or_assistant_text"),
        (not contexts, "missing_rendered_rag_context"),
        (not reference, "missing_reference_for_case_id"),
        (case_id in seen_case_ids, "duplicate_case_id"),
        (scope is None, "missing_case_scope"),
        (
            scope is not None and scope["scope"] != "semantic_retrieval_single_turn",
            f"out_of_scope_{scope['scope']}" if scope is not None else "missing_case_scope",
        ),
    )
    reason = next((message for failed, message in checks if failed), "")
    if reason:
        return None, reason
    return (
        {
            "query_id": case_id,
            "run_id": str(payload.get("run_id") or run_dir.name),
            "trace_id": str(payload.get("trace_id") or trace.get("trace_id") or ""),
            "user_input": str(user["text"]),
            "response": str(assistant["text"]),
            "reference": reference,
            "contexts": contexts,
            "evaluation_group": "rag_retrieval_verified",
            "evaluation_scope": scope["scope"] if scope else None,
            "selection_reason": scope["reason"] if scope else None,
            "retrieval_metrics_eligible": True,
            "source_path": str(path),
        },
        "",
    )


def load_verified_cases(
    run_dirs: list[Path],
    references: dict[int, str],
    case_scopes: dict[str, dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    cases: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    seen_case_ids: set[str] = set()
    for run_dir in run_dirs:
        for path in sorted((run_dir / "turns").glob("*.json")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            case, reason = build_verified_case(
                payload,
                path=path,
                run_dir=run_dir,
                references=references,
                seen_case_ids=seen_case_ids,
                case_scopes=case_scopes,
            )
            if case is None:
                skipped.append({"path": str(path), "case_id": str(payload.get("case_id") or ""), "reason": reason})
                continue
            seen_case_ids.add(str(case["query_id"]))
            cases.append(case)
    return cases, skipped


def clamp(value: object) -> float:
    score = float(value)
    if not math.isfinite(score):
        raise ValueError("score_must_be_finite")
    return max(0.0, min(1.0, score))


def is_true(value: object) -> bool:
    return value in (True, 1) or str(value).lower() in ("true", "1")


def score_supported_claims(claims: object) -> tuple[float, list[dict[str, Any]]]:
    """Compute RAGAS-style claim coverage instead of accepting an LLM scalar."""
    if not isinstance(claims, list) or not claims:
        raise ValueError("missing_claims")
    if not all(isinstance(item, dict) and str(item.get("claim") or "").strip() for item in claims):
        raise ValueError("invalid_claims")
    normalized_claims = [dict(item) for item in claims]
    supported = sum(is_true(item.get("is_supported")) for item in normalized_claims)
    return clamp(supported / len(normalized_claims)), normalized_claims


async def call_judge(client: AsyncOpenAI, prompt: str) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(5):
        try:
            response = await client.chat.completions.create(
                model=JUDGE_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                response_format={"type": "json_object"},
            )
            payload = json.loads(response.choices[0].message.content)
            if not isinstance(payload, dict):
                raise ValueError("judge_response_is_not_a_json_object")
            return payload
        except Exception as exc:
            last_error = exc
            if attempt < 4:
                await asyncio.sleep(2.0 * (attempt + 1))
    raise RuntimeError(f"judge_request_failed:{type(last_error).__name__ if last_error else 'unknown'}") from last_error


async def evaluate_faithfulness(client: AsyncOpenAI, contexts: list[str], response: str) -> float:
    context_text = "\n---\n".join(contexts)
    payload = await call_judge(
        client,
        "Ngữ cảnh nguồn:\n"
        f"{context_text}\n\nCâu trả lời:\n{response}\n\n"
        "Nhiệm vụ:\n"
        "1. Phân rã câu trả lời thành các mệnh đề khẳng định nhỏ (atomic claims).\n"
        "2. Kiểm tra xem từng mệnh đề có được suy ra trực tiếp từ ngữ cảnh nguồn hay không.\n"
        "Trả về định dạng JSON duy nhất:\n"
        '{"claims": [{"claim": "...", "is_supported": true/false}]}'
    )
    claims = payload.get("claims")
    if not isinstance(claims, list) or not claims:
        raise ValueError("missing_claims")
    score, _ = score_supported_claims(claims)
    return score


async def evaluate_context_recall(
    client: AsyncOpenAI,
    reference: str,
    contexts: list[str],
) -> tuple[float, list[dict[str, Any]]]:
    payload = await call_judge(
        client,
        f"Đáp án chuẩn (Reference): {reference}\n\n"
        f"Các đoạn ngữ cảnh trích xuất (Retrieved Contexts):\n{'\n---\n'.join(contexts)}\n\n"
        "Nhiệm vụ:\n"
        "1. Phân rã Đáp án chuẩn thành các mệnh đề thông tin nhỏ, không trùng lặp (atomic claims).\n"
        "2. Với từng mệnh đề, xác định nó có được suy ra trực tiếp từ các đoạn ngữ cảnh trích xuất hay không.\n"
        "Không tự chấm một điểm tổng quát.\n"
        'Trả về JSON duy nhất: {"claims": [{"claim": "...", "is_supported": true/false}]}',
    )
    return score_supported_claims(payload.get("claims"))


async def evaluate_context_precision(client: AsyncOpenAI, question: str, reference: str, contexts: list[str]) -> float:
    formatted_contexts = "\n".join(f"Chunk [{index}]: {context}" for index, context in enumerate(contexts, start=1))
    payload = await call_judge(
        client,
        f"Câu hỏi: {question}\n\nĐáp án chuẩn: {reference}\n\n"
        "Danh sách các đoạn ngữ cảnh trích xuất theo thứ tự xếp hạng (từ Top 1 đến Top K):\n"
        f"{formatted_contexts}\n\n"
        "Nhiệm vụ: Kiểm tra từng Chunk xem nó có thông tin liên quan để hỗ trợ đáp án chuẩn hay không.\n"
        'Trả về kết quả dưới định dạng JSON duy nhất: {"verdicts": [true/false cho Chunk 1, true/false cho Chunk 2, ...]}',
    )
    verdicts = payload.get("verdicts")
    if not isinstance(verdicts, list) or len(verdicts) != len(contexts):
        raise ValueError("invalid_verdict_count")
    relevant = 0
    sum_precision = 0.0
    for rank, verdict in enumerate(verdicts, start=1):
        is_relevant = verdict in (True, 1) or str(verdict).lower() in ("true", "1")
        if is_relevant:
            relevant += 1
            sum_precision += relevant / rank
    return 0.0 if relevant == 0 else clamp(sum_precision / relevant)


async def judge_case(client: AsyncOpenAI, case: dict[str, Any], semaphore: asyncio.Semaphore) -> dict[str, Any]:
    async with semaphore:
        result = {key: case[key] for key in ("query_id", "run_id", "trace_id", "source_path")}
        metrics = {
            "faithfulness": evaluate_faithfulness(client, case["contexts"], case["response"]),
            "context_precision": evaluate_context_precision(
                client, case["user_input"], case["reference"], case["contexts"]
            ),
        }
        for metric, coroutine in metrics.items():
            try:
                result[metric] = await coroutine
                result[f"{metric}_status"] = "scored"
            except Exception as exc:
                result[metric] = None
                result[f"{metric}_status"] = f"{type(exc).__name__}:{str(exc)[:160]}"
        try:
            context_recall, recall_claims = await evaluate_context_recall(
                client,
                case["reference"],
                case["contexts"],
            )
            result["context_recall"] = context_recall
            result["context_recall_claims"] = recall_claims
            result["context_recall_status"] = "scored"
        except Exception as exc:
            result["context_recall"] = None
            result["context_recall_status"] = f"{type(exc).__name__}:{str(exc)[:160]}"
        return result


def metric_summary(rows: list[dict[str, Any]]) -> dict[str, dict[str, float | int | None]]:
    summary: dict[str, dict[str, float | int | None]] = {}
    for metric in ("faithfulness", "context_recall", "context_precision"):
        scores = [float(row[metric]) for row in rows if isinstance(row.get(metric), int | float)]
        summary[metric] = {
            "mean": round(sum(scores) / len(scores), 4) if scores else None,
            "evaluated": len(scores),
            "judge_errors": sum(row.get(f"{metric}_status") != "scored" for row in rows),
        }
    return summary


def median_run_summary(summaries: list[dict[str, dict[str, float | int | None]]]) -> dict[str, dict[str, float | int | list[float] | None]]:
    """Summarize repeated judge runs using the median of their per-run means."""
    result: dict[str, dict[str, float | int | list[float] | None]] = {}
    for metric in ("faithfulness", "context_recall", "context_precision"):
        run_means = [float(summary[metric]["mean"]) for summary in summaries if summary[metric]["mean"] is not None]
        result[metric] = {
            "median_of_run_means": round(float(statistics.median(run_means)), 4) if run_means else None,
            "run_means": [round(value, 4) for value in run_means],
            "min_run_mean": round(min(run_means), 4) if run_means else None,
            "max_run_mean": round(max(run_means), 4) if run_means else None,
            "completed_runs": len(run_means),
        }
    return result


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate verified RAG voice-capture turns with LLM-as-a-Judge.")
    parser.add_argument("--run-dir", type=Path, action="append", required=True, help="Capture run directory; repeat for more runs.")
    parser.add_argument("--reference-latex", type=Path, default=DEFAULT_REFERENCE_LATEX)
    parser.add_argument("--case-scope-manifest", type=Path, default=DEFAULT_CASE_SCOPE_MANIFEST)
    parser.add_argument("--repeat", type=int, default=1, help="Number of complete judge repetitions.")
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument(
        "--reuse-results-dir",
        type=Path,
        default=None,
        help="Recompute a scoped report from prior judge_rows_run_*.json without API calls.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate and write the frozen dataset without API calls.")
    return parser.parse_args()


async def main_async(args: argparse.Namespace) -> int:
    references = load_references_from_latex(args.reference_latex)
    case_scopes = load_case_scopes(args.case_scope_manifest)
    cases, skipped = load_verified_cases(args.run_dir, references, case_scopes)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = args.output_dir or DEFAULT_OUTPUT_ROOT / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)

    write_json(output_dir / "voice_rag_dataset.json", cases)
    write_json(
        output_dir / "manifest.json",
        {
            "created_at": datetime.now().isoformat(),
            "judge_model": JUDGE_MODEL,
            "run_directories": [str(path) for path in args.run_dir],
            "reference_latex": str(args.reference_latex),
            "reference_latex_sha256": _sha256(args.reference_latex),
            "case_scope_manifest": str(args.case_scope_manifest),
            "case_scope_manifest_sha256": _sha256(args.case_scope_manifest),
            "source_turn_sha256": {
                str(path): _sha256(path)
                for run_dir in args.run_dir
                for path in sorted((run_dir / "turns").glob("*.json"))
            },
            "eligible_cases": len(cases),
            "skipped_cases": Counter(item["reason"] for item in skipped),
        },
    )
    write_json(output_dir / "skipped_cases.json", skipped)
    print(f"Verified RAG cases: {len(cases)} | skipped: {len(skipped)} | output: {output_dir}")
    if args.dry_run:
        return 0
    if not cases:
        raise ValueError("No verified RAG cases available for judge evaluation.")

    if args.reuse_results_dir is not None:
        eligible_case_ids = {str(case["query_id"]) for case in cases}
        source_rows = sorted(args.reuse_results_dir.glob("judge_rows_run_*.json"))
        if not source_rows:
            raise ValueError("No prior judge_rows_run_*.json files found for reuse.")
        all_summaries: list[dict[str, Any]] = []
        for source_path in source_rows:
            rows = json.loads(source_path.read_text(encoding="utf-8"))
            if not isinstance(rows, list):
                raise ValueError(f"invalid_prior_judge_rows:{source_path.name}")
            scoped_rows = [row for row in rows if isinstance(row, dict) and str(row.get("query_id")) in eligible_case_ids]
            if len(scoped_rows) != len(eligible_case_ids):
                raise ValueError(f"missing_prior_judge_rows:{source_path.name}")
            run_number = re.search(r"run_(\d+)$", source_path.stem)
            label = run_number.group(1) if run_number else str(len(all_summaries) + 1)
            summary = metric_summary(scoped_rows)
            write_json(output_dir / f"judge_rows_run_{label}.json", scoped_rows)
            write_json(output_dir / f"judge_summary_run_{label}.json", summary)
            all_summaries.append(summary)
        write_json(output_dir / "judge_summaries.json", all_summaries)
        median_summary = median_run_summary(all_summaries)
        write_json(output_dir / "judge_median_summary.json", median_summary)
        write_json(output_dir / "reuse_source.json", {"source_results_dir": str(args.reuse_results_dir)})
        print(f"Reused {len(all_summaries)} prior judge runs without API calls.")
        print(f"Median of run means: {json.dumps(median_summary, ensure_ascii=False)}")
        return 0

    load_dotenv(override=True)
    client = AsyncOpenAI(api_key=os.environ["GEMINI_API_KEY"], base_url=os.environ["GEMINI_BASE_URL"])
    repeats = max(1, args.repeat)
    all_summaries: list[dict[str, Any]] = []
    for repetition in range(1, repeats + 1):
        semaphore = asyncio.Semaphore(4)
        rows = await asyncio.gather(*(judge_case(client, case, semaphore) for case in cases))
        summary = metric_summary(rows)
        write_json(output_dir / f"judge_rows_run_{repetition}.json", rows)
        write_json(output_dir / f"judge_summary_run_{repetition}.json", summary)
        all_summaries.append(summary)
        print(f"Run {repetition}/{repeats}: {json.dumps(summary, ensure_ascii=False)}")
    write_json(output_dir / "judge_summaries.json", all_summaries)
    median_summary = median_run_summary(all_summaries)
    write_json(output_dir / "judge_median_summary.json", median_summary)
    print(f"Median of run means: {json.dumps(median_summary, ensure_ascii=False)}")
    return 0


def main() -> None:
    args = parse_args()
    raise SystemExit(asyncio.run(main_async(args)))


if __name__ == "__main__":
    main()

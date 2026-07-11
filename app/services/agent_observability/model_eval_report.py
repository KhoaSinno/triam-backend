from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

MODEL_CONFIG_KEYS = (
    "AGENT_MODEL_PROFILE",
    "VOICE_AGENT_TEXT_LLM_MODEL",
    "OPENAI_STREAM_MODEL_NAME",
    "OPENAI_REALTIME_TRANSCRIPTION_MODEL",
    "VOICE_AGENT_PERMISSION_CLASSIFIER_MODEL",
)
RUNTIME_CONFIG_KEYS = (
    "BOOK_SECTION_EMBEDDING_VERSION",
    "BOOK_SECTION_RAG_MATCH_THRESHOLD",
    "BOOK_SECTION_RAG_MATCH_COUNT",
)
REPORT_CONFIG_KEYS = MODEL_CONFIG_KEYS + RUNTIME_CONFIG_KEYS
MODEL_ENV_ALLOWLIST = set(MODEL_CONFIG_KEYS) - {"AGENT_MODEL_PROFILE"}
BOOK_SOURCES = {"book_metadata", "book_section", "book_rag"}
SNAPSHOT_COMPARE_KEYS = (
    "database_label",
    "book_id",
    "book_sections_count",
    "book_section_knowledge_count",
    "embedding_model",
    "embedding_version",
    "outline_hash",
    "app_git_sha",
)


def _trace_section_ids(trace: dict[str, Any] | None) -> set[str]:
    if not trace:
        return set()
    return set(trace.get("resolved_section_ids") or []) | set(trace.get("retrieval_section_ids") or [])


def _section_failure_is_trace_coverage(
    checks: dict[str, bool | None],
    trace: dict[str, Any] | None,
) -> bool:
    return (
        not _trace_section_ids(trace)
        and checks.get("expected_intent") is True
        and checks.get("expected_answer_source") is True
        and checks.get("must_include") is not False
        and checks.get("must_not_include") is not False
    )


def _content_failure_is_fixture_review(
    checks: dict[str, bool | None],
    actual_source: Any,
) -> bool:
    return (
        checks.get("expected_intent") is True
        and checks.get("expected_answer_source") is True
        and checks.get("expected_section") in (True, None)
        and actual_source in {"book_metadata", "book_section"}
    )


def _input_and_web_failures(
    case: dict[str, Any],
    checks: dict[str, bool | None],
    *,
    actual_source: Any,
) -> list[str]:
    failures: list[str] = []
    expected_source = case.get("expected_answer_source")
    if checks.get("trace_available") is False:
        failures.append("TRACE_COVERAGE")
    if checks.get("voice_transcript_meaning") is False:
        failures.append("INPUT_STT")
    if checks.get("web_not_used_without_permission") is False:
        failures.append("WEB_PERMISSION")
    if checks.get("expected_answer_source") is False and expected_source in BOOK_SOURCES and actual_source in {"policy", "web"}:
        failures.append("WEB_PERMISSION")
    return failures


def _routing_failures(
    checks: dict[str, bool | None],
    trace: dict[str, Any] | None,
) -> list[str]:
    failures: list[str] = []
    if checks.get("expected_intent") is False:
        failures.append("ROUTING_INTENT")
    if checks.get("expected_section") is False:
        failures.append("TRACE_COVERAGE" if _section_failure_is_trace_coverage(checks, trace) else "ROUTING_SECTION")
    return failures


def _content_failures(
    checks: dict[str, bool | None],
    *,
    actual_source: Any,
    retrieval_count: int,
) -> list[str]:
    if checks.get("must_include") is not False and checks.get("must_not_include") is not False:
        return []
    if _content_failure_is_fixture_review(checks, actual_source):
        return ["EVAL_FIXTURE_MISMATCH"]
    return ["RETRIEVAL_RELEVANCE" if retrieval_count else "RETRIEVAL_COVERAGE"]


def _voice_tool_bypass_failures(
    case: dict[str, Any],
    checks: dict[str, bool | None],
    trace: dict[str, Any] | None,
) -> list[str]:
    if trace is None:
        return []
    if case.get("input_mode") != "voice":
        return []
    if case.get("expected_answer_source") not in BOOK_SOURCES:
        return []
    if checks.get("voice_transcript_meaning") is False:
        return []
    if checks.get("must_include") is False or checks.get("must_not_include") is False:
        return []

    actual_source = str(trace.get("answer_source") or "unknown").casefold()
    tool_names = trace.get("tool_names") or []
    if actual_source in {"unknown", "none", ""} and not tool_names:
        return ["VOICE_TOOL_BYPASS"]
    return []


def percentile(values: list[int], quantile: float) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * quantile
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return round(ordered[lower] + (ordered[upper] - ordered[lower]) * fraction)


def latency_summary(values: list[int]) -> dict[str, int | None]:
    return {
        "samples": len(values),
        "p50_ms": percentile(values, 0.50),
        "p95_ms": percentile(values, 0.95),
        "max_ms": max(values) if values else None,
    }


def classify_failure_codes(
    case: dict[str, Any],
    checks: dict[str, bool | None],
    trace: dict[str, Any] | None,
) -> list[str]:
    failures: list[str] = []
    actual_source = trace.get("answer_source") if trace else None
    retrieval_count = int(trace.get("retrieval_result_count") or 0) if trace else 0

    failures.extend(_input_and_web_failures(case, checks, actual_source=actual_source))
    failures.extend(_voice_tool_bypass_failures(case, checks, trace))
    if "VOICE_TOOL_BYPASS" not in failures:
        failures.extend(_routing_failures(checks, trace))
        if checks.get("expected_answer_source") is False and "WEB_PERMISSION" not in failures:
            failures.append("CONTEXT_VALIDATION")
        failures.extend(_content_failures(checks, actual_source=actual_source, retrieval_count=retrieval_count))

    return list(dict.fromkeys(failures)) or ["UNKNOWN"]


def classify_exception_failure_codes(
    *,
    input_mode: str,
    error_type: str,
    error_message: str,
) -> list[str]:
    normalized = f"{error_type} {error_message}".casefold()
    if input_mode == "voice" and "transcript role=user" in normalized:
        return ["NO_USER_TRANSCRIPT"]
    if "timeout" in normalized or "timed out" in normalized:
        return ["INPUT_TIMEOUT"]
    if "voice fixture" in normalized or "wav" in normalized:
        return ["INPUT_AUDIO_FIXTURE"]
    return ["UNKNOWN"]


def build_metrics(results: list[dict[str, Any]]) -> dict[str, Any]:
    check_names = {
        "content_accuracy": ("must_include", "must_not_include"),
        "intent_accuracy": ("expected_intent",),
        "answer_source_accuracy": ("expected_answer_source",),
        "section_resolution_accuracy": ("expected_section",),
        "web_policy_safety_rate": ("web_not_used_without_permission",),
        "voice_meaning_preservation_rate": ("voice_transcript_meaning",),
    }
    accuracy: dict[str, dict[str, int | float]] = {}
    for metric_name, names in check_names.items():
        values: list[bool] = []
        for result in results:
            checks = result.get("checks") or {}
            selected = [checks.get(name) for name in names if checks.get(name) is not None]
            if selected:
                values.append(all(selected))
        passed = sum(values)
        accuracy[metric_name] = {
            "passed": passed,
            "evaluated": len(values),
            "rate": round(passed / len(values), 4) if values else 0.0,
        }

    latency: dict[str, dict[str, dict[str, int | None]]] = {}
    for mode in ("text", "voice"):
        mode_results = [result for result in results if result.get("input_mode") == mode]
        turn_values = [
            int(result["trace"]["stage_latency_ms"]["turn_total"])
            for result in mode_results
            if result.get("trace") and result["trace"].get("stage_latency_ms", {}).get("turn_total") is not None
        ]
        retrieval_values = [
            int(result["trace"]["stage_latency_ms"]["retrieval"])
            for result in mode_results
            if result.get("trace") and result["trace"].get("stage_latency_ms", {}).get("retrieval") is not None
        ]
        if mode_results:
            latency[mode] = {
                "turn_total": latency_summary(turn_values),
                "retrieval": latency_summary(retrieval_values),
            }

    failure_counts = Counter(code for result in results for code in result.get("failure_codes", []))
    warning_counts = Counter(code for result in results for code in result.get("warnings", []))
    web_permission_violations = failure_counts.get("WEB_PERMISSION", 0)
    return {
        "strict_case_pass_rate": round(sum(result.get("status") == "passed" for result in results) / len(results), 4) if results else 0.0,
        "accuracy": accuracy,
        "latency": latency,
        "failure_counts": dict(sorted(failure_counts.items())),
        "warning_counts": dict(sorted(warning_counts.items())),
        "web_permission_violations": web_permission_violations,
    }


def summarize_results(results: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "total": len(results),
        "passed": sum(result.get("status") == "passed" for result in results),
        "failed": sum(result.get("status") == "failed" for result in results),
    }


def safe_model_config_from_settings(settings_obj: Any) -> dict[str, str]:
    return {
        key: str(getattr(settings_obj, key, ""))
        for key in REPORT_CONFIG_KEYS
    }


def validate_candidate_matrix(candidates: list[dict[str, Any]]) -> None:
    seen_names: set[str] = set()
    for candidate in candidates:
        name = str(candidate.get("name") or "").strip()
        if not name:
            raise ValueError("Candidate matrix item is missing name.")
        if name in seen_names:
            raise ValueError(f"Duplicate candidate name: {name}")
        seen_names.add(name)

        env = candidate.get("env")
        if not isinstance(env, dict):
            raise ValueError(f"Candidate {name} env must be an object.")

        disallowed = sorted(set(env) - MODEL_ENV_ALLOWLIST)
        if disallowed:
            raise ValueError(f"Candidate {name} uses disallowed env keys: {', '.join(disallowed)}")

        if name != "baseline" and len(env) > 1 and not candidate.get("combined_experiment"):
            unique_values = {key: value for key, value in env.items() if value not in (None, "", "<candidate-model>", "<candidate-realtime-model>")}
            if len(unique_values) > 1:
                raise ValueError(f"Candidate {name} changes multiple model surfaces without combined_experiment=true.")


def load_candidate_matrix(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Candidate matrix must be a list.")
    validate_candidate_matrix(payload)
    return payload


def find_candidate(candidates: list[dict[str, Any]], name: str) -> dict[str, Any]:
    for candidate in candidates:
        if candidate.get("name") == name:
            return candidate
    raise ValueError(f"Candidate not found: {name}")


def _safe_outline_items(outline: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "id": str(item.get("id") or ""),
            "path": str(item.get("path") or ""),
            "title": str(item.get("title") or ""),
        }
        for item in outline
    ]


def build_snapshot_metadata(
    *,
    book: dict[str, Any],
    outline: list[dict[str, Any]],
    app_git_sha: str,
    database_label: str,
    embedding_model: str,
    embedding_version: str,
    book_section_knowledge_count: int | None = None,
) -> dict[str, Any]:
    safe_outline = _safe_outline_items(outline)
    outline_hash = hashlib.sha256(json.dumps(safe_outline, ensure_ascii=True, sort_keys=True).encode("utf-8")).hexdigest()
    return {
        "book_id": str(book.get("id") or ""),
        "thread_id": None,
        "book_sections_count": len(outline),
        "book_section_knowledge_count": book_section_knowledge_count,
        "embedding_model": embedding_model,
        "embedding_version": embedding_version,
        "outline_hash": outline_hash,
        "app_git_sha": app_git_sha,
        "database_label": database_label,
    }


def snapshots_compatible(baseline: dict[str, Any], candidate: dict[str, Any]) -> tuple[bool, list[str]]:
    mismatches: list[str] = []
    for key in SNAPSHOT_COMPARE_KEYS:
        left = baseline.get(key)
        right = candidate.get(key)
        if left in (None, "", "unknown") or right in (None, "", "unknown"):
            continue
        if left != right:
            mismatches.append(key)
    return not mismatches, mismatches


def _metric_rate(report: dict[str, Any], metric_name: str) -> float:
    return float(report.get("metrics", {}).get("accuracy", {}).get(metric_name, {}).get("rate", 0.0))


def compare_reports(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
    *,
    max_chat_p95_regression_ratio: float = 0.30,
    max_voice_p95_regression_ratio: float = 0.25,
) -> dict[str, Any]:
    compatible, snapshot_mismatches = snapshots_compatible(baseline.get("snapshot") or {}, candidate.get("snapshot") or {})
    hard_gate_failures: list[str] = []
    warnings: list[str] = []

    if not compatible:
        hard_gate_failures.append("SNAPSHOT_MISMATCH")

    if int(candidate.get("metrics", {}).get("web_permission_violations") or 0) > 0:
        hard_gate_failures.append("WEB_PERMISSION_VIOLATION")

    if _metric_rate(candidate, "answer_source_accuracy") < _metric_rate(baseline, "answer_source_accuracy"):
        hard_gate_failures.append("SOURCE_ACCURACY_REGRESSION")

    if _metric_rate(candidate, "content_accuracy") < _metric_rate(baseline, "content_accuracy"):
        hard_gate_failures.append("CONTENT_ACCURACY_REGRESSION")

    latency_warnings = _compare_latency_regression(
        baseline,
        candidate,
        max_chat_p95_regression_ratio=max_chat_p95_regression_ratio,
        max_voice_p95_regression_ratio=max_voice_p95_regression_ratio,
    )
    warnings.extend(latency_warnings)

    recommendation = "go" if not hard_gate_failures else "no-go"
    return {
        "recommendation": recommendation,
        "hard_gate_failures": hard_gate_failures,
        "warnings": warnings,
        "snapshot_mismatches": snapshot_mismatches,
        "baseline_candidate": baseline.get("candidate"),
        "candidate": candidate.get("candidate"),
        "metric_deltas": {
            name: round(_metric_rate(candidate, name) - _metric_rate(baseline, name), 4)
            for name in ("content_accuracy", "answer_source_accuracy", "intent_accuracy", "voice_meaning_preservation_rate")
        },
    }


def _compare_latency_regression(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
    *,
    max_chat_p95_regression_ratio: float,
    max_voice_p95_regression_ratio: float,
) -> list[str]:
    warnings: list[str] = []
    thresholds = {
        "text": max_chat_p95_regression_ratio,
        "voice": max_voice_p95_regression_ratio,
    }
    for mode, threshold in thresholds.items():
        base_p95 = baseline.get("metrics", {}).get("latency", {}).get(mode, {}).get("turn_total", {}).get("p95_ms")
        cand_p95 = candidate.get("metrics", {}).get("latency", {}).get(mode, {}).get("turn_total", {}).get("p95_ms")
        if not base_p95 or not cand_p95:
            continue
        if cand_p95 > base_p95 * (1 + threshold):
            warnings.append(f"{mode.upper()}_P95_LATENCY_REGRESSION")
    return warnings


def write_eval_reports(output_dir: Path, report: dict[str, Any], *, prefix: str = "phase10_7_eval") -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    candidate_name = str(report.get("candidate") or "unknown").replace(" ", "_")
    json_path = output_dir / f"{prefix}_{timestamp}_{candidate_name}.json"
    md_path = output_dir / f"{prefix}_{timestamp}_{candidate_name}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Phase 10 Agent Model Evaluation Run",
        "",
        f"- Candidate: `{report.get('candidate')}`",
        f"- Environment: `{report.get('environment')}`",
        f"- Book: `{report.get('ground_truth', {}).get('title')}`",
        f"- Cases: `{report.get('summary', {}).get('total')}`",
        f"- Passed: `{report.get('summary', {}).get('passed')}`",
        f"- Failed: `{report.get('summary', {}).get('failed')}`",
        f"- DB message delta: `{report.get('db_message_delta')}`",
        "",
    ]
    voice_isolation = report.get("voice_isolation")
    if isinstance(voice_isolation, dict):
        lines.extend(
            [
                "## Voice Isolation",
                "",
                f"- Enabled: `{voice_isolation.get('enabled')}`",
                f"- Strategy: `{voice_isolation.get('strategy')}`",
                f"- Isolation Quality: `{voice_isolation.get('quality')}`",
                f"- Eval Threads: `{voice_isolation.get('thread_count')}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Model Config",
            "",
            "| Key | Value |",
            "| --- | --- |",
        ]
    )
    lines.extend(f"| `{key}` | `{value}` |" for key, value in (report.get("model_config") or {}).items())
    lines.extend(
        [
            "",
            "## Snapshot",
            "",
            "| Key | Value |",
            "| --- | --- |",
        ]
    )
    lines.extend(f"| `{key}` | `{value}` |" for key, value in (report.get("snapshot") or {}).items())
    lines.extend(
        [
            "",
            "## Accuracy",
            "",
            "| Metric | Passed | Evaluated | Rate |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    lines.extend(
        f"| {name} | {metric['passed']} | {metric['evaluated']} | {metric['rate']:.1%} |"
        for name, metric in report.get("metrics", {}).get("accuracy", {}).items()
    )
    lines.extend(
        [
            "",
            "## Failures",
            "",
            "| Failure code | Count |",
            "| --- | ---: |",
        ]
    )
    lines.extend(f"| {code} | {count} |" for code, count in report.get("metrics", {}).get("failure_counts", {}).items())
    warning_counts = report.get("metrics", {}).get("warning_counts", {})
    if warning_counts:
        lines.extend(
            [
                "",
                "## Warnings",
                "",
                "| Warning code | Count |",
                "| --- | ---: |",
            ]
        )
        lines.extend(f"| {code} | {count} |" for code, count in warning_counts.items())
    lines.extend(
        [
            "",
            "## Cases",
            "",
            "| Case | Mode | Status |",
            "| --- | --- | --- |",
        ]
    )
    lines.extend(f"| {result['id']} | {result['input_mode']} | {result['status']} |" for result in report.get("results", []))
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path

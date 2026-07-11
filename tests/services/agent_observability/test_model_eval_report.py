from pathlib import Path

import pytest

from app.services.agent_observability.model_eval_report import (
    build_metrics,
    classify_exception_failure_codes,
    classify_failure_codes,
    compare_reports,
    load_candidate_matrix,
    snapshots_compatible,
    validate_candidate_matrix,
    write_eval_reports,
)


def _result(status: str, *, source_ok: bool = True, content_ok: bool = True, web_ok: bool = True) -> dict:
    failures = []
    if not web_ok:
        failures.append("WEB_PERMISSION")
    return {
        "id": "case-1",
        "input_mode": "text",
        "status": status,
        "failure_codes": failures,
        "checks": {
            "must_include": content_ok,
            "must_not_include": content_ok,
            "expected_intent": True,
            "expected_answer_source": source_ok,
            "expected_section": None,
            "web_not_used_without_permission": web_ok,
            "voice_transcript_meaning": None,
        },
        "trace": {
            "stage_latency_ms": {
                "turn_total": 1000,
                "retrieval": 100,
            }
        },
    }


def _report(name: str, results: list[dict], *, snapshot: dict | None = None) -> dict:
    return {
        "candidate": name,
        "snapshot": snapshot
        or {
            "database_label": "dev",
            "book_id": "book-1",
            "book_sections_count": 3,
            "book_section_knowledge_count": 10,
            "embedding_model": "text-embedding-3-small",
            "embedding_version": "section-v1",
            "outline_hash": "same",
            "app_git_sha": "abc",
        },
        "metrics": build_metrics(results),
    }


def test_candidate_matrix_fixture_validates_successfully():
    candidates = load_candidate_matrix(Path("tests/fixtures/agent_eval/model_candidate_matrix.json"))

    assert candidates[0]["name"] == "baseline"


def test_candidate_matrix_rejects_disallowed_env_key():
    with pytest.raises(ValueError, match="disallowed env keys"):
        validate_candidate_matrix(
            [
                {
                    "name": "bad",
                    "description": "Bad candidate",
                    "env": {"OPENAI_API_KEY": "secret"},
                }
            ]
        )


def test_candidate_matrix_allows_baseline_to_document_multiple_surfaces():
    validate_candidate_matrix(
        [
            {
                "name": "baseline",
                "description": "Full production defaults",
                "env": {
                    "VOICE_AGENT_TEXT_LLM_MODEL": "gpt-4o-mini",
                    "OPENAI_STREAM_MODEL_NAME": "gpt-realtime",
                },
            }
        ]
    )


def test_safe_model_config_includes_section_rag_runtime_flags():
    from app.core.config import settings
    from app.services.agent_observability.model_eval_report import safe_model_config_from_settings

    config = safe_model_config_from_settings(settings)

    assert "BOOK_SECTION_EMBEDDING_VERSION" in config
    assert "BOOK_SECTION_RAG_MATCH_THRESHOLD" in config
    assert "BOOK_SECTION_RAG_MATCH_COUNT" in config
    # AGENT_HYBRID_RAG_ENABLED đã bị xóa vì Hybrid RAG luôn bật
    assert "AGENT_HYBRID_RAG_ENABLED" not in config


def test_classify_failure_codes_marks_missing_section_trace_as_trace_coverage():
    case = {"expected_answer_source": "book_rag"}
    checks = {
        "trace_available": True,
        "voice_transcript_meaning": None,
        "web_not_used_without_permission": True,
        "expected_intent": True,
        "expected_answer_source": True,
        "expected_section": False,
        "must_include": True,
        "must_not_include": True,
    }
    trace = {
        "answer_source": "book_rag",
        "retrieval_result_count": 10,
        "resolved_section_ids": [],
        "retrieval_section_ids": [],
    }

    failures = classify_failure_codes(case, checks, trace)

    assert failures == ["TRACE_COVERAGE"]


def test_classify_failure_codes_marks_missing_trace_as_trace_coverage():
    failures = classify_failure_codes(
        {"expected_answer_source": "book_section"},
        {
            "trace_available": False,
            "must_include": True,
            "must_not_include": True,
            "expected_intent": None,
            "expected_answer_source": None,
            "expected_section": None,
            "web_not_used_without_permission": None,
            "voice_transcript_meaning": None,
        },
        None,
    )

    assert failures == ["TRACE_COVERAGE"]


def test_classify_failure_codes_marks_direct_section_content_gap_as_fixture_review():
    case = {"expected_answer_source": "book_section"}
    checks = {
        "trace_available": True,
        "voice_transcript_meaning": None,
        "web_not_used_without_permission": True,
        "expected_intent": True,
        "expected_answer_source": True,
        "expected_section": True,
        "must_include": False,
        "must_not_include": True,
    }
    trace = {
        "answer_source": "book_section",
        "retrieval_result_count": 0,
        "resolved_section_ids": ["section-5"],
        "retrieval_section_ids": [],
    }

    failures = classify_failure_codes(case, checks, trace)

    assert failures == ["EVAL_FIXTURE_MISMATCH"]


def test_classify_failure_codes_marks_voice_tool_bypass_for_grounded_book_answer():
    case = {
        "input_mode": "voice",
        "expected_answer_source": "book_section",
    }
    checks = {
        "trace_available": True,
        "voice_transcript_meaning": True,
        "web_not_used_without_permission": True,
        "expected_intent": False,
        "expected_answer_source": False,
        "expected_section": False,
        "must_include": True,
        "must_not_include": True,
    }
    trace = {
        "answer_source": "unknown",
        "tool_names": [],
        "retrieval_result_count": 0,
    }

    failures = classify_failure_codes(case, checks, trace)

    assert failures == ["VOICE_TOOL_BYPASS"]


def test_classify_failure_codes_does_not_mark_voice_tool_bypass_when_stt_failed():
    case = {
        "input_mode": "voice",
        "expected_answer_source": "book_section",
    }
    checks = {
        "trace_available": True,
        "voice_transcript_meaning": False,
        "web_not_used_without_permission": True,
        "expected_intent": False,
        "expected_answer_source": False,
        "expected_section": False,
        "must_include": True,
        "must_not_include": True,
    }
    trace = {
        "answer_source": "unknown",
        "tool_names": [],
        "retrieval_result_count": 0,
    }

    failures = classify_failure_codes(case, checks, trace)

    assert "INPUT_STT" in failures
    assert "VOICE_TOOL_BYPASS" not in failures


def test_classify_exception_failure_codes_separates_voice_transcript_timeout():
    failures = classify_exception_failure_codes(
        input_mode="voice",
        error_type="RuntimeError",
        error_message="Timeout waiting for transcript role=user",
    )

    assert failures == ["NO_USER_TRANSCRIPT"]


def test_classify_exception_failure_codes_marks_generic_timeout():
    failures = classify_exception_failure_codes(
        input_mode="text",
        error_type="TimeoutError",
        error_message="request timed out",
    )

    assert failures == ["INPUT_TIMEOUT"]


def test_snapshot_compatibility_detects_rag_index_drift():
    baseline = {"book_id": "book-1", "outline_hash": "old", "database_label": "dev"}
    candidate = {"book_id": "book-1", "outline_hash": "new", "database_label": "dev"}

    compatible, mismatches = snapshots_compatible(baseline, candidate)

    assert compatible is False
    assert mismatches == ["outline_hash"]


def test_compare_reports_rejects_web_permission_violation():
    baseline = _report("baseline", [_result("passed")])
    candidate = _report("candidate", [_result("failed", web_ok=False)])

    comparison = compare_reports(baseline, candidate)

    assert comparison["recommendation"] == "no-go"
    assert "WEB_PERMISSION_VIOLATION" in comparison["hard_gate_failures"]


def test_compare_reports_rejects_snapshot_mismatch():
    baseline = _report("baseline", [_result("passed")])
    candidate = _report(
        "candidate",
        [_result("passed")],
        snapshot={
            "database_label": "dev",
            "book_id": "book-1",
            "book_sections_count": 4,
            "book_section_knowledge_count": 10,
            "embedding_model": "text-embedding-3-small",
            "embedding_version": "section-v1",
            "outline_hash": "same",
            "app_git_sha": "abc",
        },
    )

    comparison = compare_reports(baseline, candidate)

    assert comparison["recommendation"] == "no-go"
    assert "SNAPSHOT_MISMATCH" in comparison["hard_gate_failures"]
    assert comparison["snapshot_mismatches"] == ["book_sections_count"]


def test_compare_reports_allows_safe_candidate_with_equal_or_better_accuracy():
    baseline = _report("baseline", [_result("failed", source_ok=False), _result("passed")])
    candidate = _report("candidate", [_result("passed"), _result("passed")])

    comparison = compare_reports(baseline, candidate)

    assert comparison["recommendation"] == "go"
    assert comparison["hard_gate_failures"] == []
    assert comparison["metric_deltas"]["answer_source_accuracy"] > 0


def test_build_metrics_counts_non_fatal_warnings():
    metrics = build_metrics(
        [
            _result("passed"),
            {
                **_result("passed"),
                "warnings": ["INPUT_STT_MINOR"],
            },
        ]
    )

    assert metrics["warning_counts"] == {"INPUT_STT_MINOR": 1}


def test_write_eval_reports_renders_voice_isolation_section(tmp_path):
    report = {
        "candidate": "baseline",
        "environment": "local",
        "ground_truth": {"title": "Book"},
        "summary": {"total": 1, "passed": 1, "failed": 0},
        "db_message_delta": 2,
        "voice_isolation": {
            "enabled": True,
            "strategy": "case_thread_new_room",
            "quality": "thread_and_room",
            "thread_count": 5,
        },
        "model_config": {},
        "snapshot": {},
        "metrics": {"accuracy": {}, "failure_counts": {}, "warning_counts": {"INPUT_STT_MINOR": 1}},
        "results": [{"id": "case-1", "input_mode": "voice", "status": "passed", "warnings": ["INPUT_STT_MINOR"]}],
    }

    _, md_path = write_eval_reports(tmp_path, report, prefix="test_eval")

    content = md_path.read_text(encoding="utf-8")
    assert "## Voice Isolation" in content
    assert "- Strategy: `case_thread_new_room`" in content
    assert "- Isolation Quality: `thread_and_room`" in content
    assert "## Warnings" in content
    assert "| INPUT_STT_MINOR | 1 |" in content

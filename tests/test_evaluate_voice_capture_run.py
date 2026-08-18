from pathlib import Path

from scripts.evaluate_voice_capture_run import (
    build_verified_case,
    median_run_summary,
    score_supported_claims,
)


def test_verified_voice_case_requires_accepted_book_rag_with_rendered_context(tmp_path: Path):
    payload = {
        "run_id": "run-1",
        "trace_id": "trace-1",
        "evaluation_status": "accepted",
        "case_id": "S1-Q02",
        "trace": {
            "trace_id": "trace-1",
            "answer_source": "book_rag",
            "error_code": None,
            "transcript_final_seen": True,
        },
        "user": {"text": "Ai là nhân vật chính?"},
        "assistant": {"text": "George và Lennie."},
        "retrieved_context": {
            "rendered_context": "BOOK_CONTEXT_FOUND:\n--- Source 1 (Section: 1) ---\nGeorge and Lennie.",
        },
    }

    case, reason = build_verified_case(
        payload,
        path=tmp_path / "trace-1.json",
        run_dir=tmp_path,
        references={2: "George và Lennie là nhân vật chính."},
        seen_case_ids=set(),
        case_scopes={
            "S1-Q02": {
                "scope": "semantic_retrieval_single_turn",
                "reason": "Factual semantic retrieval case.",
            }
        },
    )

    assert reason == ""
    assert case is not None
    assert case["contexts"] == ["--- Source 1 (Section: 1) ---\nGeorge and Lennie."]
    assert case["retrieval_metrics_eligible"] is True


def test_context_recall_is_calculated_from_reference_claim_verdicts():
    score, claims = score_supported_claims(
        [
            {"claim": "George là nhân vật chính.", "is_supported": True},
            {"claim": "Lennie là nhân vật chính.", "is_supported": False},
        ]
    )

    assert score == 0.5
    assert len(claims) == 2


def test_median_summary_uses_median_of_per_run_means():
    summary = median_run_summary(
        [
            {metric: {"mean": first} for metric, first in (("faithfulness", 0.4), ("context_recall", 0.5), ("context_precision", 0.6))},
            {metric: {"mean": second} for metric, second in (("faithfulness", 0.8), ("context_recall", 0.7), ("context_precision", 0.9))},
            {metric: {"mean": third} for metric, third in (("faithfulness", 0.6), ("context_recall", 0.9), ("context_precision", 0.3))},
        ]
    )

    assert summary["faithfulness"]["median_of_run_means"] == 0.6
    assert summary["context_recall"]["median_of_run_means"] == 0.7
    assert summary["context_precision"]["median_of_run_means"] == 0.6

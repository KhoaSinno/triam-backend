import json

from scripts.ragas_dataset_validation import annotate_cases, load_provenance_checked_cases


def _write_turn_completed(log_path, *, trace_id="trace-1", chunk_ids=None, route="book_rag"):
    payload = {
        "trace_id": trace_id,
        "grounding_route": route,
        "retrieval_chunk_ids": chunk_ids or [],
    }
    log_path.write_text(f"AGENT_TRACE turn_completed | {json.dumps(payload)}\n", encoding="utf-8")


def test_annotate_cases_marks_exact_turn_context_as_retrieval_eligible(tmp_path):
    _write_turn_completed(tmp_path / "voice.md", chunk_ids=["101", "102", "103"])
    cases = annotate_cases(
        [
            {
                "query_id": "Q1",
                "intent_log_ref": "voice.md:L1",
                "contexts": ["first retrieved chunk"],
                "_contexts_source": "db:chunks=['101', '102', '103']",
                "reference": "reference",
                "response": "response",
            }
        ],
        log_dir=tmp_path,
    )

    assert cases[0]["evaluation_group"] == "rag_retrieval_verified"
    assert cases[0]["retrieval_metrics_eligible"] is True
    assert cases[0]["verified_trace_id"] == "trace-1"


def test_annotate_cases_rejects_context_from_another_turn_or_manual_lookup(tmp_path):
    _write_turn_completed(tmp_path / "voice.md", chunk_ids=["101", "102"])
    cases = annotate_cases(
        [
            {
                "query_id": "Q2",
                "intent_log_ref": "voice.md:L1",
                "contexts": ["manually selected context"],
                "_contexts_source": "db:book-section-keyword=search",
                "reference": "reference",
                "response": "response",
            }
        ],
        log_dir=tmp_path,
    )

    assert cases[0]["evaluation_group"] == "memory_or_unverifiable"
    assert cases[0]["retrieval_metrics_eligible"] is False


def test_annotate_cases_routes_metadata_away_from_retrieval_metrics(tmp_path):
    _write_turn_completed(tmp_path / "voice.md", route="book_metadata")
    cases = annotate_cases(
        [{"query_id": "Q3", "intent_log_ref": "voice.md:L1", "reference": "r", "response": "a"}],
        log_dir=tmp_path,
    )

    assert cases[0]["evaluation_group"] == "metadata_or_section"
    assert cases[0]["answer_metrics_eligible"] is True


def test_load_provenance_checked_cases_requires_annotation_fields(tmp_path):
    dataset_path = tmp_path / "checked.json"
    dataset_path.write_text(json.dumps([{"query_id": "Q1"}]), encoding="utf-8")

    try:
        load_provenance_checked_cases(dataset_path)
    except ValueError as exc:
        assert "not provenance-checked" in str(exc)
    else:
        raise AssertionError("Expected an unannotated dataset to be rejected")

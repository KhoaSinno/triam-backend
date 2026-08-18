import json

from app.services.agent_observability.local_eval_capture import LocalEvaluationCapture


def test_local_eval_capture_merges_voice_turn_artifacts(tmp_path):
    capture = LocalEvaluationCapture(
        enabled=True,
        run_id="voice session 01",
        root_dir=str(tmp_path),
        thread_id="thread-1",
        room_name="room-1",
    )

    capture.record_user_text(
        trace_id="trace-1",
        text="Tóm tắt chương bốn",
        source="final_transcript",
        language="vi",
    )
    capture.record_rendered_rag_context(
        trace_id="trace-1",
        query="Tóm tắt chương bốn",
        context_text="BOOK_CONTEXT_FOUND:\\nNội dung chương bốn",
    )
    capture.record_assistant_text(trace_id="trace-1", text="Đây là phần tóm tắt.")
    capture.emit_trace("turn_completed", {"trace_id": "trace-1", "answer_source": "book_rag"})

    path = tmp_path / "voice-session-01" / "turns" / "trace-1.json"
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["evaluation_status"] == "unreviewed"
    assert payload["case_id"] is None
    assert payload["user"]["text"] == "Tóm tắt chương bốn"
    assert payload["assistant"]["text"] == "Đây là phần tóm tắt."
    assert payload["retrieved_context"]["rendered_context"] == "BOOK_CONTEXT_FOUND:\\nNội dung chương bốn"
    assert payload["trace"]["answer_source"] == "book_rag"


def test_local_eval_capture_is_a_noop_when_disabled(tmp_path):
    capture = LocalEvaluationCapture(
        enabled=False,
        run_id="unused",
        root_dir=str(tmp_path),
        thread_id=None,
        room_name=None,
    )

    capture.record_user_text(trace_id="trace-1", text="private", source="final_transcript")

    assert not (tmp_path / "unused").exists()

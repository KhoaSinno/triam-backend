from app.services.agent_observability import AgentAnswerSource, AgentInputMode, AgentTurnTracer


def test_trace_summary_is_safe_and_records_retrieval_metadata():
    emitted: list[tuple[str, dict]] = []
    tracer = AgentTurnTracer(
        enabled=True,
        thread_id="thread-1",
        room_name="room-1",
        emitter=lambda event, payload: emitted.append((event, payload)),
    )

    tracer.begin_turn(AgentInputMode.TEXT)
    tracer.record_transcript(AgentInputMode.TEXT, char_count=24, language="vi")
    tracer.record_tool(AgentInputMode.TEXT, "search_book_knowledge_text")
    tracer.record_retrieval(
        AgentInputMode.TEXT,
        [
            {
                "id": 42,
                "learning_unit_id": "unit-1",
                "section_id": "section-4",
                "similarity": 0.812345,
                "content": "SECRET BOOK CONTENT",
            }
        ],
        elapsed_ms=123,
    )
    tracer.record_query_guard(
        AgentInputMode.TEXT,
        reason_code="valid_clarification_confirmation",
        guard_mode="clarification_confirmed",
        overlap_ratio=0.98765,
        important_overlap_ratio=0.54321,
    )
    tracer.record_answer_source(AgentInputMode.TEXT, AgentAnswerSource.BOOK_RAG)
    tracer.record_assistant(AgentInputMode.TEXT, char_count=90)
    summary = tracer.complete_turn(AgentInputMode.TEXT)

    assert summary is not None
    assert summary["retrieval_chunk_ids"] == ["42"]
    assert summary["retrieval_learning_unit_ids"] == ["unit-1"]
    assert summary["retrieval_section_ids"] == ["section-4"]
    assert summary["retrieval_scores"] == [0.8123]
    assert summary["answer_source"] == "book_rag"
    assert summary["query_guard_reason_code"] == "valid_clarification_confirmation"
    assert summary["query_guard_mode"] == "clarification_confirmed"
    assert summary["query_guard_overlap_ratio"] == 0.9877
    assert summary["query_guard_important_overlap_ratio"] == 0.5432
    assert summary["stage_latency_ms"]["retrieval"] == 123
    assert "SECRET BOOK CONTENT" not in str(summary)
    assert emitted[-1][0] == "turn_completed"


def test_late_final_transcript_updates_last_completed_voice_turn():
    emitted: list[tuple[str, dict]] = []
    tracer = AgentTurnTracer(
        enabled=True,
        thread_id="thread-1",
        room_name="room-1",
        late_transcript_window_seconds=30,
        emitter=lambda event, payload: emitted.append((event, payload)),
    )

    tracer.begin_turn(AgentInputMode.VOICE)
    tracer.record_assistant(AgentInputMode.VOICE, char_count=50)
    completed = tracer.complete_turn(AgentInputMode.VOICE)
    tracer.record_transcript(AgentInputMode.VOICE, char_count=18, language="vi")

    assert completed is not None
    assert emitted[-1][0] == "late_transcript"
    assert emitted[-1][1]["trace_id"] == completed["trace_id"]
    assert emitted[-1][1]["transcript_final_seen"] is True
    assert emitted[-1][1]["correlation_quality"] == "late_transcript_last_completed_turn"


def test_next_final_transcript_starts_new_turn_when_completed_turn_already_has_transcript():
    emitted: list[tuple[str, dict]] = []
    tracer = AgentTurnTracer(
        enabled=True,
        thread_id="thread-1",
        room_name="room-1",
        late_transcript_window_seconds=30,
        emitter=lambda event, payload: emitted.append((event, payload)),
    )

    first_trace_id = tracer.begin_turn(AgentInputMode.VOICE)
    tracer.record_transcript(AgentInputMode.VOICE, char_count=18, language="vi")
    tracer.complete_turn(AgentInputMode.VOICE)
    tracer.record_transcript(AgentInputMode.VOICE, char_count=24, language="vi")

    turn_started = [payload for event, payload in emitted if event == "turn_started"]
    late_transcripts = [payload for event, payload in emitted if event == "late_transcript"]

    assert len(turn_started) == 2
    assert turn_started[-1]["trace_id"] != first_trace_id
    assert tracer.has_active_turn(AgentInputMode.VOICE) is True
    assert late_transcripts == []


def test_disabled_tracer_is_noop():
    emitted: list[tuple[str, dict]] = []
    tracer = AgentTurnTracer(
        enabled=False,
        thread_id=None,
        room_name=None,
        emitter=lambda event, payload: emitted.append((event, payload)),
    )

    assert tracer.begin_turn(AgentInputMode.TEXT) is None
    tracer.record_retrieval(AgentInputMode.TEXT, [{"content": "private"}], elapsed_ms=10)
    assert tracer.complete_turn(AgentInputMode.TEXT) is None
    assert emitted == []


def test_duplicate_completion_does_not_emit_second_completed_event():
    emitted: list[tuple[str, dict]] = []
    tracer = AgentTurnTracer(
        enabled=True,
        thread_id=None,
        room_name=None,
        emitter=lambda event, payload: emitted.append((event, payload)),
    )

    tracer.begin_turn(AgentInputMode.TEXT)
    assert tracer.complete_turn(AgentInputMode.TEXT) is not None
    assert tracer.complete_turn(AgentInputMode.TEXT) is None
    assert [event for event, _ in emitted].count("turn_completed") == 1

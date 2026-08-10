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
    assert summary["rag_candidate_count"] == 1
    assert summary["answer_source"] == "book_rag"
    assert summary["query_guard_reason_code"] == "valid_clarification_confirmation"
    assert summary["query_guard_mode"] == "clarification_confirmed"
    assert summary["query_guard_overlap_ratio"] == 0.9877
    assert summary["query_guard_important_overlap_ratio"] == 0.5432
    assert summary["stage_latency_ms"]["retrieval"] == 123
    assert "SECRET BOOK CONTENT" not in str(summary)
    assert emitted[-1][0] == "turn_completed"


def test_trace_records_book_tool_and_final_transcript_relative_timing_without_raw_text():
    emitted: list[tuple[str, dict]] = []
    tracer = AgentTurnTracer(
        enabled=True,
        thread_id="thread-1",
        room_name="room-1",
        emitter=lambda event, payload: emitted.append((event, payload)),
    )

    tracer.begin_turn(AgentInputMode.VOICE)
    tracer.record_book_grounding_tool_started(AgentInputMode.VOICE)
    tracer.record_transcript(AgentInputMode.VOICE, char_count=18, language="vi")
    summary = tracer.complete_turn(AgentInputMode.VOICE)

    assert summary is not None
    assert summary["asr_final_status_at_book_tool"] == "final_missing"
    assert summary["book_tool_before_asr_final_ms"] is not None
    assert "private transcript" not in str(summary)
    assert [event for event, _ in emitted].count("book_grounding_tool_started") == 1


def test_trace_records_final_transcript_present_before_book_tool():
    tracer = AgentTurnTracer(enabled=True, thread_id=None, room_name=None)

    tracer.begin_turn(AgentInputMode.VOICE)
    tracer.record_transcript(AgentInputMode.VOICE, char_count=18, language="vi")
    tracer.record_book_grounding_tool_started(AgentInputMode.VOICE)
    summary = tracer.complete_turn(AgentInputMode.VOICE)

    assert summary is not None
    assert summary["asr_final_status_at_book_tool"] == "final_seen"
    assert summary["asr_final_before_book_tool_ms"] is not None


def test_trace_keeps_first_final_transcript_timing_when_a_stuck_turn_receives_later_input():
    emitted: list[tuple[str, dict]] = []
    tracer = AgentTurnTracer(
        enabled=True,
        thread_id=None,
        room_name=None,
        emitter=lambda event, payload: emitted.append((event, payload)),
    )

    tracer.begin_turn(AgentInputMode.VOICE)
    tracer.record_book_grounding_tool_started(AgentInputMode.VOICE)
    tracer.record_transcript(AgentInputMode.VOICE, char_count=10, language="vi")
    first_gap = tracer._active[AgentInputMode.VOICE].book_tool_before_asr_final_ms
    tracer.record_transcript(AgentInputMode.VOICE, char_count=20, language="vi")
    summary = tracer.complete_turn(AgentInputMode.VOICE)

    assert first_gap is not None
    assert summary is not None
    assert summary["book_tool_before_asr_final_ms"] == first_gap


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


def test_watchdog_observability_fields():
    emitted: list[tuple[str, dict]] = []
    tracer = AgentTurnTracer(
        enabled=True,
        thread_id="thread-1",
        room_name="room-1",
        emitter=lambda event, payload: emitted.append((event, payload)),
    )

    tracer.begin_turn(AgentInputMode.VOICE)
    tracer.record_tool_reply_watchdog_scheduled(
        AgentInputMode.VOICE,
        tool_name="execute_web_search",
        grace_ms=1000,
    )
    assert emitted[-1][0] == "watchdog_scheduled"
    assert emitted[-1][1]["tool_reply_watchdog_scheduled"] is True
    assert emitted[-1][1]["tool_reply_watchdog_tool_names"] == ["execute_web_search"]
    assert emitted[-1][1]["stage_latency_ms"]["tool_reply_watchdog_grace"] == 1000

    tracer.record_tool_reply_watchdog_fired(
        AgentInputMode.VOICE,
        tool_name="execute_web_search",
        elapsed_ms=1023,
        reason="no_speech_after_tool",
    )
    assert emitted[-1][0] == "watchdog_fired"
    assert emitted[-1][1]["tool_reply_watchdog_fired"] is True
    assert emitted[-1][1]["tool_reply_watchdog_reason"] == "no_speech_after_tool"
    assert emitted[-1][1]["tool_result_to_speech_ms"] == 1023
    assert emitted[-1][1]["forced_reply_reason"] == "no_speech_after_tool"

    tracer.record_tool_reply_watchdog_cancelled(
        AgentInputMode.VOICE,
        reason="speech_created",
    )
    assert emitted[-1][0] == "watchdog_cancelled"
    assert emitted[-1][1]["tool_reply_watchdog_reason"] == "cancelled_speech_created"

    tracer.record_tool_reply_speech_created(
        AgentInputMode.VOICE,
        source="agent_speech",
        elapsed_ms=450,
    )
    assert emitted[-1][0] == "speech_created"
    assert emitted[-1][1]["tool_result_to_speech_ms"] == 450

    summary = tracer.complete_turn(AgentInputMode.VOICE)
    assert summary["tool_reply_watchdog_scheduled"] is True
    assert summary["tool_reply_watchdog_fired"] is True
    assert summary["tool_reply_watchdog_tool_names"] == ["execute_web_search"]
    assert summary["tool_reply_watchdog_reason"] == "cancelled_speech_created"
    assert summary["tool_result_to_speech_ms"] == 450


def test_trace_records_rag_context_usage_without_context_text():
    emitted: list[tuple[str, dict]] = []
    tracer = AgentTurnTracer(
        enabled=True,
        thread_id="thread-1",
        room_name="room-1",
        emitter=lambda event, payload: emitted.append((event, payload)),
    )

    tracer.begin_turn(AgentInputMode.VOICE)
    tracer.record_rag_context(
        AgentInputMode.VOICE,
        selected_count=2,
        content_char_count=7000,
        budget_mode="default",
    )

    payload = emitted[-1][1]
    assert emitted[-1][0] == "rag_context_formatted"
    assert payload["rag_context_selected_count"] == 2
    assert payload["rag_context_char_count"] == 7000
    assert payload["rag_context_budget_mode"] == "default"
    assert "secret" not in str(payload)


def test_trace_records_realtime_quota_usage_and_provider_error_without_raw_content():
    emitted: list[tuple[str, dict]] = []
    tracer = AgentTurnTracer(
        enabled=True,
        thread_id="thread-1",
        room_name="room-1",
        emitter=lambda event, payload: emitted.append((event, payload)),
    )

    tracer.begin_turn(AgentInputMode.VOICE)
    trace_id = tracer.record_realtime_rate_limits(
        AgentInputMode.VOICE,
        token_limit=40000,
        token_remaining=1200,
        token_reset_seconds=8.5,
        request_limit=200,
        request_remaining=196,
        request_reset_seconds=8.5,
    )
    assert trace_id is not None
    assert tracer.record_realtime_response_created(AgentInputMode.VOICE, response_id="resp-1") == trace_id
    assert tracer.record_realtime_response_usage(
        AgentInputMode.VOICE,
        response_id="resp-1",
        input_tokens=12000,
        input_text_tokens=9000,
        input_audio_tokens=100,
        input_cached_tokens=7000,
        output_tokens=300,
        output_text_tokens=20,
        output_audio_tokens=280,
        total_tokens=12300,
        duration_ms=1300,
        ttft_ms=240,
        cancelled=False,
    ) == trace_id
    assert tracer.record_realtime_error(
        AgentInputMode.VOICE,
        error_code="rate_limit_exceeded",
        error_type="tokens",
        message_chars=88,
    ) == trace_id

    summary = tracer.complete_turn(AgentInputMode.VOICE)

    assert summary is not None
    assert summary["realtime_token_remaining"] == 1200
    assert summary["realtime_request_remaining"] == 196
    assert summary["realtime_response_ids"] == ["resp-1"]
    assert summary["realtime_input_tokens"] == 12000
    assert summary["realtime_input_cached_tokens"] == 7000
    assert summary["realtime_output_audio_tokens"] == 280
    assert summary["realtime_error_code"] == "rate_limit_exceeded"
    assert summary["realtime_error_type"] == "tokens"
    assert summary["error_code"] == "openai_rate_limit_exceeded"
    assert "PRIVATE CONTEXT" not in str(summary)
    assert [event for event, _ in emitted].count("realtime_response_usage") == 1


def test_trace_attaches_late_realtime_usage_to_matching_completed_turn():
    tracer = AgentTurnTracer(enabled=True, thread_id=None, room_name=None)
    tracer.begin_turn(AgentInputMode.VOICE)
    tracer.record_realtime_response_created(AgentInputMode.VOICE, response_id="resp-1")
    completed = tracer.complete_turn(AgentInputMode.VOICE)

    trace_id = tracer.record_realtime_response_usage(
        AgentInputMode.VOICE,
        response_id="resp-1",
        input_tokens=100,
        input_text_tokens=90,
        input_audio_tokens=10,
        input_cached_tokens=80,
        output_tokens=20,
        output_text_tokens=5,
        output_audio_tokens=15,
        total_tokens=120,
        duration_ms=500,
        ttft_ms=None,
        cancelled=False,
    )

    assert completed is not None
    assert trace_id == completed["trace_id"]

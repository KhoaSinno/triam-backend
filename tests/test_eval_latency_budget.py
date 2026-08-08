from tests.eval_latency_budget import completed_voice_traces, stage_values


def test_completed_voice_traces_deduplicates_trace_events_and_excludes_text():
    events = [
        {"event_type": "retrieval_completed", "input_mode": "voice", "trace_id": "v1", "stage_latency_ms": {"retrieval": 120}},
        {"event_type": "turn_completed", "input_mode": "voice", "trace_id": "v1", "stage_latency_ms": {"retrieval": 120, "turn_total": 400}},
        {"event_type": "turn_completed", "input_mode": "voice", "trace_id": "v1", "stage_latency_ms": {"turn_total": 400}},
        {"event_type": "turn_completed", "input_mode": "text", "trace_id": "t1", "stage_latency_ms": {"turn_total": 10}},
        {"event_type": "turn_completed", "input_mode": "voice", "trace_id": "v2", "stage_latency_ms": {"turn_total": 600}},
    ]

    traces = completed_voice_traces(events)

    assert {trace["trace_id"] for trace in traces} == {"v1", "v2"}
    assert stage_values(traces, "retrieval") == [120]
    assert sorted(stage_values(traces, "turn_total")) == [400, 600]

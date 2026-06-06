from app.services.agent_observability.model_eval_report import build_metrics, classify_failure_codes


def test_classify_failure_codes_separates_stt_routing_and_web_policy():
    case = {
        "expected_answer_source": "book_section",
    }
    checks = {
        "voice_transcript_meaning": False,
        "web_not_used_without_permission": True,
        "expected_intent": False,
        "expected_section": False,
        "expected_answer_source": False,
        "must_include": False,
        "must_not_include": True,
    }
    trace = {
        "answer_source": "policy",
        "retrieval_result_count": 10,
    }

    failures = classify_failure_codes(case, checks, trace)

    assert failures == [
        "INPUT_STT",
        "WEB_PERMISSION",
        "ROUTING_INTENT",
        "ROUTING_SECTION",
        "RETRIEVAL_RELEVANCE",
    ]


def test_build_metrics_ignores_not_evaluated_checks_and_summarizes_latency():
    results = [
        {
            "input_mode": "voice",
            "status": "failed",
            "failure_codes": ["INPUT_STT"],
            "checks": {
                "must_include": True,
                "must_not_include": True,
                "expected_intent": False,
                "expected_answer_source": False,
                "expected_section": None,
                "web_not_used_without_permission": True,
                "voice_transcript_meaning": False,
            },
            "trace": {
                "stage_latency_ms": {
                    "turn_total": 1000,
                    "retrieval": 300,
                }
            },
        },
        {
            "input_mode": "voice",
            "status": "passed",
            "checks": {
                "must_include": True,
                "must_not_include": True,
                "expected_intent": True,
                "expected_answer_source": True,
                "expected_section": True,
                "web_not_used_without_permission": True,
                "voice_transcript_meaning": True,
            },
            "trace": {
                "stage_latency_ms": {
                    "turn_total": 3000,
                    "retrieval": 500,
                }
            },
        },
    ]

    metrics = build_metrics(results)

    assert metrics["strict_case_pass_rate"] == 0.5
    assert metrics["accuracy"]["content_accuracy"]["rate"] == 1.0
    assert metrics["accuracy"]["voice_meaning_preservation_rate"]["rate"] == 0.5
    assert metrics["accuracy"]["section_resolution_accuracy"]["evaluated"] == 1
    assert metrics["latency"]["voice"]["turn_total"]["p50_ms"] == 2000
    assert metrics["latency"]["voice"]["turn_total"]["p95_ms"] == 2900
    assert metrics["failure_counts"] == {"INPUT_STT": 1}

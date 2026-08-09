import asyncio

from tests import eval_llm_as_judge as judge


def test_context_precision_uses_zero_for_no_relevant_chunks(monkeypatch):
    async def fake_call(_prompt: str) -> str:
        return '{"verdicts": [false, false]}'

    monkeypatch.setattr(judge, "call_judge_llm", fake_call)

    result = asyncio.run(judge.evaluate_context_precision("question", "reference", ["a", "b"]))

    assert result.score == 0.0
    assert result.error is None


def test_context_recall_keeps_judge_failure_out_of_the_mean(monkeypatch):
    async def fake_call(_prompt: str) -> str:
        raise RuntimeError("provider unavailable")

    monkeypatch.setattr(judge, "call_judge_llm", fake_call)

    result = asyncio.run(judge.evaluate_context_recall("question", "reference", ["context"]))

    assert result.score is None
    assert "RuntimeError" in result.error


def test_summarize_metrics_reports_evaluated_and_not_applicable_counts():
    df = judge.pd.DataFrame(
        [
            {
                "context_precision": 0.5,
                "context_precision_status": "scored",
                "context_recall": None,
                "context_recall_status": "not_applicable_unverified_retrieval",
                "faithfulness": None,
                "faithfulness_status": "RuntimeError:timeout",
                "answer_relevancy": 0.8,
                "answer_relevancy_status": "scored",
                "answer_correctness": 0.9,
                "answer_correctness_status": "scored",
            }
        ]
    )

    summary = judge.summarize_metrics(df)

    assert summary["context_precision"]["evaluated"] == 1
    assert summary["context_recall"]["not_applicable"] == 1
    assert summary["faithfulness"]["judge_errors"] == 1

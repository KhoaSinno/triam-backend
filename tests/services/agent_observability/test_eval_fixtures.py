import json
from pathlib import Path

TEXT_CASES = Path("tests/fixtures/agent_eval/book_grounding_cases.json")
VOICE_CASES = Path("tests/fixtures/agent_eval/voice_manifest.json")


def _load(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, list)
    return payload


def test_agent_eval_cases_have_unique_ids_and_required_contract():
    cases = _load(TEXT_CASES) + _load(VOICE_CASES)
    ids = [case["id"] for case in cases]

    assert len(ids) == len(set(ids))
    for case in cases:
        assert case["input_mode"] in {"text", "voice"}
        assert case["expected_intent"]
        assert case["expected_answer_source"]
        assert isinstance(case["expected_section_paths"], list)
        assert isinstance(case["must_include"], list)
        assert isinstance(case["must_not_include"], list)
        assert isinstance(case["web_search_enabled"], bool)
        assert isinstance(case["web_search_allowed"], bool)


def test_voice_eval_fixture_paths_are_declared_and_valid_when_present():
    for case in _load(VOICE_CASES):
        fixture = Path(case["audio_fixture"])
        assert fixture.suffix == ".wav"
        if fixture.exists():
            assert fixture.stat().st_size > 0

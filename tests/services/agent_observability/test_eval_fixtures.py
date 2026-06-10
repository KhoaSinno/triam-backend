import json
import uuid
from pathlib import Path

TEXT_CASES = Path("tests/fixtures/agent_eval/book_grounding_cases.json")
VOICE_CASES = Path("tests/fixtures/agent_eval/voice_manifest.json")
CANDIDATE_MATRIX = Path("tests/fixtures/agent_eval/model_candidate_matrix.json")
VOICE_CASE_THREAD_MAP_EXAMPLE = Path("tests/fixtures/agent_eval/voice_case_threads.example.json")


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


def test_model_candidate_matrix_has_required_baseline_and_unique_names():
    candidates = _load(CANDIDATE_MATRIX)
    names = [candidate["name"] for candidate in candidates]

    assert "baseline" in names
    assert len(names) == len(set(names))
    for candidate in candidates:
        assert isinstance(candidate["description"], str)
        assert isinstance(candidate["env"], dict)


def test_chapter_five_fixture_checks_fact_not_single_translation():
    cases = {case["id"]: case for case in _load(TEXT_CASES)}
    chapter_five = cases["mice-chapter-five-summary-vi-text"]

    assert chapter_five["must_include"] == ["Lennie", "Curley"]


def test_voice_case_thread_map_example_matches_voice_cases():
    voice_cases = {case["id"] for case in _load(VOICE_CASES)}
    mapping = json.loads(VOICE_CASE_THREAD_MAP_EXAMPLE.read_text(encoding="utf-8"))

    assert set(mapping) == voice_cases
    for thread_id in mapping.values():
        uuid.UUID(thread_id)

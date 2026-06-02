from app.services.pareto_signal_service import (
    extract_pareto_signal_hints,
    guess_section_language,
    infer_unit_type_from_signals,
    normalize_signal_text,
    score_pareto_signals,
)


def test_normalize_signal_text_removes_vietnamese_accents():
    assert normalize_signal_text("Khái niệm mệnh đề") == "khai niem menh de"
    assert normalize_signal_text("Định nghĩa Logic") == "dinh nghia logic"


def test_extracts_vietnamese_signal_hints_with_accents_and_without_accents():
    assert "core_concept" in extract_pareto_signal_hints("Khái niệm mệnh đề")
    assert "core_concept" in extract_pareto_signal_hints("Khai niem menh de")
    assert "definition" in extract_pareto_signal_hints("Dinh nghia logic")
    assert "method" in extract_pareto_signal_hints("Phương pháp chứng minh")
    assert "procedure" in extract_pareto_signal_hints("Hướng dẫn giải bài toán")


def test_extracts_english_signal_hints():
    assert "core_concept" in extract_pareto_signal_hints("Core Concepts")
    assert "rule" in extract_pareto_signal_hints("Rules of Inference")
    assert "reasoning" in extract_pareto_signal_hints("Rules of Inference")
    assert "method" in extract_pareto_signal_hints("Proof Methods")
    assert "formula" in extract_pareto_signal_hints("Important identities")
    assert "procedure" in extract_pareto_signal_hints("Step-by-step tutorial")


def test_short_english_terms_match_word_boundaries_only():
    assert "principle" in extract_pareto_signal_hints("Newton laws")
    assert "principle" not in extract_pareto_signal_hints("Common flaws in arguments")
    assert "principle" not in extract_pareto_signal_hints("Outlaw examples")


def test_language_guess_supports_vietnamese_english_and_mixed():
    assert guess_section_language("Khái niệm mệnh đề") == "vi"
    assert guess_section_language("Core Concepts and Methods") == "en"
    assert guess_section_language("Definition - Định nghĩa") == "mixed"
    assert guess_section_language("Logic") == "unknown"


def test_score_does_not_let_examples_outrank_core_concepts():
    core_score = score_pareto_signals("Core Concepts", "")
    example_score = score_pareto_signals("Examples and exercises", "")

    assert core_score > example_score


def test_infer_unit_type_from_signal_hints():
    assert infer_unit_type_from_signals(["method", "example"]) == "pareto_method"
    assert infer_unit_type_from_signals(["formula"]) == "pareto_formula"
    assert infer_unit_type_from_signals([]) == "pareto_focus"

import pytest

from app.services.agent_grounding.query_normalizer import normalize_query
from app.services.agent_grounding.section_reference_parser import parse_positive_integer_phrase, parse_section_reference


@pytest.mark.parametrize(
    ("phrase", "expected"),
    [
        ("4", 4),
        ("IV", 4),
        ("bốn", 4),
        ("hai mươi mốt", 21),
        ("four", 4),
        ("twenty one", 21),
    ],
)
def test_parse_positive_integer_phrase(phrase: str, expected: int):
    assert parse_positive_integer_phrase(phrase) == expected


@pytest.mark.parametrize(
    ("query", "path", "ordinal"),
    [
        ("Tóm tắt chương 4.", None, 4),
        ("Tóm tắt chương bốn.", None, 4),
        ("What happens in chapter four?", None, 4),
        ("Tóm tắt phần IV.", None, 4),
        ("Giải thích mục 1.2.3.", "1.2.3", None),
    ],
)
def test_parse_section_reference_numbers(query: str, path: str | None, ordinal: int | None):
    result = parse_section_reference(normalize_query(query))

    assert result.marker_present is True
    assert result.explicit_path == path
    assert result.explicit_ordinal == ordinal


def test_parse_exact_quoted_section_title():
    result = parse_section_reference(normalize_query('Tóm tắt mục "Phương pháp nghiên cứu".'))

    assert result.marker_present is True
    assert result.title_hint == "Phương pháp nghiên cứu"


def test_parse_missing_section_reference_for_clarification():
    result = parse_section_reference(normalize_query("Tóm tắt chương."))

    assert result.marker_present is True
    assert result.has_target is False


def test_parse_section_reference_percent_ignored():
    result = parse_section_reference(normalize_query("Phần trăm lợi nhuận là bao nhiêu?"))
    assert result.marker_present is False


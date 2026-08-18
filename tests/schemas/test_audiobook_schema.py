import pytest
from pydantic import ValidationError

from app.schemas.audiobook import BookCreateRequest, BookUpdateRequest


@pytest.mark.parametrize(
    ("schema", "payload", "expected"),
    [
        (BookCreateRequest, {"title": "Clean\x00title"}, {"title": "Cleantitle"}),
        (BookCreateRequest, {"title": "Clean title", "author": "Bad\x00author"}, {"title": "Clean title", "author": "Badauthor"}),
        (BookUpdateRequest, {"title": "Clean\x00title"}, {"title": "Cleantitle"}),
        (BookUpdateRequest, {"author": "Bad\x00author"}, {"author": "Badauthor"}),
    ],
)
def test_book_metadata_removes_nul_characters(schema, payload, expected) -> None:
    assert schema.model_validate(payload).model_dump(exclude_unset=True) == expected


def test_book_title_cannot_be_empty_after_nul_character_removal() -> None:
    with pytest.raises(ValidationError):
        BookCreateRequest.model_validate({"title": "\x00"})


def test_book_metadata_accepts_normal_text() -> None:
    payload = BookUpdateRequest.model_validate({"title": "Sách học tiếng Anh", "author": "TRIAM"})

    assert payload.title == "Sách học tiếng Anh"
    assert payload.author == "TRIAM"

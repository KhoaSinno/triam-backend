from __future__ import annotations

from docx import Document
from docx.oxml.ns import qn

from app.core.exceptions import DocumentExtractionError, DocumentOutlineRequiredError

HEADING_STYLE_NAMES = {
    "heading 1",
    "heading 2",
    "heading 3",
}


def _has_outline_level(paragraph) -> bool:
    if paragraph.style is None or paragraph.style.element is None:
        return False

    p_pr = paragraph.style.element.find(qn("w:pPr"))
    if p_pr is None:
        return False

    return p_pr.find(qn("w:outlineLvl")) is not None


def _is_heading(paragraph) -> bool:
    style_name = (paragraph.style.name or "").strip().lower() if paragraph.style else ""
    return style_name in HEADING_STYLE_NAMES or _has_outline_level(paragraph)


async def extract_docx_chapters(file_obj) -> list[dict]:
    file_obj.seek(0)

    try:
        document = Document(file_obj)
    except Exception as exc:
        raise DocumentExtractionError(f"Không thể đọc DOCX: {exc}") from exc

    chapters: list[dict] = []
    current_title: str | None = None
    current_parts: list[str] = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if not text:
            continue

        if _is_heading(paragraph):
            if current_title and current_parts:
                chapters.append(
                    {
                        "title": current_title,
                        "text": "\n".join(current_parts).strip(),
                        "page_start": None,
                        "page_end": None,
                    }
                )

            current_title = text
            current_parts = []
            continue

        if current_title:
            current_parts.append(text)

    if current_title and current_parts:
        chapters.append(
            {
                "title": current_title,
                "text": "\n".join(current_parts).strip(),
                "page_start": None,
                "page_end": None,
            }
        )

    if not chapters:
        raise DocumentOutlineRequiredError("DOCX không có Heading/mục lục hợp lệ. Vui lòng dùng Heading 1/Heading 2 cho tên chương.")

    return chapters

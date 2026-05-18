from __future__ import annotations

from io import BytesIO

from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub

from app.core.exceptions import DocumentExtractionError, DocumentOutlineRequiredError


def _html_to_text(content: bytes) -> str:
    soup = BeautifulSoup(content, "html.parser")

    for tag in soup(["script", "style", "nav"]):
        tag.decompose()

    lines = [line.strip() for line in soup.get_text("\n").splitlines() if line.strip()]
    return "\n".join(lines)


def _flatten_epub_toc(toc_items) -> list[tuple[str, str]]:
    toc: list[tuple[str, str]] = []

    for item in toc_items:
        if isinstance(item, tuple):
            parent, children = item
            title = str(getattr(parent, "title", "") or "").strip()
            href = getattr(parent, "href", None)
            if title and href:
                toc.append((title, href.split("#", 1)[0]))
            toc.extend(_flatten_epub_toc(children))
            continue

        title = str(getattr(item, "title", "") or "").strip()
        href = getattr(item, "href", None)
        if title and href:
            toc.append((title, href.split("#", 1)[0]))

    return toc


async def extract_epub_chapters(file_obj) -> list[dict]:
    file_obj.seek(0)

    try:
        book = epub.read_epub(BytesIO(file_obj.read()))
    except Exception as exc:
        raise DocumentExtractionError(f"Không thể đọc EPUB: {exc}") from exc

    toc = _flatten_epub_toc(book.toc)
    if not toc:
        raise DocumentOutlineRequiredError("EPUB không có mục lục điều hướng hợp lệ. Vui lòng upload EPUB có TOC chuẩn.")

    documents_by_href = {item.get_name(): item.get_content() for item in book.get_items_of_type(ITEM_DOCUMENT)}
    chapters: list[dict] = []
    seen_hrefs: set[str] = set()

    for title, href in toc:
        if href in seen_hrefs:
            continue
        seen_hrefs.add(href)

        content = documents_by_href.get(href)
        if not content:
            continue

        text = _html_to_text(content)
        if text:
            chapters.append(
                {
                    "title": title,
                    "text": text,
                    "page_start": None,
                    "page_end": None,
                }
            )

    if not chapters:
        raise DocumentExtractionError("EPUB có mục lục nhưng không trích xuất được text. File có thể bị lỗi hoặc không phải text-based EPUB.")

    return chapters

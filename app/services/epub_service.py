from __future__ import annotations

from io import BytesIO

from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub

from app.core.exceptions import DocumentExtractionError, DocumentOutlineRequiredError
from app.services.document_structure_types import ParsedDocument, ParsedSection, has_extractable_text


def _html_to_text(content: bytes) -> str:
    soup = BeautifulSoup(content, "html.parser")

    for tag in soup(["script", "style", "nav"]):
        tag.decompose()

    lines = [line.strip() for line in soup.get_text("\n").splitlines() if line.strip()]
    return "\n".join(lines)


def _split_href(href: str | None) -> tuple[str | None, str | None]:
    if not href:
        return None, None
    source_href, _, source_anchor = href.partition("#")
    return source_href or None, source_anchor or None


def _epub_toc_tree(toc_items, documents_by_href: dict[str, bytes], level: int = 1, parent_path: str = "") -> list[ParsedSection]:
    sections: list[ParsedSection] = []
    for item in toc_items:
        if isinstance(item, tuple):
            parent, children = item
            title = str(getattr(parent, "title", "") or "").strip()
            href = getattr(parent, "href", None)
            source_href, source_anchor = _split_href(href)
            if title and source_href:
                order_index = len(sections)
                path = f"{parent_path}.{order_index + 1}" if parent_path else str(order_index + 1)
                content = documents_by_href.get(source_href)
                sections.append(
                    ParsedSection(
                        title=title,
                        level=level,
                        order_index=order_index,
                        path=path,
                        text=_html_to_text(content) if content else "",
                        page_start=None,
                        page_end=None,
                        source_href=source_href,
                        source_anchor=source_anchor,
                        children=_epub_toc_tree(children, documents_by_href, level + 1, path),
                    )
                )
            else:
                sections.extend(_epub_toc_tree(children, documents_by_href, level, parent_path))
            continue

        title = str(getattr(item, "title", "") or "").strip()
        href = getattr(item, "href", None)
        source_href, source_anchor = _split_href(href)
        if title and source_href:
            order_index = len(sections)
            path = f"{parent_path}.{order_index + 1}" if parent_path else str(order_index + 1)
            content = documents_by_href.get(source_href)
            sections.append(
                ParsedSection(
                    title=title,
                    level=level,
                    order_index=order_index,
                    path=path,
                    text=_html_to_text(content) if content else "",
                    page_start=None,
                    page_end=None,
                    source_href=source_href,
                    source_anchor=source_anchor,
                )
            )

    return sections


async def parse_epub_structure(file_obj) -> ParsedDocument:
    file_obj.seek(0)

    try:
        book = epub.read_epub(BytesIO(file_obj.read()))
    except Exception as exc:
        raise DocumentExtractionError(f"Không thể đọc EPUB: {exc}") from exc

    documents_by_href = {item.get_name(): item.get_content() for item in book.get_items_of_type(ITEM_DOCUMENT)}
    sections = _epub_toc_tree(book.toc, documents_by_href)
    if not sections:
        raise DocumentOutlineRequiredError("EPUB không có mục lục điều hướng hợp lệ. Vui lòng upload EPUB có TOC chuẩn.")

    if not has_extractable_text(sections):
        raise DocumentExtractionError("EPUB có mục lục nhưng không trích xuất được text. File có thể bị lỗi hoặc không phải text-based EPUB.")

    return ParsedDocument(document_type="epub", sections=sections)

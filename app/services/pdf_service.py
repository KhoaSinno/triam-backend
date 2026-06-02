import pdfplumber
from pypdf import PdfReader

from app.core.exceptions import DocumentOutlineRequiredError, PdfExtractionError
from app.core.logger import log
from app.services.document_structure_types import ParsedDocument, ParsedSection, flatten_sections, has_extractable_text


def get_pdf_outline_structure(file_obj) -> list[dict]:
    return [
        {
            "title": section.title,
            "page_index": max(0, (section.page_start or 1) - 1),
            "level": section.level,
            "path": section.path,
        }
        for section in flatten_sections(_read_pdf_outline_tree(file_obj))
    ]


def _read_pdf_outline_tree(file_obj) -> list[ParsedSection]:
    file_obj.seek(0)
    try:
        reader = PdfReader(file_obj)
        if not reader.outline:
            return []

        def _walk(outline_items, level: int, parent_path: str = "") -> list[ParsedSection]:
            sections: list[ParsedSection] = []
            for item in outline_items:
                if isinstance(item, list):
                    if sections:
                        parent = sections[-1]
                        sections[-1] = ParsedSection(
                            title=parent.title,
                            level=parent.level,
                            order_index=parent.order_index,
                            path=parent.path,
                            text=parent.text,
                            page_start=parent.page_start,
                            page_end=parent.page_end,
                            top=parent.top,
                            children=_walk(item, level + 1, parent.path),
                        )
                    continue

                try:
                    page_index = reader.get_destination_page_number(item)
                    title = str(getattr(item, "title", "") or "").strip()
                    top = getattr(item, "top", None)
                    if top is not None:
                        top = float(top)
                    if title:
                        order_index = len(sections)
                        path = f"{parent_path}.{order_index + 1}" if parent_path else str(order_index + 1)
                        sections.append(
                            ParsedSection(
                                title=title,
                                level=level,
                                order_index=order_index,
                                path=path,
                                page_start=int(page_index) + 1,
                                top=top,
                            )
                        )
                except Exception as exc:
                    log.warning(f"Bỏ qua outline item lỗi: {exc}")
            return sections

        return _walk(reader.outline, level=1)
    except Exception as exc:
        log.warning(f"Lỗi đọc PDF outline: {exc}")
        return []


def _replace_section_text(section: ParsedSection, text_by_path: dict[str, tuple[str, int | None]]) -> ParsedSection:
    text, page_end = text_by_path.get(section.path, ("", section.page_end))
    return ParsedSection(
        title=section.title,
        level=section.level,
        order_index=section.order_index,
        path=section.path,
        text=text,
        page_start=section.page_start,
        page_end=page_end,
        source_href=section.source_href,
        source_anchor=section.source_anchor,
        top=section.top,
        children=[_replace_section_text(child, text_by_path) for child in section.children],
    )


def _pdf_outline_sort_key(pair: tuple[int, ParsedSection]) -> tuple[int, float]:
    _, section = pair
    page = section.page_start or 1
    top = section.top
    if top is None:
        top = float("inf")
    return (page, -top)


def _crop_text(page, y_start: float, y_end: float) -> str:
    page_height = float(page.height)
    y_start = max(0.0, min(y_start, page_height))
    y_end = max(0.0, min(y_end, page_height))
    if y_start >= y_end:
        return ""
    return page.crop((0, y_start, page.width, y_end)).extract_text() or ""


def _y_from_outline_top(page, outline_top: float | None, *, default: float) -> float:
    if outline_top is None:
        return default
    return float(page.height) - outline_top


def _extract_same_page_section_text(page, start_top: float | None, end_top: float | None) -> str:
    page_height = float(page.height)
    y_start = _y_from_outline_top(page, start_top, default=0.0)
    y_end = _y_from_outline_top(page, end_top, default=page_height)
    return _crop_text(page, y_start, y_end)


def _extract_first_page_section_text(page, start_top: float | None) -> str:
    y_start = _y_from_outline_top(page, start_top, default=0.0)
    return _crop_text(page, y_start, float(page.height))


def _extract_last_page_section_text(page, end_top: float | None) -> str:
    y_end = _y_from_outline_top(page, end_top, default=float(page.height))
    return _crop_text(page, 0.0, y_end)


def _append_non_empty(parts: list[str], text: str) -> None:
    if text.strip():
        parts.append(text)


def _extract_multi_page_section_text(pdf, p_start: int, p_end: int, start_top: float | None, end_top: float | None) -> str:
    parts: list[str] = []
    _append_non_empty(parts, _extract_first_page_section_text(pdf.pages[p_start - 1], start_top))

    for page_number in range(p_start + 1, p_end):
        _append_non_empty(parts, pdf.pages[page_number - 1].extract_text() or "")

    if p_end <= len(pdf.pages):
        _append_non_empty(parts, _extract_last_page_section_text(pdf.pages[p_end - 1], end_top))

    return "\n".join(parts).strip()


def _extract_section_text_from_pdf(pdf, current_section: ParsedSection, next_section: ParsedSection | None) -> tuple[str, int]:
    total_pages = len(pdf.pages)
    start_page = current_section.page_start or 1
    start_top = current_section.top
    end_page = (next_section.page_start or (total_pages + 1)) if next_section else total_pages + 1
    end_top = next_section.top if next_section else 0.0

    p_start = max(1, min(start_page, total_pages))
    p_end = max(1, min(end_page, total_pages + 1))

    if p_start == p_end:
        text = _extract_same_page_section_text(pdf.pages[p_start - 1], start_top, end_top)
    else:
        text = _extract_multi_page_section_text(pdf, p_start, p_end, start_top, end_top)

    section_page_end = min(total_pages, max(start_page, end_page - 1))
    return text, section_page_end


async def parse_pdf_structure(file_obj) -> ParsedDocument:
    file_obj.seek(0)
    outline_tree = _read_pdf_outline_tree(file_obj)
    outline_items = flatten_sections(outline_tree)

    if not outline_items or len(outline_items) <= 1:
        raise DocumentOutlineRequiredError(
            "PDF không có bookmark/outline ẩn. Vui lòng upload PDF có mục lục chuẩn."
        )

    file_obj.seek(0)
    text_by_path: dict[str, tuple[str, int | None]] = {}

    try:
        with pdfplumber.open(file_obj) as pdf:
            ordered_items = sorted(
                enumerate(outline_items),
                key=_pdf_outline_sort_key,
            )

            for i, (_, current_section) in enumerate(ordered_items):
                next_section = ordered_items[i + 1][1] if i < len(ordered_items) - 1 else None
                chapter_text, section_page_end = _extract_section_text_from_pdf(pdf, current_section, next_section)
                text_by_path[current_section.path] = (chapter_text, section_page_end)

    except DocumentOutlineRequiredError:
        raise
    except Exception as exc:
        raise PdfExtractionError(f"Không thể đọc nội dung PDF: {exc}") from exc

    sections = [_replace_section_text(section, text_by_path) for section in outline_tree]
    if not has_extractable_text(sections):
        raise PdfExtractionError(
            "PDF có outline nhưng không trích xuất được text. File có thể là scan ảnh hoặc bị lỗi."
        )

    return ParsedDocument(document_type="pdf", sections=sections)


async def extract_text_from_pdf(file_obj, max_pages=None):
    """
    Helper function: Extract raw text từ PDF (không chia chương).
    Dùng cho demo endpoints như /process-book-intro.

    Args:
        file_obj: File object của PDF
        max_pages: Số trang tối đa cần extract (None = all pages)

    Returns:
        str: Raw text từ PDF
    """
    file_obj.seek(0)
    extracted_text = ""

    with pdfplumber.open(file_obj) as pdf:
        pages_to_read = len(pdf.pages) if max_pages is None else min(
            max_pages, len(pdf.pages))

        for i in range(pages_to_read):
            text = pdf.pages[i].extract_text()
            if text:
                extracted_text += text + "\n"

    return extracted_text.strip()


def extract_text_by_page_range(pdf_obj, start_page: int, end_page: int):
    """
    Trích xuất text từ trang A đến trang B.
    - pdf_obj: Đối tượng pdfplumber đã mở.
    - start_page: Số trang thực tế (ví dụ: 5).
    - end_page: Số trang thực tế (ví dụ: 10).
    -> Trả về text của trang 5, 6, 7, 8, 9, 10.
    """
    extracted_text = ""

    # Validate: Đảm bảo trang kết thúc không vượt quá tổng số trang
    total_pages = len(pdf_obj.pages)
    if end_page > total_pages:
        end_page = total_pages

    # Vòng lặp lấy text
    # LƯU Ý: Python index bắt đầu từ 0.
    # Nếu muốn lấy trang 5 (start_page), index phải là 4 (start_page - 1).
    # Hàm range(a, b) chạy đến b-1, nên tham số thứ 2 là end_page (tương ứng index end_page-1)

    # Ví dụ: Lấy trang 5 đến 7.
    # start_page=5 -> index=4
    # end_page=7
    # range(4, 7) sẽ chạy qua index: 4 (trang 5), 5 (trang 6), 6 (trang 7). CHUẨN.

    for i in range(start_page - 1, end_page):
        try:
            page = pdf_obj.pages[i]
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        except Exception as e:
            log.warning(f"Lỗi đọc trang {i + 1}: {e}")

    return extracted_text


def extract_clean_text(page):
    """
    Chỉ lấy phần thân trang, bỏ Header (trên cùng) và Footer (số trang dưới cùng)
    """
    width = page.width
    height = page.height

    # Giả sử Header chiếm 50px trên cùng, Footer chiếm 50px dưới cùng
    # Tọa độ crop: (x0, top, x1, bottom)
    bounding_box = (0, 50, width, height - 50)

    try:
        cropped_page = page.crop(bounding_box)
        return cropped_page.extract_text()
    except ValueError:
        # Fallback nếu trang không crop được (ví dụ trang trắng)
        return page.extract_text()

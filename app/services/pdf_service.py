
import pdfplumber
from pypdf import PdfReader

from app.core.logger import log
from app.core.exceptions import DocumentOutlineRequiredError, PdfExtractionError

def get_pdf_outline_structure(file_obj) -> list[dict]:
    outline_data = []
    try:
        reader = PdfReader(file_obj)
        if not reader.outline:
            return []

        def _parse_outline(outline_items):
            for item in outline_items:
                if isinstance(item, list):
                    _parse_outline(item)
                    continue

                try:
                    page_index = reader.get_destination_page_number(item)
                    title = str(getattr(item, "title", "") or "").strip()
                    if title:
                        outline_data.append(
                            {
                                "title": title,
                                "page_index": page_index,
                            }
                        )
                except Exception as exc:
                    log.warning(f"Bỏ qua outline item lỗi: {exc}")

        _parse_outline(reader.outline)
        outline_data.sort(key=lambda x: x["page_index"])
        return outline_data
    except Exception as exc:
        log.warning(f"Lỗi đọc PDF outline: {exc}")
        return []


async def extract_pdf_chapters(file_obj) -> list[dict]:
    file_obj.seek(0)
    outlines = get_pdf_outline_structure(file_obj)

    if not outlines or len(outlines) <= 1:
        raise DocumentOutlineRequiredError(
            "PDF không có bookmark/outline ẩn. Vui lòng upload PDF có mục lục chuẩn."
        )

    file_obj.seek(0)
    chapters = []

    try:
        with pdfplumber.open(file_obj) as pdf:
            total_pages = len(pdf.pages)

            for i, current_chap in enumerate(outlines):
                start_idx = max(0, int(current_chap["page_index"]))
                if i < len(outlines) - 1:
                    end_idx = int(outlines[i + 1]["page_index"])
                else:
                    end_idx = total_pages

                end_idx = min(max(end_idx, start_idx + 1), total_pages)

                chapter_text_parts = []
                for page_idx in range(start_idx, end_idx):
                    text = pdf.pages[page_idx].extract_text() or ""
                    if text.strip():
                        chapter_text_parts.append(text)

                chapter_text = "\n".join(chapter_text_parts).strip()
                if chapter_text:
                    chapters.append(
                        {
                            "title": current_chap["title"],
                            "text": chapter_text,
                            "page_start": start_idx + 1,
                            "page_end": end_idx,
                        }
                    )

    except DocumentOutlineRequiredError:
        raise
    except Exception as exc:
        raise PdfExtractionError(f"Không thể đọc nội dung PDF: {exc}") from exc

    if not chapters:
        raise PdfExtractionError(
            "PDF có outline nhưng không trích xuất được text. File có thể là scan ảnh hoặc bị lỗi."
        )

    return chapters


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

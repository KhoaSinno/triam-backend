import re

import pdfplumber
from pypdf import PdfReader


def get_pdf_outline_structure(file_obj):
    """
    Hàm này cố gắng đọc Mục lục (Bookmarks) từ metadata của PDF.
    Trả về: List [{"title": "Chapter 1", "page_start": 5}, ...] hoặc [] nếu không có.
    """
    outline_data = []
    try:
        reader = PdfReader(file_obj)
        # reader.outline chứa cấu trúc mục lục
        if not reader.outline:
            return []

        def _parse_outline(outline_items):
            for item in outline_items:
                if isinstance(item, list):
                    # Đệ quy nếu có mục lục con (Sub-chapter)
                    _parse_outline(item)
                else:
                    try:
                        # Lấy số trang (pypdf trả về page object, cần lấy index)
                        page_number = reader.get_destination_page_number(item)
                        # pypdf get đúng page number
                        outline_data.append({
                            "title": item.title,
                            "page_start": page_number
                        })
                    except Exception:
                        pass # Bỏ qua nếu item bị lỗi link

        _parse_outline(reader.outline)

        # Sắp xếp lại theo số trang để chắc chắn thứ tự đúng
        outline_data.sort(key=lambda x: x["page_start"])
        return outline_data
    except Exception as e:
        print(f"Lỗi đọc Outline: {e}")
        return []

async def extract_chapters_smart(file_obj, pages_per_chunk=10):
    """
    Hàm xử lý thông minh 3 cấp độ:
    Level 1: Dùng Outline (Mục lục ẩn).
    Level 2: Dùng Regex quét text.
    Level 3: Cắt theo số trang cố định.
    """
    # --- LEVEL 1: Dùng Mục lục Metadata ---
    # Lưu ý: Phải reset pointer file về 0 trước khi đọc
    file_obj.seek(0)
    outlines = get_pdf_outline_structure(file_obj)

    chapters = []

    if outlines and len(outlines) > 1:
        print(">> Đã tìm thấy Mục lục Metadata (Outline). Sử dụng Level 1.")

        # Mở lại bằng pdfplumber để lấy text (pdfplumber extract text ngon hơn pypdf)
        file_obj.seek(0)
        with pdfplumber.open(file_obj) as pdf:
            total_pages = len(pdf.pages)

            for i in range(len(outlines)):
                current_chap = outlines[i]
                start_p = current_chap["page_start"] - 1 # index từ 0

                # Xác định trang kết thúc (là trang bắt đầu của chương sau - 1)
                if i < len(outlines) - 1:
                    end_p = outlines[i+1]["page_start"] - 1
                else:
                    end_p = total_pages # Chương cuối thì lấy hết

                # Đảm bảo không vượt quá file
                end_p = min(end_p, total_pages)

                # Gom text từ start_p đến end_p
                chap_text = ""
                for p_idx in range(start_p, end_p):
                    text = pdf.pages[p_idx].extract_text()
                    if text:
                        chap_text += text + "\n"

                if chap_text.strip():
                    chapters.append({
                        "title": current_chap["title"],
                        "text": chap_text,
                        "page_start": start_p + 1,
                        "page_end": end_p
                    })
        return chapters

    # --- LEVEL 2: Dùng Regex (Nếu Level 1 thất bại) ---
    print(">> Không có Mục lục Metadata. Chuyển sang Level 2 (Regex Scan).")
    file_obj.seek(0)

    # Compile regex patterns cho tiêu đề chương
    chapter_patterns = [
        r'^\s*(?:Chương|CHƯƠNG|Chapter|CHAPTER)\s+(?:[IVX]+|\d+)',  # Chương 1, Chapter I, etc.
        r'^\s*(?:Phần|PHẦN|Part|PART)\s+(?:[IVX]+|\d+)',  # Phần 1, Part I, etc.
    ]
    combined_pattern = re.compile('|'.join(chapter_patterns), re.MULTILINE)

    with pdfplumber.open(file_obj) as pdf:
        total_pages = len(pdf.pages)
        chapter_markers = []  # List of {title, page_idx}

        # Quét từng trang tìm tiêu đề
        for page_idx, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue

            # Tách thành từng dòng và kiểm tra
            lines = text.split('\n')
            for line in lines[:10]:  # Chỉ check 10 dòng đầu mỗi trang
                if combined_pattern.match(line.strip()):
                    chapter_markers.append({
                        'title': line.strip(),
                        'page_idx': page_idx
                    })
                    break  # Tìm được tiêu đề rồi thì next page

        # Nếu tìm được ít nhất 2 chương
        if len(chapter_markers) >= 2:
            print(f">> Tìm được {len(chapter_markers)} chương bằng Regex.")

            for i in range(len(chapter_markers)):
                start_p = chapter_markers[i]['page_idx']

                # Xác định trang kết thúc
                if i < len(chapter_markers) - 1:
                    end_p = chapter_markers[i+1]['page_idx']
                else:
                    end_p = total_pages

                # Extract text từ start đến end
                chap_text = ""
                for p_idx in range(start_p, end_p):
                    chap_text += (pdf.pages[p_idx].extract_text() or "") + "\n"

                if chap_text.strip():
                    chapters.append({
                        "title": chapter_markers[i]['title'],
                        "text": chap_text,
                        "page_start": start_p + 1,
                        "page_end": end_p
                    })

            return chapters  # Return kết quả Level 2

    # --- LEVEL 3: Cắt Page cố định (Fallback cuối cùng) ---
    print(">> Không quét được tiêu đề. Chuyển sang Level 3 (Fixed Page Chunk).")
    file_obj.seek(0)
    with pdfplumber.open(file_obj) as pdf:
        total_pages = len(pdf.pages)
        for i in range(0, total_pages, pages_per_chunk):
            chunk_text = ""
            end_page = min(i + pages_per_chunk, total_pages)
            for p_idx in range(i, end_page):
                chunk_text += (pdf.pages[p_idx].extract_text() or "") + "\n"

            chapters.append({
                "title": f"Phần {i//pages_per_chunk + 1} (Trang {i+1}-{end_page})",
                "text": chunk_text,
                "page_start": i + 1,
                "page_end": end_page
            })

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
        pages_to_read = len(pdf.pages) if max_pages is None else min(max_pages, len(pdf.pages))

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
            print(f"Lỗi đọc trang {i+1}: {e}")

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

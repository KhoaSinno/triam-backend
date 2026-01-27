import pypdf
from fastapi import UploadFile


async def extract_text_from_pdf(file: UploadFile, max_pages: int = 5) -> str:
    """
    Trích xuất text từ file PDF upload.
    max_pages: Giới hạn số trang xử lý thử nghiệm để tránh đợi lâu.
    """
    try:
        # Đọc file từ memory (stream)
        pdf_reader = pypdf.PdfReader(file.file)

        text_content = []

        # Chỉ lấy text của max_pages trang đầu tiên (Ví dụ: Intro + Chương 1)
        num_pages = min(len(pdf_reader.pages), max_pages)

        for i in range(num_pages):
            page = pdf_reader.pages[i]
            extracted = page.extract_text()
            if extracted:
                text_content.append(extracted)

        return "\n".join(text_content)
    except Exception as e:
        print(f"Lỗi đọc PDF: {e}")
        return ""

"""
app/core/exceptions.py
======================
Domain-specific exception classes cho Triam Backend.

Luồng hoạt động:
    1. Service layer raise DomainError thay vì HTTPException
    2. @app.exception_handler(AppException) trong main.py bắt tất cả và
       tự động map sang HTTP response chuẩn

Lợi ích:
    - Service layer không phụ thuộc FastAPI → dễ unit test độc lập
    - Tất cả error format tập trung một chỗ duy nhất
"""


class AppException(Exception):
    """Base class cho tất cả domain exceptions của ứng dụng."""

    status_code: int = 500
    detail: str = "An unexpected error occurred."

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.__class__.detail
        super().__init__(self.detail)


# ---------------------------------------------------------------------------
# 404 Not Found
# ---------------------------------------------------------------------------


class BookNotFoundError(AppException):
    status_code = 404
    detail = "Book not found."


class ReadingPlanNotFoundError(AppException):
    status_code = 404
    detail = "Chưa có ReadingPlan cho sách này."


class NoReadingPlanError(AppException):
    """Book tồn tại nhưng user chưa có reading plan."""
    status_code = 400
    detail = "User has no reading plan for this book."


class StudyContextNotFoundError(AppException):
    status_code = 404
    detail = "Study context not found."


class ThreadNotFoundError(AppException):
    status_code = 404
    detail = "Thread not found."


# ---------------------------------------------------------------------------
# 400 Bad Request
# ---------------------------------------------------------------------------


class UnsupportedFileTypeError(AppException):
    status_code = 400
    detail = "Loại file không hỗ trợ. Chỉ chấp nhận PDF, EPUB, DOCX."


class FileTooLargeError(AppException):
    status_code = 400
    detail = "File vượt quá giới hạn 50MB."


# ---------------------------------------------------------------------------
# 409 Conflict
# ---------------------------------------------------------------------------


class BookStatusConflictError(AppException):
    status_code = 409
    detail = "Sách đang ở trạng thái không hợp lệ để thực hiện thao tác này."


# ---------------------------------------------------------------------------
# 422 Unprocessable Entity
# ---------------------------------------------------------------------------


class PdfExtractionError(AppException):
    status_code = 422
    detail = "Không thể trích xuất nội dung từ file. File có thể bị lỗi hoặc là scan ảnh."


# ---------------------------------------------------------------------------
# 500 Internal Server Error
# ---------------------------------------------------------------------------


class DataIntegrityError(AppException):
    """Dữ liệu trong DB bị corrupt hoặc không nhất quán."""
    status_code = 500
    detail = "Data integrity error."


class DatabaseError(AppException):
    """Lỗi khi thực hiện thao tác ghi vào DB."""
    status_code = 500
    detail = "Database operation failed."

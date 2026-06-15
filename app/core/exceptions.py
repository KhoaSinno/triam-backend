"""Domain exceptions raised by service/repository layers and rendered by FastAPI handlers."""


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


class ReadingPlanSessionNotFoundError(AppException):
    status_code = 404
    detail = "Không tìm thấy buổi học."


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


class ProcessingJobNotFoundError(AppException):
    status_code = 404
    detail = "Không tìm thấy tiến trình xử lý."


class NotificationNotFoundError(AppException):
    status_code = 404
    detail = "Không tìm thấy thông báo."


class ReviewItemNotFoundError(AppException):
    status_code = 404
    detail = "Không tìm thấy mục ôn tập."


# ---------------------------------------------------------------------------
# 400 Bad Request
# ---------------------------------------------------------------------------


class BadRequestError(AppException):
    status_code = 400
    detail = "Yêu cầu không hợp lệ."


class AuthTokenInvalidError(AppException):
    status_code = 401
    detail = "Token không hợp lệ hoặc đã hết hạn."


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


class DirectBookContextConflictError(AppException):
    status_code = 409
    detail = "Direct Book Context đã được tạo đồng thời. Vui lòng thử lại."


class ReadingPlanScheduleConflictError(AppException):
    status_code = 409
    detail = "Lịch học này đang trùng với một sách khác. Hãy chọn ngày hoặc giờ khác."


class ReadingPlanSessionStatusConflictError(AppException):
    status_code = 409
    detail = "Buổi học đang ở trạng thái không thể thực hiện thao tác này."


class ProcessingJobStatusConflictError(AppException):
    status_code = 409
    detail = "Job không ở trạng thái có thể retry."


class ActiveLearningBookLimitExceededError(AppException):
    status_code = 409
    detail = "Bạn đã đạt giới hạn số sách đang học. Hãy hoàn thành hoặc tạm dừng một sách trước."


# ---------------------------------------------------------------------------
# 422 Unprocessable Entity
# ---------------------------------------------------------------------------


class DocumentExtractionError(AppException):
    status_code = 422
    detail = "Không thể trích xuất nội dung từ file. File có thể bị lỗi, là scan ảnh, hoặc không có text."


class PdfExtractionError(DocumentExtractionError):
    detail = "Không thể trích xuất nội dung từ PDF. File có thể bị lỗi hoặc là scan ảnh."


class DocumentOutlineRequiredError(AppException):
    status_code = 422
    detail = "Tài liệu không có cấu trúc chương hợp lệ. Vui lòng upload PDF có bookmark/outline, EPUB có mục lục, hoặc DOCX có heading."


class DocumentTooLargeError(AppException):
    status_code = 422
    detail = "Tài liệu quá lớn để xử lý tự động. Vui lòng tách tài liệu thành file nhỏ hơn."


class LearningUnitTooLargeError(AppException):
    status_code = 422
    detail = "Một bài học trong tài liệu quá lớn để xử lý. Vui lòng tách nội dung hoặc chọn tài liệu nhỏ hơn."


class TTSInputTooShortError(AppException):
    status_code = 422
    detail = "Nội dung quá ngắn để tạo audio."


class NoPlayableAudioError(AppException):
    status_code = 422
    detail = "Không tạo được audio có thể phát cho nội dung này."


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


class ExternalServiceError(AppException):
    """Lỗi khi gọi dịch vụ bên ngoài."""

    status_code = 502
    detail = "External service operation failed."


class LLMResponseFormatError(ExternalServiceError):
    detail = "LLM trả về dữ liệu không đúng định dạng yêu cầu."


class StorageOperationError(ExternalServiceError):
    detail = "Storage operation failed."

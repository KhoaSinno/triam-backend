from app.core.constant import NotificationType


def build_notification_copy(notification_type: NotificationType, payload: dict) -> tuple[str, str]:
    match notification_type:
        case NotificationType.PLAN_REMINDER:
            return (
                "Đến giờ học rồi",
                f"Tiếp tục nghe {payload.get('book_title', 'sách của bạn')} nhé.",
            )
        case NotificationType.CONTENT_READY:
            subtype = payload.get("subtype")
            book_title = payload.get("book_title", "sách của bạn")
            if subtype == "first_playable":
                return (
                    "Có thể bắt đầu nghe rồi",
                    f"{book_title} đã có nội dung đầu tiên sẵn sàng.",
                )
            if subtype == "book_ready":
                return (
                    "Sách đã sẵn sàng",
                    f"{book_title} đã được xử lý xong.",
                )
            return (
                "Nội dung đã sẵn sàng",
                payload.get("message", "Bạn đã có nội dung mới để nghe trong TRIAM."),
            )
        case NotificationType.SPACED_REVIEW_DUE:
            return (
                "Đến lúc ôn lại rồi",
                f"Ôn nhanh: {payload.get('unit_title', 'một bài học đã học')}.",
            )
    return ("TRIAM", "Bạn có một thông báo mới.")

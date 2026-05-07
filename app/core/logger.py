import sys
import json
import logging
from pathlib import Path
from loguru import logger

# Định cấu hình đường dẫn thư mục log
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Tùy chỉnh format log hiển thị trên console (có màu sắc)
CONSOLE_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)


def setup_logger():
    # Bỏ cấu hình mặc định
    logger.remove()

    # 1. Cấu hình log ra console (cho môi trường dev)
    logger.add(
        sys.stdout,
        format=CONSOLE_FORMAT,
        level="DEBUG",
        colorize=True,
    )

    # 2. Cấu hình log ra file văn bản chuẩn (để xem local)
    logger.add(
        LOG_DIR / "app_{time:YYYY-MM-DD}.log",
        rotation="10 MB",     # Cắt file khi đạt 10MB
        retention="7 days",   # Giữ file trong 7 ngày
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        encoding="utf-8"
    )

    # 3. Cấu hình log dạng JSON (để đẩy lên ELK / Datadog trên Production)
    logger.add(
        LOG_DIR / "app_json_{time:YYYY-MM-DD}.log",
        rotation="50 MB",
        retention="14 days",
        level="INFO",
        serialize=True,       # Ghi log dưới dạng JSON chuẩn
        encoding="utf-8"
    )

    # Chuyển hướng log từ standard logging của Python sang loguru
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage())

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Bắt luôn cả log của Uvicorn và FastAPI nếu chúng chạy độc lập
    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"):
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]
        logging_logger.propagate = False

    return logger


# Singleton logger instance
log = setup_logger()

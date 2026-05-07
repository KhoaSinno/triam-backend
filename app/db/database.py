from typing import Generator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

load_dotenv()

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,         # Tắt verbose SQL log trên production
    pool_size=10,       # Connections persistent trong pool
    max_overflow=20,    # Connections tạm thêm khi pool đầy
    pool_timeout=30,    # Giây chờ nếu pool cạn
    pool_recycle=1800,  # Recycle sau 30 phút (tránh stale connections)
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

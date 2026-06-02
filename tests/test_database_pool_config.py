import pytest
from sqlalchemy.pool import NullPool, QueuePool

from app.db.database import create_db_engine, should_use_null_pool

SUPABASE_TRANSACTION_POOLER_URL = (
    "postgresql://postgres.project_ref:password@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"
)
POSTGRES_DIRECT_URL = "postgresql://postgres:password@db.example.com:5432/postgres"


def test_auto_pool_mode_uses_null_pool_for_supabase_transaction_pooler():
    assert should_use_null_pool(SUPABASE_TRANSACTION_POOLER_URL, "auto") is True

    engine = create_db_engine(SUPABASE_TRANSACTION_POOLER_URL, pool_mode="auto")
    try:
        assert isinstance(engine.pool, NullPool)
    finally:
        engine.dispose()


def test_queue_pool_mode_uses_small_queue_pool_for_direct_database_url():
    assert should_use_null_pool(POSTGRES_DIRECT_URL, "queue") is False

    engine = create_db_engine(POSTGRES_DIRECT_URL, pool_mode="queue")
    try:
        assert isinstance(engine.pool, QueuePool)
    finally:
        engine.dispose()


def test_invalid_pool_mode_fails_fast():
    with pytest.raises(ValueError):
        should_use_null_pool(POSTGRES_DIRECT_URL, "large")

import asyncio
import threading
import time

import pytest


@pytest.mark.asyncio
async def test_storage_uploads_respect_configured_loop_concurrency(monkeypatch, tmp_path):
    from app.core.config import settings
    from app.services import storage_service

    class FakeStorage:
        def from_(self, bucket):
            return self

        def upload(self, **kwargs):
            nonlocal active_uploads, peak_uploads
            with lock:
                active_uploads += 1
                peak_uploads = max(peak_uploads, active_uploads)
            time.sleep(0.03)
            with lock:
                active_uploads -= 1

        def get_public_url(self, path):
            return f"https://storage.example/{path}"

    class FakeSupabase:
        storage = FakeStorage()

    active_uploads = 0
    peak_uploads = 0
    lock = threading.Lock()
    monkeypatch.setattr(settings, "STORAGE_UPLOAD_CONCURRENCY", 1)
    monkeypatch.setattr(storage_service, "supabase", FakeSupabase())

    local_file = tmp_path / "audio.mp3"
    local_file.write_bytes(b"audio")
    urls = await asyncio.gather(
        *[
            storage_service.upload_file_to_supabase(
                str(local_file),
                f"book/part_{index}.mp3",
                "audios",
                "audio/mpeg",
            )
            for index in range(3)
        ]
    )

    assert peak_uploads == 1
    assert len(urls) == 3

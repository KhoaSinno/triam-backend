"""
app/services/storage_service.py
=================================
Utility service để upload file lên Supabase Storage.

Trước đây là app/helper/upload2supabase.py.
Di chuyển vào services/ để thống nhất cấu trúc dự án.
"""

import asyncio

import aiofiles

from app.core.supabase import supabase

from app.core.logger import log as logger


async def upload_file_to_supabase(
    local_path: str,
    storage_path: str,
    bucket: str,
    content_type: str,
    max_retries: int = 3,
    upsert: bool = True,
) -> str:
    """
    Upload file lên Supabase Storage và trả về public URL.

    Args:
        local_path: Đường dẫn file local cần upload.
        storage_path: Đường dẫn đích trong bucket.
        bucket: Tên bucket Supabase (vd: "raw_books", "audios").
        content_type: MIME type của file.
        max_retries: Số lần retry nếu upload thất bại (default 3).
        upsert: Ghi đè nếu file đã tồn tại (default True — cần cho switch-mode).

    Returns:
        Public URL của file sau khi upload thành công.
    """
    for attempt in range(max_retries):
        try:
            async with aiofiles.open(local_path, "rb") as f:
                file_bytes = await f.read()
            supabase.storage.from_(bucket).upload(
                path=storage_path,
                file=file_bytes,
                file_options={
                    "content-type": content_type,
                    "upsert": "true" if upsert else "false",
                },
            )
            return supabase.storage.from_(bucket).get_public_url(storage_path)
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2**attempt
                logger.warning(f"Upload failed (attempt {attempt + 1}/{max_retries}), retrying in {wait}s...")
                await asyncio.sleep(wait)
            else:
                logger.error(f"Upload failed after {max_retries} attempts: {e}")
                raise

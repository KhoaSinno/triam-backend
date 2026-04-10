import asyncio
import logging

import aiofiles

from app.core.supabase import supabase

logger = logging.getLogger("upload")


# -----------------------------------------------------------------------
# Helper: Upload file lên Supabase Storage
# -----------------------------------------------------------------------
async def upload_file_to_supabase(
    local_path: str,
    storage_path: str,
    bucket: str,
    content_type: str,
    max_retries: int = 3,
) -> str:
    """Upload file lên Supabase Storage và trả về public URL."""
    for attempt in range(max_retries):
        try:
            async with aiofiles.open(local_path, "rb") as f:
                file_bytes = await f.read()
            supabase.storage.from_(bucket).upload(
                path=storage_path,
                file=file_bytes,
                file_options={"content-type": content_type},
            )
            return supabase.storage.from_(bucket).get_public_url(storage_path)
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Upload failed (attempt {attempt + 1}), retrying...")
                await asyncio.sleep(2**attempt)
            else:
                logger.error(f"Upload failed after {max_retries} attempts: {e}")
                raise

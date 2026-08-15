---
name: triam-storage-orphan-cleanup
description: Project-specific rules and procedures for auditing, detecting, and purging orphan/unowned audio and raw book files from Supabase Storage in Triam Backend. Use when checking storage utilization, cleaning up leftover audio files from cancelled/failed TTS jobs or deleted books, or running storage maintenance scripts.
---

# Triam Storage Orphan Cleanup Skill

Use this skill whenever work involves auditing, detecting, or cleaning up orphan/unowned storage files in Supabase Storage (`audios` and `raw_books` buckets) for Triam Backend.

## 1. Core Principles

- **Database as Source of Truth**: A file in Supabase Storage is valid IF AND ONLY IF its path or URL is referenced by an active `Book` row, `LearningUnitSegment.audio_url`, or `LearningUnit.review_audio_url` in Postgres.
- **Definition of Orphan Assets**: Any file stored in the `audios` or `raw_books` buckets whose top-level folder prefix (book UUID) does not exist in `books` table, or whose path is not present in `learning_unit_segments` or `learning_units`, is considered an orphan/garbage asset.
- **Fail-Safe Cleanup**: Maintenance operations must support `--dry-run` to report orphan files before performing destructive deletion in batches of 100 paths per Supabase Storage API call.

## 2. Standard Maintenance Command

Run the dedicated maintenance script from the project root:

```powershell
# 1. Audit mode (Report orphan files without deleting):
$env:PYTHONPATH="."; uv run python scripts/purge_orphan_storage_assets.py --dry-run

# 2. Purge mode (Delete all detected orphan files):
$env:PYTHONPATH="."; uv run python scripts/purge_orphan_storage_assets.py
```

## 3. Realtime Prevention & Worker Rules

To prevent accumulation of orphan audio assets during book processing, background workers must adhere to:

1. **Cancellation Checks in TTS Segments**: `_process_single_script_task` in `app/services/workers/learning_unit_tts_worker.py` must check `asyncio.current_task().cancelled()` right after generating audio bytes and before invoking `upload_file_to_supabase`.
2. **Explicit Task Cancellation**: `_generate_unit_main_segments` must wrap `asyncio.gather(*tasks)` in a `try...except BaseException` block to cancel all child segment tasks if the parent unit task is cancelled or fails.
3. **Unit Rollback Cleanup**: `_cleanup_failed_unit` in `app/services/workers/learning_unit_worker.py` must invoke Supabase Storage RPC (`get_book_asset_paths`) to purge any partially uploaded audio files for that unit prefix upon failure.
4. **Book Purge Tasks**: `purge_book_storage_assets_task` in `app/tasks/book_tasks.py` must be dispatched when a book is hard-deleted from Postgres.

## 4. Verification & Audit Checklist

- Run `uv run python scripts/purge_orphan_storage_assets.py --dry-run` after large batch processing test runs or failure recovery.
- Ensure total orphan files equals 0.
- Confirm active book audio files match the expected total in `learning_unit_segments`.

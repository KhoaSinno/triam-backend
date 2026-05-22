# Phase 3 Generation Guardrails Test Report

Date: 2026-05-21

## Scope Implemented

Phase 3 implemented:

- Token/audio estimate before heavy generation.
- LLM hard limit guard before provider call.
- Long chapter chunking path for `normalize_text_for_speech`.
- LLM JSON response validation.
- Configurable concurrency for chapter/LLM/TTS/embedding.
- `chapter_processing_states` for per-chapter/per-mode status.
- `processing_jobs` estimate fields:
  - `estimated_input_tokens`
  - `estimated_audio_seconds`
- First playable unlock:
  - process first chapter first
  - set book/job `partial_ready`
  - continue remaining chapters in background
- Chapter failure no longer deletes the `chapters` row.
- TTS now fails clearly if no playable segment is produced.

## Migration

Applied:

```text
c4f0a9d8e2b1 -> d7a2f4c9b8e1, phase 3 generation guardrails
```

Current DB head:

```text
d7a2f4c9b8e1 (head)
```

## Automated Tests

Command:

```powershell
uv run pytest tests\test_phase3_generation_guardrails.py tests\test_celery_enqueue.py tests\test_processing_jobs_api.py tests\test_document_parsers.py tests\test_api_study_context.py -q
```

Result:

```text
20 passed in 32.41s
```

Focused lint:

```powershell
uv run ruff check <phase3 changed files>
```

Result:

```text
All checks passed!
```

Py compile:

```powershell
uv run python -m py_compile <phase3 changed files>
```

Result:

```text
passed
```

## Runtime Integration Probe With Real PDF

File:

```text
Chương 4_ Phương pháp luận nghiên cứu.pdf
```

This probe used:

- Real PDF file.
- Real upload route.
- Real parser.
- Real DB writes.
- Real generate-plan route.
- Mocked Supabase Storage upload/download.
- Mocked Celery enqueue.
- Mocked chapter generation to avoid LLM/TTS quota.

### Log Summary

```text
STEP 1 | PDF_FOUND | Chương 4_ Phương pháp luận nghiên cứu.pdf | bytes=106574
STEP 2 | STORAGE_UPLOAD_MOCK | bucket=raw_books path=<book_id>/original.pdf type=application/pdf
STEP 3 | UPLOAD_STATUS | 200
STEP 4 | CELERY_ENQUEUE_MOCK | queue=document args=[<book_id>, full, <job_id>]
STEP 5 | GENERATE_STATUS | 200
STEP 6 | STORAGE_DOWNLOAD_MOCK | path=<book_id>/original.pdf
STEP 7 | PROCESS_CHAPTER_MOCK | idx=0 chars=3552 tokens=1680 audio_s=350
STEP 7 | PROCESS_CHAPTER_MOCK | idx=1 chars=16337 tokens=7795 audio_s=1612
STEP 8 | MID_STATUS | book=partial_ready job=PARTIAL_READY progress=33
STEP 7 | PROCESS_CHAPTER_MOCK | idx=2 chars=14625 tokens=6978 audio_s=1420
STEP 9 | FINAL_JOB_STATUS | 200
STEP 10 | FINAL_BOOK_STATUS | ready
STEP 11 | CLEANUP_BOOK | <book_id>
```

Upload parsed outline:

```json
[
  {"title": "Chương 4: Phương pháp luận nghiên cứu", "page_start": 1},
  {"title": "Chương 5: Kết quả phân tích và so sánh", "page_start": 2},
  {"title": "Chương 6: Bàn luận và Khuyến nghị", "page_start": 6}
]
```

Final job response:

```json
{
  "status": "ready",
  "progress_percent": 100,
  "total_units": 3,
  "done_units": 3,
  "failed_units": 0,
  "estimated_input_tokens": 16453,
  "estimated_audio_seconds": 3382,
  "error_message": null
}
```

## Remaining Trade-offs

- Chunking keeps generation alive for large chapters, but global context can still be weaker than a future map-reduce/knowledge-atom pipeline.
- Chapter state is now per mode, but `Chapter.status` is still a coarse field. Later we may expose chapter mode state to FE if needed.
- We still do not enable whole-book Celery autoretry aggressively. That should wait until storage/audio cleanup is fully idempotent.
- Notification Outbox and Celery Beat remain Phase 4.
- Real auth/user quota remains a later phase; code still uses mock user in current routes.

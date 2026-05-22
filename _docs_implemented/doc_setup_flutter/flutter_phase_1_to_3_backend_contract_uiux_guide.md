# TRIAM Flutter Implementation Guide - Phase 1 to Phase 3

Date: 2026-05-22

Audience: Flutter team implementing upload, reading plan, progress, audiobook playback, switch mode, Study Context, and Voice Agent.

Status: Backend Phase 1 -> Phase 3.1 is implemented and production-tested.

Production API:

```text
https://khoasinoo-tri-am-backend.hf.space/api/v1
```

Related source documents reviewed:

```text
_docs_implemented/phase_1_processing_jobs_progress_implementation.md
_docs_implemented/phase_2_celery_redis_worker_implementation.md
_docs_implemented/phase_2_celery_redis_test_report.md
_docs_implemented/phase_3_generation_guardrails_implementation_guide.md
_docs_implemented/phase_3_generation_guardrails_test_report.md
_docs_implemented/phase_3_1_deploy_readiness_hardening_implementation_guide.md
_docs_implemented/triam_business_logic_progress_celery_roadmap.md
_docs_implemented/doc_setup_flutter/flutter_realtime_voice_text_spec.md
_docs_implemented/doc_setup_flutter/fe_imp_study_context.md
_docs_implemented/doc_setup_flutter/fe_voice_context_contract_review_spec.md
```

---

## 1. Executive Summary For FE

TRIAM currently supports this product flow:

```text
Upload structured document
-> show extracted outline
-> user chooses learning mode and reading plan
-> backend queues long-running AI/TTS work
-> Flutter polls DB-backed job progress
-> unlock listening when first playable chapter is ready
-> continue processing remaining chapters in background
-> user listens, switches mode, and chats with AI in the correct Study Context
```

The most important FE rule:

```text
Postgres processing_jobs is the source of truth for visible progress.
Flutter must not depend on Celery, Redis, worker logs, or request lifetime.
```

From Flutter's perspective:

- Phase 1 gives progress endpoints and progress states.
- Phase 2 moves heavy work to Celery/Redis, but FE contract stays the same.
- Phase 3 adds token/audio estimates, first-playable unlock, safer errors, and resumable chapter processing.
- Phase 3.1 adds deploy health endpoints and worker hardening; useful for diagnostics, not main UX.

---

## 2. Current Production Verification

Production full flow was tested with:

```text
File: Chương 4_ Phương pháp luận nghiên cứu.pdf
Book: 971058a0-183a-4371-91bd-b0373c7bf9bc
Job: 51bb5606-f502-41d9-a0ff-3823573b193d
```

Observed job flow:

```text
queued -> processing -> partial_ready 33% -> 66% -> ready 100%
```

Final job:

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

Book details after generation:

```text
Chapter 0: 9 segments, review text yes, review audio yes
Chapter 1: 42 segments, review text yes, review audio yes
Chapter 2: 33 segments, review text yes, review audio yes
```

---

## 3. Product Rules FE Must Respect

### 3.1 Supported Upload Types

Backend supports these document types:

```text
pdf
epub
docx
```

But support means "structured document", not "any file with that extension".

Required structure:

| Type | Required Structure | FE Message If Missing |
| --- | --- | --- |
| PDF | Hidden outline/bookmarks | "PDF cần có bookmark/outline chương." |
| EPUB | TOC/navigation | "EPUB cần có mục lục hợp lệ." |
| DOCX | Heading styles | "DOCX cần dùng Heading cho từng chương." |

Backend intentionally does not fallback to:

- OCR/scanned PDF.
- Regex chapter detection.
- Auto-split by page count.
- Auto-split by token count for chapter boundaries.

Reason: TRIAM is chapter-based learning. Wrong chapter boundaries break audio playlist, progress, RAG context, and review logic.

### 3.2 Upload Is Not Generation

`POST /upload` only validates and stores the document outline.

It does not generate audio yet.

After upload:

```text
Book.status = draft
Chapter.status = draft
```

Flutter must show the outline and ask user to configure a reading plan.

### 3.3 Generate Plan Starts Long-Running Work

`POST /generate-plan` returns quickly with a `job_id`.

Backend does heavy work in Celery worker:

```text
extract text -> estimate tokens/audio -> normalize with LLM -> TTS -> upload audio -> save segments -> embed knowledge
```

Flutter must poll:

```text
GET /jobs/{job_id}
```

or, after app reload:

```text
GET /books/{book_id}/processing-status
```

### 3.4 First Playable Unlock

`partial_ready` means:

```text
At least the first useful playable content is available.
```

It does not mean "exactly 50% done".

Flutter should:

- Unlock listening when `status == partial_ready`.
- Fetch book details to load available segments.
- Continue showing background progress until `ready`.
- Refresh playlist as more chapters become available.

---

## 4. Clean Flutter Architecture Recommendation

Keep Flutter code layered. Do not let widgets call `Dio` directly.

Recommended shape:

```text
lib/
  core/
    network/
      api_client.dart
      api_error.dart
      auth_interceptor.dart
    utils/
      date_time_parser.dart
      polling_controller.dart
  features/
    books/
      data/
        book_api.dart
        book_dto.dart
        book_repository.dart
      domain/
        book_models.dart
        book_status.dart
      presentation/
        library_page.dart
        upload_document_page.dart
        reading_plan_setup_page.dart
        book_detail_page.dart
        now_listening_page.dart
        processing_banner.dart
    processing_jobs/
      data/
        processing_job_api.dart
        processing_job_dto.dart
      domain/
        processing_job_models.dart
      presentation/
        job_progress_controller.dart
    study_context/
      data/
        study_context_api.dart
        study_context_repository.dart
      presentation/
        study_context_list_page.dart
        thread_list_page.dart
    agent/
      data/
        livekit_token_api.dart
      presentation/
        agent_chat_controller.dart
        livekit_agent_service.dart
```

Recommended dependencies:

- `dio` for REST.
- `json_serializable` or `freezed` for DTOs if already used.
- `riverpod` or `bloc` for state management. Pick one and stay consistent.
- `livekit_client` for realtime voice/text.
- An audio player package that supports playlist/URL playback.

Clean-code rules for FE:

- DTOs mirror backend JSON.
- Domain models are UI-friendly and null-safe.
- Repositories hide HTTP details.
- Controllers own polling lifecycle.
- Widgets render state; they should not contain networking or polling loops.
- Cancel polling timers on dispose and app background if not needed.
- Keep upload/generation/player/chat state separate. Do not put everything into one huge provider.

---

## 5. Global API Conventions

### 5.1 Base URL

Set:

```dart
const apiBaseUrl = 'https://khoasinoo-tri-am-backend.hf.space/api/v1';
```

Then call:

```text
$apiBaseUrl/upload
$apiBaseUrl/generate-plan
$apiBaseUrl/books
```

### 5.2 Auth Status

Backend currently uses `MOCK_USER_ID` in many routes.

Today:

```text
No Authorization header is required for the current deployed backend.
```

Future:

```text
When JWT auth is enabled, Flutter must send:
Authorization: Bearer <access_token>
```

Do not send `user_id` manually from FE unless a future backend contract explicitly asks for it.

### 5.3 Error Format

Domain errors return:

```json
{
  "detail": "Human-readable message"
}
```

HTTP validation errors may return FastAPI's validation format:

```json
{
  "detail": [
    {
      "loc": ["body", "mode"],
      "msg": "...",
      "type": "..."
    }
  ]
}
```

Flutter should implement one shared error parser:

```dart
String parseApiError(Object error) {
  // If response body detail is string -> show it.
  // If detail is list -> show first msg.
  // Else show a safe fallback.
}
```

### 5.4 Important HTTP Codes

| Code | Meaning | FE Behavior |
| --- | --- | --- |
| 400 | Bad input, unsupported file, file too large | Show correction message |
| 404 | Resource not found | Show missing/deleted state |
| 409 | Invalid state, for example generating plan on non-draft book | Refresh book/job state |
| 422 | Semantically invalid document or too large to process | Show actionable document guidance |
| 500 | Internal bug | Show generic retry/support message |
| 502 | External provider/storage/LLM/TTS issue | Show retry later message |

---

## 6. Canonical Enums

### 6.1 Book Status

```dart
enum BookStatus {
  draft,
  processing,
  partialReady,
  ready,
  error,
}
```

Backend JSON values:

```text
draft
processing
partial_ready
ready
error
```

### 6.2 Processing Job Status

```dart
enum ProcessingJobStatus {
  queued,
  processing,
  partialReady,
  ready,
  error,
  cancelled,
}
```

Backend JSON values:

```text
queued
processing
partial_ready
ready
error
cancelled
```

### 6.3 Processing Job Type

```text
upload
generate_plan
switch_mode
notification
review
```

FE currently mainly uses:

```text
generate_plan
switch_mode
```

### 6.4 Plan Mode

```dart
enum PlanMode {
  full,
  pareto,
}
```

Product meaning:

- `full`: preserve the book's main content and order, rewritten for listening.
- `pareto`: generate shorter high-value learning audio, prioritizing definitions, rules, core arguments, processes, formulas, and exam/useful knowledge.

Do not describe Pareto to users as "random summary". It is a focused learning mode.

---

## 7. Core DTOs For Flutter

### 7.1 Upload Response

`POST /upload`

```json
{
  "book_id": "uuid",
  "total_chapters": 3,
  "document_type": "pdf",
  "outline": [
    {
      "title": "Chương 4: Phương pháp luận nghiên cứu",
      "page_start": 1
    }
  ]
}
```

Notes:

- `page_start` can be `null` for EPUB/DOCX.
- `book_id` is a string UUID.
- Backend returns `book_id`, not full `BookResponse`.

Dart shape:

```dart
class UploadDocumentResult {
  final String bookId;
  final int totalChapters;
  final String documentType;
  final List<OutlineItem> outline;
}

class OutlineItem {
  final String title;
  final int? pageStart;
}
```

### 7.2 Generate Plan Response

`POST /generate-plan`

```json
{
  "message": "Kế hoạch học tập đã được tạo! Chúng tôi đang xử lý sách của bạn.",
  "book_id": "uuid",
  "job_id": "uuid",
  "mode": "full",
  "status": "queued",
  "progress_percent": 0
}
```

Dart shape:

```dart
class GeneratePlanResult {
  final String message;
  final String bookId;
  final String jobId;
  final PlanMode mode;
  final ProcessingJobStatus status;
  final int progressPercent;
}
```

### 7.3 Processing Job Summary

`GET /jobs/{job_id}`

`GET /books/{book_id}/processing-status`

```json
{
  "id": "uuid",
  "book_id": "uuid",
  "job_type": "generate_plan",
  "status": "processing",
  "mode": "full",
  "progress_percent": 33,
  "current_step": "Đã có nội dung đầu tiên có thể nghe. Phần còn lại đang được xử lý.",
  "total_units": 3,
  "done_units": 1,
  "failed_units": 0,
  "estimated_input_tokens": 16453,
  "estimated_audio_seconds": 3382,
  "error_message": null
}
```

Dart shape:

```dart
class ProcessingJobSummary {
  final String id;
  final String? bookId;
  final String jobType;
  final ProcessingJobStatus status;
  final PlanMode? mode;
  final int progressPercent;
  final String? currentStep;
  final int totalUnits;
  final int doneUnits;
  final int failedUnits;
  final int? estimatedInputTokens;
  final int? estimatedAudioSeconds;
  final String? errorMessage;

  bool get isTerminal =>
      status == ProcessingJobStatus.ready ||
      status == ProcessingJobStatus.error ||
      status == ProcessingJobStatus.cancelled;

  bool get canListen =>
      status == ProcessingJobStatus.partialReady ||
      status == ProcessingJobStatus.ready;
}
```

### 7.4 Book Response

`GET /books`

`GET /books/{book_id}`

```json
{
  "id": "uuid",
  "title": "Chương 4_ Phương pháp luận nghiên cứu",
  "author": null,
  "total_chapters": 3,
  "status": "ready",
  "document_type": "pdf",
  "file_url": "https://...",
  "created_at": "2026-05-22T10:00:00Z",
  "updated_at": "2026-05-22T10:10:00Z"
}
```

Important:

- API path is plural: `/books`.
- Do not call old singular `/book/{id}`.

### 7.5 Book Detail Response

`GET /books/{book_id}/details`

```json
{
  "book_status": "ready",
  "total_chapters": 3,
  "chapters": [
    {
      "id": "uuid",
      "title": "Chương 4: Phương pháp luận nghiên cứu",
      "status": "ready",
      "chapter_index": 0,
      "review_text": "...",
      "review_audio_url": "https://...",
      "chapter_segments": [
        {
          "id": 1,
          "segment_index": 0,
          "audio_url": "https://...",
          "text_content": "...",
          "duration_ms": 123000,
          "mode": "full"
        }
      ]
    }
  ]
}
```

FE rules:

- Sort chapters by `chapter_index`.
- Sort segments by `segment_index`.
- Use `chapter_segments` as the playlist source.
- `duration_ms` can be `null`; UI must not require it.
- `review_text` and `review_audio_url` can be empty strings.
- In `partial_ready`, some later chapters may have no segments yet.

### 7.6 Switch Mode Response

`POST /books/{book_id}/switch-mode`

```json
{
  "message": "Đã chuyển sang mode pareto. Hệ thống đang sinh audio trong background.",
  "needs_generation": true,
  "job_id": "uuid",
  "status": "queued",
  "progress_percent": 0
}
```

If audio already exists:

```json
{
  "message": "Đã chuyển sang mode full. Audio đã có sẵn.",
  "needs_generation": false,
  "job_id": null,
  "status": null,
  "progress_percent": null
}
```

---

## 8. Phase 1 Contract - DB Progress + Polling

### 8.1 Why FE Polls

Mobile UI needs visible progress and recovery after reload.

Correct pattern:

```text
FE starts job
-> receives job_id
-> polls job endpoint
-> renders progress
-> stops on ready/error/cancelled
```

Do not keep only in-memory progress. If user closes app and reopens, call:

```text
GET /books/{book_id}/processing-status
```

### 8.2 Polling Intervals

Recommended:

| State | Interval |
| --- | --- |
| `queued` | 2 seconds |
| `processing` | 2-3 seconds |
| `partial_ready` and user is listening | 5-10 seconds |
| App background | pause or 30-60 seconds |
| `ready/error/cancelled` | stop |

### 8.3 Polling Controller Pseudocode

```dart
class JobProgressController {
  Timer? _timer;

  Future<void> startPolling(String jobId) async {
    await _pollOnce(jobId);
    _timer?.cancel();
    _timer = Timer.periodic(const Duration(seconds: 2), (_) async {
      await _pollOnce(jobId);
    });
  }

  Future<void> _pollOnce(String jobId) async {
    final job = await repository.getJob(jobId);
    state = state.copyWith(job: job);

    if (job.status == ProcessingJobStatus.partialReady) {
      await bookRepository.refreshBookDetails(job.bookId!);
    }

    if (job.isTerminal) {
      _timer?.cancel();
      if (job.status == ProcessingJobStatus.ready) {
        await bookRepository.refreshBookDetails(job.bookId!);
      }
    }
  }

  void dispose() {
    _timer?.cancel();
  }
}
```

### 8.4 UI Mapping

| Job Status | UI |
| --- | --- |
| `queued` | Show "Đang xếp hàng xử lý", progress 0% |
| `processing` | Show progress bar and `current_step` |
| `partial_ready` | Show progress bar plus "Có thể nghe chương đầu" CTA |
| `ready` | Hide processing overlay, show full playlist |
| `error` | Show `error_message` and retry guidance |
| `cancelled` | Show cancelled state |

---

## 9. Phase 2 Contract - Celery + Redis Is Invisible To FE

Phase 2 changed execution infrastructure:

```text
FastAPI request
-> creates DB rows
-> enqueues Celery task to Redis queue document
-> returns immediately
```

Flutter must not:

- Call Redis.
- Call Celery.
- Depend on worker logs.
- Assume `generate-plan` request waits until audio is done.

Flutter must:

- Treat `generate-plan` response as "job accepted".
- Poll `processing_jobs`.
- Recover using `book_id` if `job_id` was lost.

If job stays `queued` for too long:

- Show "Đang chờ worker xử lý".
- Keep retry/polling with lower frequency.
- Optionally expose a "Thử lại sau" UX.
- This is an operational issue, not a FE parsing issue.

---

## 10. Phase 3 Contract - Guardrails, Estimates, Partial Unlock

### 10.1 Estimate Fields

Processing job may include:

```text
estimated_input_tokens
estimated_audio_seconds
```

Use them for user-friendly hints:

```dart
final minutes = (job.estimatedAudioSeconds ?? 0) / 60;
```

Suggested UI:

```text
Dự kiến khoảng 56 phút audio.
```

Do not show token count to normal users unless it is an advanced/debug UI.

### 10.2 Hard Limit Failures

If a chapter or document is too large, backend marks job `error` with `error_message`.

Flutter should show:

```text
Tài liệu quá lớn để xử lý. Vui lòng tách tài liệu thành file nhỏ hơn hoặc giảm số chương trong một file.
```

Do not keep spinner forever.

### 10.3 Chunking Is Backend-Internal

Large chapters under the hard limit may be chunked internally.

Flutter should not know or render internal LLM chunks.

Flutter sees only:

- chapter-level progress,
- final audio segments,
- review text/audio.

### 10.4 Chapter Failure Behavior

Backend no longer deletes chapter rows on processing failure.

For FE:

- Outline should remain stable.
- If whole job errors, show error state.
- If later backend exposes per-chapter processing state, FE can render chapter-level retry; currently main contract is job-level.

---

## 11. End-To-End Flow: Upload -> Plan -> Progress -> Listen

### 11.1 Sequence

```text
User selects file
-> FE validates extension and size locally
-> POST /upload multipart
-> BE validates structure and returns outline
-> FE shows outline confirmation
-> user chooses mode full/pareto, pace, schedule_config
-> POST /generate-plan
-> BE returns job_id queued
-> FE navigates to processing/listening screen
-> FE polls /jobs/{job_id}
-> partial_ready: FE fetches /books/{book_id}/details and unlocks playback
-> ready: FE refreshes details and stops polling
```

### 11.2 Upload API

```http
POST /api/v1/upload
Content-Type: multipart/form-data

file=<PDF|EPUB|DOCX>
```

Client-side validation:

- Extensions: `.pdf`, `.epub`, `.docx`.
- Size: max 50 MB.
- Show warning that file must have outline/TOC/Heading.

Do not rely only on client validation. Backend remains authoritative.

### 11.3 Generate Plan API

```http
POST /api/v1/generate-plan
Content-Type: application/json
```

Request:

```json
{
  "book_id": "uuid",
  "mode": "full",
  "pace": 1,
  "schedule_config": ["Mon", "Wed", "Fri"]
}
```

Validation:

- Only call this after successful upload.
- Backend currently allows initial plan only when book is `draft`.
- If backend returns `409`, refresh book state; user may already have generated a plan.

### 11.4 Processing Screen UX

Recommended screen content:

- Book title.
- Mode label: "Đầy đủ" or "Pareto".
- Progress bar.
- Current step from `current_step`.
- Units: `done_units / total_units`.
- Estimated audio duration if available.
- "Bạn có thể nghe chương đầu" button when `partial_ready`.
- Error card with actionable message when `error`.

Avoid:

- Blocking user on a blank loading screen.
- Assuming progress will update every second.
- Showing fake progress not tied to backend state.

---

## 12. Playback UX And Playlist Rules

### 12.1 Loading Playlist

Call:

```text
GET /books/{book_id}/details
```

Use:

```text
chapters[].chapter_segments[].audio_url
```

Build playlist:

```dart
final chapters = details.chapters..sortBy(chapterIndex);
for (final chapter in chapters) {
  final segments = chapter.chapterSegments..sortBy(segmentIndex);
}
```

### 12.2 Partial Playlist

During `partial_ready`:

- Some chapters have segments.
- Some chapters are still `draft` or `processing`.
- FE should render locked/skeleton rows for chapters without segments.

Suggested UX:

```text
Chapter 1: Playable
Chapter 2: Đang xử lý
Chapter 3: Đang xử lý
```

Do not reorder chapters based on completion time.

### 12.3 Refresh Strategy While Listening

When job is `partial_ready`:

- Poll job every 5-10 seconds.
- When `progress_percent` or `done_units` changes, refresh book details.
- Append newly available segments without disrupting current playback.

Important:

- Do not reset player position when refreshing details.
- Keep a stable local playback queue id, for example:

```text
chapter_id + mode + segment_index
```

### 12.4 Review Audio

Each chapter may have:

```text
review_text
review_audio_url
```

Recommended UI:

- After chapter segments, show "Ôn lại chương này".
- If `review_audio_url` exists, allow quick review playback.
- If only `review_text` exists, render text review.

---

## 13. Switch Mode Flow

### 13.1 UX

User can switch between:

```text
full
pareto
```

Recommended UI:

- Use segmented control or tabs.
- Show concise explanation:
  - Full: nghe kỹ, giữ mạch nội dung.
  - Pareto: nghe nhanh phần cốt lõi.

### 13.2 API

```http
POST /api/v1/books/{book_id}/switch-mode
Content-Type: application/json
```

Request:

```json
{
  "mode": "pareto"
}
```

### 13.3 If `needs_generation == false`

Backend already has audio for this mode.

FE should:

```text
refresh /books/{book_id}/details
switch playlist immediately
show success toast
```

### 13.4 If `needs_generation == true`

Backend has changed active mode and queued generation.

FE should:

```text
store job_id
show mode generation progress
poll /jobs/{job_id}
on partial_ready: refresh details and allow playback of generated mode
on ready: refresh details and stop polling
```

Important:

- Because backend switches active `ReadingPlan.mode` before generation completes, `/details` for the new mode may temporarily have empty segments.
- If FE wants to keep old audio playing while new mode is generating, it can keep the old playlist in memory, but must label UI clearly.
- The source of truth for active mode is backend after switch response.

---

## 14. App Reload And Recovery

When user reopens app:

1. Call `GET /books`.
2. For each book with status `processing` or `partial_ready`, call:

```text
GET /books/{book_id}/processing-status
```

3. Resume polling if job is not terminal.
4. If book is `partial_ready`, fetch details and show available audio.
5. If book is `ready`, fetch details normally.

Do not require the original `job_id` to be stored forever. It is nice to keep it locally, but `/processing-status` is the recovery path.

---

## 15. Book CRUD Contract

### 15.1 List Books

```http
GET /api/v1/books
```

Response:

```json
[
  {
    "id": "uuid",
    "title": "Book title",
    "author": null,
    "total_chapters": 3,
    "status": "ready",
    "document_type": "pdf",
    "file_url": "https://...",
    "created_at": "...",
    "updated_at": "..."
  }
]
```

### 15.2 Get Book

```http
GET /api/v1/books/{book_id}
```

### 15.3 Update Metadata

```http
PUT /api/v1/books/{book_id}
```

Request:

```json
{
  "title": "New title",
  "author": "Author"
}
```

### 15.4 Delete Book

```http
DELETE /api/v1/books/{book_id}
```

Response:

```json
{
  "message": "Book deleted"
}
```

FE rules:

- Use plural `/books`.
- After delete success, remove book from local list.
- If delete returns 404, treat as already gone and refresh list.

---

## 16. Study Context And Voice Agent

### 16.1 When To Use Which Chat Flow

| Scenario | Correct Flow |
| --- | --- |
| User chats from Book Detail / Now Listening | `GET /threads/for-book/{book_id}` then `/live-token/thread/{thread_id}` |
| User creates a multi-book study space | `POST /study-contexts` -> add documents -> create thread -> `/live-token/thread/{thread_id}` |
| User reopens old thread | `GET /threads/{thread_id}/messages` then `/live-token/thread/{thread_id}` |

Avoid for production app flow:

```text
GET /live-token/{book_id}
```

This endpoint is legacy/debug because it lacks `thread_id`; conversation persistence is not guaranteed.

### 16.2 Book Detail Quick Chat

Flow:

```text
GET /threads/for-book/{book_id}
-> response { context_id, thread_id, is_auto_generated: true }
-> GET /threads/{thread_id}/messages
-> GET /live-token/thread/{thread_id}
-> connect LiveKit
```

Response:

```json
{
  "context_id": "uuid",
  "thread_id": "uuid",
  "is_auto_generated": true
}
```

Flutter rules:

- Cache `thread_id` for current book session.
- On reopen, call `/threads/for-book/{book_id}` again; it is idempotent and should return the same canonical thread.
- Do not create manual Study Context UI for this quick chat path.

### 16.3 Manual Study Context

Create context:

```http
POST /api/v1/study-contexts
```

```json
{
  "title": "Ôn thi phương pháp nghiên cứu"
}
```

Add document:

```http
POST /api/v1/study-contexts/{context_id}/documents
```

```json
{
  "book_id": "uuid"
}
```

Create thread:

```http
POST /api/v1/study-contexts/{context_id}/threads
```

```json
{
  "title": "Hỏi đáp chương 4"
}
```

Get thread messages:

```http
GET /api/v1/threads/{thread_id}/messages
```

Message response:

```json
{
  "id": "uuid",
  "thread_id": "uuid",
  "is_user": true,
  "text": "Tóm tắt chương này giúp tôi",
  "source": "livekit",
  "timestamp": "2026-05-22T10:00:00Z"
}
```

### 16.4 LiveKit Token

```http
GET /api/v1/live-token/thread/{thread_id}
```

Response:

```json
{
  "token": "<livekit_jwt>",
  "room_name": "triam_<thread>_<random>"
}
```

Frontend needs:

- Backend API base URL for token.
- LiveKit Cloud URL from app config.
- `livekit_client` package.

Do not persist `room_name` as business state. It is mostly useful for debugging.

---

## 17. LiveKit DataChannel Contract

Backend realtime worker uses three topics.

### 17.1 `lk.chat`

Payload:

```text
UTF-8 plain text
```

Direction:

```text
Client -> Server: typed text question
Server -> Client: fast assistant text/greeting
```

Reliability:

```text
reliable
```

FE rule:

- `lk.chat` can be used for fast temporary UI.
- It is not the authoritative final timeline.

### 17.2 `lk.transcript`

Payload:

```json
{
  "v": 1,
  "type": "transcript",
  "role": "user",
  "text": "...",
  "id": "<uuid>",
  "ts": "2026-05-22T10:00:00.000+00:00"
}
```

Direction:

```text
Server -> Client only
```

FE rules:

- Never publish to `lk.transcript`.
- Use `id` to dedupe.
- Use `role` to render left/right bubble.
- Use `ts` for ordering when available.
- Treat transcript as authoritative for final chat timeline.

### 17.3 `lk.control`

Payload for web search toggle:

```json
{
  "type": "toggle_web_search",
  "enabled": true
}
```

Direction:

```text
Client -> Server
```

Use only when UI has a clear web-search toggle.

### 17.4 Chat Timeline Merge Rule

Recommended model:

```dart
class ChatBubble {
  final String id;
  final String role; // user | assistant
  final String text;
  final DateTime? timestamp;
  final String source; // history | transcript | chatPreview | localOptimistic
  final bool isFinal;
}
```

Merge priority:

```text
history/transcript > chatPreview/localOptimistic
```

Avoid duplicate assistant bubbles caused by both `lk.chat` and `lk.transcript`.

---

## 18. Upload Error UX

### 18.1 No Outline / TOC / Heading

HTTP:

```text
422
```

Response:

```json
{
  "detail": "Tài liệu không có cấu trúc chương hợp lệ. Vui lòng upload PDF có bookmark/outline, EPUB có mục lục, hoặc DOCX có heading."
}
```

Recommended FE message:

```text
TRIAM cần tài liệu có cấu trúc chương rõ ràng để tạo audiobook theo từng chương.
Vui lòng upload PDF có bookmark, EPUB có mục lục, hoặc DOCX có Heading.
```

### 18.2 Scanned Or Non-Selectable PDF

HTTP:

```text
422
```

Recommended FE message:

```text
File có thể là bản scan hoặc không trích xuất được chữ. Vui lòng dùng file có text selectable.
```

### 18.3 File Too Large

HTTP:

```text
400
```

Backend detail:

```text
File vượt quá giới hạn 50MB.
```

### 18.4 Unsupported Type

HTTP:

```text
400
```

Recommended FE message:

```text
TRIAM hiện chỉ hỗ trợ PDF, EPUB và DOCX.
```

---

## 19. Health Endpoints

For diagnostics:

```http
GET /api/v1/health
```

```json
{
  "status": "ok",
  "service": "triam-backend"
}
```

Background health:

```http
GET /api/v1/health/background
```

```json
{
  "status": "ok",
  "database": "ok",
  "redis": "ok",
  "document_queue_length": 0
}
```

FE app normally does not need to call these on every launch.

Use cases:

- QA screen.
- Internal diagnostics.
- Before demo.
- Support/debug when uploads stay queued.

---

## 20. Recommended Screens And States

### 20.1 Library Screen

Data:

```text
GET /books
```

Show:

- Book cover/avatar placeholder.
- Title.
- Document type.
- Status chip.
- Progress hint for processing/partial books.

Status chip mapping:

| Status | Label |
| --- | --- |
| `draft` | Chưa tạo kế hoạch |
| `processing` | Đang xử lý |
| `partial_ready` | Có thể nghe |
| `ready` | Sẵn sàng |
| `error` | Lỗi |

### 20.2 Upload Document Screen

Steps:

1. Pick file.
2. Validate local extension/size.
3. Show requirement hint.
4. Upload with progress.
5. Show extracted outline.
6. Continue to reading plan setup.

Do not jump directly to player after upload.

### 20.3 Reading Plan Setup Screen

Inputs:

- Mode: full/pareto.
- Pace: chapters/day or sessions/day.
- Schedule days.

Submit:

```text
POST /generate-plan
```

Then navigate to processing screen with:

```text
book_id
job_id
mode
```

### 20.4 Processing Screen

State source:

```text
GET /jobs/{job_id}
```

Show:

- Linear progress.
- Current step.
- Done/total chapters.
- Estimated audio time if available.
- CTA to listen when partial.

### 20.5 Book Detail Screen

Load:

```text
GET /books/{book_id}
GET /books/{book_id}/details
GET /books/{book_id}/processing-status if status is processing/partial_ready
```

Actions:

- Play chapter.
- Switch mode.
- Ask AI.
- View review.
- Delete/update metadata.

### 20.6 Now Listening Screen

Data:

- Current book detail.
- Current chapter and segment.
- Job progress if still partial.
- Canonical chat thread for book.

Rules:

- Keep player stable while refreshing details.
- Do not clear current queue on every poll.
- Append newly ready chapters.

---

## 21. Repository Method Checklist

Flutter should have methods like:

```dart
abstract class BookRepository {
  Future<List<Book>> listBooks();
  Future<Book> getBook(String bookId);
  Future<BookDetail> getBookDetails(String bookId);
  Future<UploadDocumentResult> uploadDocument(File file);
  Future<GeneratePlanResult> generatePlan({
    required String bookId,
    required PlanMode mode,
    required int pace,
    required List<String> scheduleConfig,
  });
  Future<SwitchModeResult> switchMode(String bookId, PlanMode mode);
  Future<void> deleteBook(String bookId);
}

abstract class ProcessingJobRepository {
  Future<ProcessingJobSummary> getJob(String jobId);
  Future<ProcessingJobSummary> getLatestBookJob(String bookId);
}

abstract class StudyContextRepository {
  Future<DirectBookThread> getOrCreateThreadForBook(String bookId);
  Future<List<ChatMessage>> getThreadMessages(String threadId);
  Future<LiveKitToken> getLiveKitTokenForThread(String threadId);
}
```

This keeps UI clean and makes testing easier.

---

## 22. Offline, Retry, And Lifecycle Rules

### 22.1 Network Failure During Polling

If one poll fails:

- Do not immediately mark job error.
- Show "Mất kết nối, đang thử lại".
- Retry with backoff.

Only backend `status == error` is a real job failure.

### 22.2 App Background

When app goes background:

- Pause aggressive polling.
- Keep local job state.
- On resume, call `/processing-status` or `/jobs/{job_id}`.

### 22.3 Upload Retry

If upload fails before backend returns `book_id`, user can retry upload.

If upload succeeds but app crashes before generate-plan:

- Book exists as `draft`.
- Library should show "Chưa tạo kế hoạch".
- User can continue setup later if FE exposes draft books.

### 22.4 Generate Plan Retry

If `generate-plan` request fails due to network timeout:

- Refresh book status.
- If book is now `processing`, call `/processing-status`.
- If book is still `draft`, allow retry.

Avoid double submitting blindly.

---

## 23. FE Acceptance Checklist

Upload:

- [ ] Upload PDF/EPUB/DOCX via multipart key `file`.
- [ ] Client validates 50MB and extension before request.
- [ ] Shows outline after successful upload.
- [ ] Shows clear 422 message for no outline/TOC/Heading.

Generate plan:

- [ ] Sends `book_id`, `mode`, `pace`, `schedule_config`.
- [ ] Stores `job_id`.
- [ ] Polls `/jobs/{job_id}`.
- [ ] Stops polling on terminal state.
- [ ] Recovers with `/books/{book_id}/processing-status`.

Progress:

- [ ] Renders `progress_percent`.
- [ ] Shows `current_step`.
- [ ] Shows `done_units / total_units`.
- [ ] Unlocks listening on `partial_ready`.
- [ ] Refreshes details after `partial_ready` and `ready`.

Playback:

- [ ] Sorts chapters by `chapter_index`.
- [ ] Sorts segments by `segment_index`.
- [ ] Does not reset playback when playlist refreshes.
- [ ] Handles empty segment lists during partial processing.

Switch mode:

- [ ] Calls `/books/{book_id}/switch-mode`.
- [ ] If `needs_generation=false`, refreshes details.
- [ ] If `needs_generation=true`, polls returned `job_id`.
- [ ] Handles temporary empty playlist for newly active mode.

Study Context / Voice:

- [ ] Book Detail chat uses `/threads/for-book/{book_id}`.
- [ ] LiveKit token uses `/live-token/thread/{thread_id}`.
- [ ] Loads `/threads/{thread_id}/messages`.
- [ ] Publishes typed text to `lk.chat`.
- [ ] Subscribes to `lk.transcript`.
- [ ] Never publishes to `lk.transcript`.
- [ ] Dedupes transcript by `id`.
- [ ] Optional web search toggle publishes `lk.control`.

Diagnostics:

- [ ] QA can call `/health/background`.
- [ ] FE does not depend on container logs.

---

## 24. Known Constraints For Current Phase

Current backend still has:

- Mock user identity in many routes.
- No per-user upload quota yet.
- No notification/reminder UI yet. That is Phase 4.
- No pushed realtime progress for generation; polling is the contract.
- `/live-token/{book_id}` still exists but should not be the main app path.

Planned later:

- Auth user id from JWT.
- Upload quota per account.
- Notification outbox and reminders.
- Spaced review schedules.
- Optional realtime progress push.

---

## 25. Golden Path For Flutter MVP

Implement in this order:

1. `BookRepository.listBooks/getBook/getBookDetails`.
2. Upload screen with outline preview.
3. Reading plan setup.
4. Processing job polling.
5. Partial-ready playback unlock.
6. Full player playlist refresh.
7. Switch mode.
8. Book Detail quick chat via canonical thread.
9. Manual Study Context.
10. LiveKit transcript dedupe and web-search toggle.

If a feature seems confusing, check whether the screen can answer these questions:

```text
What book is this?
What job is currently running?
What status did backend say?
Can the user listen yet?
Which thread will chat be saved into?
```

If the UI can answer those five questions, it is aligned with TRIAM Phase 1-3.

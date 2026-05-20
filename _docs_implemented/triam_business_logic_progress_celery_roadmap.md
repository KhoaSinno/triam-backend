# TRIAM Business Logic, Progress, Celery, And Reminder Roadmap

## 1. Answer: FE Co The Hien Thi Thanh Progress Khong?

Co. Voi giai phap **DB progress + polling endpoint**, FE hoan toan co the hien thi thanh progress.

Flow:

```text
FE POST /generate-plan
-> BE tao processing_jobs row
-> BE tra ve job_id/book_id/status/progress_percent
-> Worker cap nhat DB trong luc xu ly
-> FE poll GET /jobs/{job_id} moi 2-5 giay
-> FE ve progress bar theo progress_percent
```

DB progress la source of truth. Neu user tat app/mo lai, FE chi can goi lai API status la biet job dang o dau.

## 2. Product Direction Cho Capstone

TRIAM khong nen chi duoc mo ta la "ung dung doc sach bang AI". Gia tri nen ro hon:

> TRIAM la AI Learning Companion giup nguoi ban ron hoc tu sach/tai lieu bang audio, hoi dap theo ngu canh, ke hoach nghe chu dong, va on tap lap lai de ghi nho kien thuc.

Core business value:

- **Turn documents into guided learning audio**: bien PDF/EPUB/DOCX co cau truc thanh audiobook co ke hoach.
- **Active learning while listening**: user hoi AI khi khong hieu, AI tra loi dua tren study context.
- **Pareto learning mode**: rut gon kien thuc gia tri cao, khong phai tom tat tuy tien.
- **Progress and habit loop**: theo doi tien do, nhac hoc dung luc, dong vien khi user bo do.
- **Spaced review**: sau khi nghe xong, app nhac lai kien thuc cot loi theo chu ky.

## 3. Business Workflow Chuan

### 3.1 Upload Document

Goal: validate tai lieu co the hoc duoc.

Business rules:

- User upload PDF/EPUB/DOCX.
- BE validate file type, size, outline/TOC/heading.
- Neu scanned/OCR/no outline thi tra loi ro rang, khong fallback doan chuong bua.
- Tao `Book` status `draft`.
- Tao `Chapter` outline status `draft`.
- Chua generate audio o buoc upload.

Output cho FE:

```json
{
  "book_id": "...",
  "status": "draft",
  "document_type": "pdf",
  "total_chapters": 8,
  "outline": []
}
```

### 3.2 Create Reading Plan

Goal: user chon cach hoc.

Input:

- `book_id`
- `mode`: `full` hoac `pareto`
- `pace`: toc do/so phien hoc
- `schedule_config`: thoi gian hoc mong muon

Business rules:

- Chi book `draft` moi tao plan lan dau.
- Tao `ReadingPlan`.
- Tao `processing_jobs`.
- Enqueue worker xu ly.
- Book chuyen `processing`.

Output:

```json
{
  "book_id": "...",
  "job_id": "...",
  "status": "queued",
  "progress_percent": 0
}
```

### 3.3 Generate Audio And Knowledge

Goal: user duoc nghe som nhat co the.

Business rules:

- Worker uu tien chapter dau tien truoc.
- Chapter di qua cac buoc: extract text -> token check -> normalize -> TTS -> upload audio -> save segments -> embed knowledge.
- Khi co audio dau tien hoac dat nguong partial, book chuyen `partial_ready`.
- FE unlock playback khi co playable segments.
- Worker tiep tuc xu ly cac chapter con lai.
- Khi tat ca xong, book chuyen `ready`.

### 3.4 Realtime Q&A

Goal: user hoi khi dang hoc.

Business rules:

- Chat thread gan voi Study Context.
- RAG uu tien tai lieu trong context.
- Internet search la tuy chon ro rang, khong mac dinh khi khong can.
- Voice agent khong nen tu tao them text/audio duplicate neu da co LLM text pipeline rieng.

### 3.5 Reminder And Spaced Review

Goal: bien viec nghe sach thanh habit va ghi nho.

Reminder types:

- **Plan reminder**: nhac user tiep tuc nghe theo lich.
- **Recovery reminder**: user bo do/tre plan thi nhac nhe.
- **Completion celebration**: user xong chapter/book thi ghi nhan tien do.
- **Spaced review**: nhac lai kien thuc sau 1, 3, 7, 14, 30 ngay.

Business rules:

- Reminder phai ton trong timezone va quiet hours.
- Co daily cap de khong spam.
- Notification phai co idempotency key de tranh gui trung.
- Lich nam trong DB, khong nam duy nhat trong Redis/Celery memory.

## 4. Full Mode Va Pareto Mode

### Full

Full khong phai doc y nguyen tung ky tu. Full nen la:

- Giu du y va thu tu goc.
- Chuyen thanh van noi de nghe tot hon.
- Loai header/footer/page number.
- Khong cat bo kien thuc chinh.

### Pareto

Pareto khong nen chi la doi prompt.

Pareto nen la pipeline:

```text
raw chapter
-> extract knowledge atoms
-> score importance
-> select high-value atoms
-> compose short learning script
-> generate review script
```

Rubric diem quan trong:

- Dinh nghia/cot loi ly thuyet.
- Cong thuc/quy tac/quy trinh.
- Ket luan tac gia nhan manh.
- Kien thuc lap lai nhieu lan.
- Noi dung co kha nang xuat hien trong bai tap/thi/ung dung.

## 5. Xu Ly Chapter Qua Lon

Khong nen reject moi chapter lon ngay. Nen chia 2 nguong:

- **Soft limit**: vuot nguong thi dung hierarchical chunking.
- **Hard limit**: qua lon/qua ton chi phi thi tra 422 va huong dan user tach file.

Recommended pipeline:

```text
estimate tokens
-> if under limit: normalize one pass
-> if over soft limit: split by section/paragraph
-> create chapter brief
-> normalize chunks with brief + previous tail
-> stitch/QA final scripts
-> if over hard limit: reject
```

Can them vao DB/document stats:

- `estimated_tokens`
- `estimated_audio_minutes`
- `chapter_token_count`
- `processing_cost_estimate`

## 6. Technical Architecture

### Phase 1: DB Progress + Polling

Bang `processing_jobs`:

```text
id
user_id
book_id
job_type
mode
status
progress_percent
current_step
total_units
done_units
failed_units
error_message
created_at
updated_at
started_at
finished_at
```

Endpoints:

```text
GET /api/v1/jobs/{job_id}
GET /api/v1/books/{book_id}/processing-status
```

### Phase 2: Celery + Redis

Redis:

- Message broker cho Celery.
- Khong luu business state duy nhat.

Celery queues:

```text
document
llm
tts
embedding
notification
maintenance
```

Worker rules:

- Task args chi la primitive/id.
- Worker tu mo DB session.
- Retry transient errors.
- Update `processing_jobs` sau moi milestone.
- Idempotent khi retry.

### Phase 3: Celery Beat + Notification Outbox

Khong schedule hang ngan ETA task xa. Dung DB la lich that.

Bang `notification_outbox`:

```text
id
user_id
type
payload
channel
due_at
status
sent_at
error_message
idempotency_key
```

Beat task:

```text
every minute -> scan due outbox/review items -> enqueue delivery -> mark sent/error
```

## 7. FE Contract

Progress response:

```json
{
  "job_id": "...",
  "book_id": "...",
  "job_type": "generate_plan",
  "status": "processing",
  "progress_percent": 42,
  "current_step": "Generating audio for chapter 3",
  "total_units": 10,
  "done_units": 4,
  "failed_units": 0,
  "error_message": null
}
```

FE behavior:

- `queued/processing`: show progress bar.
- `partial_ready`: unlock listen button, continue showing "dang xu ly phan con lai".
- `ready`: full playlist available.
- `error`: show retry/support message.

## 8. Branching Va Hotfix Strategy

Vi FE dang connect BE deploy tren Hugging Face, khong nen dev truc tiep tren branch deploy.

Recommended branches:

```text
main              -> stable source
deploy/hf         -> branch dang deploy Hugging Face neu can rieng
develop           -> integrate feature
feature/celery-progress
feature/reminders
hotfix/<issue>
```

Workflow khi dang dev feature ma FE can hotfix:

1. Tao branch `hotfix/<short-name>` tu branch dang deploy/stable.
2. Sua loi nho, test nhanh.
3. Merge hotfix vao branch deploy/main.
4. Cherry-pick hoac merge nguoc hotfix vao branch feature dang dev.

Rule:

- Feature lon khong merge vao deploy cho den khi contract on.
- Hotfix phai nho, co test hoac manual verification.
- Neu doi API contract, viet migration plan cho FE.

## 9. Redis Va Celery Cho Fresher

### Redis La Gi?

Redis la in-memory data store. Trong du an nay, minh dung Redis chu yeu lam **message broker**:

```text
FastAPI day message "hay xu ly book X"
-> Redis giu message
-> Celery worker lay message ra lam
```

### Celery La Gi?

Celery la distributed task queue:

```text
API nhanh chong tra response
Worker xu ly viec nang o process rieng
Co retry, queues, workers, beat scheduler
```

### Celery Beat La Gi?

Celery Beat la scheduler periodic:

```text
Moi 1 phut goi task scan_due_notifications
Task query DB xem notification nao den han
Enqueue delivery task
```

## 10. Implementation Plan De Hoc Ma Khong Bi Ngop

Step 1:

- Tao `processing_jobs`.
- Implement polling endpoint.
- Van giu FastAPI BackgroundTasks tam thoi.

Step 2:

- Cap nhat generate-plan worker de update progress DB.
- FE co thanh progress.

Step 3:

- Them Redis local bang Docker.
- Them Celery app config.
- Chuyen generate-plan sang Celery task.

Step 4:

- Tach queue `llm`, `tts`, `embedding`.
- Them retry/concurrency limits.

Step 5:

- Them notification_outbox va Celery Beat.
- Tao spaced review sau khi chapter ready.

Step 6:

- Them monitoring/logging dashboard nho cho jobs.

## 11. Sources

- FastAPI BackgroundTasks: https://fastapi.tiangolo.com/tutorial/background-tasks/
- Celery Redis broker/backend: https://docs.celeryq.dev/en/latest/getting-started/backends-and-brokers/index.html
- Celery Redis guide: https://docs.celeryq.dev/en/v5.6.2/getting-started/backends-and-brokers/redis.html
- Celery task retry/state: https://docs.celeryq.dev/en/stable/userguide/tasks.html
- Celery routing queues: https://docs.celeryq.dev/en/latest/userguide/routing.html
- Celery Beat periodic tasks: https://docs.celeryq.dev/en/4.0/userguide/periodic-tasks.html
- Redis overview: https://redis.io/tutorials/what-is-redis/
- Supabase Realtime Postgres Changes: https://supabase.com/docs/guides/realtime/postgres-changes

# Phase 5 DB Dev Guide - Separate Supabase Database And Migration Plan

Date: 2026-05-28  
Status: **Free-plan setup guide + migration safety plan**  
Audience: Backend developer, capstone maintainer  
Goal: Tách một database dev riêng để làm Phase 5 mà không đụng production data.

---

## 1. Mục Tiêu

Phase 5 sẽ refactor lớn:

```text
chapters/de mục phẳng
-> document structure tree
-> book sections
-> learning units
```

Đây là thay đổi lớn về database và business logic, nên không nên test trực tiếp trên DB production.

Mục tiêu của file này:

1. Hướng dẫn tạo DB Supabase dev riêng.
2. Hướng dẫn cấu hình `.env` dev.
3. Hướng dẫn migrate/baseline schema vào DB dev.
4. Ghi rõ trade-off và lỗi dễ gặp.
5. Chốt cách làm an toàn cho dự án TriAm.

---

## 2. Kết Luận Nhanh

Có thể dùng DB khác tách biệt.

Recommendation cập nhật sau khi kiểm tra dashboard/pricing:

```text
Không dùng Supabase Branching vì Free plan không hỗ trợ.
Tạo Supabase project dev riêng nếu Free quota còn chỗ.
Nếu không tạo thêm project được thì dùng local Docker DB để test schema/migration.
Không chạy Phase 5 migration trực tiếp trên main/production.
Không dùng credential production cho local test Phase 5.
Không chạy migration Phase 5 lên production cho tới khi FE/BE test xong.
```

Lý do:

- Phase 5 có thể reset data thoải mái.
- Không làm hỏng dữ liệu sách/audio/user thật.
- Có thể test parser, upload, generate-plan, learning units bằng file thật.
- Dễ rollback: chỉ cần bỏ project dev/local DB hoặc reset DB dev.

Nguồn Supabase pricing chính thức hiện tại ghi rõ:

```text
Free plan: Branching không được bao gồm.
Free plan: có giới hạn active projects.
```

Nguồn: https://supabase.com/pricing

---

## 3. Có Mấy Cách Tách DB?

### Option A - Supabase Project Dev Mới

Tạo một Supabase project mới, ví dụ:

```text
triam-phase5-dev
```

Đây là hướng anh khuyên dùng cho em trên Free plan nếu còn project slot.

Ưu điểm:

- Miễn phí nếu còn quota active project.
- Tách biệt với production thật.
- Có đủ Supabase Auth, Storage, API, Postgres để test end-to-end.
- Phù hợp với TriAm vì upload sách/audio cần Supabase Storage.

Nhược điểm:

- DB trống, phải baseline schema.
- Phải cấu hình lại Auth/OAuth/Storage buckets/RPC.
- Free project có thể bị pause nếu không hoạt động.

Nguồn chính thức:

- https://supabase.com/pricing
- https://supabase.com/docs/guides/deployment/database-migrations

### Option B - Local Docker DB

Chạy một Postgres local bằng Docker để test migration/schema.

Máy hiện tại đã kiểm tra có Docker:

```text
Docker version 28.5.1
```

Ưu điểm:

- Miễn phí hoàn toàn.
- Reset cực nhanh.
- Rất phù hợp để test migration và model Phase 5.

Nhược điểm:

- Chỉ là Postgres, không có Supabase Auth/Storage/API đầy đủ.
- Không test được full upload audio/storage flow nếu không tự chạy Supabase local stack.
- Cần image có `pgvector`.

### Option C - Supabase Branching

Branching là hướng tốt về kỹ thuật, nhưng hiện **không phù hợp với em** vì dashboard báo phải nâng cấp Pro.

Ưu điểm:

- Tạo environment riêng từ project chính.
- Có credential riêng.
- Phù hợp test schema/migration.

Nhược điểm:

- Free plan không hỗ trợ.
- Có chi phí branch compute theo giờ trên plan trả phí.

Nguồn chính thức:

- https://supabase.com/pricing
- https://supabase.com/docs/guides/deployment/branching
- https://supabase.com/docs/guides/platform/manage-your-usage/branching

Recommendation:

```text
Ưu tiên 1: Supabase project dev mới.
Ưu tiên 2: Local Docker DB cho schema/migration.
Không dùng Branching khi còn ở Free plan.
```

---

## 4. Cảnh Báo Quan Trọng Về Alembic Hiện Tại

Anh đã kiểm tra migration chain hiện tại:

```powershell
uv run alembic heads
```

Kết quả:

```text
f6a8c2d4e9b1 (head)
```

Nhưng migration base hiện tại:

```text
7c1f860609e9_added_error_message_to_book.py
```

đang giả định các bảng cũ như `books`, `chapters`, `chapter_segments`, `book_knowledge`, `audiobook` đã tồn tại trước đó.

Vì vậy nếu em tạo một Supabase project trắng rồi chạy:

```powershell
uv run alembic upgrade head
```

có khả năng lỗi vì migration đầu tiên không phải migration khởi tạo từ zero.

Nói ngắn gọn:

```text
Alembic hiện tại phù hợp migrate DB cũ lên schema mới.
Alembic hiện tại chưa phù hợp bootstrap DB trống.
```

Do đó Phase 5 dev DB cần một trong hai hướng miễn phí:

1. Tạo Supabase project dev mới rồi baseline schema từ SQLModel hiện tại.
2. Chạy local Docker DB rồi baseline schema từ SQLModel hiện tại.

---

## 5. Setup Dev DB Miễn Phí

Vì Branching bị khóa Pro, mình dùng một trong hai hướng sau.

### 5.1 Hướng khuyên dùng - Supabase Project Dev Mới

Trong Supabase Dashboard:

```text
New project
-> Name: triam-phase5-dev
-> Region: Singapore / ap-southeast-1 nếu có
-> Database password: tạo password mạnh và lưu lại
-> Create project
```

Vì Free plan có giới hạn active project, nếu dashboard không cho tạo thêm project thì em có ba lựa chọn:

```text
1. Pause/delete project không dùng.
2. Tạo project ở org/account khác nếu hợp lệ với quy định của em.
3. Dùng local Docker DB ở mục 5.4.
```

Không dùng project production `triam-db` để test Phase 5 migration.

### 5.2 Lấy credential của project dev

Sau khi project `triam-phase5-dev` healthy:

Vào:

```text
Project Settings -> Database -> Connection string
```

Lấy connection string của DB dev.

Sau đó vào:

```text
Project Settings -> API
```

Lấy:

```text
SUPABASE_URL
SUPABASE_KEY / anon key
SUPABASE_SERVICE_ROLE_KEY
```

Supabase có nhiều loại connection string.

Theo docs Supabase:

- Direct connection phù hợp khi môi trường hỗ trợ IPv6.
- Pooler session mode phù hợp khi mạng không hỗ trợ IPv6.
- Transaction pooler phù hợp serverless/edge nhưng có hạn chế prepared statements.

Nguồn chính thức: Supabase connection strings  
https://supabase.com/docs/reference/postgres/connection-strings

Recommendation cho Alembic/local dev:

```text
Ưu tiên Direct connection nếu máy chạy được.
Nếu Direct lỗi mạng/IPv6, dùng Session pooler.
Không dùng Transaction pooler cho Alembic nếu không thật cần.
```

Format thường gặp:

```text
postgresql://postgres:<PASSWORD>@db.<PROJECT_REF>.supabase.co:5432/postgres
```

hoặc session pooler:

```text
postgresql://postgres.<PROJECT_REF>:<PASSWORD>@aws-0-<REGION>.pooler.supabase.com:5432/postgres
```

Không commit URL thật vào git.

Lỗi dễ gặp:

```text
FATAL: password authentication failed for user "postgres..."
```

Nguyên nhân thường là:

```text
DATABASE_URL vẫn còn placeholder [YOUR-PASSWORD]
hoặc password có ký tự đặc biệt chưa được URL-encode.
```

Ví dụ nếu password có `@`, `#`, `/`, `?`, `[`, `]`, `%`, cần encode trước khi đưa vào URL.

Checklist nhanh:

```text
Pooler host: aws-...pooler.supabase.com
Pooler username: postgres.<PROJECT_REF>
Password: database password thật, không phải Supabase account password
Database: postgres
```

Lưu ý: database password là password em tạo khi tạo project Supabase. Nó không phải Google login, không phải anon key, không phải service role key.

### 5.3 Setup Auth/OAuth cho project dev

Nếu FE cần login test trên project dev:

```text
Authentication -> Providers
-> bật Email provider
-> bật Google provider nếu cần OAuth
```

Google OAuth của project dev cần redirect URL/callback đúng với `SUPABASE_URL` dev, không dùng nhầm callback của production.

Nếu chỉ test migration/schema thì có thể bỏ qua OAuth trước.

### 5.4 Hướng fallback - Local Docker DB

Nếu không tạo được Supabase project dev, dùng local Postgres có pgvector:

```powershell
docker run --name triam-phase5-postgres `
  -e POSTGRES_USER=postgres `
  -e POSTGRES_PASSWORD=postgres `
  -e POSTGRES_DB=postgres `
  -p 5433:5432 `
  -d pgvector/pgvector:pg16
```

Khi đó `.env.phase5.dev` dùng:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/postgres
```

Trade-off rất quan trọng:

```text
Local Docker DB chỉ đủ tốt để test schema/migration/repository.
Nó không thay thế đầy đủ Supabase Auth/Storage/API.
Muốn test full upload/generate/audio end-to-end thì project dev trên Supabase vẫn tốt hơn.
```

Tắt local DB:

```powershell
docker stop triam-phase5-postgres
```

Xóa sạch local DB khi muốn reset:

```powershell
docker rm -f triam-phase5-postgres
```

---

## 6. Tạo File Env Dev

Tạo file local, không commit:

```text
.env.phase5.dev
```

Nội dung mẫu:

```env
DATABASE_URL=postgresql://postgres.<PROJECT_REF>:<PASSWORD>@aws-0-<REGION>.pooler.supabase.com:5432/postgres

SUPABASE_URL=https://<PROJECT_REF>.supabase.co
SUPABASE_KEY=<anon-key>
SUPABASE_SERVICE_ROLE_KEY=<service-role-key>

CELERY_BROKER_URL=<redis-cloud-url-or-local-redis>

OPENAI_API_KEY=<same-dev-key>
GEMINI_BASE_URL=<same-dev-value>
GEMINI_API_KEY=<same-dev-key>
GEMINI_MODEL_LLM=gemini-2.5-flash

LIVEKIT_API_KEY=<optional>
LIVEKIT_API_SECRET=<optional>
LIVEKIT_AGENT_NAME=triam-voice-agent-dev

ENABLE_CELERY_WORKER=false
ENABLE_NOTIFICATION_WORKER=false
ENABLE_CELERY_BEAT=false
ENABLE_VOICE_AGENT=false
RUN_MIGRATIONS_ON_START=false
```

Lưu ý quan trọng:

Hiện tại `app/core/config.py` đang gọi:

```python
load_dotenv(override=True)
```

Điều này làm `.env` có thể override biến môi trường em set trong terminal.

Vì vậy khi muốn chạy migration vào DB dev, cách ít rủi ro nhất là:

```text
1. Backup .env hiện tại.
2. Copy .env.phase5.dev thành .env.
3. Chạy migrate/dev server.
4. Restore .env production/local cũ.
```

Không chạy migration nếu chưa chắc `.env` đang trỏ vào dev DB.

---

## 7. Supabase Setup SQL Cho Project Dev

Trước khi bootstrap schema, vào Supabase SQL Editor của project dev và chạy:

```sql
create extension if not exists vector with schema extensions;
create extension if not exists pgcrypto with schema extensions;
```

Tạo Storage buckets:

```sql
insert into storage.buckets (id, name, public)
values
  ('audios', 'audios', true),
  ('raw_books', 'raw_books', false)
on conflict (id) do nothing;
```

Vì backend dùng service role để upload/download, bucket private `raw_books` vẫn ổn. Bucket `audios` nên public vì FE cần phát audio bằng URL.

Nếu muốn đơn giản trong dev, có thể để cả hai public, nhưng production nên giữ `raw_books` private.

### 7.1 RPC cần cho xoá asset

Backend hiện gọi:

```python
supabase.rpc("get_book_asset_paths", ...)
```

Tạo function:

```sql
create or replace function public.get_book_asset_paths(
  bucket_names text[],
  book_id_prefix text
)
returns table(bucket_id text, name text)
language sql
security definer
as $$
  select o.bucket_id, o.name
  from storage.objects o
  where o.bucket_id = any(bucket_names)
    and o.name like book_id_prefix || '/%';
$$;
```

### 7.2 RPC cần cho RAG search

Backend hiện gọi:

```python
supabase.rpc("match_book_knowledge", ...)
```

Tạo function:

```sql
create or replace function public.match_book_knowledge(
  query_embedding vector(1536),
  match_threshold float,
  match_count int,
  filter_book_ids uuid[]
)
returns table(
  id int,
  book_id uuid,
  chapter_id uuid,
  content text,
  similarity float
)
language sql
stable
as $$
  select
    bk.id,
    bk.book_id,
    bk.chapter_id,
    bk.content,
    1 - (bk.embedding <=> query_embedding) as similarity
  from public.book_knowledge bk
  where bk.embedding is not null
    and bk.book_id = any(filter_book_ids)
    and 1 - (bk.embedding <=> query_embedding) > match_threshold
  order by bk.embedding <=> query_embedding
  limit match_count;
$$;
```

Nếu function này chạy trước khi bảng `book_knowledge` tồn tại thì sẽ lỗi. Vì vậy chạy function này **sau** khi baseline schema đã tạo bảng.

---

## 8. Cách Migrate Cho DB Dev

### 8.1 Kiểm tra target DB trước

Trước khi migrate, luôn in ra host DB để chắc chắn không đụng production:

```powershell
Copy-Item .env .env.backup.before-phase5-dev
Copy-Item .env.phase5.dev .env

uv run python -c "from app.core.config import settings; print(settings.DATABASE_URL)"
uv run alembic current
uv run alembic heads
```

Nếu output vẫn là DB production/main thì dừng ngay.

### 8.2 Nếu dùng Supabase Project Dev Mới Hoặc Local Docker DB

Không chạy thẳng:

```powershell
uv run alembic upgrade head
```

Vì migration chain hiện tại không boot được từ DB trống.

Thay vào đó dùng dev baseline:

```text
SQLModel.create_all()
-> alembic stamp head
-> từ Phase 5 trở đi dùng alembic upgrade bình thường
```

PowerShell flow an toàn:

```powershell
# Kiểm tra đang trỏ vào DB dev
uv run python -c "from app.core.config import settings; print(settings.DATABASE_URL)"
```

Chỉ chạy tiếp nếu output là DB dev, không phải DB production.

Bootstrap schema dev:

```powershell
@'
from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlmodel import SQLModel

import app.models.db_models  # noqa: F401
from app.db.database import engine

with engine.begin() as conn:
    conn.execute(text("create extension if not exists vector with schema extensions"))
    conn.execute(text("create extension if not exists pgcrypto with schema extensions"))

SQLModel.metadata.create_all(engine)

config = Config("alembic.ini")
command.stamp(config, "head")

print("Phase 5 dev DB baseline created and stamped to Alembic head.")
'@ | uv run python -
```

Sau đó kiểm tra:

```powershell
uv run alembic current
uv run alembic heads
```

Expected:

```text
current: f6a8c2d4e9b1
heads:   f6a8c2d4e9b1
```

Sau baseline:

```text
Nếu dùng Supabase project dev: chạy SQL function `match_book_knowledge` và `get_book_asset_paths` ở mục 7.
Nếu dùng local Docker DB: chỉ cần dùng cho schema/migration; bỏ qua Storage/RPC nếu chưa test Supabase API.
```

Cuối cùng restore env cũ nếu chưa muốn dùng dev:

```powershell
Copy-Item .env.backup.before-phase5-dev .env
```

---

## 9. Khi Phase 5 Có Migration Mới

Sau khi implement model Phase 5, quy trình chuẩn:

```powershell
# đảm bảo .env đang là dev DB
uv run alembic revision --autogenerate -m "phase 5 document structure learning units"
```

Sau đó đọc file migration mới thật kỹ:

Checklist:

- Không drop nhầm bảng cũ nếu chưa chốt reset.
- Có index cho `book_id`, `user_id`, `mode`, `status`.
- Có unique constraint cho:
  - `book_sections(book_id, section_index)`
  - `learning_units(book_id, mode, unit_index)`
  - `learning_unit_sources(learning_unit_id, section_id)`
  - `learning_unit_segments(learning_unit_id, segment_index)`
- Không tạo enum trùng tên sai.
- Không sửa storage/auth schema ngoài ý muốn.

Apply vào DB dev:

```powershell
uv run alembic upgrade head
```

Verify:

```powershell
uv run alembic current
```

---

## 10. Start Local Backend Với DB Dev

Khi đã muốn test local trên DB dev:

Terminal 1:

```powershell
Copy-Item .env.phase5.dev .env
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Terminal 2 nếu test generate-plan:

```powershell
uv run celery -A app.core.celery_app.celery_app worker -Q document -l info --pool=solo --concurrency 1
```

Terminal 3 nếu test voice:

```powershell
uv run python -m app.services.agent_voice_gpt_realtime start
```

Nhưng Phase 5 DB/dev schema test nên bắt đầu với:

```text
FastAPI only
-> upload
-> inspect DB
-> generate-plan
-> worker
```

Không bật voice agent trước khi parser/learning units ổn.

---

## 11. Production Deploy Với DB Dev

Nếu muốn deploy Hugging Face Space test riêng:

Recommendation:

```text
Tạo HF Space dev riêng.
Không đổi DATABASE_URL của Space production.
```

Env trong HF dev Space:

```env
DATABASE_URL=<dev-db-url>
SUPABASE_URL=<dev-project-url>
SUPABASE_KEY=<dev-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<dev-service-role-key>
ENABLE_CELERY_WORKER=true
ENABLE_NOTIFICATION_WORKER=false
ENABLE_CELERY_BEAT=false
ENABLE_VOICE_AGENT=false
RUN_MIGRATIONS_ON_START=false
```

Không bật migration auto-run trên HF cho tới khi em thật sự tin migration an toàn.

---

## 12. Điều Anh Đã Kiểm Tra Trong Repo

Đã chạy:

```powershell
uv run alembic heads
```

Kết quả:

```text
f6a8c2d4e9b1 (head)
```

Đã kiểm tra:

```powershell
supabase --version
```

Kết quả:

```text
Supabase CLI chưa được cài trên máy hiện tại.
```

Vì repo TriAm đang dùng Alembic, không bắt buộc cần Supabase CLI để migrate DB bằng Python/Alembic.

Đã kiểm tra Docker:

```powershell
docker --version
```

Kết quả:

```text
Docker version 28.5.1
```

Nhưng Docker daemon/Docker Desktop hiện chưa chạy:

```text
Cannot connect to dockerDesktopLinuxEngine
```

Vì vậy trong turn này anh chưa thể tạo local Postgres container để baseline/migrate. Nếu chọn hướng local Docker DB, em cần mở Docker Desktop trước rồi chạy lại lệnh ở mục 5.4 và 8.

---

## 12.1 Kết Quả Setup Supabase Dev DB

Ngày chạy: 2026-05-28

Đã chạy setup trên Supabase project dev qua pooler:

```text
target_db_host=aws-1-ap-southeast-2.pooler.supabase.com
target_db_port=6543
```

Kết quả:

```text
extensions: pgcrypto, vector
schema baseline: done
alembic stamp: f6a8c2d4e9b1
missing required tables: []
buckets: audios public=true, raw_books public=false
rpcs: get_book_asset_paths, match_book_knowledge
```

Đã restore `.env` cũ sau khi setup và xóa backup tạm chứa secret.

Lỗi đã gặp và đã fix:

```text
Alembic ConfigParser lỗi khi DATABASE_URL có password URL-encoded chứa %40.
```

Fix ở:

```text
app/db/migrations/env.py
```

Nội dung fix:

```python
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL.replace("%", "%%"))
```

Lý do: Alembic dùng `ConfigParser`, nên ký tự `%` trong URL cần escape thành `%%` để không bị hiểu là interpolation.

---

## 13. Vì Sao Anh Chưa Chạy Migrate Ngay Trong Turn Này?

Chưa chạy migrate vào DB mới vì hiện tại chưa có:

```text
DATABASE_URL của Supabase dev project mới hoặc local Docker DB đã được chốt
SUPABASE_URL của dev project mới nếu muốn test full Supabase flow
SUPABASE_SERVICE_ROLE_KEY của dev project mới nếu muốn test full Supabase flow
```

Anh cũng không được phép dùng `.env` hiện tại để migrate vì nó có thể trỏ tới DB production hoặc DB đang deploy.

Nguyên tắc an toàn:

```text
Không chạy alembic upgrade nếu chưa xác nhận target database là dev DB.
```

Khi em tạo project dev hoặc chốt dùng local Docker DB, anh sẽ chạy:

```powershell
Copy-Item .env .env.backup.before-phase5-dev
Copy-Item .env.phase5.dev .env
uv run python -c "from app.core.config import settings; print(settings.DATABASE_URL)"
# nếu đúng dev:
# baseline DB dev vì migration hiện tại chưa bootstrap-safe từ DB trống
uv run alembic current
uv run alembic heads
Copy-Item .env.backup.before-phase5-dev .env
```

---

## 14. Chưa Chốt / Cần Em Quyết Định

### 14.1 Dùng Supabase Project Dev Hay Local Docker DB?

Recommendation:

```text
Nếu Free quota còn active project: tạo Supabase project dev mới.
Nếu không còn quota: dùng local Docker DB cho migration/schema trước.
Không dùng Branching vì đang bị khóa Pro.
```

### 14.2 Dev DB có reset được không?

Recommendation:

```text
Phase 5 dev DB cho phép reset thoải mái.
```

Nếu dev DB có thể reset, mình không cần migrate dữ liệu cũ từ `chapters` sang `learning_units`.

### 14.3 Có tạo HF Space dev riêng không?

Recommendation:

```text
Có, nếu FE cần test song song production.
```

Không nên để FE dev test Phase 5 trên production backend.

### 14.4 Có sửa config để hỗ trợ nhiều env file không?

Hiện tại đổi env hơi bất tiện vì code luôn đọc `.env`.

Recommendation phase nhỏ trước Phase 5:

```text
Thêm TRIAM_ENV_FILE=.env.phase5.dev
để backend đọc env file theo biến môi trường.
```

Ví dụ sau này:

```powershell
$env:TRIAM_ENV_FILE=".env.phase5.dev"
uv run alembic current
```

Trade-off:

- Sạch hơn nhiều.
- Cần sửa `app/core/config.py` và test config.

---

## 15. Best Practice

1. Không migrate khi chưa in ra target DB host.
2. Không commit `.env.phase5.dev`.
3. Không dùng service role key ở FE.
4. Không trộn Supabase Dashboard schema edit với Alembic migration nếu đã dùng Alembic.
5. Storage buckets/auth providers phải cấu hình riêng cho dev project.
6. Phase 5 migration phải chạy trên dev DB trước.
7. Sau khi Phase 5 ổn, mới quyết định migrate production hoặc reset production demo.

Nguồn Supabase migration best practice:  
https://supabase.com/docs/guides/deployment/database-migrations

Supabase docs nhấn mạnh: khi đã dùng migration, các schema change remote nên đi qua migration files để tránh lệch migration history.

---

## 16. Final Recommendation

Cho TriAm Phase 5, anh khuyên đi theo hướng này:

```text
1. Tạo Supabase project dev mới: triam-phase5-dev nếu Free quota còn chỗ.
2. Nếu không tạo được project, chạy local Docker DB bằng pgvector/pgvector:pg16.
3. Tạo .env.phase5.dev và verify target DB không phải production.
4. Baseline DB dev bằng SQLModel.create_all + alembic stamp head.
5. Tạo Phase 5 migrations mới từ schema hiện tại.
6. Test schema/migration trước, sau đó test upload/generate/worker nếu dùng Supabase project dev.
7. Khi ổn mới quyết định migrate production demo.
```

Đây là hướng ít rủi ro nhất với tình trạng migration hiện tại của repo.

---

## 17. Update - Phase 5 Dev DB Reset Completed

Ngày chạy: 2026-05-29

Em đã chốt:

```text
Không cần giữ dữ liệu cũ.
FE sẽ refactor theo contract chuẩn mới.
Phase 5 dev DB có thể reset.
```

Anh đã dùng `.env.phase5.dev` để reset Supabase dev DB và chạy test thật.

Kết quả reset:

```text
target_db_host=aws-1-ap-southeast-2.pooler.supabase.com
target_db=postgres
missing_phase5_tables=[]
alembic_version=a2c9e7f1b5d0
```

Các bước đã chạy:

```text
drop schema public cascade
create schema public
create extension vector
create extension pgcrypto
SQLModel.metadata.create_all(engine)
create storage buckets raw_books/audios nếu thiếu
create RPC get_book_asset_paths
create RPC match_book_knowledge
stamp alembic_version = a2c9e7f1b5d0
```

Lý do dùng baseline reset thay vì `alembic upgrade head` từ DB trống:

```text
Migration chain lịch sử của repo chưa bootstrap-safe.
Một số migration cũ giả định bảng/tên cũ đã tồn tại.
Vì Phase 5 dev DB được phép reset, baseline bằng current SQLModel schema là hướng ít rủi ro nhất để test architecture mới.
```

Test đã chạy sau reset:

```text
uv run pytest tests\test_document_parsers.py tests\test_learning_unit_planner.py tests\test_upload_service_batch_commit.py tests\test_celery_enqueue.py tests\test_phase3_generation_guardrails.py tests\test_phase4_2_learning_loop.py tests\test_notification_outbox_repo.py -q
```

Result:

```text
37 passed
```

Real flow đã chạy với:

```text
Chương 4_ Phương pháp luận nghiên cứu.pdf
trr.docx
generated phase5_sample.epub
```

Result:

```text
PDF full: ready, 3 units, 82 segments
DOCX pareto: ready, 4 units, 55 segments
EPUB full: ready, 1 unit, 2 segments
```

Important:

```text
.env được restore lại sau test.
Không để lại backup env tạm.
Log real flow nằm ở phase5_real_flow_test.out.log.
```

### 17.1 Migration cleanup recommendation

Trước khi reset production hoặc migrate production thật, nên làm một trong hai hướng:

Option A - production demo reset được:

```text
Tạo baseline migration mới từ schema hiện tại.
Reset DB production demo.
Run baseline.
Deploy Phase 5.
```

Option B - cần giữ data production:

```text
Viết migration chuyển dữ liệu chapters/chapter_segments sang learning_units/learning_unit_segments.
Test trên DB clone/dev.
Sau đó mới chạy production migration.
```

Với capstone hiện tại, recommendation vẫn là:

```text
Reset demo data và dùng baseline Phase 5 sạch.
```

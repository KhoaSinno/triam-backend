# Backend Skills and Rules Review

Ngay 2026-05-18.

Tai lieu nay ghi lai viec review va bo sung rule/skill backend cho Triam Backend. Muc tieu la de em co mot bo quy tac lam do an nhat quan: FastAPI, Python, SQLModel/ORM, Alembic, MVC-ish architecture, clean code, logging, testing, background jobs.

## 1. Hien Trang Truoc Khi Bo Sung

Project co 2 skill local:

- `.agents/skills/fastapi-sqlmodel-clean-architecture`
- `.agents/skills/supabase-postgres-best-practices`

Skill Supabase/Postgres kha day du ve performance va database best practices.

Skill FastAPI/SQLModel cu co ich nhung:

- Con goi layer DB la `app/crud/`, trong khi repo hien tai dung `app/repositories/`.
- Con goi router layer la `app/api/v1/endpoints/`, trong khi repo hien tai dung `app/api/v1/routers/`.
- Chua co rule ro ve logging secret, upload parser, worker session, Alembic migration review, FE contract.
- Chua mo ta dung kien truc hien tai: router -> service -> repository -> model/database.

Vi vay minh update skill hien co thay vi tao skill moi trung lap.

## 2. Skill Da Update

File:

```text
.agents/skills/fastapi-sqlmodel-clean-architecture/SKILL.md
```

Skill moi bao gom:

- Current architecture cua Triam.
- Mapping MVC-ish:
  - Controller -> `app/api/v1/routers/`
  - Model -> `app/models/db_models.py`
  - DTO/View contract -> `app/schemas/`
  - Service -> `app/services/`
  - Repository -> `app/repositories/`
  - Worker -> `app/services/workers/`
- Request flow rule.
- FastAPI rule.
- SQLModel/repository rule.
- Alembic rule.
- Background worker rule.
- Document upload/parser rule.
- Exception/logging rule.
- Python clean code rule.
- Testing rule.
- Review checklist.

## 3. Tai Sao Khong Tao Them Qua Nhieu Skill

Neu tao cac skill rieng:

- `fastapi-best-practices`
- `python-clean-code`
- `alembic-rules`
- `mvc-architecture`
- `backend-testing`

thi moi lan Codex lam backend co the phai load nhieu skill, de trung lap va mau thuan. Voi project hien tai, cac rule nay gan chat vao cung mot backend workflow, nen tot hon la update mot skill project-specific.

Skill rieng chi nen tao khi co domain lon va doc lap, vi du:

- `triam-realtime-voice-agent`
- `triam-document-ingestion`
- `triam-rag-pipeline`

Con FastAPI/ORM/Alembic/clean code nen nam chung trong backend architecture skill.

## 4. Nguon Tham Khao Uy Tin

Minh doi chieu rule voi cac nguon official:

- FastAPI Background Tasks: https://fastapi.tiangolo.com/tutorial/background-tasks/
- SQLModel Session with FastAPI Dependency: https://sqlmodel.tiangolo.com/tutorial/fastapi/session-with-dependency/
- SQLAlchemy Session Basics: https://docs.sqlalchemy.org/20/orm/session_basics.html
- Alembic Autogenerate: https://alembic.sqlalchemy.org/en/latest/autogenerate.html
- Alembic Documentation: https://alembic.sqlalchemy.org/

Nhung rule trong skill van uu tien kien truc that cua repo, khong copy may moc tu docs.

## 5. Rule Quan Trong Em Nen Nho

### Router phai mong

Router chi nen:

- Nhan request.
- Inject `Session`.
- Goi service.
- Return response.

Khong de router:

- Parse PDF/DOCX/EPUB.
- Goi LLM/TTS truc tiep.
- Viet transaction phuc tap.
- Xu ly business rule dai.

### Service la noi quyet dinh nghiep vu

Service duoc phep:

- Goi repository.
- Goi parser/storage/LLM/TTS.
- Dieu phoi nhieu buoc.
- Raise domain exception.

Nhung service khong nen:

- Tra `HTTPException`.
- Tu format response loi FastAPI.
- Log secret/full payload.

### Repository chi noi chuyen voi DB

Repository nen:

- Nhan `session: Session`.
- Query/mutate DB.
- Khong biet FastAPI la gi.
- Khong goi Supabase Storage, LLM, parser.

### Alembic la bat buoc khi doi schema

`create_all()` khong phai migration. No tao table moi neu chua co, nhung khong quan ly thay doi schema that su cho production.

Moi khi them/sua/xoa column/table/index/constraint:

```powershell
uv run alembic revision --autogenerate -m "message"
```

Sau do doc file migration truoc khi:

```powershell
uv run alembic upgrade head
```

### Worker phai co session rieng

FastAPI request session het han sau response. Background worker khong duoc giu session do. Worker phai:

```python
with Session(engine) as session:
    ...
```

Va phai update status de FE poll.

### Upload support phai end-to-end

Neu noi support DOCX/EPUB/PDF thi phai support:

- MIME/extension detection.
- Parser.
- Storage path.
- DB record.
- Background worker download lai dung file.
- Error message 422 khi file khong co cau truc.

Khong chi sua endpoint upload.

## 6. Review Checklist Cho Moi PR Backend

Truoc khi merge, tu hoi:

- Route co mong khong?
- Logic nghiep vu co nam trong service khong?
- DB query co nam trong repository khong?
- Schema change co Alembic migration khong?
- Worker co session rieng khong?
- Co log secret/token/header/full payload khong?
- FE response contract co bi doi khong, da document chua?
- Co test regression cho bug vua fix khong?
- `ruff` va focused `pytest` da pass chua?

## 7. Huong Phat Trien Skill Tiep Theo

Nen tao skill rieng khi cac module nay lon hon:

- Realtime voice agent: LiveKit, OpenAI Realtime, transcript contract, echo/noise rules.
- Document ingestion: PDF/EPUB/DOCX/OCR, parser contract, chunking, validation.
- RAG pipeline: embedding, Pinecone/Postgres vector, retrieval policy, citations.
- FE-BE contract: OpenAPI/schema, response versioning, DataChannel contract.

Truoc mat, skill backend architecture moi la du de Codex tu giu dung style khi lam backend.

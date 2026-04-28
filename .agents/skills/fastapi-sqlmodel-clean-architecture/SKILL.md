---
name: fastapi-sqlmodel-clean-architecture
description: Project-specific guidelines for Triam Backend. Use this skill when developing new features, creating API endpoints, working with SQLModel/PostgreSQL, or handling background AI/TTS tasks in this specific codebase.
---

# Triam Backend: FastAPI + SQLModel Architecture Guide

This project follows a strict layered **Clean Architecture** using **FastAPI** and **SQLModel**. 
To ensure code maintainability, you must adhere to the specific structure and patterns defined below when adding new features or modifying existing ones.

---

## 1. Directory Structure & Responsibilities

Do not mix responsibilities. Code must be placed in the correct layer.

| Directory | Responsibility | Implementation Rules |
| :--- | :--- | :--- |
| `app/models/db_models.py` | **Database Schema** | Contains `SQLModel(table=True)` classes. This is the single source of truth for the database schema. |
| `app/schemas/` | **Data Validation (DTOs)** | Contains `SQLModel(table=False)` or Pydantic `BaseModel` classes used for API Request/Response validation. |
| `app/crud/` | **Database Operations** | Contains repository functions that interact with the database using `sqlmodel.Session`. **No HTTP logic here.** |
| `app/services/` | **Core Business Logic** | Handles external integrations (LLM, TTS, PDF parsing) and heavy data processing. |
| `app/api/v1/endpoints/` | **API Routers** | Defines FastAPI routes. Routes should be thin: validate input, call CRUD/Services, return response. |
| `app/helper/` | **Utilities & Background** | Shared utility functions (e.g., Supabase uploaders) and heavy background task orchestrators (`run_background_processing.py`). |
| `app/core/` | **Configuration** | Setup for Database, Supabase client, and environment variables. |

---

## 2. Database Modeling (SQLModel)

When adding or modifying tables, always use SQLModel.

*   **Primary Keys:** Always use `uuid.UUID` with `default_factory=uuid.uuid4` for primary keys unless there is a specific reason not to.
*   **Foreign Keys:** Define explicit foreign keys using `Field(foreign_key="table_name.id")`.

```python
# app/models/db_models.py
import uuid
from sqlmodel import SQLModel, Field

class ExampleEntity(SQLModel, table=True):
    __tablename__ = "example_entities"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    book_id: uuid.UUID = Field(foreign_key="books.id")
    mode: str = Field(default="full")
```

---

## 3. CRUD Operations Pattern

All database queries must be isolated in the `app/crud/` directory. 
*   **Always** pass `session: Session` as the first argument to CRUD functions.
*   **Do not** create database sessions inside the CRUD functions themselves.

```python
# app/crud/example.py
import uuid
from typing import Optional
from sqlmodel import Session, select
from app.models.db_models import ExampleEntity

def get_entity_by_id(session: Session, entity_id: uuid.UUID) -> Optional[ExampleEntity]:
    return session.get(ExampleEntity, entity_id)

def get_entities_by_book(session: Session, book_id: uuid.UUID) -> list[ExampleEntity]:
    return session.exec(select(ExampleEntity).where(ExampleEntity.book_id == book_id)).all()

def create_entity(session: Session, entity: ExampleEntity) -> ExampleEntity:
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity
```

---

## 4. API Endpoints & Dependency Injection

API Routers in `app/api/v1/endpoints/` must follow these rules:

1.  **Session Injection:** Inject the database session using `Depends(get_session)`.
2.  **Thin Controllers:** Endpoints should primarily handle HTTP requests, validate via Pydantic/Schemas, call CRUD/Services, and return HTTP responses.
3.  **Background Tasks:** For heavy AI/TTS operations, ALWAYS return a fast HTTP response (`200 OK` or `202 Accepted`) and delegate the heavy lifting to FastAPI's `BackgroundTasks`.

```python
# app/api/v1/endpoints/example.py
import uuid
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session
from app.db import get_session
from app.crud.example import get_entity_by_id
from app.helper.run_background_processing import some_heavy_task

router = APIRouter()

@router.post("/process/{entity_id}")
def process_entity(
    entity_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    entity = get_entity_by_id(session, entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
        
    # Delegate heavy work to background
    background_tasks.add_task(some_heavy_task, entity_id)
    
    return {"message": "Processing started in background."}
```

---

## 5. Storage & External Integrations

### Supabase Storage
For file uploads (PDFs, Audio), use the established Supabase client in `app.core.supabase`.
*   **Upserting:** When overwriting files (e.g., during a mode switch), ensure you pass `upsert="true"` in the `file_options` to avoid `409 Duplicate` errors.
*   **Path Isolation:** Always isolate file paths logically, especially for different AI modes (e.g., `/{book_id}/chap_1/full/part_1.mp3` vs `/{book_id}/chap_1/pareto/part_1.mp3`).

### Background AI Processing (LLM & TTS)
*   Do not run LLM calls or TTS generation directly in the API request thread.
*   Background workers (in `app/helper/run_background_processing.py`) should use `asyncio.Semaphore` to limit concurrency and avoid hitting API rate limits.
*   Update database status (e.g., `status="READY"` or `status="ERROR"`) within the background task so the frontend can poll for updates.

---

## 6. Development Workflow Checklist

When asked to implement a new feature in this project, follow this exact sequence:

- [ ] **1. Schema (Models):** Update or create tables in `app/models/db_models.py`.
- [ ] **2. Validation (Schemas):** Create Pydantic input/output models in `app/schemas/`.
- [ ] **3. Data Access (CRUD):** Write robust database operations in `app/crud/`.
- [ ] **4. Business Logic (Services):** Write AI prompts, TTS logic, or storage handlers in `app/services/` or `app/helper/`.
- [ ] **5. Routing (API):** Wire everything together in `app/api/v1/endpoints/`, ensuring background tasks are used for slow operations.
- [ ] **6. Database Sync:** If schema changed, remind the user to run Alembic migrations (`alembic revision --autogenerate` and `alembic upgrade head`).

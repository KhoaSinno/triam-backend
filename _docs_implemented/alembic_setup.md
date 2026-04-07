# Alembic Database Migration Setup

## Overview

Alembic is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python. In this project, it is used to automatically synchronize your `SQLModel` model definitions (Python code) with your actual database schema hosted on Supabase (PostgreSQL).

## 1. Installation

To install Alembic into the project dependency environment, we use `uv`:

```bash
uv add alembic
```

## 2. Initialization

To generate the necessary Alembic folder structure (the `migrations/` directory and `alembic.ini` file) run:

```bash
uv run alembic init migrations
```

## 3. Configuration (`migrations/env.py`)

By default, Alembic does not know about your FastAPI application's database connection string or your SQLModel schemas.
We modified `migrations/env.py` to bridge this gap:

```python
from app.core.config import settings
from sqlmodel import SQLModel
# Import all db models to make sure they are included in SQLModel.metadata
from app.models import db_models

# Pass the SQLModel metadata to Alembic for 'autogenerate' support
target_metadata = SQLModel.metadata

# Dynamically set sqlalchemy.url from our application settings
# This prevents hardcoding secrets into alembic.ini
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
```

## 4. Standard Workflow Commands

Every time you modify your `app/models/db_models.py` (e.g., adding a new column, modifying nullability, or adding new tables), follow these exactly two steps:

### Step 4.1: Generate a Migration Script

This command connects to your database, compares it with your current Python `SQLModel` definitions, and generates a script containing the exact SQL operations needed to bridge the differences:

```bash
uv run alembic revision --autogenerate -m "added error_message to book"
```

_Note: Replace `"added error_message to book"` with a short, descriptive name of what you changed so you can track history easily._

### Step 4.2: Apply the Migration

This executes the generated migration script against your live Supabase database.

```bash
uv run alembic upgrade head
```

_(The term `head` instructs Alembic to upgrade the database schema to the latest available revision)._

## FAQ / Key Concepts

> [!NOTE]
> **Why not just rely on `SQLModel.metadata.create_all()`?**
>
> While `create_all()` safely creates any missing tables upon app startup, it **does not** alter existing tables (e.g., adding or removing columns). Alembic is fundamentally required because it can calculate diffs and systematically run `ALTER TABLE` operations.

> [!TIP]
> **Database Safety**
>
> You can—and should—manually inspect the generated Python files dumped inside the `migrations/versions/` directory after running `--autogenerate`. This allows you to verify that Alembic didn't accidentally drop a table before forcefully applying changes via `upgrade head`.

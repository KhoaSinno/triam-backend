import os
import sys
import uuid
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select
from app.models.db_models import ChatThread, StudyContext, StudyContextDocumentLink, ChatMessage, Book

load_dotenv()

database_url = os.getenv("DATABASE_URL")
print(f"Connecting to database: {database_url}")
engine = create_engine(database_url)

thread_id = uuid.UUID("07be00b9-c6da-4801-8ba2-7558205b92b2")
book_id = uuid.UUID("195d9623-03d0-483a-ac09-52d9137f2471")
context_id = uuid.UUID("dd123da9-95ed-4736-8c79-3161262c2a15")

with Session(engine) as session:
    # 1. Inspect Book
    book = session.get(Book, book_id)
    if book:
        print(f"\n📖 Book found: ID={book.id}, Title={book.title}, UserID={book.user_id}, Status={book.status}")
    else:
        print(f"\n❌ Book not found: ID={book_id}")

    # 2. Inspect StudyContext
    context = session.get(StudyContext, context_id)
    if context:
        print(f"\n📂 StudyContext found: ID={context.id}, Title={context.title}, UserID={context.user_id}")
    else:
        print(f"\n❌ StudyContext not found: ID={context_id}")

    # 3. Inspect ChatThread
    thread = session.get(ChatThread, thread_id)
    if thread:
        print(f"\n💬 ChatThread found: ID={thread.id}, Title={thread.title}, ContextID={thread.context_id}")
    else:
        print(f"\n❌ ChatThread not found: ID={thread_id}")

    # 4. Inspect links
    links = session.exec(select(StudyContextDocumentLink).where(StudyContextDocumentLink.context_id == context_id)).all()
    print(f"\n🔗 StudyContextDocumentLinks for context {context_id}:")
    for link in links:
        print(f"   - BookID={link.book_id}")

    # 5. Inspect ChatMessages for this thread
    messages = session.exec(select(ChatMessage).where(ChatMessage.thread_id == thread_id).order_by(ChatMessage.timestamp)).all()
    print(f"\n💬 ChatMessages for thread {thread_id}: {len(messages)}")
    for msg in messages:
        role = "USER" if msg.is_user else "AGENT"
        print(f"   [{msg.timestamp}] {role}: {msg.text} (Source: {msg.source})")

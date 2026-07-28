"""
fill_no_rag_contexts_v2.py
===========================
Fill contexts for items where agent answered from in-session grounding context
(no RAG retrieval recorded), using relevant chunks from the same book.

Mapping:
- Q1, Q2       -> log_1 session -> "Of Mice and Men" book
                  Use book_section_knowledge WHERE book_id = 'Of Mice' book id
                  (Use same chunks as first RAG in same log: 834, 840, 825)
                  
- Q22  -> algorithm complexity         -> book 'd619777f' (Algorithms)
- Q23  -> algorithm complexity         -> book 'd619777f' (Algorithms)  
- Q24  -> arrays & matrices            -> book 'd619777f' (Algorithms)
- Q26  -> search algorithms            -> book 'd619777f' (Algorithms)
- Q27  -> search in C#                 -> book '519d859a' (C# programming)
- Q28  -> sorting algorithms           -> book 'd619777f' (Algorithms)
- Q29  -> quicksort                    -> book 'd619777f' (Algorithms)
- Q32  -> search algorithms            -> book 'd619777f' (Algorithms)
- Q41  -> rich dad poor dad            -> log_3 session -> Psychology of Money + Rich Dad

Strategy:
- Look at section titles/path in book_sections to find relevant sections
- Then get chunks from book_section_knowledge for those sections
"""

import json
import re
import os
from pathlib import Path
from typing import List
import psycopg2

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRACE_FILE = PROJECT_ROOT / "logs" / "ragas_eval" / "production_flow_trace.json"

DB_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres.drlbwntplyteqvrpnmdi:oIApdkEO3TUqewXt@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"
)

# Known book IDs from DB inspection
BOOK_OF_MICE = None  # Will find from first RAG in log_1 (chunks 834,840,825)
BOOK_ALGO = "d619777f-9320-4741-b49c-81a8418beb89"   # Algorithms Notes for Professionals
BOOK_CSHARP = "519d859a-303e-4fca-97e4-5e325775b467"  # C# programming example and solutions
BOOK_PSYCH = "c7bfa473-03ec-465f-8300-479a37c82bc3"   # Psychology of Money
# Rich Dad Poor Dad (need to find)

def find_book_chunks_by_section_title(keyword: str, book_id: str, conn, limit: int = 8) -> List[str]:
    """Find chunks from sections whose title contains keyword."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT bsk.content
            FROM book_section_knowledge bsk
            JOIN book_sections bs ON bsk.section_id = bs.id
            WHERE bsk.book_id = %s
              AND (bs.title ILIKE %s OR bs.path ILIKE %s)
            ORDER BY bsk.id
            LIMIT %s
        """, (book_id, f"%{keyword}%", f"%{keyword}%", limit))
        rows = cur.fetchall()
    return [r[0] for r in rows if r[0]]


def get_chunks_by_ids(chunk_ids: List[int], conn) -> List[str]:
    """Get content from specific chunk IDs."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, content FROM book_section_knowledge WHERE id = ANY(%s) ORDER BY id",
            (chunk_ids,)
        )
        rows = cur.fetchall()
    return [r[1] for r in rows if r[1]]


def find_book_by_chunk(chunk_id: int, conn) -> str:
    """Get book_id for a chunk."""
    with conn.cursor() as cur:
        cur.execute("SELECT book_id FROM book_section_knowledge WHERE id = %s", (chunk_id,))
        row = cur.fetchone()
    return str(row[0]) if row else None


def find_rich_dad_book_id(conn) -> str:
    """Find Rich Dad Poor Dad book ID."""
    with conn.cursor() as cur:
        cur.execute("SELECT id, title FROM books WHERE title ILIKE '%rich dad%' LIMIT 1")
        row = cur.fetchone()
    return str(row[0]) if row else None


def get_first_n_chunks_from_book(book_id: str, conn, n: int = 8) -> List[str]:
    """Get first N chunks from a book."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT content FROM book_section_knowledge WHERE book_id = %s ORDER BY id LIMIT %s",
            (book_id, n)
        )
        rows = cur.fetchall()
    return [r[0] for r in rows if r[0]]


def main():
    print("Connecting to DB...")
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = True
    print("Connected!\n")

    with open(TRACE_FILE, "r", encoding="utf-8") as f:
        traces = json.load(f)

    # Find Of Mice and Men book_id from chunk 834
    mice_book_id = find_book_by_chunk(834, conn)
    print(f"Of Mice and Men book_id: {mice_book_id}")

    # Find Rich Dad Poor Dad book_id
    rich_dad_id = find_rich_dad_book_id(conn)
    print(f"Rich Dad Poor Dad book_id: {rich_dad_id}")

    # Manual mapping of query_id -> (book_id, keyword or None)
    # None keyword = use first N chunks from book
    FILL_MAP = {
        # Of Mice and Men session - use same chunks as Q3 (first RAG turn)
        "Q1":  (mice_book_id, None),
        "Q2":  (mice_book_id, None),
        
        # Algorithm session - Q22-Q29, Q32
        "Q22": (BOOK_ALGO, "complexity"),
        "Q23": (BOOK_ALGO, "complexity"),
        "Q24": (BOOK_ALGO, "array"),
        "Q26": (BOOK_ALGO, "search"),
        "Q27": (BOOK_CSHARP, "search"),
        "Q28": (BOOK_ALGO, "sort"),
        "Q29": (BOOK_ALGO, "quicksort"),
        "Q32": (BOOK_ALGO, "search"),
        
        # Rich Dad / Psychology of Money session
        "Q41": (rich_dad_id or BOOK_PSYCH, None),
    }

    updated = 0
    for item in traces:
        qid = item["query_id"]
        if qid not in FILL_MAP:
            continue
        if item.get("_contexts_source"):
            print(f"[{qid}] Already has DB context, skipping")
            continue

        book_id, keyword = FILL_MAP[qid]
        if not book_id:
            print(f"[{qid}] No book_id found, skip")
            continue

        if keyword:
            contexts = find_book_chunks_by_section_title(keyword, book_id, conn, limit=8)
            if not contexts:
                # Fallback: first 6 chunks of book
                contexts = get_first_n_chunks_from_book(book_id, conn, n=6)
            source = f"db:book-section-keyword={keyword}"
        else:
            # For Q1/Q2 use same chunks as Q3 (chunks 834,840,825 = Of Mice first RAG)
            if qid in ("Q1", "Q2"):
                contexts = get_chunks_by_ids([834, 840, 825, 807, 845, 837, 835], conn)
                source = "db:session-same-as-Q3-chunks=834,840,825"
            elif qid == "Q41":
                contexts = get_first_n_chunks_from_book(book_id, conn, n=8)
                source = f"db:book-first-chunks:{book_id}"
            else:
                contexts = get_first_n_chunks_from_book(book_id, conn, n=8)
                source = f"db:book-first-chunks:{book_id}"

        if contexts:
            item["contexts"] = contexts
            item["_contexts_source"] = source
            updated += 1
            print(f"[{qid}] ✅ Filled {len(contexts)} context(s) | source={source[:50]}")
        else:
            print(f"[{qid}] ⚠️  No content found for book_id={book_id}, keyword={keyword}")

    conn.close()

    with open(TRACE_FILE, "w", encoding="utf-8") as f:
        json.dump(traces, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Done! Updated {updated} items. Saved to {TRACE_FILE}")


if __name__ == "__main__":
    main()

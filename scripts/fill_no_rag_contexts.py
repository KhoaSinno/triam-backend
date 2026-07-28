"""
scripts/fill_no_rag_contexts.py
===============================
Cho các câu Q1, Q2, Q22-Q29, Q32, Q41 - agent trả lời từ GROUNDING CONTEXT 
(không dùng RAG search_book_knowledge) mà dùng system prompt context load 
toàn bộ sections khi khởi tạo session.

Strategy: Lấy section IDs từ bảng book_sections theo book_id
- Session log_live_context_1.md: books=1, "Of Mice and Men" → Q1, Q2 (câu về sách)
- Session log_live_context_2_1.md: books=2, "Algorithm" → Q22-Q29, Q32
- Session log_live_context_3.md → Q41

Tìm book_id từ resolved_book_ids trong AGENT_TRACE sau trong cùng session,
rồi query book_sections.content theo book_id.
"""

import json
import re
import os
from pathlib import Path
from typing import Optional, List
import psycopg2

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRACE_FILE = PROJECT_ROOT / "logs" / "ragas_eval" / "production_flow_trace.json"

LOG_FILES = {
    "log_live_context_1.md":   PROJECT_ROOT / "log_live_context_1.md",
    "log_live_context_2.md":   PROJECT_ROOT / "log_live_context_2.md",
    "log_live_context_2_1.md": PROJECT_ROOT / "log_live_context_2_1.md",
    "log_live_context_3.md":   PROJECT_ROOT / "log_live_context_3.md",
    "log_live_context_3_1.md": PROJECT_ROOT / "log_live_context_3_1.md",
}

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres.drlbwntplyteqvrpnmdi:oIApdkEO3TUqewXt@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"
)

_log_cache: dict[str, list[str]] = {}


def get_log_lines(fname: str) -> list[str]:
    if fname not in _log_cache:
        fpath = LOG_FILES[fname]
        with open(fpath, "r", encoding="utf-8") as f:
            _log_cache[fname] = f.readlines()
    return _log_cache[fname]


def find_first_rag_trace(fname: str) -> Optional[dict]:
    """Find the first AGENT_TRACE with retrieval in this log file."""
    lines = get_log_lines(fname)
    for line in lines:
        if "AGENT_TRACE" in line and ("turn_completed" in line or "retrieval_completed" in line):
            m = re.search(r"AGENT_TRACE \w+ \| (\{.*\})$", line.strip())
            if m:
                try:
                    d = json.loads(m.group(1))
                    if d.get("retrieval_chunk_ids") or d.get("retrieval_section_ids"):
                        return d
                except:
                    pass
    return None


def find_thread_book_ids(fname: str) -> List[str]:
    """
    Extract book IDs from log: search for resolved_book_ids in any AGENT_TRACE.
    If none, look for section_ids from any retrieval.
    """
    lines = get_log_lines(fname)
    # Look for resolved_book_ids
    for line in lines:
        if "AGENT_TRACE" in line and "resolved_book_ids" in line:
            m = re.search(r"AGENT_TRACE \w+ \| (\{.*\})$", line.strip())
            if m:
                try:
                    d = json.loads(m.group(1))
                    bids = d.get("resolved_book_ids", [])
                    if bids:
                        return bids
                except:
                    pass
    return []


def find_section_ids_from_rag(fname: str) -> List[str]:
    """Find section IDs from first successful RAG in this log."""
    lines = get_log_lines(fname)
    for line in lines:
        if "AGENT_TRACE" in line:
            m = re.search(r"AGENT_TRACE \w+ \| (\{.*\})$", line.strip())
            if m:
                try:
                    d = json.loads(m.group(1))
                    sids = d.get("retrieval_section_ids", [])
                    if sids:
                        return sids
                except:
                    pass
    return []


def query_sections_by_ids(section_ids: List[str], conn, limit=5) -> List[str]:
    """Query book_sections by UUIDs, returning content."""
    if not section_ids:
        return []
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, content FROM book_sections WHERE id = ANY(%s) LIMIT %s",
            (section_ids[:limit], limit)
        )
        rows = cur.fetchall()
    return [row[1] for row in rows if row[1]]


def query_sections_by_book_id(book_id: str, conn, limit=5) -> List[str]:
    """Query book_sections by book_id."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, content FROM book_sections WHERE book_id = %s ORDER BY id LIMIT %s",
            (book_id, limit)
        )
        rows = cur.fetchall()
    return [row[1] for row in rows if row[1]]


def query_chunks_by_ids(chunk_ids: List[str], conn) -> List[str]:
    """Query book_section_knowledge by ids."""
    if not chunk_ids:
        return []
    ids_int = []
    for cid in chunk_ids:
        try:
            ids_int.append(int(cid))
        except:
            pass
    if not ids_int:
        return []
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, content FROM book_section_knowledge WHERE id = ANY(%s) ORDER BY id",
            (ids_int,)
        )
        rows = cur.fetchall()
    return [row[1] for row in rows if row[1]]


def main():
    print("Connecting to DB...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    print("Connected!")

    with open(TRACE_FILE, "r", encoding="utf-8") as f:
        traces = json.load(f)

    # Targets: items that still have no _contexts_source AND are book_rag
    targets = [
        item for item in traces
        if not item.get("_contexts_source")
        and item.get("route") == "book_rag"
    ]
    print(f"\nFound {len(targets)} book_rag items without DB contexts\n")

    for item in targets:
        qid = item["query_id"]
        log_ref = item.get("intent_log_ref", "")
        if ":" not in log_ref:
            print(f"[{qid}] SKIP - no log ref")
            continue

        fname, lstr = log_ref.rsplit(":", 1)
        fname = fname.strip()
        if fname not in LOG_FILES:
            print(f"[{qid}] SKIP - log file not mapped: {fname}")
            continue

        # Strategy: use retrieval_section_ids from the FIRST rag retrieval in this session
        rag_trace = find_first_rag_trace(fname)
        if rag_trace:
            chunk_ids = rag_trace.get("retrieval_chunk_ids", [])
            section_ids = rag_trace.get("retrieval_section_ids", [])
            
            contexts = []
            if chunk_ids:
                print(f"[{qid}] Using first-rag chunk_ids from {fname}: {chunk_ids[:3]}...")
                contexts = query_chunks_by_ids(chunk_ids, conn)
            if not contexts and section_ids:
                print(f"[{qid}] Using first-rag section_ids from {fname}: {section_ids[:2]}...")
                contexts = query_sections_by_ids(section_ids, conn)
            
            if contexts:
                item["contexts"] = contexts
                item["_contexts_source"] = f"db:session-first-rag:chunks={chunk_ids[:3]}"
                print(f"[{qid}] ✅ Filled {len(contexts)} context(s) from first-session RAG")
            else:
                print(f"[{qid}] ⚠️ DB returned empty even from first-rag trace")
        else:
            print(f"[{qid}] ❌ No RAG trace found in entire {fname}")

    conn.close()

    with open(TRACE_FILE, "w", encoding="utf-8") as f:
        json.dump(traces, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Done! Saved to {TRACE_FILE}")


if __name__ == "__main__":
    main()

"""
scripts/fill_contexts_from_db.py
==================================
Fill `contexts` trong production_flow_trace.json bằng nội dung THỰC SỰ từ DB.

Logic:
1. Đọc intent_log_ref (vd: "log_live_context_1.md:L41") → mở file log → đọc dòng L41
2. Tìm AGENT_TRACE turn_completed gần nhất có retrieval_chunk_ids (scan forward/backward ±40 dòng)
3. Nếu turn đó không có chunk_ids (session memory turn): scan NGƯỢC lại toàn file để lấy
   chunk_ids của lần RAG cuối cùng trước đó (cùng session = cùng file log)
4. Query bảng book_section_knowledge (id IN chunk_ids) để lấy content thực tế
5. Fallback: retrieval_section_ids → query bảng book_sections
6. Fill vào contexts, không bịa gì cả
"""

import json
import re
import os
from pathlib import Path
from typing import Optional
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

# Cache log lines
_log_cache: dict[str, list[str]] = {}


def get_log_lines(fname: str) -> list[str]:
    if fname not in _log_cache:
        fpath = LOG_FILES[fname]
        with open(fpath, "r", encoding="utf-8") as f:
            _log_cache[fname] = f.readlines()
    return _log_cache[fname]


def extract_trace_near_line(fname: str, target_line: int) -> Optional[dict]:
    """
    Tìm AGENT_TRACE gần target_line nhất có retrieval_chunk_ids.
    Nếu không tìm thấy (session memory turn), scan NGƯỢC toàn file lấy RAG turn cuối cùng.
    """
    lines = get_log_lines(fname)
    target_idx = target_line - 1  # 0-indexed

    def parse_trace(line_text: str) -> Optional[dict]:
        for event in ["turn_completed", "retrieval_completed"]:
            if f"AGENT_TRACE {event}" in line_text:
                m = re.search(r"AGENT_TRACE \w+ \| (\{.*\})$", line_text.strip())
                if m:
                    try:
                        return json.loads(m.group(1))
                    except:
                        pass
        return None

    # Phase 1: Scan ±40 dòng xung quanh target_line
    search_range = 40
    best_trace = None
    for offset in range(0, search_range):
        for idx in [target_idx + offset, target_idx - offset]:
            if 0 <= idx < len(lines):
                t = parse_trace(lines[idx])
                if t:
                    if t.get("retrieval_chunk_ids") or t.get("retrieval_section_ids"):
                        return t  # Found a turn with actual retrieval
                    if best_trace is None:
                        best_trace = t  # Keep for fallback

    # Phase 2: Session memory turn - scan BACKWARD from target_line để lấy RAG gần nhất
    # Đây là hành vi thực tế: agent dùng lại context của lần RAG trước trong cùng session
    for idx in range(target_idx, -1, -1):
        t = parse_trace(lines[idx])
        if t and (t.get("retrieval_chunk_ids") or t.get("retrieval_section_ids")):
            return t  # Last known RAG context in this session

    return best_trace


def query_chunks(chunk_ids: list[str], conn) -> list[str]:
    """Query book_section_knowledge by chunk IDs."""
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


def query_sections(section_ids: list[str], conn) -> list[str]:
    """Query book_sections by section UUIDs."""
    if not section_ids:
        return []
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, content FROM book_sections WHERE id = ANY(%s)",
            (section_ids,)
        )
        rows = cur.fetchall()
    return [row[1] for row in rows if row[1]]


def main():
    print(f"🔌 Connecting to DB...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    print(f"✅ DB connected!")

    with open(TRACE_FILE, "r", encoding="utf-8") as f:
        traces = json.load(f)

    updated = 0
    skipped_no_trace = 0
    skipped_no_chunks = 0
    kept_existing = 0

    for item in traces:
        qid = item.get("query_id", "?")
        intent_log_ref = item.get("intent_log_ref", "")
        route = item.get("route", "")

        # Bỏ qua web_policy / book_metadata - không có RAG context
        if route in ("web_policy", "book_metadata"):
            print(f"  [{qid}] SKIP (route={route}) - not RAG")
            continue

        # Parse intent_log_ref
        if ":" not in intent_log_ref:
            print(f"  [{qid}] SKIP - no intent_log_ref")
            skipped_no_trace += 1
            continue

        fname, lstr = intent_log_ref.rsplit(":", 1)
        if not lstr.startswith("L"):
            print(f"  [{qid}] SKIP - bad intent_log_ref format: {intent_log_ref}")
            skipped_no_trace += 1
            continue

        target_line = int(lstr[1:])
        fname = fname.strip()

        if fname not in LOG_FILES:
            print(f"  [{qid}] SKIP - log file not found: {fname}")
            skipped_no_trace += 1
            continue

        # Extract AGENT_TRACE
        trace_data = extract_trace_near_line(fname, target_line)

        if not trace_data:
            print(f"  [{qid}] SKIP - no AGENT_TRACE near {fname}:L{target_line}")
            skipped_no_trace += 1
            continue

        chunk_ids = trace_data.get("retrieval_chunk_ids", [])
        section_ids = trace_data.get("retrieval_section_ids", [])

        if not chunk_ids and not section_ids:
            print(f"  [{qid}] SKIP - AGENT_TRACE has no chunk/section IDs")
            skipped_no_chunks += 1
            continue

        # Query DB
        contexts = []

        if chunk_ids:
            print(f"  [{qid}] Querying {len(chunk_ids)} chunks: {chunk_ids[:3]}...")
            chunk_texts = query_chunks(chunk_ids, conn)
            contexts.extend(chunk_texts)

        if not contexts and section_ids:
            print(f"  [{qid}] Fallback: querying {len(section_ids)} sections...")
            section_texts = query_sections(section_ids, conn)
            contexts.extend(section_texts)

        if not contexts:
            print(f"  [{qid}] ⚠️  DB returned empty for chunk_ids={chunk_ids[:3]}")
            skipped_no_chunks += 1
            continue

        item["contexts"] = contexts
        item["_contexts_source"] = f"db:chunks={chunk_ids[:5]}"
        updated += 1
        print(f"  [{qid}] ✅ Filled {len(contexts)} context chunk(s)")

    conn.close()

    # Save
    with open(TRACE_FILE, "w", encoding="utf-8") as f:
        json.dump(traces, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"✅ DONE! Updated: {updated} | Skip(no trace): {skipped_no_trace} | Skip(no data): {skipped_no_chunks}")
    print(f"📁 Saved to: {TRACE_FILE}")


if __name__ == "__main__":
    main()

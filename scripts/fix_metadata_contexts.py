"""
Fix Q20 and Q59 which have book_metadata route but still need real contexts
from the last RAG retrieval in their respective session.
"""
import json
import re
import os
from pathlib import Path
import psycopg2

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRACE_FILE = PROJECT_ROOT / "logs" / "ragas_eval" / "production_flow_trace.json"

LOG_FILES = {
    "log_live_context_1.md":   PROJECT_ROOT / "log_live_context_1.md",
    "log_live_context_3.md":   PROJECT_ROOT / "log_live_context_3.md",
}

DB_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres.drlbwntplyteqvrpnmdi:oIApdkEO3TUqewXt@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"
)


def find_last_rag_before_line(fname: str, target_line: int):
    fpath = LOG_FILES[fname]
    with open(fpath, encoding="utf-8") as f:
        lines = f.readlines()
    
    target_idx = target_line - 1
    # Scan backward from target_line
    for idx in range(target_idx, -1, -1):
        line = lines[idx]
        if "AGENT_TRACE" in line and ("turn_completed" in line or "retrieval_completed" in line):
            m = re.search(r"AGENT_TRACE \w+ \| (\{.*\})$", line.strip())
            if m:
                try:
                    d = json.loads(m.group(1))
                    cids = d.get("retrieval_chunk_ids", [])
                    if cids:
                        return d
                except:
                    pass
    return None


def query_chunks(chunk_ids, conn):
    ids_int = [int(c) for c in chunk_ids if str(c).isdigit()]
    if not ids_int:
        return []
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, content FROM book_section_knowledge WHERE id = ANY(%s) ORDER BY id",
            (ids_int,)
        )
        rows = cur.fetchall()
    return [r[1] for r in rows if r[1]]


def main():
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = True

    with open(TRACE_FILE, encoding="utf-8") as f:
        traces = json.load(f)

    targets = {"Q20": "log_live_context_1.md:L936", "Q59": "log_live_context_3.md:L906"}

    for item in traces:
        qid = item["query_id"]
        if qid not in targets:
            continue
        if item.get("_contexts_source"):
            print(f"[{qid}] Already has source, skip")
            continue

        log_ref = targets[qid]
        fname, lstr = log_ref.rsplit(":", 1)
        target_line = int(lstr[1:])

        print(f"[{qid}] Looking for last RAG before L{target_line} in {fname}...")
        trace = find_last_rag_before_line(fname, target_line)
        if not trace:
            print(f"  ❌ No RAG found")
            continue

        chunk_ids = trace.get("retrieval_chunk_ids", [])
        print(f"  Found chunks: {chunk_ids[:5]}")
        contexts = query_chunks(chunk_ids, conn)
        if contexts:
            item["contexts"] = contexts
            item["_contexts_source"] = f"db:last-session-rag:chunks={chunk_ids[:5]}"
            print(f"  ✅ Filled {len(contexts)} context(s)")
        else:
            print(f"  ⚠️ DB returned empty")

    conn.close()
    with open(TRACE_FILE, "w", encoding="utf-8") as f:
        json.dump(traces, f, ensure_ascii=False, indent=2)
    print("\n✅ Done!")


if __name__ == "__main__":
    main()

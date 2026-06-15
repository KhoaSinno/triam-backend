import os
import statistics
import sys
import time
from pathlib import Path

import httpx

from dotenv import load_dotenv

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def get_env_required(name: str) -> str:
    val = os.getenv(name)
    if not val:
        print(f"Error: Environment variable {name} is required for this benchmark script.")
        print(f"Please set {name} and run again.")
        sys.exit(1)
    return val

def run_benchmark():
    load_dotenv(override=True)
    base_url = os.getenv("TRIAM_API_BASE_URL", "http://127.0.0.1:8000/api/v1").rstrip("/")
    token = get_env_required("TRIAM_ACCESS_TOKEN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    client = httpx.Client(headers=headers, base_url=base_url, timeout=30.0)

    # 1. Probe library to find a book_id
    print("Probing library to find test book...")
    try:
        resp = client.get("/books")
        if resp.status_code != 200:
            print(f"Failed to probe library: {resp.status_code} - {resp.text}")
            sys.exit(1)
        books = resp.json()
    except Exception as e:
        print(f"Connection error: {e}")
        sys.exit(1)

    book_id = None
    if books:
        book_id = books[0]["id"]
        print(f"Found book: {books[0].get('title')} ({book_id})")
    else:
        print("Warning: Library is empty. Book details and plan endpoints will be skipped.")

    endpoints = [
        ("/books", "GET"),
        ("/notifications?limit=30", "GET"),
    ]

    if book_id:
        endpoints.extend([
            (f"/books/{book_id}", "GET"),
            (f"/books/{book_id}/details", "GET"),
            (f"/books/{book_id}/outline", "GET"),
            (f"/books/{book_id}/reading-plan", "GET"),
            ("/reading-plan/sessions/today", "GET"),
        ])

    print("\nStarting benchmark (10 runs per endpoint)...")
    print("| Endpoint | Method | p50 (ms) | p95 (ms) | Max (ms) | Status |")
    print("| --- | --- | --- | --- | --- | --- |")

    for path, method in endpoints:
        latencies = []
        status_codes = set()

        # Warm-up run
        try:
            client.get(path) if method == "GET" else client.post(path)
        except Exception:
            pass

        for _ in range(10):
            start = time.perf_counter()
            try:
                if method == "GET":
                    r = client.get(path)
                else:
                    r = client.post(path)
                status_codes.add(r.status_code)
            except Exception:
                status_codes.add("ERROR")

            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies.append(elapsed_ms)

        p50 = statistics.median(latencies)
        p95 = sorted(latencies)[int(len(latencies) * 0.95) - 1]
        max_val = max(latencies)
        status_str = ",".join(str(s) for s in status_codes)

        print(f"| `{path}` | {method} | {p50:.1f} | {p95:.1f} | {max_val:.1f} | {status_str} |")

if __name__ == "__main__":
    run_benchmark()

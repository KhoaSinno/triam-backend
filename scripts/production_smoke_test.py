from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Any

import httpx

TERMINAL_JOB_STATUSES = {"ready", "error", "cancelled"}


def _print_json(label: str, payload: dict[str, Any]) -> None:
    print(f"\n[{label}]")
    for key, value in payload.items():
        print(f"{key}: {value}")


def _request_json(client: httpx.Client, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
    response = client.request(method, path, **kwargs)
    try:
        payload = response.json()
    except ValueError:
        payload = {"raw_body": response.text}

    if response.status_code >= 400:
        _print_json(f"{method} {path} failed with HTTP {response.status_code}", payload)
        raise SystemExit(1)

    return payload


def _check_health(client: httpx.Client, require_background_ok: bool) -> None:
    health = _request_json(client, "GET", "/api/v1/health")
    _print_json("health", health)
    if health.get("status") != "ok":
        raise SystemExit("API health is not ok.")

    background_health = _request_json(client, "GET", "/api/v1/health/background")
    _print_json("background health", background_health)
    if require_background_ok and background_health.get("status") != "ok":
        raise SystemExit("Background health is degraded.")


def _upload_document(client: httpx.Client, pdf_path: Path) -> str:
    if not pdf_path.exists():
        raise SystemExit(f"File not found: {pdf_path}")

    with pdf_path.open("rb") as file_obj:
        response = _request_json(
            client,
            "POST",
            "/api/v1/upload",
            files={"file": (pdf_path.name, file_obj, "application/pdf")},
            timeout=180,
        )

    _print_json("upload", response)
    book_id = response.get("book_id")
    if not book_id:
        raise SystemExit("Upload response does not contain book_id.")
    return str(book_id)


def _generate_plan(client: httpx.Client, book_id: str, mode: str, pace: int, schedule_config: list[str]) -> str:
    response = _request_json(
        client,
        "POST",
        "/api/v1/generate-plan",
        json={
            "book_id": book_id,
            "mode": mode,
            "pace": pace,
            "schedule_config": schedule_config,
        },
        timeout=60,
    )

    _print_json("generate-plan", response)
    job_id = response.get("job_id")
    if not job_id:
        raise SystemExit("Generate-plan response does not contain job_id.")
    return str(job_id)


def _poll_job(client: httpx.Client, job_id: str, timeout_seconds: int, interval_seconds: int, accept_partial: bool) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    last_payload: dict[str, Any] = {}

    while time.monotonic() < deadline:
        last_payload = _request_json(client, "GET", f"/api/v1/jobs/{job_id}", timeout=30)
        status = str(last_payload.get("status"))
        progress = last_payload.get("progress_percent")
        step = last_payload.get("current_step")
        print(f"job={job_id} status={status} progress={progress}% step={step}")

        if status == "partial_ready" and accept_partial:
            return last_payload
        if status in TERMINAL_JOB_STATUSES:
            if status != "ready":
                _print_json("job terminal error", last_payload)
                raise SystemExit(1)
            return last_payload

        time.sleep(interval_seconds)

    _print_json("last job payload before timeout", last_payload)
    raise SystemExit(f"Timed out waiting for job {job_id}.")


def _read_book_processing_status(client: httpx.Client, book_id: str) -> None:
    payload = _request_json(client, "GET", f"/api/v1/books/{book_id}/processing-status", timeout=30)
    _print_json("book processing status", payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smoke test a deployed TRIAM API without exposing secrets.")
    parser.add_argument("--base-url", default=os.getenv("TRIAM_API_BASE_URL", "http://127.0.0.1:8000"), help="API base URL, for example https://<space>.hf.space")
    parser.add_argument("--access-token", default=os.getenv("TRIAM_ACCESS_TOKEN"), help="Supabase access token for authenticated user-owned APIs.")
    parser.add_argument("--pdf-path", type=Path, help="Optional PDF path to upload through the production API.")
    parser.add_argument("--book-id", help="Existing book id to inspect or generate a plan for.")
    parser.add_argument("--job-id", help="Existing job id to inspect or poll.")
    parser.add_argument("--generate-plan", action="store_true", help="Create a generate-plan job for the uploaded/existing book.")
    parser.add_argument("--mode", choices=["full", "pareto"], default="full")
    parser.add_argument("--pace", type=int, default=1)
    parser.add_argument("--schedule-day", action="append", dest="schedule_days", help="Repeatable schedule day, e.g. --schedule-day Mon --schedule-day Wed.")
    parser.add_argument("--poll", action="store_true", help="Poll job until ready/error/cancelled.")
    parser.add_argument("--check-book-status", action="store_true", help="Call /books/{book_id}/processing-status even when no job id is available.")
    parser.add_argument("--accept-partial", action="store_true", help="Exit successfully when a job reaches partial_ready.")
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    parser.add_argument("--interval-seconds", type=int, default=10)
    parser.add_argument("--request-timeout", type=int, default=60)
    parser.add_argument("--require-background-ok", action="store_true", help="Fail when Redis/DB background health is degraded.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_url = args.base_url.rstrip("/")
    schedule_config = args.schedule_days or ["Mon"]
    headers = {"Authorization": f"Bearer {args.access_token}"} if args.access_token else {}

    with httpx.Client(base_url=base_url, timeout=args.request_timeout, headers=headers) as client:
        _check_health(client, args.require_background_ok)

        if (args.pdf_path or args.book_id or args.job_id or args.generate_plan) and not args.access_token:
            raise SystemExit("Authenticated smoke steps require --access-token or TRIAM_ACCESS_TOKEN.")

        book_id = args.book_id
        if args.pdf_path:
            book_id = _upload_document(client, args.pdf_path)

        job_id = args.job_id
        if args.generate_plan:
            if not book_id:
                raise SystemExit("--generate-plan requires --book-id or --pdf-path.")
            job_id = _generate_plan(client, book_id, args.mode, args.pace, schedule_config)

        if book_id and (job_id or args.check_book_status):
            _read_book_processing_status(client, book_id)

        if job_id:
            if args.poll:
                final_job = _poll_job(client, job_id, args.timeout_seconds, args.interval_seconds, args.accept_partial)
            else:
                final_job = _request_json(client, "GET", f"/api/v1/jobs/{job_id}", timeout=30)
            _print_json("job", final_job)

    print("\nSmoke test completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

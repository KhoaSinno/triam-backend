# ruff: noqa: E402
"""Run a real, DB-free A/B test for Full-mode Gemini normalization.

Example:
    uv run python scripts/manual_integration/full_mode_normalize_ab.py `
      --export-file "C:/Users/Lenovo/Downloads/Of Mice And Men_full_mode_export.json" `
      --chapter-index 4 --chunk-tokens 5000 --include-scripts

The script reads GEMINI_API_KEY and GEMINI_BASE_URL through app settings. It
does not create audio, connect to Postgres, or update any book records.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter

# Allow direct execution with `uv run python scripts/manual_integration/...py`.
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from app.core.config import settings
from app.services.chapter_chunking_service import TextChunk
from app.services.llm_service import _call_normalize_llm
from app.services.token_budget_service import estimate_tokens

DEFAULT_SEPARATORS = ["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""]
PAGE_MARKER_RE = re.compile(r"^\s*\[\d+]\s*\n?")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="A/B-test Full mode normalization without DB or TTS writes.")
    parser.add_argument("--export-file", type=Path, required=True, help="Path to admin Full-mode JSON export.")
    parser.add_argument("--chapter-index", type=int, default=4, help="Zero-based section index to test; default 4 is Chapter 5.")
    parser.add_argument("--chunk-tokens", type=int, default=5000, help="Token target for the chunked strategy.")
    parser.add_argument("--dry-run", action="store_true", help="Validate the input and show call plan without calling Gemini.")
    parser.add_argument("--include-scripts", action="store_true", help="Include generated script text in the ignored local report.")
    parser.add_argument("--output-dir", type=Path, default=Path("script_outputs"), help="Directory for local JSON reports.")
    return parser.parse_args()


def _strip_page_marker(text: str) -> str:
    return PAGE_MARKER_RE.sub("", text or "").strip()


def _append_without_export_overlap(combined: str, next_part: str) -> str:
    """Remove the exact overlap inserted in exported embedding chunks."""
    if not combined:
        return next_part
    max_overlap = min(len(combined), len(next_part), 5000)
    for length in range(max_overlap, 0, -1):
        if combined[-length:] == next_part[:length]:
            return combined + next_part[length:]
    return combined + "\n\n" + next_part


def reconstruct_section_text(section: dict[str, Any]) -> str:
    combined = ""
    for chunk in section.get("chunks", []):
        content = _strip_page_marker(str(chunk.get("content") or ""))
        if content:
            combined = _append_without_export_overlap(combined, content)
    return combined.strip()


def split_without_overlap(text: str, chunk_tokens: int) -> list[TextChunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_tokens,
        chunk_overlap=0,
        length_function=estimate_tokens,
        separators=DEFAULT_SEPARATORS,
    )
    parts = [part.strip() for part in splitter.split_text(text) if part.strip()]
    return [TextChunk(index=index, text=part, estimated_tokens=estimate_tokens(part)) for index, part in enumerate(parts)]


def serialize_result(main_scripts: list[str], review_script: str, source_text: str, *, include_scripts: bool) -> dict[str, Any]:
    main_text = " ".join(main_scripts).strip()
    result: dict[str, Any] = {
        "main_script_count": len(main_scripts),
        "main_chars": len(main_text),
        "source_chars": len(source_text),
        "main_to_source_char_ratio": round(len(main_text) / len(source_text), 4) if source_text else 0,
        "review_chars": len(review_script),
    }
    if include_scripts:
        result["main_scripts"] = main_scripts
        result["review_script"] = review_script
    return result


async def normalize_single_call(source_text: str) -> tuple[dict[str, Any], list[str], str]:
    normalized = await _call_normalize_llm(source_text, "full")
    return (
        serialize_result(normalized.main_scripts, normalized.review_script, source_text, include_scripts=False),
        normalized.main_scripts,
        normalized.review_script,
    )


async def normalize_chunked(source_text: str, title: str, chunks: list[TextChunk]) -> tuple[dict[str, Any], list[str], str]:
    all_scripts: list[str] = []
    review_parts: list[str] = []
    previous_tail = ""
    for chunk in chunks:
        print(f"Calling chunk {chunk.index + 1}/{len(chunks)} ({chunk.estimated_tokens} estimated tokens)...")
        context_hint = (
            f"Bài học: {title}.\n"
            f"Đây là phần {chunk.index + 1}/{len(chunks)} của cùng một bài học.\n"
            "Giữ mạch văn nối tiếp với phần trước. Không tự nhắc 'phần' hoặc 'chunk' trong câu trả lời.\n"
            f"Đoạn cuối phần trước để nối ngữ cảnh: {previous_tail[-600:]}"
        )
        normalized = await _call_normalize_llm(chunk.text, "full", context_hint=context_hint)
        all_scripts.extend(normalized.main_scripts)
        review_parts.append(normalized.review_script)
        previous_tail = chunk.text[-1000:]
    review_script = " ".join(part for part in review_parts if part).strip()
    return serialize_result(all_scripts, review_script, source_text, include_scripts=False), all_scripts, review_script


async def main() -> None:
    args = parse_args()
    if args.chunk_tokens < 1000:
        raise SystemExit("--chunk-tokens must be at least 1000.")
    if not args.export_file.is_file():
        raise SystemExit(f"Export file not found: {args.export_file}")
    if not settings.GEMINI_API_KEY:
        raise SystemExit("GEMINI_API_KEY is not configured. Add it to .env before running this script.")

    payload = json.loads(args.export_file.read_text(encoding="utf-8"))
    sections = payload.get("sections") or []
    if args.chapter_index < 0 or args.chapter_index >= len(sections):
        raise SystemExit(f"--chapter-index must be between 0 and {len(sections) - 1}.")

    section = sections[args.chapter_index]
    source_text = reconstruct_section_text(section)
    chunks = split_without_overlap(source_text, args.chunk_tokens)
    if not source_text:
        raise SystemExit("Selected section has no reconstructable source text.")

    plan = {
        "model": settings.GEMINI_MODEL_LLM,
        "section_index": section.get("section_index"),
        "section_title": section.get("title"),
        "source_chars": len(source_text),
        "source_estimated_tokens": estimate_tokens(source_text),
        "single_call_requests": 1,
        "chunked_call_requests": len(chunks),
        "chunk_tokens": [chunk.estimated_tokens for chunk in chunks],
        "overlap_tokens": 0,
    }
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    if args.dry_run:
        return

    print("Calling baseline single-request Full normalization...")
    single, single_scripts, single_review = await normalize_single_call(source_text)
    print("Calling chunked Full normalization...")
    chunked, chunked_scripts, chunked_review = await normalize_chunked(source_text, str(section.get("title") or "Bài học"), chunks)

    if args.include_scripts:
        single["main_scripts"] = single_scripts
        single["review_script"] = single_review
        chunked["main_scripts"] = chunked_scripts
        chunked["review_script"] = chunked_review

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "test_type": "full_mode_normalization_ab",
        "safety": "No database writes, no TTS generation, no storage writes.",
        "plan": plan,
        "single_request": single,
        "chunked_request": chunked,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_file = args.output_dir / f"full_mode_ab_section_{section.get('section_index', args.chapter_index)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Report written to {output_file}")
    print("Compare main_to_source_char_ratio, main_script_count, and review_chars. Review generated scripts manually if --include-scripts was used.")


if __name__ == "__main__":
    asyncio.run(main())

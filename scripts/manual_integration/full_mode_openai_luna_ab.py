"""Run a DB-free Full-mode A/B test against GPT-5.6 Luna.

Example:
    uv run python scripts/manual_integration/full_mode_openai_luna_ab.py `
      --export-file "C:/Users/Lenovo/Downloads/Of Mice And Men_full_mode_export.json" `
      --chapter-index 4 --chunk-tokens 5000 --include-scripts

This script reads OPENAI_API_KEY through app settings. It does not create
audio, connect to Postgres, update book records, or modify Gemini settings.
"""

# ruff: noqa: E402
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from openai import AsyncOpenAI

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from app.core.config import settings
from app.services.llm_service import SYSTEM_PROMPT_REWRITE_FULL, NormalizedUnitPayload
from app.services.token_budget_service import estimate_tokens
from app.services.tts_script_quality_service import sanitize_tts_script_list, sanitize_tts_script_text
from scripts.manual_integration.full_mode_normalize_ab import (
    reconstruct_section_text,
    serialize_result,
    split_without_overlap,
)

MODEL = "gpt-5.6-luna"
MAX_OUTPUT_TOKENS = 16000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="A/B-test Full normalization with GPT-5.6 Luna without DB or TTS writes.")
    parser.add_argument("--export-file", type=Path, required=True, help="Path to admin Full-mode JSON export.")
    parser.add_argument("--chapter-index", type=int, default=4, help="Zero-based section index to test; default 4 is Chapter 5.")
    parser.add_argument("--chunk-tokens", type=int, default=5000, help="Token target for the chunked strategy.")
    parser.add_argument("--dry-run", action="store_true", help="Validate the input and show call plan without calling OpenAI.")
    parser.add_argument("--include-scripts", action="store_true", help="Include generated script text in the ignored local report.")
    parser.add_argument("--output-dir", type=Path, default=Path("script_outputs"), help="Directory for local JSON reports.")
    return parser.parse_args()


def _usage_dict(response: Any) -> dict[str, int | None]:
    usage = getattr(response, "usage", None)
    return {
        "input_tokens": getattr(usage, "input_tokens", None),
        "output_tokens": getattr(usage, "output_tokens", None),
        "reasoning_tokens": getattr(getattr(usage, "output_tokens_details", None), "reasoning_tokens", None),
    }


async def call_luna(client: AsyncOpenAI, source_text: str, *, context_hint: str | None = None) -> tuple[list[str], str, dict[str, int | None]]:
    user_content = source_text if not context_hint else f"{context_hint}\n\n--- INPUT ---\n{source_text}"
    response = await client.responses.parse(
        model=MODEL,
        instructions=SYSTEM_PROMPT_REWRITE_FULL,
        input=user_content,
        text_format=NormalizedUnitPayload,
        max_output_tokens=MAX_OUTPUT_TOKENS,
        reasoning={"effort": "low"},
        text={"verbosity": "high"},
        store=False,
    )
    parsed = response.output_parsed
    if parsed is None:
        raise RuntimeError("GPT-5.6 Luna returned no parsed structured output.")
    validated = NormalizedUnitPayload.model_validate(parsed)
    return sanitize_tts_script_list(validated.main_scripts), sanitize_tts_script_text(validated.review_script), _usage_dict(response)


async def main() -> None:
    args = parse_args()
    if args.chunk_tokens < 1000:
        raise SystemExit("--chunk-tokens must be at least 1000.")
    if not args.export_file.is_file():
        raise SystemExit(f"Export file not found: {args.export_file}")
    if not settings.OPENAI_API_KEY:
        raise SystemExit("OPENAI_API_KEY is not configured. Add it to .env before running this script.")

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
        "model": MODEL,
        "reasoning_effort": "low",
        "verbosity": "high",
        "store": False,
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

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY, timeout=120.0)
    print("Calling baseline single-request Full normalization with GPT-5.6 Luna...")
    single_scripts, single_review, single_usage = await call_luna(client, source_text)
    single = serialize_result(single_scripts, single_review, source_text, include_scripts=args.include_scripts)
    single["usage"] = single_usage

    print("Calling chunked Full normalization with GPT-5.6 Luna...")
    chunked_scripts: list[str] = []
    review_parts: list[str] = []
    usage: list[dict[str, int | None]] = []
    previous_tail = ""
    for chunk in chunks:
        print(f"Calling chunk {chunk.index + 1}/{len(chunks)} ({chunk.estimated_tokens} estimated tokens)...")
        context_hint = (
            f"Bài học: {section.get('title') or 'Bài học'}.\n"
            f"Đây là phần {chunk.index + 1}/{len(chunks)} của cùng một bài học.\n"
            "Giữ mạch văn nối tiếp với phần trước. Không tự nhắc 'phần' hoặc 'chunk' trong câu trả lời.\n"
            f"Đoạn cuối phần trước để nối ngữ cảnh: {previous_tail[-600:]}"
        )
        scripts, review, chunk_usage = await call_luna(client, chunk.text, context_hint=context_hint)
        chunked_scripts.extend(scripts)
        review_parts.append(review)
        usage.append(chunk_usage)
        previous_tail = chunk.text[-1000:]
    chunked_review = " ".join(part for part in review_parts if part).strip()
    chunked = serialize_result(chunked_scripts, chunked_review, source_text, include_scripts=args.include_scripts)
    chunked["usage_per_call"] = usage

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "test_type": "full_mode_openai_luna_ab",
        "safety": "No database writes, no TTS generation, no storage writes. OpenAI Responses are sent with store=false.",
        "plan": plan,
        "single_request": single,
        "chunked_request": chunked,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_file = args.output_dir / f"full_mode_luna_ab_section_{section.get('section_index', args.chapter_index)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Report written to {output_file}")
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())

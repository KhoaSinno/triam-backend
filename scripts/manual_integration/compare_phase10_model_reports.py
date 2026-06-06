"""Compare Phase 10.7 model evaluation reports.

This script is offline and deterministic. It does not call providers or DB.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.agent_observability.model_eval_report import compare_reports


def load_report(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Report must be a JSON object: {path}")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare Phase 10.7 baseline and candidate model reports.")
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--max-chat-p95-regression-ratio", type=float, default=0.30)
    parser.add_argument("--max-voice-p95-regression-ratio", type=float, default=0.25)
    args = parser.parse_args()

    result = compare_reports(
        load_report(Path(args.baseline)),
        load_report(Path(args.candidate)),
        max_chat_p95_regression_ratio=args.max_chat_p95_regression_ratio,
        max_voice_p95_regression_ratio=args.max_voice_p95_regression_ratio,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["recommendation"] != "go":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

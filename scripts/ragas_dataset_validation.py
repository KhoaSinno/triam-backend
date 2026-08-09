"""Offline provenance checks for the historical RAG evaluation dataset.

The evaluator must not infer a retrieved context from a previous turn, a book
keyword, or a hand-picked section.  A case is eligible for retrieval metrics
only when its ``intent_log_ref`` points to a ``turn_completed`` trace with
retrieval chunk IDs and the saved context source identifies the same chunks.

This module deliberately does not contact the database or an LLM.  It can be
run before a paid judge run to write an auditable, derived dataset.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATASET_PATH = PROJECT_ROOT / "logs" / "ragas_eval" / "production_flow_trace.json"
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "logs" / "ragas_eval" / "production_flow_trace_provenance_checked.json"

_TRACE_REF_PATTERN = re.compile(r"^(?P<filename>[^:]+):L(?P<line_number>\d+)$")
_TRACE_LINE_PATTERN = re.compile(r"AGENT_TRACE\s+turn_completed\s+\|\s+(?P<payload>\{.*\})\s*$")
_SOURCE_IDS_PATTERN = re.compile(r"db:chunks=\[(?P<ids>[^\]]*)\]")


@dataclass(frozen=True)
class CaseVerification:
    group: str
    reason: str
    trace_id: str | None
    retrieval_chunk_ids: list[str]

    @property
    def retrieval_metrics_eligible(self) -> bool:
        return self.group == "rag_retrieval_verified"


def _read_trace_at_reference(reference: str, *, log_dir: Path) -> dict[str, Any] | None:
    match = _TRACE_REF_PATTERN.fullmatch(reference.strip())
    if not match:
        return None

    log_path = log_dir / match.group("filename")
    if not log_path.is_file():
        return None

    line_number = int(match.group("line_number"))
    lines = log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    if line_number < 1 or line_number > len(lines):
        return None

    trace_match = _TRACE_LINE_PATTERN.search(lines[line_number - 1])
    if not trace_match:
        return None
    try:
        payload = json.loads(trace_match.group("payload"))
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def _source_chunk_ids(context_source: object) -> list[str]:
    if not isinstance(context_source, str):
        return []
    match = _SOURCE_IDS_PATTERN.search(context_source)
    if not match:
        return []
    return re.findall(r"[A-Za-z0-9_-]+", match.group("ids"))


def _is_direct_context_source(context_source: object, retrieval_chunk_ids: list[str]) -> bool:
    source_ids = _source_chunk_ids(context_source)
    if not source_ids or not retrieval_chunk_ids:
        return False
    # Historical files record at most the first five IDs in _contexts_source.
    return source_ids == retrieval_chunk_ids[: len(source_ids)]


def verify_case(case: dict[str, Any], *, log_dir: Path) -> CaseVerification:
    trace = _read_trace_at_reference(str(case.get("intent_log_ref") or ""), log_dir=log_dir)
    route = str((trace or {}).get("grounding_route") or case.get("route") or "").casefold()
    answer_source = str((trace or {}).get("answer_source") or "").casefold()

    if route in {"book_metadata", "book_section"} or answer_source in {"book_metadata", "book_section"}:
        return CaseVerification("metadata_or_section", "deterministic_or_section_route", None, [])
    if route == "web_policy" or answer_source in {"web", "policy"}:
        return CaseVerification("web_policy", "web_or_permission_route", None, [])
    if trace is None:
        return CaseVerification("memory_or_unverifiable", "missing_or_invalid_turn_completed_reference", None, [])

    retrieval_chunk_ids = [str(value) for value in trace.get("retrieval_chunk_ids") or []]
    trace_id = str(trace.get("trace_id")) if trace.get("trace_id") else None
    contexts = case.get("contexts") or []
    if retrieval_chunk_ids and contexts and _is_direct_context_source(case.get("_contexts_source"), retrieval_chunk_ids):
        return CaseVerification("rag_retrieval_verified", "exact_turn_retrieval_ids_match_context_source", trace_id, retrieval_chunk_ids)
    if retrieval_chunk_ids:
        return CaseVerification("memory_or_unverifiable", "retrieval_ids_do_not_prove_saved_context_provenance", trace_id, retrieval_chunk_ids)
    return CaseVerification("memory_or_unverifiable", "no_retrieval_in_referenced_turn", trace_id, [])


def annotate_cases(cases: list[dict[str, Any]], *, log_dir: Path) -> list[dict[str, Any]]:
    annotated: list[dict[str, Any]] = []
    for case in cases:
        item = dict(case)
        verification = verify_case(item, log_dir=log_dir)
        item["evaluation_group"] = verification.group
        item["verification_reason"] = verification.reason
        item["verified_trace_id"] = verification.trace_id
        item["verified_retrieval_chunk_ids"] = verification.retrieval_chunk_ids
        item["retrieval_metrics_eligible"] = verification.retrieval_metrics_eligible
        item["answer_metrics_eligible"] = bool(item.get("reference") and item.get("response"))
        annotated.append(item)
    return annotated


def load_and_annotate(dataset_path: Path = DEFAULT_DATASET_PATH, *, log_dir: Path = PROJECT_ROOT) -> list[dict[str, Any]]:
    payload = json.loads(dataset_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("RAGAS dataset must be a JSON list.")
    return annotate_cases(payload, log_dir=log_dir)


def load_provenance_checked_cases(dataset_path: Path = DEFAULT_OUTPUT_PATH) -> list[dict[str, Any]]:
    """Load the frozen, provenance-checked dataset used by paid judge runs."""
    payload = json.loads(dataset_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Provenance-checked dataset must be a JSON list.")

    required_fields = {"evaluation_group", "retrieval_metrics_eligible", "answer_metrics_eligible"}
    for index, case in enumerate(payload, start=1):
        if not isinstance(case, dict) or not required_fields.issubset(case):
            raise ValueError(
                f"Case {index} is not provenance-checked. "
                "Run ragas_dataset_validation.py before the judge."
            )
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_manifest(*, source_path: Path, output_path: Path, log_dir: Path, cases: list[dict[str, Any]], manifest_path: Path) -> None:
    """Write a small audit manifest without changing the source dataset."""
    log_paths = sorted(log_dir.glob("log_live_context*.md"))
    manifest = {
        "source_dataset": str(source_path),
        "source_dataset_sha256": _sha256(source_path),
        "provenance_checked_dataset": str(output_path),
        "provenance_checked_dataset_sha256": _sha256(output_path),
        "raw_log_sha256": {path.name: _sha256(path) for path in log_paths},
        "total_cases": len(cases),
        "evaluation_groups": dict(Counter(str(case["evaluation_group"]) for case in cases)),
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def print_summary(cases: list[dict[str, Any]]) -> None:
    groups = Counter(str(case["evaluation_group"]) for case in cases)
    reasons = Counter(str(case["verification_reason"]) for case in cases)
    print(f"Cases: {len(cases)}")
    print("Evaluation groups:")
    for name, count in sorted(groups.items()):
        print(f"  - {name}: {count}")
    print("Verification reasons:")
    for name, count in sorted(reasons.items()):
        print(f"  - {name}: {count}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify provenance for a RAG evaluation dataset without provider calls.")
    parser.add_argument("--input", type=Path, default=DEFAULT_DATASET_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--log-dir", type=Path, default=PROJECT_ROOT)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Path for the reproducibility manifest (defaults beside --output).",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cases = load_and_annotate(args.input, log_dir=args.log_dir)
    print_summary(cases)
    if args.dry_run:
        return
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(cases, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest_path = args.manifest or args.output.with_suffix(".manifest.json")
    write_manifest(
        source_path=args.input,
        output_path=args.output,
        log_dir=args.log_dir,
        cases=cases,
        manifest_path=manifest_path,
    )
    print(f"Provenance-checked dataset: {args.output}")
    print(f"Reproducibility manifest: {manifest_path}")


if __name__ == "__main__":
    main()

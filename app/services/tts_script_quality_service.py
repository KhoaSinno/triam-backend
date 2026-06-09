import re
from dataclasses import dataclass

_STAGE_TAG_RE = re.compile(r"\[(?:[A-Za-zÀ-ỹ_ -]{2,40})\]")
_HEADING_RE = re.compile(r"(?m)^\s*#{1,6}\s*")
_BULLET_RE = re.compile(r"(?m)^\s*(?:[-*+]|\d+[.)])\s+")
_BLOCKQUOTE_RE = re.compile(r"(?m)^\s*>\s?")
_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]+\)")
_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_CITATION_RE = re.compile(r"(?<!\w)\[\d{1,4}\](?!\w)")
_HTML_TAG_RE = re.compile(r"</?[^>]+>")
_SPACE_BEFORE_PUNCTUATION_RE = re.compile(r"\s+([.,;:!?])")
_MULTISPACE_RE = re.compile(r"\s+")
_MARKDOWN_ARTIFACT_RE = re.compile(r"(\*\*|__|`{1,3}|~~|^\s*#{1,6}\s+|^\s*(?:[-*+]|\d+[.)])\s+)", re.MULTILINE)
_ACRONYM_RE = re.compile(
    r"(?<![\w])(?:[A-Z]{2,}-[A-Za-z0-9]+|[A-Z][A-Z0-9]{2,}(?:[-/.][A-Z0-9]{1,})*)(?![\w])"
)


@dataclass(frozen=True)
class TTSQualityReport:
    markdown_artifacts: int
    unexplained_acronyms: tuple[str, ...]

    @property
    def has_warnings(self) -> bool:
        return self.markdown_artifacts > 0 or bool(self.unexplained_acronyms)


def sanitize_tts_script_text(text: str) -> str:
    """Remove visual markup that should never reach an audio renderer."""
    cleaned = text or ""
    cleaned = _IMAGE_RE.sub(r"\1", cleaned)
    cleaned = _LINK_RE.sub(r"\1", cleaned)
    cleaned = _STAGE_TAG_RE.sub("", cleaned)
    cleaned = _HEADING_RE.sub("", cleaned)
    cleaned = _BULLET_RE.sub("", cleaned)
    cleaned = _BLOCKQUOTE_RE.sub("", cleaned)
    cleaned = _CITATION_RE.sub("", cleaned)
    cleaned = _HTML_TAG_RE.sub("", cleaned)
    cleaned = cleaned.replace("**", "")
    cleaned = cleaned.replace("__", "")
    cleaned = cleaned.replace("~~", "")
    cleaned = cleaned.replace("`", "")
    cleaned = cleaned.replace("|", ", ")
    cleaned = cleaned.replace("•", ". ")
    cleaned = _MULTISPACE_RE.sub(" ", cleaned)
    cleaned = _SPACE_BEFORE_PUNCTUATION_RE.sub(r"\1", cleaned)
    return cleaned.strip()


def sanitize_tts_script_list(scripts: list[str]) -> list[str]:
    return [cleaned for script in scripts if (cleaned := sanitize_tts_script_text(script))]


def has_markdown_artifacts(text: str) -> bool:
    return bool(_MARKDOWN_ARTIFACT_RE.search(text or ""))


def _looks_explained(context: str, acronym: str) -> bool:
    lower_context = context.lower()
    lower_acronym = acronym.lower()
    explanation_markers = (
        f"gọi tắt là {lower_acronym}",
        f"viết tắt là {lower_acronym}",
        f"tức là {lower_acronym}",
        f"{lower_acronym}, một ",
        f"{lower_acronym}, là ",
        f"{lower_acronym} là ",
        f"{lower_acronym}, bộ ",
        f"{lower_acronym}, bài ",
        f"{lower_acronym}, phương pháp ",
        f"{lower_acronym}, kỹ thuật ",
    )
    if any(marker in lower_context for marker in explanation_markers):
        return True

    acronym_pos = context.find(acronym)
    if acronym_pos == -1:
        return False

    before = context[max(0, acronym_pos - 100) : acronym_pos]
    after = context[acronym_pos + len(acronym) : acronym_pos + len(acronym) + 120]
    if "(" in before and ")" in after:
        return True
    if before.rstrip().endswith((" -", " –", " —")) or after.lstrip().startswith(("- ", "– ", "— ")):
        return True
    return False


def find_unexplained_acronyms(texts: list[str], *, max_items: int = 8) -> tuple[str, ...]:
    combined = " ".join(texts)
    seen: set[str] = set()
    warnings: list[str] = []
    for match in _ACRONYM_RE.finditer(combined):
        acronym = match.group(0).strip(".,;:!?")
        if acronym in seen or len(acronym) < 3:
            continue
        seen.add(acronym)
        window = combined[max(0, match.start() - 140) : match.end() + 160]
        if not _looks_explained(window, acronym):
            warnings.append(acronym)
            if len(warnings) >= max_items:
                break
    return tuple(warnings)


def inspect_tts_script_quality(texts: list[str]) -> TTSQualityReport:
    raw_text = " ".join(texts)
    return TTSQualityReport(
        markdown_artifacts=len(_MARKDOWN_ARTIFACT_RE.findall(raw_text)),
        unexplained_acronyms=find_unexplained_acronyms(texts),
    )

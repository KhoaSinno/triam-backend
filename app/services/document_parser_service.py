from __future__ import annotations

from urllib.parse import unquote, urlparse

from app.core.exceptions import UnsupportedFileTypeError
from app.services.document_structure_types import ParsedDocument
from app.services.docx_service import parse_docx_structure
from app.services.epub_service import parse_epub_structure
from app.services.pdf_service import parse_pdf_structure

SUPPORTED_DOCUMENT_TYPES = {"pdf", "epub", "docx"}


def normalize_document_type(document_type: str | None) -> str:
    normalized = (document_type or "").strip().lower().lstrip(".")
    if normalized not in SUPPORTED_DOCUMENT_TYPES:
        raise UnsupportedFileTypeError(f"Loại file không hỗ trợ ({document_type}). Chỉ chấp nhận PDF, EPUB, DOCX.")
    return normalized


def infer_document_type_from_url(file_url: str | None) -> str:
    if not file_url:
        return "pdf"

    path = unquote(urlparse(file_url).path).lower()
    for document_type in SUPPORTED_DOCUMENT_TYPES:
        if path.endswith(f".{document_type}"):
            return document_type

    return "pdf"


async def parse_document_structure(file_obj, document_type: str) -> ParsedDocument:
    normalized_type = normalize_document_type(document_type)

    if normalized_type == "pdf":
        return await parse_pdf_structure(file_obj)

    if normalized_type == "epub":
        return await parse_epub_structure(file_obj)

    if normalized_type == "docx":
        return await parse_docx_structure(file_obj)

    raise UnsupportedFileTypeError()

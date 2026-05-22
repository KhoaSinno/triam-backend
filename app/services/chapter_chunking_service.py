from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.services.token_budget_service import estimate_tokens


@dataclass(frozen=True)
class TextChunk:
    index: int
    text: str
    estimated_tokens: int


def split_text_for_llm(text: str) -> list[TextChunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.LLM_CHUNK_TARGET_TOKENS,
        chunk_overlap=settings.LLM_CHUNK_OVERLAP_TOKENS,
        length_function=estimate_tokens,
        separators=["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""],
    )
    parts = [part.strip() for part in splitter.split_text(text or "") if part.strip()]
    return [
        TextChunk(
            index=index,
            text=part,
            estimated_tokens=estimate_tokens(part),
        )
        for index, part in enumerate(parts)
    ]

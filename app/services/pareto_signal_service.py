from __future__ import annotations

import numpy as np
from openai import AsyncOpenAI

from app.core.config import settings

# 1. Định nghĩa bộ neo ngữ nghĩa mô tả mẫu (Label Enrichment)
ENRICHED_ANCHORS: dict[str, str] = {
    "core_concept": (
        "Khái niệm nền tảng, tổng quan lý thuyết, giới thiệu tổng thể, định nghĩa cơ bản. "
        "Foundational core concepts, basic overview, theoretical background, introduction to the topic."
    ),
    "definition": (
        "Định nghĩa thuật ngữ, giải thích ý nghĩa từ ngữ, phát biểu định nghĩa khoa học. "
        "Scientific definition of terms, formal explanation of meaning, vocabulary terminology."
    ),
    "theorem": (
        "Định lý toán học, bổ đề, hệ quả, định luật khoa học, quy luật tự nhiên đã được chứng minh. "
        "Mathematical theorems, logic lemmas, scientific laws, corollaries, axioms."
    ),
    "formula": (
        "Công thức toán học, biểu thức số học, phương trình đại số, hệ thức tính toán giá trị. "
        "Mathematical formulas, equations, arithmetic expressions, calculation rules."
    ),
    "method": (
        "Phương pháp giải quyết, thuật toán máy tính, kỹ thuật thực hiện, giải pháp công nghệ. "
        "Problem-solving methods, computer algorithms, techniques, solutions."
    ),
    "procedure": (
        "Quy trình thực hiện, các bước tiến hành, hướng dẫn từng bước, kịch bản nghiệp vụ. "
        "Step-by-step procedures, execution workflows, guide tutorials, sequential processes."
    ),
    "reasoning": (
        "Suy luận logic, chứng minh toán học, lập luận phản bác, lý luận khoa học chặt chẽ. "
        "Logical reasoning, mathematical proofs, arguments, deductive inference."
    ),
    "example": (
        "Ví dụ thực tế, minh họa cụ thể, bài tập vận dụng mẫu, tình huống nghiên cứu điển hình. "
        "Practical examples, concrete illustrations, sample exercises, case studies."
    )
}

# 2. Siêu dữ liệu cấu hình các tín hiệu trọng tâm (Weights & Unit Types)
PARETO_SIGNAL_METADATA: dict[str, dict[str, str | float]] = {
    "core_concept": {"unit_type": "pareto_core", "weight": 1.0},
    "definition": {"unit_type": "pareto_core", "weight": 1.0},
    "principle": {"unit_type": "pareto_core", "weight": 0.95},
    "method": {"unit_type": "pareto_method", "weight": 0.9},
    "procedure": {"unit_type": "pareto_method", "weight": 0.85},
    "rule": {"unit_type": "pareto_rule", "weight": 0.9},
    "formula": {"unit_type": "pareto_formula", "weight": 0.9},
    "theorem": {"unit_type": "pareto_rule", "weight": 0.9},
    "reasoning": {"unit_type": "pareto_core", "weight": 0.85},
    "example": {"unit_type": "pareto_example", "weight": 0.4},
}

_ANCHOR_VECTORS_CACHE: dict[str, list[float]] = {}


async def get_or_create_anchor_embeddings() -> dict[str, list[float]]:
    """Tải và lưu trữ vector neo vào RAM bằng OpenAI embeddings API."""
    global _ANCHOR_VECTORS_CACHE
    if _ANCHOR_VECTORS_CACHE:
        return _ANCHOR_VECTORS_CACHE

    # Sử dụng OpenAI API key chính thức để lấy embeddings cho text-embedding-3-small
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    keys = list(ENRICHED_ANCHORS.keys())
    texts = list(ENRICHED_ANCHORS.values())

    response = await client.embeddings.create(
        model=settings.BOOK_SECTION_EMBEDDING_MODEL,
        input=texts
    )
    for idx, key in enumerate(keys):
        _ANCHOR_VECTORS_CACHE[key] = response.data[idx].embedding

    return _ANCHOR_VECTORS_CACHE


def extract_pareto_signal_hints(
    embedding: list[float] | None = None,
    anchor_vectors: dict[str, list[float]] | None = None,
    threshold: float = 0.20,
) -> list[str]:
    """
    Phân loại tín hiệu dựa trên tích vô hướng vector NumPy (Cosine Similarity).
    Chỉ trả về 1 nhãn duy nhất có độ khớp cao nhất đạt ngưỡng (Arg-max).
    Dùng ngưỡng 0.20 theo kiểm nghiệm thực nghiệm tối ưu của OpenAI text-embedding-3-small.
    """
    if embedding is None or not anchor_vectors:
        return []

    similarities = {}
    v_sec = np.array(embedding)
    for key, anchor in anchor_vectors.items():
        sim = float(np.dot(v_sec, np.array(anchor)))
        if sim >= threshold:
            similarities[key] = sim
            
    if similarities:
        best_key = max(similarities, key=similarities.get)
        return [best_key]
    return []


def infer_unit_type_from_signals(hints: list[str]) -> str:
    for hint in hints:
        meta = PARETO_SIGNAL_METADATA.get(hint)
        if meta:
            return str(meta["unit_type"])
    return "pareto_focus"

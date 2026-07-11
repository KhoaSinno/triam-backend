from app.services.agent_grounding.hybrid_retrieval import (
    HybridRetrievalConfig,
    build_hybrid_retrieval_result,
    merge_candidates,
    rerank_candidates,
    select_context_candidates,
    validate_evidence,
)


def _config(**overrides):
    values = {
        "min_final_score": 0.25,
        "max_context_chunks": 6,
        "max_chunks_per_section": 2,
    }
    values.update(overrides)
    return HybridRetrievalConfig(**values)


def _candidate_payload(
    item_id: int,
    *,
    section_id: str = "section-1",
    section_path: str = "Chapter 4 > Crooks",
    section_title: str = "Crooks",
    chunk_index: int = 0,
    content: str = "Crooks lives alone in his room.",
    similarity: float | None = None,
    lexical_score: float | None = None,
):
    payload = {
        "id": item_id,
        "book_id": "book-1",
        "section_id": section_id,
        "section_path": section_path,
        "section_title": section_title,
        "chunk_index": chunk_index,
        "content": content,
    }
    if similarity is not None:
        payload["similarity"] = similarity
    if lexical_score is not None:
        payload["lexical_score"] = lexical_score
    return payload


def test_merge_candidates_deduplicates_vector_and_lexical_hits():
    vector = [_candidate_payload(1, similarity=0.62)]
    lexical = [_candidate_payload(1, lexical_score=0.45)]

    candidates = merge_candidates(vector, lexical)

    assert len(candidates) == 1
    assert candidates[0].vector_score == 0.62
    assert candidates[0].lexical_score == 0.45
    assert candidates[0].sources == {"vector", "lexical"}


def test_rerank_prioritizes_multi_source_hits():
    vector = [_candidate_payload(1, similarity=0.50), _candidate_payload(2, section_title="Other", similarity=0.58)]
    lexical = [_candidate_payload(1, lexical_score=0.60)]
    candidates = merge_candidates(vector, lexical)

    ranked = rerank_candidates("Crooks ở chương 4", candidates, vector, lexical, _config())

    assert ranked[0].id == "1"
    assert ranked[0].final_score > ranked[1].final_score


def test_select_context_candidates_limits_chunks_per_section():
    vector = [
        _candidate_payload(index, chunk_index=index, similarity=0.9 - index * 0.01)
        for index in range(4)
    ]
    lexical = []
    candidates = merge_candidates(vector, lexical)
    ranked = rerank_candidates("Crooks", candidates, vector, lexical, _config(max_chunks_per_section=2))

    selected = select_context_candidates(ranked, _config(max_chunks_per_section=2))

    assert len(selected) == 2
    assert {candidate.section_id for candidate in selected} == {"section-1"}


def test_validate_evidence_rejects_low_confidence():
    vector = [_candidate_payload(1, similarity=0.1)]
    lexical = []
    candidates = merge_candidates(vector, lexical)
    ranked = rerank_candidates("Crooks", candidates, vector, lexical, _config(min_final_score=0.5))

    result = validate_evidence("Crooks", ranked, _config(min_final_score=0.5))

    assert result.valid is False
    assert result.reason_code == "low_confidence"


def test_rerank_preserves_strong_single_source_lexical_hit():
    vector = []
    lexical = [_candidate_payload(1, section_title="Benchmarks", content="GPQA is a benchmark.", lexical_score=0.80)]
    candidates = merge_candidates(vector, lexical)

    ranked = rerank_candidates("GPQA là gì?", candidates, vector, lexical, _config())
    result = validate_evidence("GPQA là gì?", ranked, _config())

    assert ranked[0].final_score > 0.0
    assert result.valid is True


def test_validate_evidence_rejects_missing_named_entity():
    vector = [
        _candidate_payload(
            1,
            section_path="Chapter 2 > Ranch",
            section_title="Ranch",
            content="George and Lennie arrive at the ranch.",
            similarity=0.9,
        )
    ]
    lexical = []
    candidates = merge_candidates(vector, lexical)
    ranked = rerank_candidates("Crooks ở chương nào?", candidates, vector, lexical, _config())

    result = validate_evidence("Crooks ở chương nào?", ranked, _config())

    assert result.valid is False
    assert result.reason_code == "missing_named_entity"


def test_build_hybrid_retrieval_result_returns_payload_with_safe_scores():
    result = build_hybrid_retrieval_result(
        query="Crooks ở chương nào?",
        vector_payload=[_candidate_payload(1, similarity=0.78)],
        lexical_payload=[_candidate_payload(1, lexical_score=0.52)],
        config=_config(),
    )

    assert result.found is True
    assert result.reason_code == "valid"
    assert result.chunks[0]["retrieval_method"] == "hybrid"
    assert result.chunks[0]["final_score"] == result.chunks[0]["similarity"]
    assert result.chunks[0]["retrieval_sources"] == ["lexical", "vector"]

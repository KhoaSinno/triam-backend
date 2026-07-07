import pytest
from app.services.pareto_signal_service import (
    extract_pareto_signal_hints,
    infer_unit_type_from_signals,
)

def test_extract_pareto_signal_hints_with_vectors():
    # Định nghĩa mock anchors đơn giản dạng trực giao
    mock_anchors = {
        "core_concept": [1.0, 0.0, 0.0],
        "formula": [0.0, 1.0, 0.0],
        "example": [0.0, 0.0, 1.0]
    }

    # Trường hợp 1: Vector chỉ gần core_concept (độ tương đồng 0.9)
    sec_embedding_1 = [0.9, 0.1, 0.0]
    hints_1 = extract_pareto_signal_hints(
        embedding=sec_embedding_1, 
        anchor_vectors=mock_anchors,
        threshold=0.65
    )
    assert hints_1 == ["core_concept"]

    # Trường hợp 2: Không có vector nào đạt ngưỡng tương đồng
    sec_embedding_2 = [0.1, 0.1, 0.1]
    hints_2 = extract_pareto_signal_hints(
        embedding=sec_embedding_2, 
        anchor_vectors=mock_anchors,
        threshold=0.65
    )
    assert hints_2 == []


def test_infer_unit_type_from_signal_hints():
    assert infer_unit_type_from_signals(["method", "example"]) == "pareto_method"
    assert infer_unit_type_from_signals(["formula"]) == "pareto_formula"
    assert infer_unit_type_from_signals([]) == "pareto_focus"

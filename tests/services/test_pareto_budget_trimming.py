import uuid
from app.services.learning_unit_planner_service import PlannedLearningUnit
from app.services.pareto_planner_service import _trim_to_target

def test_value_based_trimming_logic():
    # Tạo danh sách bài nghe giả lập
    # Unit 1: Chương 1 (Index 0), tầm quan trọng 3/5, 1000 tokens
    u1 = PlannedLearningUnit(
        title="Unit 1", unit_type="pareto_core", source_section_ids=[uuid.uuid4()],
        source_text="text", source_text_char_count=10, estimated_tokens=1000,
        estimated_audio_seconds=100, planner_reason="Điểm quan trọng: 3/5. Lý do..."
    )
    # Unit 2: Chương 3 (Index 1), tầm quan trọng 5/5, 1500 tokens (CỰC KỲ QUAN TRỌNG)
    u2 = PlannedLearningUnit(
        title="Unit 2", unit_type="pareto_core", source_section_ids=[uuid.uuid4()],
        source_text="text", source_text_char_count=10, estimated_tokens=1500,
        estimated_audio_seconds=150, planner_reason="Điểm quan trọng: 5/5. Lý do..."
    )
    # Unit 3: Chương 5 (Index 2), tầm quan trọng 4/5, 2000 tokens
    u3 = PlannedLearningUnit(
        title="Unit 3", unit_type="pareto_core", source_section_ids=[uuid.uuid4()],
        source_text="text", source_text_char_count=10, estimated_tokens=2000,
        estimated_audio_seconds=200, planner_reason="Điểm quan trọng: 4/5. Lý do..."
    )
    # Unit 4: Chương 8 (Index 3), tầm quan trọng 5/5, 1200 tokens (CỰC KỲ QUAN TRỌNG, ở cuối sách)
    u4 = PlannedLearningUnit(
        title="Unit 4", unit_type="pareto_core", source_section_ids=[uuid.uuid4()],
        source_text="text", source_text_char_count=10, estimated_tokens=1200,
        estimated_audio_seconds=120, planner_reason="Điểm quan trọng: 5/5. Lý do..."
    )

    units = [u1, u2, u3, u4]
    
    # Tổng token nguồn = 10,000 tokens. 
    # Target = 40% * 10,000 = 4000 tokens.
    # Tổng Planned = 1000 + 1500 + 2000 + 1200 = 5700 tokens (> 4000 tokens) -> Tiến hành cắt tỉa!
    # Thứ tự ưu tiên sắp xếp:
    # 1. Unit 2 (score 5, index 1)
    # 2. Unit 4 (score 5, index 3)
    # 3. Unit 3 (score 4, index 2)
    # 4. Unit 1 (score 3, index 0)
    # Gom ngân sách (tối đa 4000 tokens):
    # Unit 2 (1500 tokens) + Unit 4 (1200 tokens) = 2700 tokens (2 bài học).
    # Vì chưa đạt số bài học tối thiểu (PARETO_PLANNER_MIN_UNITS = 3), thuật toán bắt buộc nhặt tiếp Unit 3 (2000 tokens).
    # Tổng tích lũy sau khi nhặt Unit 3 = 4700 tokens (đã vượt 4000).
    # Lúc này số lượng đã đạt 3, và nếu cộng thêm Unit 1 (1000 tokens) -> 5700 tokens (> 4000) -> Dừng lại!
    # Kết quả trả ra phải được sắp xếp lại theo thứ tự thời gian gốc: [Unit 2, Unit 3, Unit 4]
    res_trimmed = _trim_to_target(units, total_source_tokens=10000)
    assert len(res_trimmed) == 3
    assert res_trimmed[0].title == "Unit 2"
    assert res_trimmed[1].title == "Unit 3"
    assert res_trimmed[2].title == "Unit 4"


def test_pareto_budget_trimming_with_tolerance():
    # Tổng token nguồn = 10,000 tokens. 
    # Target = 40% * 10,000 = 4000 tokens.
    # Allowed ceiling (15% tolerance) = 4000 * 1.15 = 4600 tokens.
    
    # Tạo 4 units có tổng token là 4300 tokens (vượt 4000 nhưng dưới 4600)
    u1 = PlannedLearningUnit(
        title="Unit 1", unit_type="pareto_core", source_section_ids=[uuid.uuid4()],
        source_text="text", source_text_char_count=10, estimated_tokens=1000,
        estimated_audio_seconds=100, planner_reason="Điểm quan trọng: 3/5."
    )
    u2 = PlannedLearningUnit(
        title="Unit 2", unit_type="pareto_core", source_section_ids=[uuid.uuid4()],
        source_text="text", source_text_char_count=10, estimated_tokens=1500,
        estimated_audio_seconds=150, planner_reason="Điểm quan trọng: 5/5."
    )
    u3 = PlannedLearningUnit(
        title="Unit 3", unit_type="pareto_core", source_section_ids=[uuid.uuid4()],
        source_text="text", source_text_char_count=10, estimated_tokens=1800,
        estimated_audio_seconds=180, planner_reason="Điểm quan trọng: 4/5."
    )

    units = [u1, u2, u3] # Tổng 4300 tokens
    
    # Phải giữ nguyên toàn bộ 3 units vì nằm dưới ngưỡng trần cho phép (4600 tokens)
    res = _trim_to_target(units, total_source_tokens=10000)
    assert len(res) == 3
    assert res[0].title == "Unit 1"
    assert res[1].title == "Unit 2"
    assert res[2].title == "Unit 3"


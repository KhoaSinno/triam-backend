# Phase 24: Value-Based Pareto Budget Trimming Implementation Guide

Hướng dẫn này trình bày chi tiết cách thiết lập và hiện thực cơ chế **Cắt tỉa ngân sách học tập dựa trên Giá trị (Value-Based Pareto Budget Trimming)** trong hệ thống TRIAM. Cơ chế này thay thế thuật toán cắt tỉa theo trình tự thời gian cũ để đảm bảo người học nắm giữ được những kiến thức cốt lõi và tinh hoa nhất của toàn bộ cuốn sách.

---

## 1. Mục tiêu Nghiệp vụ (Business Goal)
*   **Chế độ Pareto (Pareto Focus)** được thiết kế để chọn lọc ra tối đa những kiến thức quan trọng nhất của cuốn sách, giới hạn trong khoảng **$40\%$** (`PARETO_TARGET_COVERAGE_RATIO`) dung lượng token của sách gốc.
*   **Hạn chế của cơ chế cũ:** 
    *   Sắp xếp các bài học (`units`) do LLM (Gemini) lập kế hoạch theo thứ tự thời gian (chronological) từ đầu đến cuối sách.
    *   Cộng dồn token và cắt bỏ hoàn toàn các bài học phía sau ngay khi vượt quá ngưỡng ngân sách.
    *   **Hậu quả:** Hệ thống chỉ giữ lại các bài học ở chương 1, 2 đầu sách và vứt bỏ hoàn toàn các bài học quan trọng nhất ở các chương giữa hoặc cuối sách (như chương 5, chương 10), phá vỡ mục tiêu giáo dục.
*   **Giải pháp mới (Phase 24):**
    *   Nâng ngưỡng tỉ lệ bao phủ mục tiêu `PARETO_TARGET_COVERAGE_RATIO` lên **`0.40` (40%)**.
    *   Nếu tổng lượng bài do LLM đề xuất có dung lượng nằm dưới $40\%$, giữ nguyên toàn bộ để bảo toàn mạch kiến thức tự nhiên của sách.
    *   Nếu vượt quá $40\%$, thực hiện **Cắt tỉa theo giá trị (Value-Based Trimming)**:
        1. Sắp xếp ưu tiên các bài học theo độ quan trọng (`importance_score`) từ cao xuống thấp.
        2. Nếu độ quan trọng bằng nhau, ưu tiên bài học xuất hiện trước trong sách (chronological order index) làm tiêu chí phá vỡ liên kết bằng nhau (tie-breaker), tránh phạt các bài viết dài có lượng giải thích sâu sắc.
        3. Gom các bài học từ trên xuống dưới cho đến khi tổng số token đạt sát nút dưới hoặc bằng $40\%$. Chỉ vượt quá $40\%$ trong trường hợp cần giữ đủ tối thiểu 3 bài học (`PARETO_PLANNER_MIN_UNITS`).
    *   **Sắp xếp lại thứ tự thời gian gốc:** Sau khi lọc xong các bài học tinh hoa nhất, sắp xếp chúng lại theo thứ tự đọc tự nhiên trước khi lưu trữ vào Database để người học không bị xáo trộn kiến thức.

---

## 2. Thiết Kế Luồng Xử Lý (Dataflow Design)

```text
                  Audiobook Ingest / Switch Mode
                                │
                                ▼
         pareto_planner_service.py: plan_pareto_learning_units
                                │
                                ▼
                       build_section_cards
                                │
                                ▼
                       _call_pareto_llm
                                │
                                ▼
                   _validate_planner_payload
                                │
                                ▼
                       _trim_to_target  ◄── [THUẬT TOÁN ĐƯỢC NÂNG CẤP Ở PHASE 24]
        (Sắp xếp theo Importance, Trimming theo budget, Re-sort chronological)
                                │
                                ▼
                      planned_units returned
```

---

## 3. Mã Nguồn Chi Tiết Cần Hiện Thực (Code Specifications)

### Bước 3.1: Cấu hình tham số môi trường mới

#### 1. Cập nhật cấu hình tỉ lệ bao phủ trong [app/core/config.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/core/config.py)
Nâng giá trị mặc định của `PARETO_TARGET_COVERAGE_RATIO` từ `0.25` lên `0.40`.

```python
    PARETO_TARGET_COVERAGE_RATIO: float = 0.40  # Đã nâng lên 40% theo nhu cầu nghiệp vụ mới
```

#### 2. Cập nhật file môi trường mẫu [.env.example](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/.env.example)
```env
PARETO_TARGET_COVERAGE_RATIO=0.40
```

#### 3. Bổ sung luật ràng buộc ngân sách vào System Prompt trong [app/services/pareto_planner_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/pareto_planner_service.py)
Thêm dòng luật sau vào cuối danh sách `Rules` của biến `PARETO_PLANNER_SYSTEM_PROMPT` (khoảng dòng 30-49):
```text
- Select source sections such that the sum of their estimated_tokens is close to or under the requested target_tokens in the user payload.
```

---

### Bước 3.2: Hiện thực thuật toán cắt tỉa thông minh

#### Cập nhật hàm `_trim_to_target` trong [app/services/pareto_planner_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/pareto_planner_service.py)

Nâng cấp thuật toán cắt tỉa cứng cũ bằng bộ lọc thông minh dựa trên độ quan trọng và thứ tự chương:

```python
from sqlalchemy.orm.exc import StaleDataError  # Giữ nguyên các import cũ của file
from app.services.token_budget_service import estimate_text_budget

def _trim_to_target(units: list[PlannedLearningUnit], *, total_source_tokens: int) -> list[PlannedLearningUnit]:
    """
    Cắt tỉa các bài học học tập Pareto theo ngân sách token mục tiêu.
    Quy tắc:
    1. Giữ tối thiểu PARETO_PLANNER_MIN_UNITS (3 bài).
    2. Nếu tổng lượng token do LLM đề xuất <= 40% (PARETO_TARGET_COVERAGE_RATIO) tổng token sách gốc (cho phép sai số 15% vượt ngưỡng),
       giữ nguyên toàn bộ để tránh gãy mạch kiến thức.
    3. Nếu vượt quá ngưỡng cho phép, tiến hành cắt tỉa theo độ quan trọng (importance_score) giảm dần.
       Nếu điểm bằng nhau, ưu tiên bài học xuất hiện trước trong sách (chronological index).
    4. Trả các bài học đã chọn về thứ tự đọc tự nhiên của sách.
    """
    # 1. Bảo toàn số lượng bài học tối thiểu
    if len(units) <= settings.PARETO_PLANNER_MIN_UNITS:
        return units

    # Tính toán các ngưỡng token mục tiêu
    target_tokens = int(total_source_tokens * settings.PARETO_TARGET_COVERAGE_RATIO)
    total_planned_tokens = sum(u.estimated_tokens for u in units)

    # 2. Nếu tổng token do LLM chọn nằm dưới ngưỡng cho phép (có sai số 15% để tránh cắt tỉa khi vượt nhẹ), giữ nguyên toàn bộ
    allowed_ceiling = int(target_tokens * 1.15)
    if total_planned_tokens <= allowed_ceiling:
        log.info(f"Keep all planned units | total_planned={total_planned_tokens} <= allowed_ceiling={allowed_ceiling} (target={target_tokens})")
        return units

    log.info(f"Start value-based trimming | total_planned={total_planned_tokens} > allowed_ceiling={allowed_ceiling} (target={target_tokens})")

    # 3. Tiến hành cắt tỉa dựa trên giá trị (Value-Based)
    # Lưu lại chỉ số gốc (index) đại diện cho thứ tự xuất hiện gốc trong sách
    indexed_units = [(i, unit) for i, unit in enumerate(units)]
    
    # Hàm trích xuất điểm quan trọng từ planner_reason (ví dụ: "Điểm quan trọng: X/5")
    def get_importance_score(unit: PlannedLearningUnit) -> int:
        try:
            # Parse chuỗi "Điểm quan trọng: X/5" để lấy X làm tiêu chuẩn sắp xếp
            if "Điểm quan trọng: " in unit.planner_reason:
                return int(unit.planner_reason.split("Điểm quan trọng: ")[1].split("/")[0])
        except Exception as exc:
            log.warning(f"Failed to parse importance score from planner_reason: {exc}")
        return 3  # Điểm mặc định trung bình nếu lỗi parse

    # Sắp xếp theo: 
    # Tiêu chí 1: Importance Score giảm dần (ưu tiên bài quan trọng nhất)
    # Tiêu chí 2: Chỉ số index gốc tăng dần (nếu cùng quan trọng, ưu tiên bài xuất hiện trước trong sách)
    indexed_units.sort(key=lambda item: (-get_importance_score(item[1]), item[0]))

    selected_indexed: list[tuple[int, PlannedLearningUnit]] = []
    selected_tokens = 0

    # Gom các bài học tốt nhất theo ngân sách
    for index, unit in indexed_units:
        # Nếu cộng thêm unit này mà vượt quá 40% ngân sách và chúng ta đã đạt số lượng tối thiểu (3 bài),
        # thì dừng lại để không vượt quá ngưỡng 40%.
        if len(selected_indexed) >= settings.PARETO_PLANNER_MIN_UNITS and (selected_tokens + unit.estimated_tokens) > target_tokens:
            break
            
        selected_indexed.append((index, unit))
        selected_tokens += unit.estimated_tokens

    # 4. Trả các bài học đã chọn về thứ tự đọc tự nhiên của sách (sắp xếp lại theo index gốc)
    selected_indexed.sort(key=lambda item: item[0])
    
    final_units = [unit for _, unit in selected_indexed]
    log.info(
        f"Trimming complete | retained_units={len(final_units)} "
        f"| retained_tokens={sum(u.estimated_tokens for u in final_units)}/{total_source_tokens}"
    )
    return final_units
```

---

## 4. Hướng Dẫn Từng Bước Cho Fresher (Step-by-Step Guide)

Để hiện thực hóa tính năng này, fresher thực hiện theo các bước cụ thể sau:

### Bước 1: Khai báo biến cấu hình hệ thống
1. Mở file [app/core/config.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/core/config.py).
2. Tìm đến nhóm biến `Pareto learning unit planner` (khoảng dòng 194-202).
3. Đổi giá trị mặc định của `PARETO_TARGET_COVERAGE_RATIO: float = 0.25` thành `0.40`.
4. Mở file [.env.example](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/.env.example), tìm đến vị trí tương ứng và sửa thành `PARETO_TARGET_COVERAGE_RATIO=0.40`.

### Bước 2: Cập nhật thuật toán cắt tỉa trong Service
1. Mở file [app/services/pareto_planner_service.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/pareto_planner_service.py).
2. Di chuyển đến định nghĩa hàm `_trim_to_target` (khoảng dòng 248).
3. Đọc hiểu logic cũ và tiến hành thay thế toàn bộ thân hàm `_trim_to_target` bằng khối mã nguồn mới ở mục **Bước 3.2**.
4. Hãy chú ý cấu trúc sắp xếp `sort(key=lambda item: (-get_importance_score(item[1]), item[0]))`: 
    * Dấu trừ (`-`) giúp điểm số cao xếp lên trước (sắp xếp giảm dần).
    * `item[0]` là chỉ số index cũ giúp sắp xếp tăng dần theo thời gian (giữ nguyên thứ tự đọc gốc của sách).

### Bước 3: Chạy thử và kiểm thử unit test
1. Bật terminal tại thư mục gốc của dự án.
2. Chạy bộ kiểm thử hiện tại của hệ thống để đảm bảo không bị lỗi biên dịch:
   ```bash
   uv run pytest tests/services/test_reset_reading_plan.py -v
   ```

---

## 5. Kịch Bản Kiểm Thử & Xác Minh (Verification & Testing Plan)

### 5.1. Viết Unit Test Xác Minh Cắt Tỉa (Value-Based Trimming Test)
Tạo file kiểm thử mới `tests/services/test_pareto_budget_trimming.py` để chạy thử trực tiếp logic cắt tỉa:

```python
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
```

### 5.2. Hướng dẫn chạy thử nghiệm
Chạy lệnh kiểm thử sau khi viết file test:
```bash
uv run pytest tests/services/test_pareto_budget_trimming.py -v
```
Nếu toàn bộ kiểm thử thông báo màu xanh `PASSED`, chúc mừng bạn đã nâng cấp thành công hệ thống Pareto planner sang chuẩn tối ưu mới!

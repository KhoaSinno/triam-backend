# Hướng Dẫn Triển Khai - Phase 21: Đồng Nhất Mô Hỏi Nhúng Cục Bộ Và Tối Ưu Hóa Phân Loại Quyền Tìm Kiếm

Tài liệu này hướng dẫn chi tiết cách triển khai đồng nhất mô hình nhúng cục bộ (Local Embedding) sang sử dụng duy nhất mô hình **`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`** (L12) cho cả bộ định tuyến ý định (`intent_router.py`) và bộ xác nhận quyền tìm kiếm (`web_permission_intent_classifier.py`).

---

## 🎯 Mục Tiêu & Thiết Kế Kiến Trúc

### 1. Đồng bộ hóa mô hình (Unify Local Embedding Model)
*   **Hiện trạng**: Bộ định tuyến `intent_router.py` sử dụng mô hình tiếng Anh `all-MiniLM-L6-v2` (L6), còn bộ phân loại quyền tìm kiếm `web_permission_intent_classifier.py` gọi API OpenAI `gpt-4o-mini` từ xa làm trễ đàm thoại thoại (>500ms).
*   **Giải pháp**: Đồng bộ hóa toàn bộ sang sử dụng duy nhất mô hình L12 đa ngôn ngữ chạy cục bộ. Điều này giúp:
    *   **Giải phóng RAM**: Không phải nạp đồng thời 2 tệp trọng số mô hình khác nhau (tiết kiệm ~90MB RAM cho container LiveKit Worker).
    *   **Tăng độ chính xác tiếng Việt**: L12 hiểu cấu trúc ngữ nghĩa tiếng Việt có dấu natively, loại bỏ hoàn toàn các lỗi định tuyến sai lệch (False Positives) của mô hình L6.

### 2. Tái cấu trúc bộ phân loại quyền tìm kiếm (2-Pass Classifier)
Loại bỏ hoàn toàn cuộc gọi API OpenAI trễ và tốn phí trong `web_permission_intent_classifier.py`, thay thế bằng 2 lớp lọc cục bộ:
*   **Lớp 1 (Fast-Path)**: Khớp nhanh chuỗi ký tự chuẩn hóa không dấu đối với các câu trả lời cực ngắn ($\le 2$ từ) như *"ok"*, *"ừ"*, *"có"*, *"không"*, *"no"* để phản hồi lập tức trong dưới 1ms.
*   **Lớp 2 (Local Cosine Similarity)**: Đối với các câu dài hơn hoặc phức tạp hơn, sử dụng mô hình nhúng L12 để so sánh độ tương đồng Cosine với các nhóm câu thoại mẫu (Prototypes).
    *   *Tránh rò rỉ bộ nhớ (RAM Double-Allocation)*: Không khai báo khởi tạo mô hình L12 mới trong `web_permission_intent_classifier.py`. Thay vào đó, tái sử dụng trực tiếp Singleton mô hình `_classifier` được khai báo trong `intent_router.py`.

---

## 📂 Chi Tiết Các Tệp Cần Chỉnh Sửa

### Tệp 1: Cấu hình mặc định hệ thống
#### [MODIFY] [app/core/config.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/core/config.py)
Cập nhật các tham số cấu hình mặc định cho mô hình nhúng và ngưỡng định tuyến:
*   Mô hình nhúng mặc định của Intent Router: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
*   Ngưỡng định tuyến tối ưu của Intent Router: `0.60`.

```python
    # Config model nhúng cục bộ cho bộ định tuyến ý định
    AGENT_INTENT_CLASSIFIER_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    AGENT_INTENT_CLASSIFIER_THRESHOLD: float = 0.60
```

---

### Tệp 2: Bộ định tuyến ý định (Intent Router)
#### [MODIFY] [app/services/agent_grounding/intent_router.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_grounding/intent_router.py)
Thay đổi mô hình sang L12 và cập nhật tham số ngưỡng mặc định về `0.60`.

```python
class SemanticIntentClassifier:
    def __init__(self) -> None:
        # Cập nhật sang mô hình L12 đa ngôn ngữ
        self.model_name = settings.AGENT_INTENT_CLASSIFIER_MODEL or "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        self.tokenizer = None
        self.model = None
        self.proto_embeddings = {}
        self._lock = asyncio.Lock()
        self._initialized = False

    # ... giữ nguyên phương thức initialize và mean_pooling ...

    async def classify(self, query_text: str, threshold: float = 0.60) -> GroundingIntent:
        """
        Tính toán cosine similarity của câu hỏi với các mẫu.
        Ngưỡng tối ưu mặc định là 0.60.
        """
        # ... giữ nguyên logic tính toán cosine ...
```

---

### Tệp 3: Bộ phân loại quyền tìm kiếm (Web Permission Classifier)
#### [MODIFY] [app/services/voice_agent/web_permission_intent_classifier.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/voice_agent/web_permission_intent_classifier.py)
Thay thế toàn bộ nội dung tệp để thực hiện phân loại 2 lớp cục bộ. Tái sử dụng Singleton `_classifier` và hàm `mean_pooling` từ `intent_router.py`.

```python
from __future__ import annotations

import os
import torch
from typing import Any

from app.core.logger import log
from app.services.voice_agent.contracts import WebPermissionIntent, WebPermissionIntentResult
from app.services.voice_agent.voice_intent_classifier import (
    classify_voice_reply_intent_fast_path,
    normalize_voice_intent_text,
    looks_like_new_question,
)
# Tái sử dụng bộ nạp mô hình Singleton để tránh double-allocation RAM
from app.services.agent_grounding.intent_router import _classifier, mean_pooling

# Danh sách câu mẫu có dấu để mô hình L12 Multilingual so khớp ngữ nghĩa natively
L12_WEB_PERMISSION_PROTOTYPES = {
    "grant": [
        "đồng ý cho tìm kiếm", "ừ tìm trên internet đi", "cho phép tra cứu google",
        "tìm giúp mình trên mạng", "search hộ mình thông tin này", "đồng ý nha",
        "được chứ tìm đi", "yes search it", "go ahead and search", "nhất trí tìm đi"
    ],
    "deny": [
        "không cần tìm đâu", "đừng tra cứu internet", "thôi khỏi cần",
        "bỏ qua đi bạn", "không muốn tìm trên web", "đừng tìm kiếm",
        "no don't search", "cancel web search", "thôi bỏ qua đi"
    ],
    "unclear": [
        "chưa biết nữa", "để tính sau đi", "tùy bạn thôi", "cái đó khó nói",
        "sao cũng được", "maybe later", "chưa chắc nữa", "để mình suy nghĩ tí"
    ]
}

# Biến toàn cục lưu vector nhúng của câu mẫu sau khi khởi tạo
_proto_embeddings: dict[str, torch.Tensor] = {}

def _initialize_permission_prototypes() -> None:
    global _proto_embeddings
    if _proto_embeddings:
        return

    # Bảo đảm mô hình intent router đã được nạp
    _classifier.initialize()
    tokenizer = _classifier.tokenizer
    model = _classifier.model

    with torch.no_grad():
        for intent, phrases in L12_WEB_PERMISSION_PROTOTYPES.items():
            inputs = tokenizer(phrases, padding=True, truncation=True, return_tensors="pt")
            outputs = model(**inputs)
            embeddings = mean_pooling(outputs, inputs['attention_mask'])
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            _proto_embeddings[intent] = embeddings

def classify_web_permission_intent_fast_path(user_reply: str) -> WebPermissionIntentResult | None:
    normalized = normalize_voice_intent_text(user_reply)
    if not normalized:
        return None

    # Lớp 1 (Fast-Path): Chỉ áp dụng cho câu cực ngắn <= 2 từ
    token_count = len(normalized.split())
    if token_count <= 2:
        result = classify_voice_reply_intent_fast_path(user_reply)
        if result is not None:
            return WebPermissionIntentResult(result.intent, result.confidence, result.reason, result.source)
    
    return None

async def classify_web_permission_intent(
    *,
    pending_query: str,
    user_reply: str,
    threshold: float = 0.55,
    **kwargs: Any,
) -> WebPermissionIntentResult:
    """
    Bộ phân loại Quyền tìm kiếm Web bằng Local Cosine Similarity thông qua mô hình L12 Multilingual.
    Không gọi API OpenAI.
    """
    # 1. Chạy Fast-path lớp 1
    fast_result = classify_web_permission_intent_fast_path(user_reply)
    if fast_result is not None:
        return fast_result

    # 2. Xử lý câu dài qua lớp 2 (Local Embedding Cosine)
    normalized = normalize_voice_intent_text(user_reply)
    
    # Kiểm tra xem có phải câu hỏi mới hoàn toàn (new_question)
    if looks_like_new_question(user_reply, normalized):
        return WebPermissionIntentResult("new_question", 1.0, "Matched new question signature", "local_embedding")

    try:
        # Khởi tạo câu mẫu (nếu chưa có)
        _initialize_permission_prototypes()
        
        tokenizer = _classifier.tokenizer
        model = _classifier.model

        with torch.no_grad():
            inputs = tokenizer([user_reply.strip().lower()], padding=True, truncation=True, return_tensors="pt")
            outputs = model(**inputs)
            query_emb = mean_pooling(outputs, inputs['attention_mask'])
            query_emb = torch.nn.functional.normalize(query_emb, p=2, dim=1)

            best_intent: WebPermissionIntent = "unclear"
            best_score = -1.0

            for intent, proto_embs in _proto_embeddings.items():
                sims = torch.matmul(query_emb, proto_embs.T).squeeze(0)
                max_sim = torch.max(sims).item()
                if max_sim > best_score:
                    best_score = max_sim
                    best_intent = intent  # type: ignore[assignment]

            if best_score < threshold:
                log.info(f"Web permission local cosine below threshold ({best_score:.2f} < {threshold}) | Fallback to new_question")
                return WebPermissionIntentResult("new_question", best_score, "Cosine score below threshold", "local_embedding")

            return WebPermissionIntentResult(best_intent, best_score, "Classified by local L12 Cosine", "local_embedding")

    except Exception as exc:
        log.error(f"Web permission local classifier failed: {exc} | Fallback to unclear")
        return WebPermissionIntentResult("unclear", 0.0, f"Error: {exc}", "local_embedding")
```

---

## 🧪 Kế Hoạch Xác Minh (Verification Plan)

Sau khi chỉnh sửa mã nguồn, fresher cần chạy hai tệp kiểm thử tích hợp để đảm bảo tính ổn định và chính xác của hệ thống:

1.  **Chạy kiểm thử so sánh Intent Router**:
    ```bash
    .venv\Scripts\python.exe tests/test_intent_router_comparison.py
    ```
    *Đảm bảo*: Độ chính xác của mô hình L12 ở ngưỡng `0.60` đạt từ **97.62%** trở lên.
2.  **Chạy kiểm thử so sánh Web Search Permission**:
    ```bash
    .venv\Scripts\python.exe tests/test_permission_classifier.py
    ```
    *Đảm bảo*: Độ chính xác đạt từ **92.00%** trở lên, độ trễ trung bình của Method C nằm trong khoảng **dưới 10ms**, không phát sinh lỗi nạp lại model.

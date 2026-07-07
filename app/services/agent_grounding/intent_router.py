from __future__ import annotations

import asyncio
import torch
from transformers import AutoTokenizer, AutoModel
from app.services.agent_grounding.contracts import GroundingIntent, NormalizedQuery

# Định nghĩa các câu mẫu đặc trưng đại diện cho từng lớp Ý định (Intent Class)
PROTOTYPES = {
    GroundingIntent.BOOK_METADATA_ROOT_SECTION_COUNT: [
        "sách có bao nhiêu chương chính",
        "quyển sách này gồm bao nhiêu chương",
        "sách có mấy chương",
        "sách gồm mấy phần",
        "tổng số chương chính",
        "how many chapters",
        "how many main sections"
    ],
    GroundingIntent.BOOK_METADATA_AUTHOR: [
        "ai là tác giả cuốn sách này",
        "tác giả quyển sách này là ai",
        "ai viết tác phẩm này",
        "sách này được soạn bởi ai",
        "author của cuốn sách này",
        "who wrote this book",
        "written by"
    ],
    GroundingIntent.BOOK_METADATA_TITLE: [
        "tên sách là gì",
        "tựa đề quyển sách này",
        "đang đọc quyển sách nào",
        "tên của quyển sách đang học",
        "quyển sách này tên là gì",
        "book title"
    ],
    GroundingIntent.BOOK_SECTION_SUMMARY: [
        "tóm tắt chương 1",
        "đại ý của chương hai",
        "tổng quan chương 3",
        "kể tóm lược phần 4",
        "ý chương bốn là gì",
        "ý chính của chương này",
        "ý nghĩa của chương",
        "đại ý chương",
        "summarize",
        "summary of chapter"
    ],
    GroundingIntent.BOOK_SECTION_CONTENT: [
        "nội dung chương 1 là gì",
        "giải thích chương 2",
        "đọc nội dung phần ba",
        "trình bày chi tiết mục 1.1",
        "nội dung phần",
        "what is in section"
    ],
    GroundingIntent.BOOK_METADATA_DOCUMENT_TYPE: [
        "định dạng tài liệu này là gì",
        "đây là loại file gì",
        "đây là tài liệu pdf hay word",
        "loại tài liệu hiện tại",
        "document type",
        "file format"
    ],
    GroundingIntent.BOOK_METADATA_STATUS: [
        "sách đã xử lý xong chưa",
        "trạng thái xử lý của sách",
        "sách đã được nạp thành công chưa",
        "tiến trình nạp sách thế nào",
        "sach da ingest thanh cong chua"
    ],
    GroundingIntent.BOOK_METADATA_SECTION_COUNT: [
        "bao nhiêu đề mục",
        "quyển này có bao nhiêu mục tất cả",
        "tổng số mục trong sách",
        "how many sections",
        "section count"
    ]
}

AUTHOR_CONTENT_VERBS = ("giải thích", "trình bày", "cho rằng", "nói gì", "quan điểm", "nghĩ gì")
AUTHOR_IDENTITY_KEYWORDS = ("ai viết", "who wrote", "written by", "tên của tác giả", "tác giả là ai")

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

class SemanticIntentClassifier:
    def __init__(self) -> None:
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.tokenizer = None
        self.model = None
        self.proto_embeddings = {}
        self._lock = asyncio.Lock()
        self._initialized = False

    def initialize(self) -> None:
        """
        Nạp tokenizer, weights và tính toán trước vector nhúng của các câu mẫu.
        Phương thức này chạy đồng bộ (blocking CPU) nên cần được bao bọc khi gọi từ async loop.
        """
        if self._initialized:
            return
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        self.model.eval()
        
        with torch.no_grad():
            for intent, phrases in PROTOTYPES.items():
                inputs = self.tokenizer(phrases, padding=True, truncation=True, return_tensors="pt")
                outputs = self.model(**inputs)
                embeddings = mean_pooling(outputs, inputs['attention_mask'])
                embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
                self.proto_embeddings[intent] = embeddings
                
        self._initialized = True

    async def initialize_async(self) -> None:
        """
        Khởi tạo an toàn bất đồng bộ. Đẩy tác vụ nạp model nặng sang Executor Thread
        để không chặn Event Loop chính của LiveKit.
        """
        if self._initialized:
            return
        async with self._lock:
            if not self._initialized:
                loop = asyncio.get_running_loop()
                await loop.run_in_executor(None, self.initialize)

    async def classify(self, query_text: str, threshold: float = 0.65) -> GroundingIntent:
        """
        Tính toán cosine similarity của câu hỏi với các mẫu.
        Nếu điểm số cao nhất dưới threshold, mặc định trả về RAG (BOOK_SEMANTIC_QUESTION).
        """
        await self.initialize_async()
        
        text = query_text.strip().lower()
        if not text:
            return GroundingIntent.BOOK_SEMANTIC_QUESTION

        with torch.no_grad():
            inputs = self.tokenizer([text], padding=True, truncation=True, return_tensors="pt")
            outputs = self.model(**inputs)
            query_emb = mean_pooling(outputs, inputs['attention_mask'])
            query_emb = torch.nn.functional.normalize(query_emb, p=2, dim=1)
            
            best_intent = GroundingIntent.BOOK_SEMANTIC_QUESTION
            best_score = -1.0
            
            for intent, proto_embs in self.proto_embeddings.items():
                # Nhân ma trận tính khoảng cách Cosine nhanh trên Pytorch
                sims = torch.matmul(query_emb, proto_embs.T).squeeze(0)
                max_sim = torch.max(sims).item()
                if max_sim > best_score:
                    best_score = max_sim
                    best_intent = intent
                    
            if best_score >= threshold:
                # Kiểm duyệt biên: Nếu hỏi nội dung tác giả viết (RAG) thay vì danh tính tác giả (Metadata)
                if best_intent == GroundingIntent.BOOK_METADATA_AUTHOR:
                    has_content_verb = any(v in text for v in AUTHOR_CONTENT_VERBS)
                    has_identity_keyword = any(k in text for k in AUTHOR_IDENTITY_KEYWORDS)
                    if has_content_verb and not has_identity_keyword:
                        return GroundingIntent.BOOK_SEMANTIC_QUESTION
                return best_intent
                
            return GroundingIntent.BOOK_SEMANTIC_QUESTION

# Đối tượng Singleton dùng chung trong suốt phiên hoạt động của module
_classifier = SemanticIntentClassifier()

async def classify_intent(query: NormalizedQuery) -> GroundingIntent:
    """
    Hàm giao tiếp hướng ngoại tương thích với các module gọi ngoài.
    """
    return await _classifier.classify(query.normalized)

import asyncio
import numpy as np
from openai import AsyncOpenAI

# 1. Tập dữ liệu Ground Truth gán nhãn thực tế
EVAL_DATASET = [
    {"title": "Định nghĩa mảng 2 chiều và cấu trúc con trỏ", "label": "definition"},
    {"title": "Định lý Euler về đa diện lồi", "label": "theorem"},
    {"title": "Công thức tính diện tích hình quạt tròn", "label": "formula"},
    {"title": "Algorithm for binary search in arrays", "label": "method"},
    {"title": "Step-by-step installation guide for Docker", "label": "procedure"},
    {"title": "Ví dụ minh họa cách giải hệ phương trình tuyến tính", "label": "example"},
    {"title": "Chứng minh toán học cho bổ đề Gauss", "label": "reasoning"},
    {"title": "Giới thiệu tổng quan về giải thuật Euclid", "label": "core_concept"},
    {"title": "Hệ thức lượng trong tam giác vuông", "label": "formula"},
    {"title": "Định luật bảo toàn cơ năng Newton", "label": "theorem"},
]

# Quy tắc so khớp V1 cũ để so sánh
V1_KEYWORDS = {
    "core_concept": ["khái niệm", "concept", "nền tảng"],
    "definition": ["định nghĩa", "definition"],
    "theorem": ["định lý", "theorem", "bổ đề"],
    "formula": ["công thức", "formula", "phương trình"],
    "method": ["phương pháp", "method", "thuật toán"],
    "procedure": ["quy trình", "hướng dẫn", "tutorial", "step-by-step"],
    "reasoning": ["suy luận", "chứng minh", "proof"],
    "example": ["ví dụ", "example", "minh họa"],
}

async def run_evaluation():
    from app.core.config import settings
    from app.services.pareto_signal_service import ENRICHED_ANCHORS
    
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    anchor_keys = list(ENRICHED_ANCHORS.keys())
    anchor_texts = list(ENRICHED_ANCHORS.values())
    test_titles = [item["title"] for item in EVAL_DATASET]
    
    print("⏳ Đang gọi OpenAI Embedding API để vectơ hóa dữ liệu thực nghiệm...")
    
    # Batch embedding
    all_texts = anchor_texts + test_titles
    res = await client.embeddings.create(model=settings.BOOK_SECTION_EMBEDDING_MODEL, input=all_texts)
    
    anchor_vectors = {anchor_keys[i]: res.data[i].embedding for i in range(len(anchor_keys))}
    test_vectors = [res.data[len(anchor_keys) + i].embedding for i in range(len(test_titles))]
    
    v1_hits = 0
    v2_hits = 0
    total = len(EVAL_DATASET)
    threshold = 0.20  # Ngưỡng tối ưu hóa thực nghiệm
    
    print("\n=====================================================================")
    print("                     KẾT QUẢ SO KHỚP CHI TIẾT")
    print("=====================================================================")
    
    for idx, item in enumerate(EVAL_DATASET):
        title = item["title"]
        gold_label = item["label"]
        
        # Luồng V1 (Keywords)
        v1_pred = "none"
        for key, keywords in V1_KEYWORDS.items():
            if any(kw in title.lower() for kw in keywords):
                v1_pred = key
                break
                
        # Luồng V2 (Semantic Anchoring - Arg-max)
        v_sec = np.array(test_vectors[idx])
        similarities = {}
        for key, anchor in anchor_vectors.items():
            sim = float(np.dot(v_sec, np.array(anchor)))
            if sim >= threshold:
                similarities[key] = sim
        v2_pred = max(similarities, key=similarities.get) if similarities else "none"
        
        # Tính độ chính xác
        is_v1_correct = (v1_pred == gold_label)
        is_v2_correct = (v2_pred == gold_label)
        
        if is_v1_correct: v1_hits += 1
        if is_v2_correct: v2_hits += 1
        
        print(f"Tiêu đề: '{title}'")
        print(f"  └─ Nhãn gốc (Gold):  {gold_label}")
        print(f"  └─ V1 (Từ khóa):     {v1_pred} {'[ĐÚNG]' if is_v1_correct else '[SAI]'}")
        print(f"  └─ V2 (Ngữ nghĩa):   {v2_pred} {'[ĐÚNG]' if is_v2_correct else '[SAI]'}")
        print("-" * 65)

    print("\n=====================================================================")
    print("                 TỔNG HỢP CHỈ SỐ ĐỘ CHÍNH XÁC (ACCURACY)")
    print("=====================================================================")
    print(f"  * Tổng số mẫu thử nghiệm:    {total}")
    print(f"  * Độ chính xác V1 (Keywords): {v1_hits}/{total} ({v1_hits/total*100:.1f}%)")
    print(f"  * Độ chính xác V2 (Semantic): {v2_hits}/{total} ({v2_hits/total*100:.1f}%)")
    print("=====================================================================")

if __name__ == "__main__":
    asyncio.run(run_evaluation())

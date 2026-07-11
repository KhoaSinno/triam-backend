import os
import sys
sys.path.append(os.getcwd())

# Load environment variables from .env file before importing Pydantic Settings
try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    pass

# Mock required environment variables that may be missing in local .env
os.environ["LIVEKIT_AGENT_NAME"] = "test-agent"


import time
import asyncio
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel

# Use HF Mirror for fast downloads
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"



# Import contracts from the project to ensure alignment
from app.services.agent_grounding.contracts import GroundingIntent, NormalizedQuery
from app.services.agent_grounding.intent_router import PROTOTYPES, mean_pooling

# ==============================================================================
# CLASS CLASSIFIER FOR TESTING (L6 vs L12)
# ==============================================================================

class IntentClassifierTestBed:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()
        self.proto_embeddings = {}
        
        # Precompute prototype embeddings
        with torch.no_grad():
            for intent, phrases in PROTOTYPES.items():
                inputs = self.tokenizer(phrases, padding=True, truncation=True, return_tensors="pt")
                outputs = self.model(**inputs)
                embeddings = mean_pooling(outputs, inputs['attention_mask'])
                embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
                self.proto_embeddings[intent] = embeddings

    def classify(self, query_text: str, threshold: float) -> tuple[GroundingIntent, float]:
        text = query_text.strip().lower()
        if not text:
            return GroundingIntent.BOOK_SEMANTIC_QUESTION, 0.0

        with torch.no_grad():
            inputs = self.tokenizer([text], padding=True, truncation=True, return_tensors="pt")
            outputs = self.model(**inputs)
            query_emb = mean_pooling(outputs, inputs['attention_mask'])
            query_emb = torch.nn.functional.normalize(query_emb, p=2, dim=1)
            
            best_intent = GroundingIntent.BOOK_SEMANTIC_QUESTION
            best_score = -1.0
            
            for intent, proto_embs in self.proto_embeddings.items():
                sims = torch.matmul(query_emb, proto_embs.T).squeeze(0)
                max_sim = torch.max(sims).item()
                if max_sim > best_score:
                    best_score = max_sim
                    best_intent = intent
                    
            # Border conditions check as done in the actual intent_router.py
            if best_intent == GroundingIntent.BOOK_METADATA_AUTHOR:
                AUTHOR_CONTENT_VERBS = ("giải thích", "trình bày", "cho rằng", "nói gì", "quan điểm", "nghĩ gì")
                AUTHOR_IDENTITY_KEYWORDS = ("ai viết", "who wrote", "written by", "tên của tác giả", "tác giả là ai")
                has_content_verb = any(v in text for v in AUTHOR_CONTENT_VERBS)
                has_identity_keyword = any(k in text for k in AUTHOR_IDENTITY_KEYWORDS)
                if has_content_verb and not has_identity_keyword:
                    return GroundingIntent.BOOK_SEMANTIC_QUESTION, best_score
                    
            if best_score >= threshold:
                return best_intent, best_score
                
            return GroundingIntent.BOOK_SEMANTIC_QUESTION, best_score

# ==============================================================================
# TEST DATASET FOR INTENT ROUTER (45 CASES)
# ==============================================================================

INTENT_TEST_CASES = [
    # --- BOOK_METADATA_TITLE ---
    {"text": "sách này tên là gì vậy", "expected": GroundingIntent.BOOK_METADATA_TITLE},
    {"text": "tự đề của quyển sách đang học", "expected": GroundingIntent.BOOK_METADATA_TITLE},
    {"text": "cho hỏi tên quyển sách hiện tại", "expected": GroundingIntent.BOOK_METADATA_TITLE},
    {"text": "quyển này tên là gì", "expected": GroundingIntent.BOOK_METADATA_TITLE},
    {"text": "book title please", "expected": GroundingIntent.BOOK_METADATA_TITLE},

    # --- BOOK_METADATA_AUTHOR ---
    {"text": "ai viết cuốn sách này thế", "expected": GroundingIntent.BOOK_METADATA_AUTHOR},
    {"text": "tác giả quyển sách này là ai", "expected": GroundingIntent.BOOK_METADATA_AUTHOR},
    {"text": "cuốn này được viết bởi ai", "expected": GroundingIntent.BOOK_METADATA_AUTHOR},
    {"text": "who is the author of this book", "expected": GroundingIntent.BOOK_METADATA_AUTHOR},
    {"text": "tác giả cuốn này", "expected": GroundingIntent.BOOK_METADATA_AUTHOR},

    # --- BOOK_METADATA_ROOT_SECTION_COUNT ---
    {"text": "sách có bao nhiêu chương chính", "expected": GroundingIntent.BOOK_METADATA_ROOT_SECTION_COUNT},
    {"text": "tổng số chương chính của sách là mấy", "expected": GroundingIntent.BOOK_METADATA_ROOT_SECTION_COUNT},
    {"text": "quyển sách này gồm mấy chương chính", "expected": GroundingIntent.BOOK_METADATA_ROOT_SECTION_COUNT},
    {"text": "how many main chapters are there", "expected": GroundingIntent.BOOK_METADATA_ROOT_SECTION_COUNT},

    # --- BOOK_METADATA_SECTION_COUNT ---
    {"text": "sách có bao nhiêu đề mục", "expected": GroundingIntent.BOOK_METADATA_SECTION_COUNT},
    {"text": "tổng số mục lớn nhỏ trong sách", "expected": GroundingIntent.BOOK_METADATA_SECTION_COUNT},
    {"text": "quyển này có bao nhiêu mục tất cả", "expected": GroundingIntent.BOOK_METADATA_SECTION_COUNT},

    # --- BOOK_METADATA_DOCUMENT_TYPE ---
    {"text": "định dạng tài liệu này là gì", "expected": GroundingIntent.BOOK_METADATA_DOCUMENT_TYPE},
    {"text": "đây là file pdf hay epub", "expected": GroundingIntent.BOOK_METADATA_DOCUMENT_TYPE},
    {"text": "loại file của sách hiện tại", "expected": GroundingIntent.BOOK_METADATA_DOCUMENT_TYPE},

    # --- BOOK_METADATA_STATUS ---
    {"text": "sách đã xử lý xong chưa", "expected": GroundingIntent.BOOK_METADATA_STATUS},
    {"text": "tiến trình ingest sách đến đâu rồi", "expected": GroundingIntent.BOOK_METADATA_STATUS},
    {"text": "sách nạp thành công chưa", "expected": GroundingIntent.BOOK_METADATA_STATUS},

    # --- BOOK_SECTION_SUMMARY ---
    {"text": "tóm tắt chương 1 giúp mình", "expected": GroundingIntent.BOOK_SECTION_SUMMARY},
    {"text": "đại ý của chương hai là gì", "expected": GroundingIntent.BOOK_SECTION_SUMMARY},
    {"text": "tổng quan chương 3", "expected": GroundingIntent.BOOK_SECTION_SUMMARY},
    {"text": "kể tóm tắt nội dung chính phần 4", "expected": GroundingIntent.BOOK_SECTION_SUMMARY},
    {"text": "summarize chapter 5", "expected": GroundingIntent.BOOK_SECTION_SUMMARY},

    # --- BOOK_SECTION_CONTENT ---
    {"text": "nội dung chương 1 có gì", "expected": GroundingIntent.BOOK_SECTION_CONTENT},
    {"text": "giải thích chi tiết mục 1.2", "expected": GroundingIntent.BOOK_SECTION_CONTENT},
    {"text": "đọc nội dung phần ba", "expected": GroundingIntent.BOOK_SECTION_CONTENT},
    {"text": "trình bày phần 2.3", "expected": GroundingIntent.BOOK_SECTION_CONTENT},

    # --- Fallback: BOOK_SEMANTIC_QUESTION (RAG Fallback) ---
    {"text": "làm sao để vượt qua sự cô đơn trong cuộc sống", "expected": GroundingIntent.BOOK_SEMANTIC_QUESTION},
    {"text": "tại sao nhân vật Lennie lại thích nuôi thỏ", "expected": GroundingIntent.BOOK_SEMANTIC_QUESTION},
    {"text": "hướng dẫn cài đặt livekit server cục bộ", "expected": GroundingIntent.BOOK_SEMANTIC_QUESTION},
    {"text": "phương pháp Pareto giúp ích gì cho quản lý thời gian", "expected": GroundingIntent.BOOK_SEMANTIC_QUESTION},
    {"text": "phương pháp học thông minh của triam hoạt động ra sao", "expected": GroundingIntent.BOOK_SEMANTIC_QUESTION},
    {"text": "phân tích diễn biến tâm lý nhân vật George", "expected": GroundingIntent.BOOK_SEMANTIC_QUESTION},
    {"text": "độ phức tạp của thuật toán RRF là bao nhiêu", "expected": GroundingIntent.BOOK_SEMANTIC_QUESTION},
    {"text": "cấu hình VAD trong livekit thế nào", "expected": GroundingIntent.BOOK_SEMANTIC_QUESTION},
    {"text": "hệ thống WebRTC đồng bộ dữ liệu thoại như thế nào", "expected": GroundingIntent.BOOK_SEMANTIC_QUESTION},
    {"text": "tại sao Reranking Cohere lại tốt hơn FlashRank", "expected": GroundingIntent.BOOK_SEMANTIC_QUESTION}
]

# ==============================================================================
# EVALUATION FUNCTION
# ==============================================================================

def run_evaluation(classifier: IntentClassifierTestBed, threshold: float):
    results = []
    latencies = []
    
    for case in INTENT_TEST_CASES:
        start_time = time.perf_counter()
        predicted, score = classifier.classify(case["text"], threshold)
        latency = (time.perf_counter() - start_time) * 1000
        
        latencies.append(latency)
        results.append({
            "text": case["text"],
            "expected": case["expected"],
            "predicted": predicted,
            "score": score,
            "latency": latency
        })
        
    correct = sum(1 for r in results if r["expected"] == r["predicted"])
    accuracy = (correct / len(INTENT_TEST_CASES)) * 100
    avg_latency = np.mean(latencies)
    
    return accuracy, avg_latency, results

def main():
    print("=" * 70)
    print("INTENT ROUTER COMPARISON: L6 ENGLISH VS L12 MULTILINGUAL")
    print("=" * 70)
    
    print("Loading L6 English Model (sentence-transformers/all-MiniLM-L6-v2)...")
    clf_l6 = IntentClassifierTestBed("sentence-transformers/all-MiniLM-L6-v2")
    
    print("Loading L12 Multilingual Model (sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)...")
    clf_l12 = IntentClassifierTestBed("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    print("Models loaded successfully.\n")

    # Evaluate L6 at threshold 0.65 (Current default)
    acc_l6_65, lat_l6_65, res_l6_65 = run_evaluation(clf_l6, 0.65)
    
    # Evaluate L12 at thresholds 0.60, 0.65, 0.70 to find the best configuration
    acc_l12_60, lat_l12_60, res_l12_60 = run_evaluation(clf_l12, 0.60)
    acc_l12_65, lat_l12_65, res_l12_65 = run_evaluation(clf_l12, 0.65)
    acc_l12_70, lat_l12_70, res_l12_70 = run_evaluation(clf_l12, 0.70)

    print("=" * 70)
    print("COMPARATIVE EVALUATION SUMMARY (44 CASES)")
    print("=" * 70)
    print(f"Model L6 (English-only) @ Threshold 0.65:")
    print(f"  - Accuracy: {acc_l6_65:.2f}%")
    print(f"  - Avg Latency: {lat_l6_65:.2f} ms")
    print("-" * 50)
    print(f"Model L12 (Multilingual) @ Threshold 0.60:")
    print(f"  - Accuracy: {acc_l12_60:.2f}%")
    print(f"  - Avg Latency: {lat_l12_60:.2f} ms")
    print(f"Model L12 (Multilingual) @ Threshold 0.65:")
    print(f"  - Accuracy: {acc_l12_65:.2f}%")
    print(f"  - Avg Latency: {lat_l12_65:.2f} ms")
    print(f"Model L12 (Multilingual) @ Threshold 0.70:")
    print(f"  - Accuracy: {acc_l12_70:.2f}%")
    print(f"  - Avg Latency: {lat_l12_70:.2f} ms")
    print("=" * 70)

    # Detailed side-by-side comparison for best L12 (0.65) vs L6 (0.65)
    print("\nDETAILED COMPARISON (L6 @ 0.65 vs L12 @ 0.65):")
    print(f"{'No':<3} | {'Query Text':<45} | {'Expected Intent':<32} | {'L6 Pred/Score':<22} | {'L12 Pred/Score':<22} | {'L12 Match?'}")
    print("-" * 145)
    
    for idx, (r_l6, r_l12) in enumerate(zip(res_l6_65, res_l12_65)):
        match_l12 = "YES" if r_l12["expected"] == r_l12["predicted"] else "NO"
        # Truncate labels for print alignment
        exp_name = r_l12["expected"].name.replace("BOOK_", "")
        l6_pred_name = r_l6["predicted"].name.replace("BOOK_", "")
        l12_pred_name = r_l12["predicted"].name.replace("BOOK_", "")
        
        pred_score_l6 = f"{l6_pred_name:<15} ({r_l6['score']:.2f})"
        pred_score_l12 = f"{l12_pred_name:<15} ({r_l12['score']:.2f})"
        
        print(f"{idx+1:<3} | {r_l6['text']:<45} | {exp_name:<32} | {pred_score_l6:<22} | {pred_score_l12:<22} | {match_l12}")

if __name__ == "__main__":
    main()

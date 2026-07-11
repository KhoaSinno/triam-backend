import os
import re
import time
import unicodedata
import json
import asyncio
from dataclasses import dataclass
from typing import Literal, Any

# Use HF Mirror for fast downloads in Southeast Asia
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"


# Ensure we import packages properly
try:
    import torch
    from transformers import AutoTokenizer, AutoModel
    import numpy as np
except ImportError:
    print("Error: PyTorch and Transformers must be installed in the virtual environment to run this script.")
    print("Please activate your virtual environment (.venv) and install dependencies:")
    print("  pip install torch transformers numpy openai")
    exit(1)

# ==============================================================================
# 1. CORE LOGIC FROM APPS (COPIED FOR SELF-CONTAINED EXECUTION)
# ==============================================================================

VoiceReplyIntent = Literal["grant", "deny", "unclear", "new_question"]

POSITIVE_ACTION_PHRASES = (
    "dong y", "dung roi", "dung do", "chinh xac", "phai roi", "tim di", 
    "tim kiem di", "search di", "lam di", "cu lam", "cu tim", "tiep di", 
    "thu xem", "go ahead", "do it", "search it", "cho phep", "cho phep di", 
    "cho phep lam", "duoc phep", "tim tren mang", "tim tren web", "tim google", 
    "tim internet", "dong y tim", "dong y luon", "chap nhan", "dong y nha", 
    "duoc chu", "co chu", "tim giup", "tim ho", "tim di ban", "u tim"
)
POSITIVE_SHORT_REPLIES = (
    "co", "uh", "um", "ok", "oke", "okay", "yes", "yep", "yup", "yub", 
    "sure", "duoc", "duoc roi", "dung", "dung roi", "phai", "phai roi", 
    "cho phep", "vang", "da vang", "da", "u", "ua"
)
NEGATIVE_PHRASES = (
    "khong phai", "khong can", "khong dau", "khong duoc", "khong muon", 
    "khong thich", "khong", "khoi", "dung lam", "dung tim", "dung search", 
    "thoi", "bo qua", "skip", "cancel", "stop", "nope", "nah", "no", 
    "dont", "do not"
)

CONTEXT_SENSITIVE_NEGATIONS = {"khong", "no"}
CONTEXT_SENSITIVE_CONFIRMATIONS = {"co", "duoc", "dung", "phai", "uh", "um", "u", "da", "ua"}

@dataclass(frozen=True)
class VoiceReplyIntentResult:
    intent: VoiceReplyIntent
    confidence: float
    reason: str = ""
    source: str = "fast_path"

def normalize_voice_intent_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", (text or "").casefold())
    without_marks = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    without_marks = without_marks.replace("đ", "d")
    without_marks = re.sub(r"[^a-z0-9]+", " ", without_marks)
    return " ".join(without_marks.split())

def phrase_in_text(phrase: str, text: str) -> bool:
    return f" {phrase} " in f" {text} "

def looks_like_new_question(original_text: str, normalized_text: str) -> bool:
    if "?" in original_text:
        return True
    question_words = [
        "la gi", "sao", "nao", "the nao", "ai", "bao nhieu", "chong may", 
        "chuong may", "tai sao", "lam sao", "what is", "who is", "how many", "why"
    ]
    return any(phrase_in_text(qw, normalized_text) for qw in question_words)

def classify_voice_reply_intent_fast_path(text: str, *, max_grant_tokens: int = 4) -> VoiceReplyIntentResult | None:
    normalized = normalize_voice_intent_text(text)
    if not normalized:
        return None

    token_count = len(normalized.split())
    # Constrain fast path positive/negative matching to short replies only
    if token_count > max(4, max_grant_tokens):
        if looks_like_new_question(text, normalized):
            return VoiceReplyIntentResult("new_question", 0.88, "Explicit question mark or word detected", "fast_path")
        return None

    # 1. Match negative fast path phrases first
    for phrase in NEGATIVE_PHRASES:
        if phrase in CONTEXT_SENSITIVE_NEGATIONS:
            if token_count <= 2 and phrase_in_text(phrase, normalized):
                return VoiceReplyIntentResult("deny", 0.96, "Matched negative fast path", "fast_path")
        else:
            if phrase_in_text(phrase, normalized):
                return VoiceReplyIntentResult("deny", 0.96, "Matched negative fast path", "fast_path")

    # 2. Match positive action phrases
    if any(phrase_in_text(phrase, normalized) for phrase in POSITIVE_ACTION_PHRASES):
        return VoiceReplyIntentResult("grant", 0.96, "Matched positive action fast path", "fast_path")

    # 3. Match positive short replies
    for phrase in POSITIVE_SHORT_REPLIES:
        if phrase in CONTEXT_SENSITIVE_CONFIRMATIONS:
            if token_count <= 2 and phrase_in_text(phrase, normalized):
                return VoiceReplyIntentResult("grant", 0.94, "Matched short positive fast path", "fast_path")
        else:
            if phrase_in_text(phrase, normalized):
                return VoiceReplyIntentResult("grant", 0.94, "Matched short positive fast path", "fast_path")

    # 4. Check if it looks like a new question only if it does not match positive/negative phrases
    if looks_like_new_question(text, normalized):
        return VoiceReplyIntentResult("new_question", 0.88, "Explicit question mark or word detected", "fast_path")

    return None

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

# ==============================================================================
# 2. LOCAL COSIM EMBEDDING CLASSIFIER - L6 ENGLISH (METHOD B)
# ==============================================================================

L6_WEB_PERMISSION_PROTOTYPES = {
    "grant": [
        "dong y cho tim kiem", "u tim tren internet di", "cho phep tra cuu google",
        "tim giup minh tren mang", "search ho minh thong tin nay", "dong y nha",
        "duoc chu tim di", "yes search it", "go ahead and search"
    ],
    "deny": [
        "khong can tim dau", "dung tra cuu internet", "thoi khoi can",
        "bo qua di ban", "khong muon tim tren web", "dung tim kiem",
        "no don't search", "cancel web search"
    ],
    "unclear": [
        "chua biet nua", "de tinh sau di", "tuy ban thoi", "cai do kho noi",
        "sao cung duoc", "maybe later"
    ]
}

class LocalSemanticClassifierL6:
    def __init__(self):
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        self.model.eval()
        self.proto_embeddings = {}
        
        with torch.no_grad():
            for intent, phrases in L6_WEB_PERMISSION_PROTOTYPES.items():
                inputs = self.tokenizer(phrases, padding=True, truncation=True, return_tensors="pt")
                outputs = self.model(**inputs)
                embeddings = mean_pooling(outputs, inputs['attention_mask'])
                embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
                self.proto_embeddings[intent] = embeddings

    def classify(self, query_text: str, threshold: float = 0.55) -> tuple[VoiceReplyIntent, float]:
        normalized = normalize_voice_intent_text(query_text)
        if looks_like_new_question(query_text, normalized):
            return "new_question", 1.0
            
        with torch.no_grad():
            inputs = self.tokenizer([normalized], padding=True, truncation=True, return_tensors="pt")
            outputs = self.model(**inputs)
            query_emb = mean_pooling(outputs, inputs['attention_mask'])
            query_emb = torch.nn.functional.normalize(query_emb, p=2, dim=1)
            
            best_intent = "unclear"
            best_score = -1.0
            
            for intent, proto_embs in self.proto_embeddings.items():
                sims = torch.matmul(query_emb, proto_embs.T).squeeze(0)
                max_sim = torch.max(sims).item()
                if max_sim > best_score:
                    best_score = max_sim
                    best_intent = intent
            
            if best_score < threshold:
                return "new_question", best_score
                
            return best_intent, best_score

# ==============================================================================
# 3. LOCAL COSIM EMBEDDING CLASSIFIER - L12 MULTILINGUAL (METHOD C)
# ==============================================================================

# Multilingual prototypes keep accented Vietnamese for native understanding!
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

class LocalSemanticClassifierL12:
    def __init__(self):
        # paraphrase-multilingual-MiniLM-L12-v2 natively understands Vietnamese
        self.model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        self.model.eval()
        self.proto_embeddings = {}
        
        with torch.no_grad():
            for intent, phrases in L12_WEB_PERMISSION_PROTOTYPES.items():
                # We do NOT normalize/strip accents here; keep them for multilingual semantics
                inputs = self.tokenizer(phrases, padding=True, truncation=True, return_tensors="pt")
                outputs = self.model(**inputs)
                embeddings = mean_pooling(outputs, inputs['attention_mask'])
                embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
                self.proto_embeddings[intent] = embeddings

    def classify(self, query_text: str, threshold: float = 0.55) -> tuple[VoiceReplyIntent, float]:
        # For looks_like_new_question we still use normalized representation
        normalized = normalize_voice_intent_text(query_text)
        if looks_like_new_question(query_text, normalized):
            return "new_question", 1.0
            
        with torch.no_grad():
            # Pass original accented text directly to multilingual tokenizer!
            inputs = self.tokenizer([query_text.strip().lower()], padding=True, truncation=True, return_tensors="pt")
            outputs = self.model(**inputs)
            query_emb = mean_pooling(outputs, inputs['attention_mask'])
            query_emb = torch.nn.functional.normalize(query_emb, p=2, dim=1)
            
            best_intent = "unclear"
            best_score = -1.0
            
            for intent, proto_embs in self.proto_embeddings.items():
                sims = torch.matmul(query_emb, proto_embs.T).squeeze(0)
                max_sim = torch.max(sims).item()
                if max_sim > best_score:
                    best_score = max_sim
                    best_intent = intent
            
            if best_score < threshold:
                return "new_question", best_score
                
            return best_intent, best_score

# ==============================================================================
# 4. OPENAI API CLASSIFIER (CURRENT BACKUP METHOD)
# ==============================================================================

async def classify_with_openai_mock_or_real(query_text: str, pending_query: str) -> VoiceReplyIntent:
    from openai import AsyncOpenAI
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        try:
            with open(".env", "r") as f:
                for line in f:
                    if line.startswith("OPENAI_API_KEY="):
                        api_key = line.strip().split("=", 1)[1].strip("'\"")
                        break
        except Exception:
            pass

    if not api_key:
        normalized = normalize_voice_intent_text(query_text)
        if looks_like_new_question(query_text, normalized):
            return "new_question"
        if any(w in normalized for w in ["dong y", "tim di", "search", "yes", "duoc", "vang", "co"]):
            return "grant"
        if any(w in normalized for w in ["khong", "dung", "no", "cancel", "thoi"]):
            return "deny"
        return "unclear"

    client = AsyncOpenAI(api_key=api_key)
    system_prompt = """Classify whether the user is answering a web-search permission question. Return only valid JSON: {"intent":"grant|deny|unclear|new_question"}"""
    user_prompt = f"Pending web query: {pending_query}\nUser reply: {query_text}"
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            timeout=5.0
        )
        payload = json.loads(response.choices[0].message.content)
        intent = payload.get("intent", "unclear")
        if intent in ["grant", "deny", "unclear", "new_question"]:
            return intent
    except Exception:
        pass
    return "unclear"

# ==============================================================================
# 5. EXPANDED TEST CASES DATASET (50 CASES)
# ==============================================================================

TEST_CASES = [
    # === 1. EASY VIETNAMESE POSITIVES (10) ===
    {"text": "đồng ý", "expected": "grant", "type": "easy_vi"},
    {"text": "có chứ", "expected": "grant", "type": "easy_vi"},
    {"text": "tìm đi", "expected": "grant", "type": "easy_vi"},
    {"text": "được", "expected": "grant", "type": "easy_vi"},
    {"text": "tìm đi bạn", "expected": "grant", "type": "easy_vi"},
    {"text": "ừ tìm đi", "expected": "grant", "type": "easy_vi"},
    {"text": "ok nha", "expected": "grant", "type": "easy_vi_en"},
    {"text": "đồng ý luôn", "expected": "grant", "type": "easy_vi"},
    {"text": "nhất trí", "expected": "grant", "type": "easy_vi"},
    {"text": "cho phép nha", "expected": "grant", "type": "easy_vi"},
    
    # === 2. EASY ENGLISH POSITIVES (5) ===
    {"text": "ok", "expected": "grant", "type": "easy_en"},
    {"text": "yes", "expected": "grant", "type": "easy_en"},
    {"text": "sure", "expected": "grant", "type": "easy_en"},
    {"text": "yep", "expected": "grant", "type": "easy_en"},
    {"text": "go ahead", "expected": "grant", "type": "easy_en"},
    
    # === 3. EASY VIETNAMESE NEGATIVES (10) ===
    {"text": "không", "expected": "deny", "type": "easy_vi"},
    {"text": "không cần", "expected": "deny", "type": "easy_vi"},
    {"text": "thôi khỏi", "expected": "deny", "type": "easy_vi"},
    {"text": "thôi đừng", "expected": "deny", "type": "easy_vi"},
    {"text": "đừng tìm", "expected": "deny", "type": "easy_vi"},
    {"text": "khỏi đi", "expected": "deny", "type": "easy_vi"},
    {"text": "bỏ qua đi", "expected": "deny", "type": "easy_vi"},
    {"text": "không search", "expected": "deny", "type": "easy_vi_en"},
    {"text": "hủy đi", "expected": "deny", "type": "easy_vi"},
    {"text": "thôi bỏ qua", "expected": "deny", "type": "easy_vi"},

    # === 4. EASY ENGLISH NEGATIVES (5) ===
    {"text": "no", "expected": "deny", "type": "easy_en"},
    {"text": "nope", "expected": "deny", "type": "easy_en"},
    {"text": "skip", "expected": "deny", "type": "easy_en"},
    {"text": "cancel", "expected": "deny", "type": "easy_en"},
    {"text": "don't", "expected": "deny", "type": "easy_en"},

    # === 5. HARD VIETNAMESE POSITIVES (5) ===
    {"text": "ừ bạn tra cứu giúp mình trên mạng xem", "expected": "grant", "type": "hard_vi"},
    {"text": "cho phép tìm kiếm trên internet nha", "expected": "grant", "type": "hard_vi"},
    {"text": "ừ thì cứ tìm đi xem có thông tin gì không", "expected": "grant", "type": "hard_vi"},
    {"text": "tìm kiếm thông tin liên quan trên mạng giúp mình với nhé", "expected": "grant", "type": "hard_vi"},
    {"text": "bạn thử tra cứu tài liệu trên google xem thế nào", "expected": "grant", "type": "hard_vi"},
    
    # === 6. HARD VIETNAMESE NEGATIVES (5) ===
    {"text": "thôi không cần tra mạng đâu mất công", "expected": "deny", "type": "hard_vi"},
    {"text": "đừng tìm kiếm internet làm gì mất thời gian lắm", "expected": "deny", "type": "hard_vi"},
    {"text": "bỏ qua phần tìm kiếm internet đi mình tự đọc sách được", "expected": "deny", "type": "hard_vi"},
    {"text": "không cần search google đâu trả lời tiếp đi", "expected": "deny", "type": "hard_vi_en"},
    {"text": "thôi đừng tra mạng nữa mất thời gian lắm", "expected": "deny", "type": "hard_vi"},

    # === 7. UNCLEAR VIETNAMESE & ENGLISH (5) ===
    {"text": "để mình suy nghĩ tí", "expected": "unclear", "type": "unclear_vi"},
    {"text": "cái này tùy bạn quyết định", "expected": "unclear", "type": "unclear_vi"},
    {"text": "chưa chắc nữa để sau đi", "expected": "unclear", "type": "unclear_vi"},
    {"text": "để xem tình hình thế nào đã", "expected": "unclear", "type": "unclear_vi"},
    {"text": "maybe later let's see", "expected": "unclear", "type": "unclear_en"},

    # === 8. NEW QUESTIONS / SEMANTIC SHIFT (5) ===
    {"text": "chương 4 nói về cái gì vậy", "expected": "new_question", "type": "new_q_vi"},
    {"text": "tác giả cuốn sách này là ai vậy bạn", "expected": "new_question", "type": "new_q_vi"},
    {"text": "thôi bỏ qua đi, cho hỏi chương 2 có những đề mục nào", "expected": "new_question", "type": "new_q_vi"},
    {"text": "what is pareto study method?", "expected": "new_question", "type": "new_q_en"},
    {"text": "sách này có mấy chương tất cả thế", "expected": "new_question", "type": "new_q_vi"}
]

# ==============================================================================
# 6. RUNNER
# ==============================================================================

async def main():
    print("=" * 70)
    print("EVALUATION RUNNER: THREE WEB SEARCH PERMISSION CLASSIFICATION METHODS")
    print("=" * 70)
    
    print("Loading Model L6 (English-only MiniLM-L6)...")
    classifier_l6 = LocalSemanticClassifierL6()
    
    print("Loading Model L12 (Multilingual MiniLM-L12 - understands Vietnamese)...")
    classifier_l12 = LocalSemanticClassifierL12()
    
    print("Models loaded successfully.\n")

    pending_query = "phương pháp học Pareto giúp nhớ bao nhiêu kiến thức"

    # --- Method A Evaluation (OpenAI) ---
    print("Running Method A: Fast Path + OpenAI API Fallback...")
    results_a = []
    latencies_a = []
    for case in TEST_CASES:
        start_time = time.perf_counter()
        fast_res = classify_voice_reply_intent_fast_path(case["text"])
        if fast_res is not None:
            predicted = fast_res.intent
            source = "fast_path"
        else:
            predicted = await classify_with_openai_mock_or_real(case["text"], pending_query)
            source = "openai"
        latency = (time.perf_counter() - start_time) * 1000
        latencies_a.append(latency)
        results_a.append({"text": case["text"], "expected": case["expected"], "predicted": predicted, "source": source, "latency": latency})

    # --- Method B Evaluation (L6 English Cosine) ---
    print("Running Method B: Fast Path <= 2 + Local L6 English Cosine...")
    results_b = []
    latencies_b = []
    for case in TEST_CASES:
        start_time = time.perf_counter()
        normalized = normalize_voice_intent_text(case["text"])
        token_count = len(normalized.split())
        
        if token_count <= 2:
            fast_res = classify_voice_reply_intent_fast_path(case["text"])
            if fast_res is not None:
                predicted = fast_res.intent
                source = "fast_path"
            else:
                predicted, score = classifier_l6.classify(case["text"])
                source = "l6_embeddings"
        else:
            predicted, score = classifier_l6.classify(case["text"])
            source = "l6_embeddings"
            
        latency = (time.perf_counter() - start_time) * 1000
        latencies_b.append(latency)
        results_b.append({"text": case["text"], "expected": case["expected"], "predicted": predicted, "source": source, "latency": latency})

    # --- Method C Evaluation (L12 Multilingual Cosine) ---
    print("Running Method C: Fast Path <= 2 + Local L12 Multilingual Cosine...")
    results_c = []
    latencies_c = []
    for case in TEST_CASES:
        start_time = time.perf_counter()
        normalized = normalize_voice_intent_text(case["text"])
        token_count = len(normalized.split())
        
        if token_count <= 2:
            fast_res = classify_voice_reply_intent_fast_path(case["text"])
            if fast_res is not None:
                predicted = fast_res.intent
                source = "fast_path"
            else:
                predicted, score = classifier_l12.classify(case["text"])
                source = "l12_embeddings"
        else:
            predicted, score = classifier_l12.classify(case["text"])
            source = "l12_embeddings"
            
        latency = (time.perf_counter() - start_time) * 1000
        latencies_c.append(latency)
        results_c.append({"text": case["text"], "expected": case["expected"], "predicted": predicted, "source": source, "latency": latency})

    # ==============================================================================
    # 7. PRINT SUMMARY REPORT
    # ==============================================================================
    
    def get_stats(results, latencies, api_source_name):
        correct = sum(1 for r in results if r["expected"] == r["predicted"])
        acc = (correct / len(results)) * 100
        avg_lat = np.mean(latencies)
        calls = sum(1 for r in results if r["source"] == api_source_name)
        return acc, avg_lat, calls

    acc_a, lat_a, calls_a = get_stats(results_a, latencies_a, "openai")
    acc_b, lat_b, calls_b = get_stats(results_b, latencies_b, "l6_embeddings")
    acc_c, lat_c, calls_c = get_stats(results_c, latencies_c, "l12_embeddings")

    print("\n" + "=" * 60)
    print("METRIC RESULTS COMPARISON SUMMARY (50 CASES)")
    print("=" * 60)
    print(f"Method A (Current: Fast Path + OpenAI API):")
    print(f"  - Accuracy: {acc_a:.2f}%")
    print(f"  - Avg Latency: {lat_a:.2f} ms")
    print(f"  - OpenAI API calls: {calls_a} / {len(TEST_CASES)}")
    print(f"Method B (Proposed: Fast Path <= 2 + Local L6 English Cosine):")
    print(f"  - Accuracy: {acc_b:.2f}%")
    print(f"  - Avg Latency: {lat_b:.2f} ms")
    print(f"  - L6 Embeddings calls: {calls_b} / {len(TEST_CASES)}")
    print(f"Method C (Proposed: Fast Path <= 2 + Local L12 Multilingual Cosine):")
    print(f"  - Accuracy: {acc_c:.2f}%")
    print(f"  - Avg Latency: {lat_c:.2f} ms")
    print(f"  - L12 Embeddings calls: {calls_c} / {len(TEST_CASES)}")
    print("=" * 60)

    # Detailed comparison list
    print("\nDETAILED COMPARISON TABLE:")
    print(f"{'No':<3} | {'Query Text':<50} | {'Expected':<12} | {'A (Pred/Src)':<20} | {'B (Pred/Src)':<20} | {'C (Pred/Src)':<20} | {'C Match?'}")
    print("-" * 155)
    for idx, (r_a, r_b, r_c) in enumerate(zip(results_a, results_b, results_c)):
        match_c = "YES" if r_c["expected"] == r_c["predicted"] else "NO"
        pred_src_a = f"{r_a['predicted']}/{r_a['source']}"
        pred_src_b = f"{r_b['predicted']}/{r_b['source']}"
        pred_src_c = f"{r_c['predicted']}/{r_c['source']}"
        print(f"{idx+1:<3} | {r_a['text']:<50} | {r_a['expected']:<12} | {pred_src_a:<20} | {pred_src_b:<20} | {pred_src_c:<20} | {match_c}")

if __name__ == "__main__":
    asyncio.run(main())

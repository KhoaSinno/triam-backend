import sys
import os
import asyncio
from typing import Any

# Ensure parent directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(override=True)

from sqlmodel import Session, select
from app.db.database import engine
from app.models.db_models import Book, BookSection
from app.services.rag_service import search_book_section_knowledge, search_book_section_knowledge_lexical, _hybrid_config
from app.services.agent_grounding.hybrid_retrieval import (
    merge_candidates,
    rerank_candidates as base_rerank_candidates,
    select_context_candidates,
    _candidate_to_payload
)
from app.services.agent_grounding.reranker import rerank_candidates as cohere_rerank_candidates
from app.core.config import settings

# Test queries and expectation snippets (corresponds to actual books in the DB)
TEST_CASES = [
    # Book: Chapter 4 ( v2_Chương 4_ Phương pháp luận nghiên cứu )
    {
        "case_num": 1,
        "book_title": "Chương 4_ Phương pháp luận nghiên cứu",
        "query": "Quy trình SLR giúp tránh các đánh giá cảm tính cá nhân của người viết như thế nào?",
        "expected_snippet": "giảm thiểu thiên lệch của đánh giá chủ quan",
    },
    {
        "case_num": 2,
        "book_title": "Chương 4_ Phương pháp luận nghiên cứu",
        "query": "Mô hình nào được đánh giá là hữu dụng hơn khi xử lý toàn bộ kho mã nguồn khổng lồ?",
        "expected_snippet": "phân tích được toàn bộ dự án hay đa tệp tin cùng lúc",
    },
    {
        "case_num": 3,
        "book_title": "Chương 4_ Phương pháp luận nghiên cứu",
        "query": "So sánh điểm số của GPT-5 và Gemini 2.5 Pro trên bộ kiểm tra năng lực lập trình phần mềm SWE-bench?",
        "expected_snippet": "SWE-bench Verified (Lập trình)",
    },
    {
        "case_num": 4,
        "book_title": "Chương 4_ Phương pháp luận nghiên cứu",
        "query": "Hình ảnh được tạo ra từ Imagen và Nano Banana có ưu thế gì trong việc chỉnh sửa?",
        "expected_snippet": "duy trì tính nhất quán của hình ảnh qua các lần chỉnh sửa",
    },
    {
        "case_num": 9,
        "book_title": "Chương 4_ Phương pháp luận nghiên cứu",
        "query": "Sự khác biệt về triết lý an toàn thông tin và bảo mật dữ liệu giữa OpenAI và Google?",
        "expected_snippet": "OpenAI mặc định lưu trữ nội dung người dùng nhập vào API trong 30 ngày",
    },
    {
        "case_num": 10,
        "book_title": "Chương 4_ Phương pháp luận nghiên cứu",
        "query": "So sánh chi phí sử dụng API và chính sách giá giữa ChatGPT và Gemini cho nhà phát triển?",
        "expected_snippet": "GPT-5 tính phí khoảng $1,25/1M tokens đầu vào",
    },
    # Book: outline ( tai_lieu_outline_mau_rag_audio )
    {
        "case_num": 7,
        "book_title": "tai_lieu_outline_mau_rag_audio",
        "query": "Thiết bị tưới nước tự động giúp giải quyết khó khăn gì cho người trồng cây ở thành phố?",
        "expected_snippet": "người dùng thường thiếu thời gian chăm sóc cây",
    },
    {
        "case_num": 8,
        "book_title": "tai_lieu_outline_mau_rag_audio",
        "query": "Tài liệu đề cương này có bao gồm hướng dẫn chi tiết cách lắp ráp linh kiện và viết code hay không?",
        "expected_snippet": "Nội dung không đi sâu vào sơ đồ mạch, mã nguồn hoặc lựa chọn linh kiện cụ thể",
    }
]

# Helper to look up document IDs in DB matching book_title
def get_matching_document_ids(session: Session, title_query: str) -> list[str]:
    books = session.exec(select(Book)).all()
    matching_ids = []
    for b in books:
        if title_query.lower() in b.title.lower():
            matching_ids.append(str(b.id))
    return matching_ids

def get_item_id(item: dict[str, Any]) -> str:
    item_id = item.get("id")
    if item_id is not None:
        return str(item_id)
    return f"{item.get('section_id', '')}:{item.get('chunk_index', '')}"

def compute_rrf(vector_res: list[dict[str, Any]], lexical_res: list[dict[str, Any]], candidates: list[Any], k: int = 60) -> dict[str, float]:
    vector_ranks = {get_item_id(item): idx + 1 for idx, item in enumerate(vector_res)}
    lexical_ranks = {get_item_id(item): idx + 1 for idx, item in enumerate(lexical_res)}
    
    rrf_scores = {}
    for c in candidates:
        c_id = c.id
        term_v = 1.0 / (k + vector_ranks[c_id]) if c_id in vector_ranks else 0.0
        term_l = 1.0 / (k + lexical_ranks[c_id]) if c_id in lexical_ranks else 0.0
        rrf_scores[c_id] = term_v + term_l
    return rrf_scores

async def run_evaluation():
    print("🚀 Starting Hybrid Fusion Evaluation Script...")
    
    # Import ranx on-the-fly
    try:
        from ranx import Qrels, Run, compare
    except ImportError:
        print("❌ Error: ranx is not installed. Please run this script with 'uv run --with ranx ...'")
        sys.exit(1)
        
    qrels_dict = {}
    base_run_dict = {}
    rrf_run_dict = {}
    cohere_run_dict = {}
    
    # Enable reranker in settings for testing
    settings.AGENT_RERANKER_ENABLED = True
    config = _hybrid_config()
    
    with Session(engine) as session:
        for case in TEST_CASES:
            case_id = f"q_{case['case_num']}"
            query = case["query"]
            book_title = case["book_title"]
            expected_snippet = case["expected_snippet"]
            
            # 1. Resolve Document IDs
            doc_ids = get_matching_document_ids(session, book_title)
            if not doc_ids:
                print(f"⚠️ Case {case['case_num']}: No book matching '{book_title}' found in DB. Skipping.")
                continue
                
            print(f"\nEvaluating Case {case['case_num']}: \"{query}\" (doc_ids: {doc_ids})")
            
            # 2. Run Retrieval Tasks
            vector_raw = await search_book_section_knowledge(query, doc_ids, match_count=20)
            lexical_raw = await search_book_section_knowledge_lexical(query, doc_ids, match_count=20)
            
            vector_res = vector_raw if isinstance(vector_raw, list) else []
            lexical_res = lexical_raw if isinstance(lexical_raw, list) else []
            
            # 3. Merge candidates
            candidates = merge_candidates(vector_res, lexical_res)
            if not candidates:
                print(f"⚠️ Case {case['case_num']}: No candidates retrieved. Skipping.")
                continue
                
            # 4. Find Ground Truth (Qrels)
            target_id = None
            for c in candidates:
                if expected_snippet.lower() in c.content.lower():
                    target_id = c.id
                    break
                    
            if not target_id:
                # Look up directly in DB BookSection table
                sections = session.exec(select(BookSection).where(BookSection.book_id.in_(doc_ids))).all()
                for s in sections:
                    if s.text_content and expected_snippet.lower() in s.text_content.lower():
                        target_id = str(s.id)
                        print(f"🎯 Found target ID directly in DB BookSection: {target_id}")
                        break
            
            if not target_id:
                print(f"❌ Case {case['case_num']}: Could not find any section containing expected snippet. Skipping.")
                continue
                
            # Add to Qrels
            qrels_dict[case_id] = {target_id: 1}
            
            # 5. Method A: Base Reranker
            ranked_base = base_rerank_candidates(query, candidates, vector_res, lexical_res, config)
            selected_base = select_context_candidates(ranked_base, config)
            base_run_dict[case_id] = {c.id: c.final_score for c in selected_base}
            
            # 6. Method B: Reciprocal Rank Fusion (RRF)
            rrf_scores = compute_rrf(vector_res, lexical_res, candidates, k=60)
            # Sort and slice top 20
            sorted_rrf = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:config.max_context_chunks]
            rrf_run_dict[case_id] = {d_id: score for d_id, score in sorted_rrf}
            
            # 7. Method C: Cohere Rerank
            cohere_payload = [_candidate_to_payload(c) for c in selected_base]
            cohere_res = await cohere_rerank_candidates(query, cohere_payload, top_n=20)
            cohere_run_dict[case_id] = {item["id"]: item["final_score"] for item in cohere_res}
            
            # Debug ranking locations
            base_rank = "N/A"
            for idx, c in enumerate(selected_base):
                if c.id == target_id:
                    base_rank = idx + 1
                    break
                    
            rrf_rank = "N/A"
            for idx, (d_id, _) in enumerate(sorted_rrf):
                if d_id == target_id:
                    rrf_rank = idx + 1
                    break
                    
            cohere_rank = "N/A"
            for idx, item in enumerate(cohere_res):
                if item["id"] == target_id:
                    cohere_rank = idx + 1
                    break
                    
            print(f"📊 target_id={target_id} | Ranks: Base Reranker={base_rank} | RRF={rrf_rank} | Cohere={cohere_rank}")

    # Ensure all run dicts have all keys to satisfy ranx
    for q_id in qrels_dict.keys():
        if q_id not in base_run_dict:
            base_run_dict[q_id] = {}
        if q_id not in rrf_run_dict:
            rrf_run_dict[q_id] = {}
        if q_id not in cohere_run_dict:
            cohere_run_dict[q_id] = {}

    # Initialize ranx objects
    qrels = Qrels(qrels_dict)
    run_base = Run(base_run_dict, name="Base Reranker (CombSUM+CombMAX)")
    run_rrf = Run(rrf_run_dict, name="RRF (k=60)")
    run_cohere = Run(cohere_run_dict, name="Cohere Rerank v3.0")
    
    # Run comparison
    print("\n🏆 Calculating comparison metrics using ranx...")
    report = compare(
        qrels=qrels,
        runs=[run_base, run_rrf, run_cohere],
        metrics=["map", "mrr", "ndcg@1", "ndcg@3", "ndcg@5", "recall@3", "recall@5"]
    )
    
    # Print console report
    print("\n=================== 📊 RANX EVALUATION REPORT ===================")
    print(report)
    print("=================================================================\n")
    
    # Save report to Markdown file
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "script_outputs")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "hybrid_search_fusion_evaluation.md")
    
    # Convert report to markdown string
    report_dict = report.to_dict()
    
    markdown_content = f"""# 🏆 Báo cáo Đánh giá Thử nghiệm các Thuật toán hợp nhất Hybrid Search
    
Báo cáo này so sánh hiệu năng xếp hạng giữa 3 thuật toán:
1. **Base Reranker (CombSUM + CombMAX + Heuristic Boosts)**: Thuật toán chập điểm tuyến tính có cộng điểm thưởng tiêu đề và đa nguồn (hiện tại của hệ thống).
2. **RRF (Reciprocal Rank Fusion - k=60)**: Thuật toán gộp xếp hạng nghịch đảo chuẩn quốc tế.
3. **Cohere Rerank v3.0**: Mô hình học sâu chuyên sâu xếp hạng lại ngữ nghĩa.

Đánh giá được thực hiện trên **{len(qrels_dict)} truy vấn mẫu** thực tế dựa trên dữ liệu sách đã tải lên trong database của hệ thống.

## 📊 1. Kết quả so sánh chỉ số đo lường (ranx output)

{report}

## 🔍 2. Phân tích chi tiết từng trường hợp kiểm thử

"""
    
    # Append cases details
    for case in TEST_CASES:
        case_id = f"q_{case['case_num']}"
        if case_id not in qrels_dict:
            continue
            
        target_id = list(qrels_dict[case_id].keys())[0]
        
        # Extract ranks
        base_rank = "N/A"
        for idx, (c_id, _) in enumerate(base_run_dict[case_id].items()):
            if c_id == target_id:
                base_rank = idx + 1
                break
                
        rrf_rank = "N/A"
        for idx, (c_id, _) in enumerate(rrf_run_dict[case_id].items()):
            if c_id == target_id:
                rrf_rank = idx + 1
                break
                
        cohere_rank = "N/A"
        for idx, (c_id, _) in enumerate(cohere_run_dict[case_id].items()):
            if c_id == target_id:
                cohere_rank = idx + 1
                break
                
        markdown_content += f"""### Case {case['case_num']}: *\"{case['query']}\"*
* **Snippet mong muốn (Ground Truth)**: `\"{case['expected_snippet']}\"`
* **Vị trí xếp hạng của đáp án đúng**:
  * **Base Reranker (CombSUM+CombMAX)**: Hạng **{base_rank}**
  * **RRF (k=60)**: Hạng **{rrf_rank}**
  * **Cohere Rerank v3.0**: Hạng **{cohere_rank}**

---
"""
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    print(f"✅ Metric evaluation completed. Saved markdown report to: {output_path}")

if __name__ == "__main__":
    asyncio.run(run_evaluation())

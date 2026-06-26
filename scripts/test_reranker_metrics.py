import os
import json
import time
import asyncio
import httpx
from dotenv import load_dotenv

# Load env variables
load_dotenv(override=True)

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    print("⚠️ WARNING: COHERE_API_KEY not found in environment!")

# Paths to script outputs
SCRIPT_OUTPUTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "script_outputs")
VI_OUTLINE_PATH = os.path.join(SCRIPT_OUTPUTS_DIR, "book_section_knowledge_outline_testdoc.json")
VI_CHAP4_PATH = os.path.join(SCRIPT_OUTPUTS_DIR, "section_chap4.json")
VI_TRR_PATH = os.path.join(SCRIPT_OUTPUTS_DIR, "section_trr.json")


def load_outline_candidates():
    if not os.path.exists(VI_OUTLINE_PATH):
        print(f"❌ File not found: {VI_OUTLINE_PATH}")
        return []
    with open(VI_OUTLINE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_section_candidates(filepath):
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        sections = json.load(f)
    
    candidates = []
    for idx, s in enumerate(sections):
        text = s.get("text_content")
        if text:
            candidates.append({
                "id": s.get("id") or str(idx),
                "chunk_index": s.get("section_index", idx),
                "content": f"[{s.get('path', '')}] {s.get('title', '')}\n{text}"
            })
    return candidates


# Gọi API Cohere Reranker v2 trực tiếp
async def cohere_rerank(query, candidates, model="rerank-multilingual-v3.0"):
    if not COHERE_API_KEY:
        return None, 0.0

    url = "https://api.cohere.com/v2/rerank"
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json",
        "accept": "application/json",
    }
    payload = {
        "model": model,
        "query": query,
        "documents": [c["content"] for c in candidates],
        "top_n": len(candidates)
    }

    start_time = time.perf_counter()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=20.0)
            elapsed = (time.perf_counter() - start_time) * 1000
            if response.status_code == 200:
                results = response.json().get("results", [])
                reranked = [None] * len(candidates)
                for item in results:
                    idx = item["index"]
                    candidate = candidates[idx].copy()
                    candidate["rerank_score"] = item["relevance_score"]
                    reranked[item["index"]] = candidate
                # Sort by score descending
                reranked = [c for c in reranked if c is not None]
                reranked.sort(key=lambda x: x.get("rerank_score", 0.0), reverse=True)
                return reranked, elapsed
            else:
                print(f"❌ Cohere API v2 returned status {response.status_code}: {response.text}")
                return None, 0.0
    except Exception as e:
        print(f"❌ Cohere API v2 call failed: {e}")
        return None, 0.0


def normalize_whitespace(text: str) -> str:
    return " ".join(text.lower().split())


async def run_test_suite(case_num, title, query, candidates, expected_snippet):
    print(f"\n======================================================================")
    print(f"📝 CASE {case_num}: {title}")
    print(f"💬 Query: \"{query}\"")
    print(f"======================================================================")
    
    if not candidates:
        print("❌ Candidate list is empty!")
        return None
    
    # Lấy tối đa 20 ứng viên
    subset = candidates[:20]
    
    # 1. Đo lường Cohere Rerank
    cohere_res, cohere_time = await cohere_rerank(query, subset)
    
    # 2. Giả định Baseline (Không Rerank - Giữ nguyên thứ tự thô của tập subset)
    baseline_res = subset.copy()
    
    # Tìm thứ hạng của chunk mong muốn sau khi chuẩn hóa khoảng trắng
    cohere_exp_rank = "N/A"
    baseline_exp_rank = "N/A"
    
    expected_norm = normalize_whitespace(expected_snippet)
    
    if cohere_res:
        for idx, c in enumerate(cohere_res):
            if expected_norm in normalize_whitespace(c["content"]):
                cohere_exp_rank = idx + 1
                break
                
    for idx, c in enumerate(baseline_res):
        if expected_norm in normalize_whitespace(c["content"]):
            baseline_exp_rank = idx + 1
            break
                
    print(f"🎯 Expected Target Rank: Cohere Rerank = {cohere_exp_rank} | Baseline (Không Rerank) = {baseline_exp_rank}")
    print(f"🥇 Cohere Top 1 ({cohere_res[0].get('rerank_score', 0.0) if cohere_res else 0.0}): {cohere_res[0].get('content', '').replace('\n', ' ')[:80] if cohere_res else 'N/A'}...")
    
    return {
        "case_num": case_num,
        "title": title,
        "query": query,
        "cohere_time": cohere_time,
        "cohere_rank": cohere_exp_rank,
        "baseline_rank": baseline_exp_rank,
        "cohere_top_score": cohere_res[0].get('rerank_score', 0.0) if cohere_res else 0.0,
        "cohere_top_text": cohere_res[0].get('content', '').replace('\n', ' ')[:100] if cohere_res else 'N/A'
    }


async def main():
    # Nạp danh sách ứng viên từ các tệp dữ liệu thực tế
    outline_candidates = load_outline_candidates()
    chap4_candidates = load_section_candidates(VI_CHAP4_PATH)
    trr_candidates = load_section_candidates(VI_TRR_PATH)
    
    results = []
    
    # Case 1: SLR Methodology Synonym Search (Zero Keyword Overlap)
    results.append(await run_test_suite(
        case_num=1,
        title="SLR Methodology Synonym Search (Zero keyword overlap)",
        query="Quy trình SLR giúp tránh các đánh giá cảm tính cá nhân của người viết như thế nào?",
        candidates=chap4_candidates,
        expected_snippet="giảm thiểu thiên lệch của đánh giá chủ quan"
    ))
    
    # Case 2: Coding capability of Gemini vs GPT-5 on codebase scale (Synonym / context search)
    results.append(await run_test_suite(
        case_num=2,
        title="Gemini vs GPT-5 Codebase scale (Synonym/Context)",
        query="Mô hình nào được đánh giá là hữu dụng hơn khi xử lý toàn bộ kho mã nguồn khổng lồ?",
        candidates=chap4_candidates,
        expected_snippet="phân tích được toàn bộ dự án hay đa tệp tin cùng lúc"
    ))
    
    # Case 3: SWE-bench Benchmark Comparison (Numerical & Metric match)
    results.append(await run_test_suite(
        case_num=3,
        title="SWE-bench Benchmark Comparison (Numerical Match)",
        query="So sánh điểm số của GPT-5 và Gemini 2.5 Pro trên bộ kiểm tra năng lực lập trình phần mềm SWE-bench?",
        candidates=chap4_candidates,
        expected_snippet="SWE-bench Verified (Lập trình)"
    ))

    # Case 4: Imagen vs Nano Banana Image Editing Advantage (Synonym & Feature match)
    results.append(await run_test_suite(
        case_num=4,
        title="Imagen vs Nano Banana Image Editing Advantage",
        query="Hình ảnh được tạo ra từ Imagen và Nano Banana có ưu thế gì trong việc chỉnh sửa?",
        candidates=chap4_candidates,
        expected_snippet="duy trì tính nhất quán của hình ảnh qua các lần chỉnh sửa"
    ))

    # Case 5: Variable Definition in Logic Math (Discrete Math Concept)
    results.append(await run_test_suite(
        case_num=5,
        title="Variable Definition in Logic Math (Discrete Math Concept)",
        query="Phát biểu thế nào là một biến mệnh đề trong logic học?",
        candidates=trr_candidates,
        expected_snippet="ký hiệu cho các biến logic (biến mệnh đề)"
    ))

    # Case 6: Discrete Math Distractor / Non-proposition check
    results.append(await run_test_suite(
        case_num=6,
        title="Discrete Math Distractor / Non-proposition check",
        query="Tại sao phát biểu 'Toán rời rạc là một môn học khó' lại không được coi là một mệnh đề toán học?",
        candidates=trr_candidates,
        expected_snippet="không phải là mệnh đề (toán học) vì tính đúng sai của chúng không xác định"
    ))

    # Case 7: IoT automatic watering system benefits (Balcony context)
    results.append(await run_test_suite(
        case_num=7,
        title="IoT Automatic watering system benefits (Balcony context)",
        query="Thiết bị tưới nước tự động giúp giải quyết khó khăn gì cho người trồng cây ở thành phố?",
        candidates=outline_candidates,
        expected_snippet="người dùng thường thiếu thời gian chăm sóc cây"
    ))

    # Case 8: IoT Balcony system outline scope limits (Negative search)
    results.append(await run_test_suite(
        case_num=8,
        title="IoT Balcony system outline scope limits (Negative search)",
        query="Tài liệu đề cương này có bao gồm hướng dẫn chi tiết cách lắp ráp linh kiện và viết code hay không?",
        candidates=outline_candidates,
        expected_snippet="Nội dung không đi sâu vào sơ đồ mạch, mã nguồn hoặc lựa chọn linh kiện cụ thể"
    ))

    # Case 9: OpenAI vs Google Privacy Policy & Safety (Detailed Comparison)
    results.append(await run_test_suite(
        case_num=9,
        title="OpenAI vs Google Privacy Policy & Safety (Detailed Comparison)",
        query="Sự khác biệt về triết lý an toàn thông tin và bảo mật dữ liệu giữa OpenAI và Google?",
        candidates=chap4_candidates,
        expected_snippet="OpenAI mặc định lưu trữ nội dung người dùng nhập vào API trong 30 ngày"
    ))

    # Case 10: LLM API cost and billing comparison (Financial comparison)
    results.append(await run_test_suite(
        case_num=10,
        title="LLM API cost and billing comparison (Financial)",
        query="So sánh chi phí sử dụng API và chính sách giá giữa ChatGPT và Gemini cho nhà phát triển?",
        candidates=chap4_candidates,
        expected_snippet="GPT-5 tính phí khoảng $1,25/1M tokens đầu vào"
    ))
    
    # Xuất báo cáo kết quả Markdown mới sạch sẽ
    output_path = os.path.join(SCRIPT_OUTPUTS_DIR, "reranker_metrics_results.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 🏆 Kết Quả Đánh Giá Reranker - Chỉ Sử Dụng Cohere Multilingual Rerank v3.0\n\n")
        f.write("Báo cáo so sánh độ chính xác thu hồi giữa **Cohere Multilingual Rerank API** và **Baseline thô (Không Rerank)** trên 10 trường hợp kiểm thử thực tế bằng tiếng Việt.\n\n")
        
        f.write("## ⏱️ 1. Thống kê Độ trễ API Cohere (Latency)\n\n")
        f.write("| Case | Mô tả kiểm thử | Độ trễ API Cohere v2 |\n")
        f.write("| :--- | :--- | :--- |\n")
        for r in results:
            f.write(f"| Case {r['case_num']} | {r['title']} | {r['cohere_time']:.2f} ms |\n")
        
        f.write("\n## 🎯 2. Độ chính xác xếp hạng (Rank Improvement Evaluation)\n\n")
        f.write("| Case | Truy vấn (Query) | Thứ hạng Cohere | Thứ hạng Baseline | Kết luận cải tiến |\n")
        f.write("| :--- | :--- | :---: | :---: | :--- |\n")
        for r in results:
            if r["cohere_rank"] == "N/A":
                eval_str = "❌ Không tìm thấy chunk"
            elif r["baseline_rank"] == "N/A":
                eval_str = "✅ Cohere tìm được, Baseline mất dấu"
            elif int(r["cohere_rank"]) < int(r["baseline_rank"]):
                eval_str = f"🚀 Tăng hạng: {r['baseline_rank']} ➔ **{r['cohere_rank']}**"
            elif int(r["cohere_rank"]) == int(r["baseline_rank"]):
                eval_str = f"➖ Giữ nguyên hạng: {r['cohere_rank']}"
            else:
                eval_str = f"📉 Giảm hạng: {r['baseline_rank']} ➔ {r['cohere_rank']}"
                
            f.write(f"| Case {r['case_num']} | *\"{r['query']}\"* | **{r['cohere_rank']}** | {r['baseline_rank']} | {eval_str} |\n")
            
        f.write("\n## 🔍 3. Nhật ký kiểm thử chi tiết từng Case (Detailed Case Logs)\n\n")
        for r in results:
            f.write(f"### Case {r['case_num']}: {r['title']}\n")
            f.write(f"* **Query**: *\"{r['query']}\"*\n")
            f.write(f"* **Thứ hạng mong muốn**: Cohere Rerank = **{r['cohere_rank']}** | Baseline = **{r['baseline_rank']}**\n")
            f.write(f"* **Cohere Top 1 (Relevance Score: {r['cohere_top_score']:.4f})**: `{r['cohere_top_text']}`\n\n")
            f.write("---\n\n")
            
    print(f"\n✅ All tests completed successfully. Report written to {output_path}")


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import json
import os
import sys
import time
import uuid
from pathlib import Path

# Thêm root workspace vào sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from openai import AsyncOpenAI
from pydantic import BaseModel, Field, ValidationError

from app.core.config import settings
from app.services.book_summary_service import _normalize_raw_summary_dict, BookSummarySchema
from app.services.llm_service import NormalizedUnitPayload, SYSTEM_PROMPT_REWRITE_FULL, SYSTEM_PROMPT_REWRITE_PARETO
from app.services.pareto_planner_service import PARETO_PLANNER_SYSTEM_PROMPT, ParetoPlannerPayload

# Khởi tạo client OpenAI kết nối với Gemini API
client = AsyncOpenAI(
    api_key=settings.GEMINI_API_KEY,
    base_url=settings.GEMINI_BASE_URL,
    timeout=120.0
)

# Nạp dữ liệu ai_sum.json
AI_SUM_FILE = Path(__file__).resolve().parent.parent / "logs" / "sumary_ai" / "ai_sum.json"

def load_ai_sum_data():
    with open(AI_SUM_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Helper đánh giá chất lượng tiếng Việt nói và định dạng plain text
def evaluate_tts_script_quality(scripts: list[str], review_script: str) -> dict:
    violations = []
    markdown_symbols = ["#", "**", "*", "```", "---", "##", "###", "[", "]"]
    
    all_text = " ".join(scripts) + " " + review_script
    for sym in markdown_symbols:
        if sym in all_text:
            violations.append(f"Ký tự Markdown cấm: '{sym}'")
            
    # Kiểm tra độ dài câu nói
    avg_paragraph_len = sum(len(s) for s in scripts) / max(1, len(scripts))
    
    return {
        "valid_plain_text": len(violations) == 0,
        "violations": violations,
        "script_paragraph_count": len(scripts),
        "avg_paragraph_chars": round(avg_paragraph_len, 1),
        "review_words": len(review_script.split()),
    }

# ---------------------------------------------------------------------------
# 1. BENCHMARK PARETO PLANNER (gemini-2.5-flash vs gemini-3.6-flash)
# ---------------------------------------------------------------------------
async def benchmark_pareto_planner(chunks_data: list[dict], model_name: str) -> dict:
    # Xây dựng mock SectionCards từ ai_sum.json
    section_cards = []
    seen_sections = set()
    
    for c in chunks_data[:10]:
        sec_id = c.get("section_id", str(uuid.uuid4()))
        if sec_id in seen_sections:
            continue
        seen_sections.add(sec_id)
        
        text = c.get("content", "")
        section_cards.append({
            "id": str(sec_id),
            "title": f"Chapter Section {c.get('section_index', 0)}",
            "path": f"/section/{c.get('section_index', 0)}",
            "level": 1,
            "parent_path": None,
            "estimated_tokens": int(len(text.split()) * 1.3),
            "child_count": 0,
            "signal_hints": ["core_concept", "foundational_definition"],
            "excerpt": text[:200].replace("\n", " "),
        })

    user_payload = {
        "mode": "pareto",
        "target_coverage_ratio": 0.3,
        "target_tokens": 1500,
        "min_units": 2,
        "max_units": 5,
        "section_cards": section_cards,
    }

    start_t = time.perf_counter()
    status = "SUCCESS"
    parsed_result = None
    error_msg = None

    try:
        response = await client.beta.chat.completions.parse(
            model=model_name,
            messages=[
                {"role": "system", "content": PARETO_PLANNER_SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
            ],
            temperature=0.1,
            response_format=ParetoPlannerPayload,
        )
        parsed_result = response.choices[0].message.parsed.model_dump()
    except Exception as e:
        status = "FAILED"
        error_msg = str(e)

    elapsed = time.perf_counter() - start_t

    # Đánh giá chất lượng
    quality_score = 0
    quality_notes = []
    if status == "SUCCESS" and parsed_result:
        quality_score += 2  # Schema valid
        units = parsed_result.get("units", [])
        if 2 <= len(units) <= 5:
            quality_score += 1.5
            quality_notes.append(f"Tạo đúng {len(units)} units theo yêu cầu (2-5).")
        else:
            quality_notes.append(f"Số lượng units {len(units)} ngoài khoảng dự kiến.")
            
        valid_ids = True
        for u in units:
            if not u.get("source_section_ids") or not u.get("planner_reason"):
                valid_ids = False
        if valid_ids:
            quality_score += 1.5
            quality_notes.append("Các field source_section_ids và planner_reason đầy đủ.")
    else:
        quality_notes.append(f"Lỗi: {error_msg}")

    return {
        "task": "pareto_learning_planner",
        "model": model_name,
        "status": status,
        "elapsed_seconds": round(elapsed, 3),
        "quality_score_out_of_5": quality_score,
        "quality_notes": quality_notes,
        "output_data": parsed_result,
        "error": error_msg,
    }


# ---------------------------------------------------------------------------
# 2. BENCHMARK EXECUTIVE BOOK SUMMARY (gemini-2.5-flash vs gemini-3.5-flash-lite)
# ---------------------------------------------------------------------------
async def benchmark_book_summary(chunks_data: list[dict], model_name: str) -> dict:
    # Tổng hợp toàn bộ văn bản từ chunks
    full_text = "\n\n".join([c.get("content", "") for c in chunks_data[:8]])
    word_count = len(full_text.split())

    prompt_messages = [
        {
            "role": "system",
            "content": (
                "You are an expert literary analyst and executive book summarizer.\n"
                "Your task is to read the provided text of the book and extract a structured executive summary in raw JSON format.\n\n"
                "REQUIRED JSON SCHEMA:\n"
                "Your JSON output MUST contain EXACTLY these keys:\n"
                "{\n"
                '  "key_idea": "String - Main core idea/message of the book in 2-3 sentences.",\n'
                '  "target_audience": "String - Intended target audience (e.g. Độc giả yêu thích...)",\n'
                '  "estimated_read_minutes": Integer - Estimated reading time in minutes (e.g. 180),\n'
                '  "key_takeaways": ["String", "String"] - List of 5-7 key takeaways or main reviews,\n'
                '  "summary": "String - Comprehensive summary of the book plot/content.",\n'
                '  "main_characters": ["String", "String"] - List of main character names as strings (e.g. ["George Milton: Anh nông dân nhân hậu", "Lennie Small: Người bạn trung thành"])\n'
                "}\n\n"
                "CRITICAL GROUNDING CONSTRAINTS:\n"
                "1. Base your summary STRICTLY AND EXCLUSIVELY on the provided book text.\n"
                "2. DO NOT hallucinate, infer, or fabricate any details, facts, plot points, or character traits not explicitly mentioned in the text.\n"
                "3. If any field cannot be explicitly determined from the text, set its string value to 'Chưa có thông tin' (or an empty array [] for list fields).\n"
                "4. Write all string values in fluent, natural Vietnamese for direct display on the mobile app UI.\n"
                "5. Output ONLY valid raw JSON matching the required schema without Markdown code blocks."
            ),
        },
        {"role": "user", "content": f"Here is the complete content of the book:\n\n{full_text}\n\nProvide the executive summary in valid JSON format matching the schema."},
    ]

    start_t = time.perf_counter()
    status = "SUCCESS"
    validated_summary = None
    error_msg = None

    try:
        completion = await client.chat.completions.create(
            model=model_name,
            messages=prompt_messages,
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        raw_output = completion.choices[0].message.content.strip()
        if raw_output.startswith("```"):
            raw_output = raw_output.strip("`").strip()
            if raw_output.lower().startswith("json"):
                raw_output = raw_output[4:].strip()
                
        raw_dict = json.loads(raw_output)
        normalized_dict = _normalize_raw_summary_dict(raw_dict, word_count)
        validated_summary = BookSummarySchema.model_validate(normalized_dict).model_dump()
    except Exception as e:
        status = "FAILED"
        error_msg = str(e)

    elapsed = time.perf_counter() - start_t

    # Đánh giá chất lượng
    quality_score = 0
    quality_notes = []
    if status == "SUCCESS" and validated_summary:
        quality_score += 2.0  # Pydantic valid
        if validated_summary.get("key_idea") and len(validated_summary.get("key_idea")) > 20:
            quality_score += 1.0
            quality_notes.append("Trích xuất key_idea súc tích và có ý nghĩa.")
        if len(validated_summary.get("key_takeaways", [])) >= 3:
            quality_score += 1.0
            quality_notes.append(f"Tạo được {len(validated_summary.get('key_takeaways'))} key takeaways.")
        if len(validated_summary.get("main_characters", [])) >= 2:
            quality_score += 1.0
            quality_notes.append(f"Trích xuất {len(validated_summary.get('main_characters'))} nhân vật chính chuẩn xác.")
    else:
        quality_notes.append(f"Lỗi: {error_msg}")

    return {
        "task": "executive_book_summary",
        "model": model_name,
        "status": status,
        "elapsed_seconds": round(elapsed, 3),
        "quality_score_out_of_5": quality_score,
        "quality_notes": quality_notes,
        "output_data": validated_summary,
        "error": error_msg,
    }


# ---------------------------------------------------------------------------
# 3. BENCHMARK LLM TTS REWRITE (gemini-2.5-flash vs gemini-3.5-flash-lite)
# ---------------------------------------------------------------------------
async def benchmark_tts_rewrite(chunks_data: list[dict], model_name: str, mode: str) -> dict:
    sample_text = "\n\n".join([c.get("content", "") for c in chunks_data[:2]])
    system_prompt = SYSTEM_PROMPT_REWRITE_PARETO if mode.upper() == "PARETO" else SYSTEM_PROMPT_REWRITE_FULL

    start_t = time.perf_counter()
    status = "SUCCESS"
    validated_unit = None
    error_msg = None
    tts_eval = {}

    try:
        response = await client.beta.chat.completions.parse(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Textbook content to rewrite for spoken audio:\n\n{sample_text}"},
            ],
            temperature=0.2,
            response_format=NormalizedUnitPayload,
        )
        parsed = response.choices[0].message.parsed
        validated_unit = parsed.model_dump()
        tts_eval = evaluate_tts_script_quality(parsed.main_scripts, parsed.review_script)
    except Exception as e:
        status = "FAILED"
        error_msg = str(e)

    elapsed = time.perf_counter() - start_t

    # Đánh giá chất lượng
    quality_score = 0
    quality_notes = []
    if status == "SUCCESS" and validated_unit:
        quality_score += 2.0  # JSON / Pydantic valid
        if tts_eval.get("valid_plain_text"):
            quality_score += 1.5
            quality_notes.append("Không vi phạm các ký tự Markdown/Ký hiệu đọc kém.")
        else:
            quality_notes.append(f"Vi phạm ký hiệu: {tts_eval.get('violations')}")

        if len(validated_unit.get("main_scripts", [])) >= 1:
            quality_score += 1.5
            quality_notes.append(f"Tạo thành công {len(validated_unit.get('main_scripts'))} đoạn kịch bản nói ({tts_eval.get('avg_paragraph_chars')} chars/đoạn).")
    else:
        quality_notes.append(f"Lỗi: {error_msg}")

    return {
        "task": f"tts_script_rewrite_{mode.lower()}",
        "model": model_name,
        "status": status,
        "elapsed_seconds": round(elapsed, 3),
        "quality_score_out_of_5": quality_score,
        "quality_notes": quality_notes,
        "tts_evaluation": tts_eval,
        "output_data": validated_unit,
        "error": error_msg,
    }


# ---------------------------------------------------------------------------
# MAIN RUNNER & REPORT GENERATOR
# ---------------------------------------------------------------------------
async def run_all_benchmarks():
    print("🚀 BẮT ĐẦU CHẠY BENCHMARK ĐÁNH GIÁ MÔ HÌNH GEMINI... (Data: ai_sum.json)\n", flush=True)
    chunks = load_ai_sum_data()
    
    results = []

    # 1. Pareto Planner: Baseline gemini-2.5-flash vs Upgrade gemini-3.6-flash
    print("1/4. Đang kiểm thử Pareto Learning Unit Planner...", flush=True)
    r1_base = await benchmark_pareto_planner(chunks, "gemini-2.5-flash")
    print(f"   [DONE] gemini-2.5-flash ({r1_base['elapsed_seconds']}s)", flush=True)
    r1_upg = await benchmark_pareto_planner(chunks, "gemini-3.6-flash")
    print(f"   [DONE] gemini-3.6-flash ({r1_upg['elapsed_seconds']}s)", flush=True)
    results.extend([r1_base, r1_upg])

    # 2. Executive Summary: Baseline gemini-2.5-flash vs Upgrade gemini-3.5-flash-lite
    print("2/4. Đang kiểm thử Executive Book Summary...", flush=True)
    r2_base = await benchmark_book_summary(chunks, "gemini-2.5-flash")
    print(f"   [DONE] gemini-2.5-flash ({r2_base['elapsed_seconds']}s)", flush=True)
    r2_upg = await benchmark_book_summary(chunks, "gemini-3.5-flash-lite")
    print(f"   [DONE] gemini-3.5-flash-lite ({r2_upg['elapsed_seconds']}s)", flush=True)
    results.extend([r2_base, r2_upg])

    # 3. TTS Rewrite Full Mode: Baseline gemini-2.5-flash vs Upgrade gemini-3.5-flash-lite
    print("3/4. Đang kiểm thử TTS Rewrite (Full Mode)...", flush=True)
    r3_base = await benchmark_tts_rewrite(chunks, "gemini-2.5-flash", "FULL")
    print(f"   [DONE] gemini-2.5-flash ({r3_base['elapsed_seconds']}s)", flush=True)
    r3_upg = await benchmark_tts_rewrite(chunks, "gemini-3.5-flash-lite", "FULL")
    print(f"   [DONE] gemini-3.5-flash-lite ({r3_upg['elapsed_seconds']}s)", flush=True)
    results.extend([r3_base, r3_upg])

    # 4. TTS Rewrite Pareto Mode: Baseline gemini-2.5-flash vs Upgrade gemini-3.5-flash-lite
    print("4/4. Đang kiểm thử TTS Rewrite (Pareto Mode)...", flush=True)
    r4_base = await benchmark_tts_rewrite(chunks, "gemini-2.5-flash", "PARETO")
    print(f"   [DONE] gemini-2.5-flash ({r4_base['elapsed_seconds']}s)", flush=True)
    r4_upg = await benchmark_tts_rewrite(chunks, "gemini-3.5-flash-lite", "PARETO")
    print(f"   [DONE] gemini-3.5-flash-lite ({r4_upg['elapsed_seconds']}s)", flush=True)
    results.extend([r4_base, r4_upg])

    # Lưu log chi tiết JSON
    log_dir = Path(__file__).resolve().parent.parent / "logs" / "model_benchmark"
    log_dir.mkdir(parents=True, exist_ok=True)
    json_log_path = log_dir / "gemini_model_upgrade_benchmark.json"
    
    with open(json_log_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Đã hoàn thành Benchmark! Đã ghi log chi tiết vào: {json_log_path}\n", flush=True)

    # In bảng tổng hợp kết quả lên Console
    print("=" * 85, flush=True)
    print(f"{'TASK':<30} | {'MODEL':<22} | {'TIME (s)':<9} | {'SCORE':<5} | {'STATUS'}", flush=True)
    print("=" * 85, flush=True)
    for r in results:
        print(f"{r['task']:<30} | {r['model']:<22} | {r['elapsed_seconds']:<9} | {r['quality_score_out_of_5']:<5} | {r['status']}", flush=True)
    print("=" * 85, flush=True)

if __name__ == "__main__":
    asyncio.run(run_all_benchmarks())

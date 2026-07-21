import asyncio
import json
import os
import time
import sys

# Tự động nạp đường dẫn gốc dự án vào sys.path để chạy trực tiếp không bị lỗi ModuleNotFoundError
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List
from pydantic import BaseModel, Field
from openai import AsyncOpenAI

# 1. Import cài đặt từ hệ thống TRIAM Backend
from app.core.config import settings

# Structured Output Schema cho FE UI
class BookAiSummarySchema(BaseModel):
    key_idea: str = Field(description="Ý tưởng chính tổng quan nhất của toàn bộ cuốn sách (2-3 câu ngắn gọn).")
    target_audience: str = Field(description="Đối tượng độc giả phù hợp nhất để đọc cuốn sách này.")
    key_takeaways: List[str] = Field(description="Danh sách 5 đến 7 bài học / điểm cốt lõi đắt giá nhất xuyên suốt từ đầu tới cuối sách.")
    estimated_read_minutes: int = Field(description="Thời gian đọc ước tính (phút).")

async def test_full_book_summarization():
    ai_sum_path = os.path.join(os.getcwd(), "ai_sum.json")
    print(f"📖 1. Đang đọc tệp nội dung sách: {ai_sum_path}...")
    
    with open(ai_sum_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        
    print(f"  -> Tổng số chunks tìm thấy: {len(chunks)}")
    
    # Sắp xếp chunks theo section_index và chunk_index
    chunks.sort(key=lambda x: (x.get("section_index", 0), x.get("chunk_index", 0)))
    
    # Ghép toàn bộ nội dung sách thành 1 chuỗi text duy nhất
    full_text_list = []
    for c in chunks:
        content = c.get("content", "").strip()
        if content:
            full_text_list.append(content)
            
    full_book_text = "\n\n".join(full_text_list)
    char_count = len(full_book_text)
    word_count = len(full_book_text.split())
    estimated_tokens = int(word_count * 1.3)
    
    print(f"📊 2. Thống kê độ dài cuốn sách:")
    print(f"  -> Tổng ký tự (chars): {char_count:,}")
    print(f"  -> Tổng số từ (words): {word_count:,}")
    print(f"  -> Ước tính Tokens: ~{estimated_tokens:,} tokens")
    
    # 3. Khởi tạo Gemini OpenAI-compatible Client từ settings
    client = AsyncOpenAI(
        api_key=settings.GEMINI_API_KEY,
        base_url=settings.GEMINI_BASE_URL,
        timeout=120.0
    )
    
    selected_model = settings.GEMINI_MODEL_LLM or "gemini-2.5-flash"
            
    print(f"\n⚡ 3. Đang gửi 1 Prompt duy nhất ({estimated_tokens:,} tokens) tới Model: [{selected_model}]...")
    
    prompt_messages = [
        {
            "role": "system",
            "content": (
                "You are an expert literary analyst and executive book summarizer.\n"
                "Your task is to read the provided text of the book and extract a structured executive summary in raw JSON format.\n\n"
                "CRITICAL GROUNDING CONSTRAINTS:\n"
                "1. Base your summary STRICTLY AND EXCLUSIVELY on the provided book text.\n"
                "2. DO NOT hallucinate, infer, or fabricate any details, facts, plot points, or character traits not explicitly mentioned in the text.\n"
                "3. If any field cannot be explicitly determined from the text, set its string value to 'Chưa có thông tin' (or an empty array [] for list fields).\n"
                "4. Write the summary values in fluent, natural Vietnamese for direct display on the mobile app UI.\n"
                "5. Output ONLY valid raw JSON matching the required schema without Markdown code blocks."
            ),
        },
        {
            "role": "user",
            "content": f"Here is the complete content of the book:\n\n{full_book_text}\n\nProvide the executive summary in valid JSON format."
        }
    ]
    
    start_time = time.perf_counter()
    error_occurred = False
    response_json = None
    
    try:
        completion = await client.chat.completions.create(
            model=selected_model,
            messages=prompt_messages,
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        end_time = time.perf_counter()
        elapsed_seconds = end_time - start_time
        
        raw_output = completion.choices[0].message.content
        print(f"\n✅ 4. Gửi request THÀNH CÔNG!")
        print(f"⏱️  Thời gian phản hồi thực tế: {elapsed_seconds:.2f} giây")
        
        if completion.usage:
            print(f"📈 Prompt Tokens: {completion.usage.prompt_tokens:,}")
            print(f"📉 Completion Tokens: {completion.usage.completion_tokens:,}")
            print(f"📊 Total Tokens: {completion.usage.total_tokens:,}")
            
        print("\n🔍 5. Kiểm tra chất lượng dữ liệu phản hồi (JSON Output):")
        try:
            response_json = json.loads(raw_output)
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
            
            # Ghi ra file gemini_summary_result.json trong dự án
            with open("gemini_summary_result.json", "w", encoding="utf-8") as rf:
                json.dump(response_json, rf, indent=2, ensure_ascii=False)
        except Exception as pe:
            print(f"⚠️ Không parse được JSON trực tiếp: {pe}\nRaw output:\n{raw_output}")
            
    except Exception as exc:
        end_time = time.perf_counter()
        elapsed_seconds = end_time - start_time
        error_occurred = True
        print(f"\n❌ 4. Thất bại / Lỗi nạp Context: {exc}")
        print(f"⏱️ Thời gian trước khi báo lỗi: {elapsed_seconds:.2f} giây")

if __name__ == "__main__":
    asyncio.run(test_full_book_summarization())

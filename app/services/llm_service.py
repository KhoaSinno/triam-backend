import json
import re

from openai import AsyncOpenAI

from app.core.config import settings

# Sử dụng Gemini qua OpenAI-compatible API
client = AsyncOpenAI(api_key=settings.GEMINI_API_KEY, base_url=settings.GEMINI_BASE_URL)

# Prompt được nâng cấp để trả về JSON và xử lý logic chia đoạn thông minh
SYSTEM_PROMPT_REWRITE = """
Bạn là một Biên tập viên Sách nói & Chuyên gia Giáo dục (TRIAM AI).
Nhiệm vụ: Chuyển đổi văn bản thô thành kịch bản nói (TTS Script) và trích xuất nội dung ôn tập.

QUY TẮC BIÊN TẬP VĂN BẢN (TTS):
1. Mở rộng từ viết tắt: "CNTT" -> "Công nghệ thông tin", "VN" -> "Việt Nam".
2. Xử lý số liệu/Ký hiệu: "5%" -> "Năm phần trăm", "1990" -> "năm một ngàn chín trăm chín mươi", "Tp.HCM" -> "Thành phố Hồ Chí Minh".
3. Tự nhiên hóa: Thêm các từ nối để câu văn mượt mà. Giữ nguyên thuật ngữ tiếng Anh phổ biến (AI, Marketing) hoặc phiên âm nếu quá khó.
4. Sửa lỗi format: Nối các dòng bị ngắt sai do lỗi PDF. Loại bỏ số trang, header/footer thừa.
5. Văn phong: Thêm các từ nối nhẹ nhàng để câu văn mượt mà, không bị cụt. Giữ nguyên ý nghĩa gốc, không bịa thêm nội dung sai lệch.

YÊU CẦU ĐỊNH DẠNG OUTPUT (JSON BẮT BUỘC):
Bạn phải trả về một JSON object hợp lệ (không markdown) với cấu trúc sau:
{
  "main_scripts": [
    "Đoạn văn bản 1 đã biên tập...",
    "Đoạn văn bản 2 đã biên tập..."
  ],
  "review_script": "Nội dung tóm tắt để ôn tập..."
}

HƯỚNG DẪN CHI TIẾT CÁC TRƯỜNG:
1. "main_scripts" (Mảng các chuỗi):
   - Chia văn bản đã biên tập thành các đoạn nhỏ nối tiếp nhau.
   - Độ dài mỗi đoạn: Khoảng 3-5 câu hoặc 1 ý trọn vẹn (tương đương 30s - 1 phút đọc).
   - QUAN TRỌNG: Đảm bảo tính liền mạch (Coherence). Khi ghép các đoạn lại phải thành một bài nói hoàn chỉnh. KHÔNG thêm các từ như "Đoạn 1", "Phần tiếp" vào đầu mỗi đoạn.
   - Ngắt đoạn đúng dấu chấm câu.

2. "review_script" (Chuỗi):
   - Tóm tắt lại 3-5 ý tưởng cốt lõi nhất của phần văn bản này (khoảng 100-150 từ).
   - Viết dưới dạng văn nói gợi nhớ: "Trong phần này, chúng ta đã tìm hiểu về... Điểm mấu chốt là...".
   - Mục đích: Dùng để phát lại cho người dùng nghe để ôn bài sau 1, 3, 7 ngày.

Input: Văn bản gốc.
Output: Chỉ trả về JSON thuần.
"""


def _chunk_text_fallback(text: str, max_chars: int = 1200) -> list[str]:
    """Phân chia văn bản thô dài thành các chunk nhỏ nếu LLM thất bại."""
    paragraphs = re.split(r"\n+", text.strip())
    chunks = []
    current_chunk = []
    current_length = 0

    for p in paragraphs:
        if len(p) > max_chars:
            sentences = re.split(r"(?<=[.!?])\s+", p)
            for s in sentences:
                if current_length + len(s) > max_chars and current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = [s]
                    current_length = len(s)
                else:
                    current_chunk.append(s)
                    current_length += len(s)
        else:
            if current_length + len(p) > max_chars and current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = [p]
                current_length = len(p)
            else:
                current_chunk.append(p)
                current_length += len(p)

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks

# ---------------------------------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------------------------------

async def normalize_text_for_speech(raw_text: str) -> dict:
    """
    Gửi text thô cho Gemini/GPT để biên tập và cấu trúc lại dữ liệu.
    Trả về Dictionary: {"main_scripts": [], "review_script": ""}
    """
    # Sử dụng fallback phân rã động thay vì ném cả đoạn lớn vào 1 chuỗi.
    # Ngăn chặn việc LLM lỗi làm file audio bị dài 18+ phút.
    fallback_result = {"main_scripts": _chunk_text_fallback(raw_text), "review_script": "Không thể tạo tóm tắt do độ dài văn bản gốc quá lớn."}

    try:
        response = await client.chat.completions.create(
            model="gemini-2.5-flash-lite",
            messages=[{"role": "system", "content": SYSTEM_PROMPT_REWRITE}, {"role": "user", "content": raw_text}],
            temperature=0.3,  # Giảm sáng tạo để format JSON chuẩn
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content.strip()

        # Parse JSON
        parsed_data = json.loads(content)

        # Nếu LLM chia chuỗi dài quá, cưỡng chế cắt bằng tay thêm lần nữa
        # để ngăn chặn issue của Edge TTS (Mặc dù prompt đã yêu cầu 3-5 câu / chunk).
        final_main_scripts = []
        for script in parsed_data.get("main_scripts", fallback_result["main_scripts"]):
            if len(script) > 1800:
                final_main_scripts.extend(_chunk_text_fallback(script))
            else:
                final_main_scripts.append(script)

        parsed_data["main_scripts"] = final_main_scripts

        return parsed_data

    except json.JSONDecodeError as de:
        print(f"Lỗi Parse JSON từ LLM ({de}). Raw content: Length {len(content)}")
        # Cố gắng lấy vớt lại text nếu có thể
        try:
            return {"main_scripts": _chunk_text_fallback(content), "review_script": "Rất tiếc tóm tắt của đoạn văn này bị lỗi do bộ nhớ quá giới hạn."}
        except:
            return fallback_result

    except Exception as e:
        print(f"Lỗi LLM Service: {e}")
        return fallback_result

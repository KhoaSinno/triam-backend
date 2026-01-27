from openai import AsyncOpenAI
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

# Prompt "thần thánh" để định hình phong cách đọc
SYSTEM_PROMPT = """
Bạn là một biên tập viên phát thanh chuyên nghiệp (Script Editor).
Nhiệm vụ: Chuyển đổi văn bản thô thành kịch bản nói (Spoken Script) để người đọc tin (AI TTS) đọc tự nhiên nhất.

QUY TẮC BẮT BUỘC:
1. Mở rộng từ viết tắt: Dựa vào ngữ cảnh, hãy viết đầy đủ các từ viết tắt.
   - Ví dụ: "CNTT" -> "Công nghệ thông tin", "DN" -> "Doanh nghiệp", "NS" -> "Nhân sự".
2. Xử lý Tiếng Anh/Thuật ngữ:
   - Các từ tiếng Anh phổ biến (AI, CEO, Marketing) -> Giữ nguyên (nếu bộ đọc tốt) hoặc chú thích phiên âm nếu cần.
   - Ví dụ đặc biệt: "AI" -> "Ây Ai", "Agile" -> "A-chao".
3. Số liệu & Ký hiệu:
   - "5%" -> "Năm phần trăm".
   - "Tp.HCM" -> "Thành phố Hồ Chí Minh".
4. Văn phong: Thêm các từ nối nhẹ nhàng để câu văn mượt mà, không bị cụt. Giữ nguyên ý nghĩa gốc, không bịa thêm nội dung sai lệch.

Input: Văn bản gốc từ sách.
Output: Chỉ trả về văn bản đã biên tập, không thêm lời chào hay giải thích gì khác.
"""

async def normalize_text_for_speech(raw_text: str) -> str:
    """
    Gửi text thô cho GPT-4o-mini biên tập lại trước khi đọc.
    Dùng model 'gpt-4o-mini' cho rẻ và nhanh (Latency thấp).
    """
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": raw_text}
            ],
            temperature=0.3,  # Giữ cho AI tập trung, ít sáng tạo lung tung
            max_tokens=2000   # Giới hạn output
        )
        normalized_text = response.choices[0].message.content
        return normalized_text
    except Exception as e:
        print(f"Lỗi Normalization: {e}")
        return raw_text  # Fallback: Nếu lỗi thì trả về text gốc đọc tạm

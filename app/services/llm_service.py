import json

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

async def normalize_text_for_speech(raw_text: str) -> dict:
    """
    Gửi text thô cho Gemini/GPT để biên tập và cấu trúc lại dữ liệu.
    Trả về Dictionary: {"main_scripts": [], "review_script": ""}
    """
    # Fallback structure nếu AI lỗi
    fallback_result = {
        "main_scripts": [raw_text],
        "review_script": "Không thể tạo tóm tắt cho đoạn này."
    }

    try:
        response = await client.chat.completions.create(
            # model="gpt-4o-mini",
            model="gemini-2.5-flash-lite", # Model này input token lớn, rẻ
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_REWRITE},
                {"role": "user", "content": raw_text}
            ],
            temperature=0.3, # Giảm sáng tạo để format JSON chuẩn
            response_format={"type": "json_object"}

        )

        content = response.choices[0].message.content.strip()

        # Xử lý trường hợp AI trả về markdown ```json ... ```
      #   if content.startswith("```json"):
      #       content = content.replace("```json", "").replace("```", "")
      #   elif content.startswith("```"):
      #       content = content.replace("```", "")

        # Parse JSON
        parsed_data = json.loads(content)

        # Validate sơ bộ
      #   if "main_scripts" not in parsed_data or not isinstance(parsed_data["main_scripts"], list):
      #       print("Cảnh báo: Output thiếu main_scripts hoặc sai định dạng.")
      #       return fallback_result

        return parsed_data

    except json.JSONDecodeError:
        print(f"Lỗi Parse JSON từ LLM. Raw content: {content[:100]}...")
        # Trường hợp này có thể fallback bằng cách trả về raw text vào main_scripts
        return {
            "main_scripts": [content], # Cố gắng lấy nội dung dù không đúng format
            "review_script": "Lỗi định dạng tóm tắt."
        }
    except Exception as e:
        print(f"Lỗi LLM Service: {e}")
        return fallback_result

# /////////////// code V1 ///////////////

# from openai import AsyncOpenAI
# from app.core.config import settings

# # client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
# client = AsyncOpenAI(api_key=settings.GEMINI_API_KEY, base_url=settings.GEMINI_BASE_URL)

# # Prompt "thần thánh" để định hình phong cách đọc
# SYSTEM_PROMPT_REWRITE = """
# Bạn là một biên tập viên phát thanh chuyên nghiệp (Script Editor).
# Nhiệm vụ: Chuyển đổi văn bản thô thành kịch bản nói (Spoken Script) để AI TTS đọc tự nhiên nhất.

# QUY TẮC BẮT BUỘC:
# 1. Mở rộng từ viết tắt: Dựa vào ngữ cảnh, hãy viết đầy đủ các từ viết tắt.
#    - Ví dụ: "CNTT" -> "Công nghệ thông tin", "DN" -> "Doanh nghiệp", "NS" -> "Nhân sự".
# 2. Xử lý Tiếng Anh/Thuật ngữ:
#    - Các từ tiếng Anh phổ biến (AI, CEO, Marketing) -> Giữ nguyên (nếu bộ đọc tốt) hoặc chú thích phiên âm nếu cần.
#    - Ví dụ đặc biệt: "AI" -> "Ây Ai", "Agile" -> "A-chao".
# 3. Số liệu & Ký hiệu:
#    - "5%" -> "Năm phần trăm".
#    - "Tp.HCM" -> "Thành phố Hồ Chí Minh".
# 4. Xử lý lỗi PDF & Format (Quan trọng nhất):
#    - Nối các dòng bị ngắt quãng giữa chừng do lỗi PDF (line break).
#    - Loại bỏ số trang (ví dụ số "10", "11" nằm trơ trọi cuối đoạn).
#    - Xóa các ký tự rác do lỗi font (ví dụ: "J", "", các dấu gạch ngang vô nghĩa).
#    - Tự động sửa lỗi chính tả hiển nhiên (ví dụ: "Qcmenia" -> "Armenia").
# 5. Tự nhiên hóa số liệu & Thời gian (Văn nói người Việt):
#    - "1,5 giờ" -> Chuyển thành "một tiếng rưỡi" (KHÔNG dùng "một phẩy năm giờ").
#    - "0.5" -> "nửa" hoặc "không phẩy năm" tùy ngữ cảnh.
#    - "30km" -> "ba mươi ki-lô-mét".
#    - "1990" -> "năm một ngàn chín trăm chín mươi".
#    - Danh sách "1. 2. 3." -> Chuyển thành "Điều thứ nhất: ... Điều thứ hai: ... Điều thứ ba: ..." (để tạo nhịp điệu).

# 6. Văn phong: Thêm các từ nối nhẹ nhàng để câu văn mượt mà, không bị cụt. Giữ nguyên ý nghĩa gốc, không bịa thêm nội dung sai lệch.

# Input: Văn bản gốc từ sách.
# Output: Chỉ trả về văn bản đã biên tập, không thêm lời chào hay giải thích gì khác.
# """

# async def normalize_text_for_speech(raw_text: str) -> str:
#     """
#     Gửi text thô cho GPT-4o-mini biên tập lại trước khi đọc.
#     Dùng model 'gpt-4o-mini' cho rẻ và nhanh (Latency thấp).
#     """
#     try:
#         response = await client.chat.completions.create(
#             # model="gpt-4o-mini",
#             model="gemini-2.5-flash-lite",
#             messages=[
#                 {"role": "system", "content": SYSTEM_PROMPT_REWRITE},
#                 {"role": "user", "content": raw_text}
#             ],
#             temperature=0.3,  # Giữ cho AI tập trung, ít sáng tạo lung tung
#             # max_tokens=2000   # Giới hạn output
#         )
#         normalized_text = response.choices[0].message.content
#         return normalized_text
#     except Exception as e:
#         print(f"Lỗi Normalization: {e}")
#         return raw_text  # Fallback: Nếu lỗi thì trả về text gốc đọc tạm

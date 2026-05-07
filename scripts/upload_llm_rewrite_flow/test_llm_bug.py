import asyncio
from app.services.llm_service import normalize_text_for_speech

text = """
Để có khuyến nghị cụ thể hơn cho từng ngành nghề khi ứng dụng trí tuệ nhân tạo, chúng ta cần nghiên cứu theo chiều dọc và tuân thủ quy định chuyên ngành.
Một hướng nghiên cứu quan trọng khác là phân tích hiệu quả chi phí và trải nghiệm người dùng khi triển khai các mô hình trí tuệ nhân tạo. Ví dụ, chúng ta cần xem xét mô hình nào tiết kiệm chi phí điện toán hơn cho cùng một khối lượng công việc, hoặc khảo sát mức độ hài lòng của người dùng cuối khi tương tác với các mô hình như ChatGPT và Gemini, đánh giá về tốc độ, sự mượt mà và chất lượng câu trả lời.
Những dữ liệu định tính này sẽ bổ sung cho phân tích định lượng, giúp đưa ra quyết định dựa trên sự tổng hòa giữa hiệu quả, chi phí và trải nghiệm người dùng, chứ không chỉ dựa vào năng lực kỹ thuật.
Cuộc so sánh giữa ChatGPT và Gemini cho thấy sự cân bằng, một chín một mười giữa hai mô hình ngôn ngữ trí tuệ nhân tạo tiên tiến nhất hiện nay. Mỗi mô hình đã khẳng định vị thế ở một số khía cạnh và không ngừng học hỏi điểm mạnh của nhau để hoàn thiện.
Trong tương lai gần, ranh giới giữa ChatGPT và Gemini có thể sẽ còn mờ nhạt hơn nữa do cả hai liên tục cập nhật và đổi mới. Do đó, người dùng và nhà nghiên cứu cần theo dõi sát sao các tiến bộ mới và linh hoạt điều chỉnh lựa chọn công nghệ cho phù hợp.
Những khuyến nghị và phân tích trong nghiên cứu này hy vọng sẽ là cơ sở tham khảo hữu ích, đồng thời mở đường cho các nghiên cứu tiếp nối, hướng tới mục tiêu tối ưu hóa việc ứng dụng các mô hình ngôn ngữ lớn vào thực tiễn một cách hiệu quả, an toàn và kinh tế nhất.
"""

async def main():
    try:
        res = await normalize_text_for_speech(text, "pareto")
        print("Success PARETO!", res)
    except Exception as e:
        print("Error PARETO:", e)

    try:
        res = await normalize_text_for_speech(text, "full")
        print("Success FULL!", res)
    except Exception as e:
        print("Error FULL:", e)

if __name__ == "__main__":
    asyncio.run(main())

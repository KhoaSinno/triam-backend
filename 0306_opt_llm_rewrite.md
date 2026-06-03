# /api/v1/upload

```json
{
  "book_id": "59696335-526a-4905-9d6b-970edbbf1081",
  "total_sections": 3,
  "max_depth": 1,
  "outline_tree": [
    {
      "title": "Chương 4: Phương pháp luận nghiên cứu",
      "level": 1,
      "path": "1",
      "page_start": 1,
      "page_end": 1,
      "text_char_count": 4215,
      "children": []
    },
    {
      "title": "Chương 5: Kết quả phân tích và so sánh",
      "level": 1,
      "path": "2",
      "page_start": 2,
      "page_end": 5,
      "text_char_count": 16439,
      "children": []
    },
    {
      "title": "Chương 6: Bàn luận và Khuyến nghị",
      "level": 1,
      "path": "3",
      "page_start": 6,
      "page_end": 9,
      "text_char_count": 13860,
      "children": []
    }
  ],
  "warnings": [],
  "document_type": "pdf"
}
```

# /api/v1/generate-plan

```json
{
  "message": "Kế hoạch học tập đã được tạo! Chúng tôi đang xử lý sách của bạn.",
  "book_id": "59696335-526a-4905-9d6b-970edbbf1081",
  "plan_id": "48a059ca-fabd-4960-b04f-3edc5ebca1aa",
  "job_id": "5499cf4a-fa49-4304-b42c-d194dd61085f",
  "mode": "pareto",
  "plan_status": "active",
  "pace": 2,
  "schedule_config": [
    "Mon"
  ],
  "reminder_time": "21:00",
  "status": "queued",
  "progress_percent": 0,
  "active_slots": [
    {
      "id": "68af46b2-2075-4eed-96af-bd3f99c009c4",
      "weekday": 0,
      "weekday_label": "monday",
      "reminder_time": "21:00",
      "timezone": "Asia/Ho_Chi_Minh",
      "is_active": true
    }
  ],
  "planned_units": [
    {
      "unit_index": 0,
      "title": "Chương 4: Phương pháp luận nghiên cứu",
      "unit_type": "pareto_core",
      "source_section_count": 1,
      "estimated_audio_seconds": 419
    },
    {
      "unit_index": 1,
      "title": "Chương 5: Kết quả phân tích và so sánh",
      "unit_type": "pareto_core",
      "source_section_count": 1,
      "estimated_audio_seconds": 1617
    }
  ]
}
```

# /api/v1/books/{book_id}/details

```json
{
  "book_id": "59696335-526a-4905-9d6b-970edbbf1081",
  "book_status": "ready",
  "mode": "pareto",
  "total_sections": 3,
  "total_units": 2,
  "units": [
    {
      "id": "c2df3fbf-38f5-4479-a9dd-354fc408f1e1",
      "title": "Chương 4: Phương pháp luận nghiên cứu",
      "status": "ready",
      "unit_index": 0,
      "unit_type": "pareto_core",
      "source_text_char_count": 4215,
      "estimated_audio_seconds": 419,
      "main_segment_count": 5,
      "review_text": "Nghiên cứu này sử dụng phương pháp tổng quan tài liệu có hệ thống (SLR) để thu thập dữ liệu từ các nguồn chính thống như blog của OpenAI, Google DeepMind và arXiv. Chúng tôi so sánh hai mô hình ngôn ngữ lớn (LLM) là ChatGPT và Gemini dựa trên năm tiêu chí chính. Các tiêu chí này bao gồm kiến trúc và quá trình huấn luyện, hiệu suất qua các bộ đánh giá chuẩn, khả năng đa phương thức, năng lực lý luận và an toàn, cùng với hệ sinh thái và khả năng tích hợp. Khung phân tích này giúp đánh giá ưu điểm và hạn chế của mỗi mô hình một cách toàn diện.",
      "review_audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_1/pareto/review.mp3",
      "planner_reason": "Pareto chọn cụm nội dung có nhiều giá trị hoặc đóng vai trò nền tảng.",
      "segments": [
        {
          "id": 1919,
          "segment_index": 0,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_1/pareto/part_1.mp3",
          "text_content": "Nghiên cứu này áp dụng phương pháp tổng quan tài liệu có hệ thống, viết tắt là SLR, để thu thập và phân tích thông tin. SLR là một cách tiếp cận khoa học, rõ ràng và toàn diện nhằm xác định, sàng lọc, sau đó tổng hợp các tài liệu liên quan một cách khách quan. Phương pháp này giúp giảm thiểu sự thiên lệch của đánh giá chủ quan bằng cách tuân theo một quy trình nghiêm ngặt, đảm bảo kết quả có thể tái lập và khắc phục hạn chế của các tổng quan truyền thống. Nhờ đó, việc tổng hợp dữ liệu từ nhiều nguồn khác nhau trở nên chặt chẽ và đáng tin cậy, tạo nền tảng vững chắc cho việc so sánh học thuật giữa hai mô hình ngôn ngữ lớn.",
          "duration_ms": 34728
        },
        {
          "id": 1920,
          "segment_index": 1,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_1/pareto/part_2.mp3",
          "text_content": "Trên cơ sở phương pháp SLR, nghiên cứu đã thu thập dữ liệu từ các nguồn chính thống và uy tín liên quan đến ChatGPT và Gemini. Cụ thể, chúng tôi truy xuất thông tin từ các blog chính thức của OpenAI và Google DeepMind, các tài liệu nghiên cứu trên arXiv, và các bài phân tích từ bên thứ ba. Các nguồn này cung cấp số liệu đánh giá hiệu suất cập nhật nhất, thông tin về kỹ thuật nâng cao khả năng lập luận của mô hình như học tăng cường và chuỗi suy nghĩ, cũng như kiến trúc và tính năng mới của các hệ thống.",
          "duration_ms": 28488
        },
        {
          "id": 1921,
          "segment_index": 2,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_1/pareto/part_3.mp3",
          "text_content": "Dựa trên tổng quan tài liệu, nghiên cứu đã xây dựng một khung tiêu chí gồm năm trục chính để so sánh hai mô hình ngôn ngữ lớn, hay còn gọi là LLM, là ChatGPT và Google Gemini. Các tiêu chí này bao gồm kiến trúc mô hình và quá trình huấn luyện, hiệu suất qua các bộ đánh giá chuẩn, khả năng đa phương thức, khả năng lý luận và an toàn, cùng với hệ sinh thái và khả năng tích hợp.",
          "duration_ms": 21936
        },
        {
          "id": 1922,
          "segment_index": 3,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_1/pareto/part_4.mp3",
          "text_content": "Trục đầu tiên là kiến trúc mô hình và quá trình huấn luyện, so sánh nền tảng thiết kế và các kỹ thuật điều chỉnh của mỗi mô hình, làm rõ cách chúng ảnh hưởng đến khả năng và ưu tiên. Trục thứ hai là hiệu suất qua các bộ đánh giá chuẩn, đối chiếu kết quả trên các bài kiểm tra tư duy AI, hỏi đáp khoa học, lập trình phần mềm và các thang đo tổng thể khác. Tiêu chí này cung cấp số liệu định lượng về điểm mạnh và điểm yếu của mỗi mô hình trên nhiều khía cạnh nhiệm vụ.",
          "duration_ms": 25512
        },
        {
          "id": 1923,
          "segment_index": 4,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_1/pareto/part_5.mp3",
          "text_content": "Trục thứ ba là khả năng đa phương thức, xem xét mức độ hỗ trợ xử lý văn bản, hình ảnh, âm thanh, video và các công cụ tạo hình ảnh đi kèm. Trục thứ tư đánh giá khả năng lý luận và an toàn, bao gồm năng lực suy luận chuỗi bước, độ tin cậy, tỷ lệ ảo giác, cơ chế kiểm duyệt nội dung, cũng như cách xử lý dữ liệu nhạy cảm và các rào cản đạo đức. Cuối cùng, trục thứ năm là hệ sinh thái và tích hợp, xem xét các dịch vụ API, nền tảng triển khai, chi phí sử dụng, công cụ lập trình và mức độ dễ dàng tích hợp vào ứng dụng thực tế. Các tiêu chí này đảm bảo một so sánh có hệ thống và toàn diện.",
          "duration_ms": 36792
        }
      ]
    },
    {
      "id": "50179d98-37eb-4455-93be-ec3a27b26c6f",
      "title": "Chương 5: Kết quả phân tích và so sánh",
      "status": "ready",
      "unit_index": 1,
      "unit_type": "pareto_core",
      "source_text_char_count": 16439,
      "estimated_audio_seconds": 1617,
      "main_segment_count": 14,
      "review_text": "ChatGPT và Gemini đều dựa trên kiến trúc transformer nhưng có định hướng khác biệt. ChatGPT, với GPT-5, tối ưu cho hội thoại và lập luận dài, tích hợp khả năng tác tử. Gemini 2.5 Pro được thiết kế đa phương thức từ đầu, xử lý đồng thời nhiều định dạng dữ liệu và có ngữ cảnh đầu vào lớn. Về hiệu suất, GPT-5 nhỉnh hơn ở các bài kiểm tra kiến thức chuyên sâu và lập trình, trong khi Gemini mạnh về đa phương thức và kiến thức tổng quát. ChatGPT có độ tin cậy cao hơn một chút và chính sách an toàn nghiêm ngặt hơn. Hệ sinh thái ChatGPT trưởng thành và độc lập, còn Gemini tích hợp sâu với các dịch vụ của Google.",
      "review_audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_2/pareto/review.mp3",
      "planner_reason": "Pareto chọn cụm nội dung có nhiều giá trị hoặc đóng vai trò nền tảng.",
      "segments": [
        {
          "id": 1924,
          "segment_index": 0,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_2/pareto/part_1.mp3",
          "text_content": "Về kiến trúc và quá trình huấn luyện, cả ChatGPT, đại diện bởi GPT-5, và Google Gemini, đại diện bởi phiên bản Gemini 2.5 Pro, đều dựa trên nền tảng kiến trúc transformer, một loại mạng nơ-ron chuyên xử lý chuỗi dữ liệu. Tuy nhiên, định hướng thiết kế của chúng có sự khác biệt quan trọng. ChatGPT sử dụng mô hình transformer chỉ có bộ giải mã, được tối ưu cho hội thoại và lập luận ngữ cảnh dài. Thế hệ GPT-5 mới nhất còn giới thiệu cơ chế điều phối mô hình theo thời gian thực, cho phép hệ thống tự động chọn cấu phần mô hình phù hợp dựa trên loại tác vụ hoặc độ phức tạp của câu hỏi. Đồng thời, GPT-5 tích hợp các khả năng tác tử, ví dụ như thiết lập không gian làm việc và tìm kiếm tài liệu trên web trong quá trình trả lời.",
          "duration_ms": 43848
        },
        {
          "id": 1925,
          "segment_index": 1,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_2/pareto/part_2.mp3",
          "text_content": "Ngược lại, Gemini được xây dựng đa phương thức ngay từ đầu, nghĩa là được thiết kế để xử lý đồng thời văn bản, hình ảnh, âm thanh, video và mã nguồn trong một mô hình thống nhất. Kiến trúc của Gemini 2.5 cho phép hợp nhất thông tin từ nhiều định dạng, ví dụ phân tích hình ảnh hoặc biểu đồ rồi liên hệ với câu hỏi văn bản. Bên cạnh đó, Gemini duy trì lợi thế về ngữ cảnh đầu vào cực lớn, hỗ trợ tới một triệu token đầu vào, trong khi GPT-5 hỗ trợ khoảng bốn trăm nghìn token ngữ cảnh. Về phương pháp huấn luyện, cả hai đều áp dụng kỹ thuật học tăng cường từ phản hồi con người, viết tắt là RLHF, để điều chỉnh mô hình theo hướng có lợi cho người dùng. ChatGPT nổi tiếng với việc dùng RLHF sớm để cải thiện tính tự nhiên và an toàn trong đối thoại. Google Gemini cũng được huấn luyện với các chiến lược tương tự, đồng thời bổ sung cơ chế Deep Think, cho phép mô hình tạm dừng và phân tích sâu hơn với những câu hỏi phức tạp, mô phỏng quá trình suy nghĩ đa bước.",
          "duration_ms": 56832
        },
        {
          "id": 1926,
          "segment_index": 2,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_2/pareto/part_3.mp3",
          "text_content": "Dựa trên dữ liệu mới nhất năm hai không hai lăm, có thể thấy cả GPT-5 của ChatGPT và Gemini 2.5 Pro đều đạt kết quả rất cao trên các bộ đánh giá tiêu chuẩn, nhưng vẫn có sự chênh lệch nhất định trên từng hạng mục. Cụ thể, ChatGPT đạt điểm cao hơn đáng kể trên AIME hai không hai lăm, một bài kiểm tra toán và khoa học trí tuệ nhân tạo, với chín mươi bốn phẩy sáu phần trăm so với tám mươi tám phần trăm của Gemini. Tương tự, trên GPQA, một bài kiểm tra hỏi đáp tổng quát, ChatGPT đạt tám mươi tám phẩy bốn phần trăm so với tám mươi sáu phẩy bốn phần trăm của Gemini. Điều này xác nhận lợi thế của GPT-5 trong các bài kiểm tra kiến thức chuyên sâu và lập luận khoa học.",
          "duration_ms": 38952
        },
        {
          "id": 1927,
          "segment_index": 3,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_2/pareto/part_4.mp3",
          "text_content": "Trên SWE-bench, một bộ đánh giá kỹ thuật phần mềm về khả năng viết và sửa lỗi mã, GPT-5 vượt trội với bảy mươi bốn phẩy chín phần trăm so với năm mươi chín phẩy sáu phần trăm của Gemini. Điều này phản ánh GPT-5 có tư duy thuật toán và năng lực phân tích lỗi tốt hơn trong môi trường lập trình phức tạp. Ngược lại, Gemini 2.5 Pro tuy kém hơn một chút về điểm số tuyệt đối nhưng vẫn nằm trong nhóm dẫn đầu. Đặc biệt, trong bối cảnh đa phương thức, khoảng cách giữa hai mô hình càng thu hẹp: GPT-5 đạt tám mươi tư phẩy hai phần trăm trên bài kiểm tra hiểu hình ảnh MMMU, còn Gemini đạt tám mươi hai phần trăm, chỉ kém khoảng hai phẩy hai phần trăm. Kết quả này phù hợp với thiết kế Gemini vốn mạnh về xử lý hình ảnh và dữ liệu phức hợp.",
          "duration_ms": 44256
        },
        {
          "id": 1928,
          "segment_index": 4,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_2/pareto/part_5.mp3",
          "text_content": "Trong nhiệm vụ lập trình, GPT-5 thường triển khai phương pháp tiếp cận có tính tác tử, tự động chia nhỏ bài toán lập trình thành các bước giải quyết tuần tự, bao gồm viết mã, kiểm thử và gỡ lỗi. Nhờ chiến lược này, GPT-5 có khả năng xử lý những lỗi logic tinh vi và hoàn thiện chương trình tốt hơn. Ngược lại, Gemini 2.5 Pro tạo mã với phong cách ngắn gọn, có cấu trúc rõ ràng, phù hợp để tích hợp trực tiếp vào dự án hiện có. Lợi thế của Gemini là tốc độ sinh mã nhanh và khả năng xử lý các kho mã lớn nhờ ngữ cảnh dài, tới một triệu token, giúp mô hình phân tích được toàn bộ dự án hay đa tệp tin cùng lúc.",
          "duration_ms": 37848
        },
        {
          "id": 1929,
          "segment_index": 5,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_2/pareto/part_6.mp3",
          "text_content": "Về khả năng đa phương thức, cả hai mô hình đều đã mở rộng năng lực này, nhưng phương thức hỗ trợ và mức độ tích hợp có khác biệt. ChatGPT ban đầu là mô hình thuần văn bản, sau đó mới bổ sung khả năng xử lý hình ảnh và giọng nói thông qua tích hợp các mô-đun ngoài như DALL·E cho tạo ảnh và Whisper cho nhận dạng giọng nói. ChatGPT sử dụng dịch vụ DALL·E để tạo sinh hình ảnh theo mô tả, ưu điểm là tính sáng tạo phong phú và nghệ thuật cao. Tuy vậy, ChatGPT không thực sự hiểu hình ảnh theo cùng một mô hình ngôn ngữ mà phải gọi mô-đun ngoài.",
          "duration_ms": 31752
        },
        {
          "id": 1930,
          "segment_index": 6,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_2/pareto/part_7.mp3",
          "text_content": "Ngược lại, Gemini được thiết kế tích hợp đa phương thức ngay trong mô hình lõi, do đó hiểu ngữ cảnh hình ảnh song song với văn bản một cách tự nhiên. Gemini 2.5 cho phép người dùng tải ảnh, PDF, hoặc thậm chí video, âm thanh lên cùng lời nhắc, mô hình sẽ phân tích và trả lời dựa trên cả nội dung hình ảnh lẫn văn bản. Về khả năng sinh ảnh, Gemini tích hợp hai công cụ nội bộ là Imagen và Nano Banana, tỏ ra hiệu quả trong việc duy trì tính nhất quán của hình ảnh qua các lần chỉnh sửa. Nhờ vậy, Gemini phù hợp với các tác vụ cần chỉnh sửa hình ảnh có điều khiển hơn là tạo mới sáng tạo. Gemini thường cung cấp câu trả lời chi tiết và có căn cứ hơn khi phân tích hình ảnh, văn bản kỹ thuật so với ChatGPT.",
          "duration_ms": 42912
        },
        {
          "id": 1931,
          "segment_index": 7,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_2/pareto/part_8.mp3",
          "text_content": "Về khả năng lý luận nhiều bước và mức độ đáng tin cậy của thông tin, GPT-5 được thiết kế với chế độ GPT-5 Thinking, khi gặp câu hỏi phức tạp, mô hình sẽ phân bổ thêm tài nguyên tính toán để suy nghĩ, tương tự việc triển khai kỹ thuật chuỗi suy nghĩ trong lời giải. Thực nghiệm cho thấy GPT-5 cải thiện rõ rệt tính nhất quán trong các bài toán logic dài, giảm lỗi suy luận. Đối với Gemini, Google DeepMind cũng trang bị cơ chế Deep Think và ngân sách suy nghĩ, cho phép mô hình dừng lại phân tích sâu hơn trước khi trả lời. Nhìn chung, cả hai mô hình đều đã đạt trình độ suy luận xuất sắc so với thế hệ trước.",
          "duration_ms": 35592
        },
        {
          "id": 1932,
          "segment_index": 8,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_2/pareto/part_9.mp3",
          "text_content": "Về mức độ chính xác và ảo giác thông tin, không mô hình nào hoàn hảo một trăm phần trăm. Để định lượng khía cạnh này, Stanford đã tiến hành đánh giá độc lập HELM, viết tắt của Holistic Evaluation of Language Models, trên nhiều tác vụ và tính điểm độ tin cậy trung bình. Kết quả GPT-5 đạt không phẩy tám không bảy so với không phẩy bảy bốn lăm của Gemini, cho thấy ChatGPT ít ảo giác hơn và nhất quán hơn đôi chút so với Gemini. Khoảng cách này không quá lớn, hàm ý rằng Gemini chỉ kém nhẹ về độ tin cậy. Đáng chú ý, khi làm việc với các câu hỏi nhạy cảm hoặc cần độ chính xác cao, cả hai mô hình đều cần được kiểm chứng lại thông tin trước khi sử dụng.",
          "duration_ms": 40056
        },
        {
          "id": 1933,
          "segment_index": 9,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_2/pareto/part_10.mp3",
          "text_content": "Về khía cạnh an toàn và kiểm duyệt, OpenAI của ChatGPT áp dụng các rào chắn nghiêm ngặt hơn để tránh câu trả lời không phù hợp, đôi khi gây cảm giác hạn chế cho người dùng. Ngược lại, Gemini linh hoạt hơn, ít khi từ chối thẳng nhưng đòi hỏi người dùng hoặc nhà phát triển phải tinh chỉnh thêm để tránh các tình huống biên có thể phát sinh nội dung không mong muốn. Về quyền riêng tư, OpenAI mặc định lưu trữ nội dung người dùng nhập vào API trong ba mươi ngày để giám sát lạm dụng. Google thì thông báo rằng không sử dụng dữ liệu người dùng qua API Gemini để huấn luyện theo mặc định, và cho phép quản trị viên tùy chỉnh thời gian lưu trữ trên Workspace.",
          "duration_ms": 35160
        },
        {
          "id": 1934,
          "segment_index": 10,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_2/pareto/part_11.mp3",
          "text_content": "Một điểm khác biệt thực tiễn giữa ChatGPT và Gemini nằm ở hệ sinh thái dịch vụ và khả năng tích hợp của chúng. ChatGPT của OpenAI sở hữu hệ sinh thái trưởng thành hơn tính đến năm hai không hai lăm, phần lớn nhờ xuất phát sớm và được cộng đồng phát triển tích cực. OpenAI cung cấp API cho ChatGPT với nhiều lựa chọn mô hình và hỗ trợ đa dạng ngôn ngữ lập trình thông qua các bộ công cụ phát triển phần mềm chính thức. Hãng cũng hợp tác với Microsoft để cung cấp dịch vụ Azure OpenAI, tích hợp ChatGPT vào hạ tầng đám mây Azure, giúp các doanh nghiệp dễ dàng đưa ChatGPT vào ứng dụng của mình.",
          "duration_ms": 32183
        },
        {
          "id": 1935,
          "segment_index": 11,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_2/pareto/part_12.mp3",
          "text_content": "Về tính năng cho lập trình viên, ChatGPT API hỗ trợ gọi hàm, truy vấn web và thậm chí thực thi mã qua giao diện sử dụng công cụ, cho phép xây dựng các tác tử phức tạp biết tương tác với hệ thống bên ngoài. Ngoài ra, OpenAI còn triển khai cửa hàng plugin cho ChatGPT, giúp tích hợp trực tiếp dịch vụ bên thứ ba vào cuộc hội thoại. Hệ sinh thái ChatGPT cũng bao gồm tính năng Custom GPTs, tức là tùy biến ChatGPT theo phong cách hoặc hướng dẫn hệ thống riêng, và dịch vụ tinh chỉnh mô hình cho khách hàng doanh nghiệp.",
          "duration_ms": 28176
        },
        {
          "id": 1936,
          "segment_index": 12,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_2/pareto/part_13.mp3",
          "text_content": "Về phía Google Gemini, mặc dù ra mắt sau, hệ sinh thái đang mở rộng nhanh chóng nhờ lợi thế nền tảng Google. Gemini tích hợp sâu với các sản phẩm Google Cloud, đặc biệt qua Vertex AI, nền tảng học máy dưới dạng dịch vụ của Google. Một ưu thế của Gemini cho các tổ chức đã dùng Google là sự liền mạch: mô hình có thể truy cập dữ liệu trong Google Drive, bảng tính, tài liệu và thậm chí e-mail nếu được cấp quyền, giúp xây dựng các ứng dụng trợ lý thông minh trong nội bộ doanh nghiệp dễ dàng. Google cũng đẩy mạnh tích hợp Gemini vào công cụ phát triển phần mềm, ví dụ dịch vụ Gemini Code Assist có sẵn trong Google Cloud Shell và nhiều môi trường phát triển tích hợp, hỗ trợ lập trình viên với gợi ý mã và phân tích mã ngay trong quá trình viết.",
          "duration_ms": 43056
        },
        {
          "id": 1937,
          "segment_index": 13,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/59696335-526a-4905-9d6b-970edbbf1081/unit_2/pareto/part_14.mp3",
          "text_content": "Về chi phí và giới hạn, ChatGPT hiện có gói miễn phí với quyền truy cập GPT-5 giới hạn, gói Plus hai mươi đô la Mỹ một tháng và Pro hai trăm đô la Mỹ một tháng cho người dùng cá nhân hoặc cao cấp, cũng như gói doanh nghiệp tùy biến. Gemini cung cấp miễn phí đầy đủ tính năng cho người dùng có tài khoản Google và dự kiến có gói nâng cao qua Google One trong tương lai. Đối với API, giá của hai bên tương đương ở mức cao. Tóm lại, hệ sinh thái ChatGPT tỏ ra phong phú và độc lập nền tảng, phù hợp nhiều kiểu tích hợp. Hệ sinh thái Gemini thì mạnh trong hệ sinh thái Google, thuận lợi cho khách hàng đã dùng Google Cloud và cần tận dụng dữ liệu, hạ tầng sẵn có của Google.",
          "duration_ms": 40032
        }
      ]
    }
  ]
}
```

# /api/v1/jobs/{job_id}

```json
{
  "id": "5499cf4a-fa49-4304-b42c-d194dd61085f",
  "book_id": "59696335-526a-4905-9d6b-970edbbf1081",
  "job_type": "generate_plan",
  "status": "ready",
  "mode": "pareto",
  "progress_percent": 100,
  "current_step": "Sách đã xử lý xong.",
  "total_units": 2,
  "done_units": 2,
  "failed_units": 0,
  "estimated_input_tokens": 9824,
  "estimated_audio_seconds": 2036,
  "error_message": null
}
```

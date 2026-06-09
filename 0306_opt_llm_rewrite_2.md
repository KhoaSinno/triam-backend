# /api/v1/upload

```json
{
  "book_id": "f6429753-fe29-41e1-80bf-cbc4f5020a77",
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
  "book_id": "f6429753-fe29-41e1-80bf-cbc4f5020a77",
  "plan_id": "bd27e887-01cf-4455-a41a-afc21f44ebc9",
  "job_id": "4c0c1680-a016-48e9-bd81-1a74208cdb7c",
  "mode": "pareto",
  "plan_status": "active",
  "pace": 2,
  "schedule_config": [
    "Mon"
  ],
  "reminder_time": "19:00",
  "status": "queued",
  "progress_percent": 0,
  "active_slots": [
    {
      "id": "4e968c78-f2ce-49af-96f7-6760530e7aab",
      "weekday": 0,
      "weekday_label": "monday",
      "reminder_time": "19:00",
      "timezone": "Asia/Ho_Chi_Minh",
      "is_active": true
    }
  ],
  "planned_units": [
    {
      "unit_index": 0,
      "title": "Phương pháp luận nghiên cứu (SLR)",
      "unit_type": "Methodology",
      "source_section_count": 1,
      "estimated_audio_seconds": 419
    },
    {
      "unit_index": 1,
      "title": "So sánh Kiến trúc và Hiệu suất giữa ChatGPT và Gemini",
      "unit_type": "Core Analysis",
      "source_section_count": 1,
      "estimated_audio_seconds": 1617
    },
    {
      "unit_index": 2,
      "title": "Đánh giá tổng quan và Khuyến nghị ứng dụng",
      "unit_type": "Synthesis & Application",
      "source_section_count": 1,
      "estimated_audio_seconds": 1346
    }
  ]
}
```

# /api/v1/books/{book_id}/details

```json
{
  "book_id": "f6429753-fe29-41e1-80bf-cbc4f5020a77",
  "book_status": "ready",
  "mode": "pareto",
  "total_sections": 3,
  "total_units": 3,
  "units": [
    {
      "id": "222df312-4d42-4ed7-a875-3934fa6ea3dc",
      "title": "Phương pháp luận nghiên cứu (SLR)",
      "status": "ready",
      "unit_index": 0,
      "unit_type": "Methodology",
      "source_text_char_count": 4215,
      "estimated_audio_seconds": 419,
      "main_segment_count": 5,
      "review_text": "Nghiên cứu này sử dụng phương pháp Tổng quan tài liệu có hệ thống, SLR, để thu thập và phân tích dữ liệu từ các nguồn uy tín như blog chính thức của OpenAI, Google DeepMind và các tài liệu nghiên cứu. Chúng tôi so sánh ChatGPT phiên bản GPT-5 và Google Gemini phiên bản Gemini hai phẩy năm Pro dựa trên năm tiêu chí chính. Đó là: kiến trúc mô hình và quá trình huấn luyện; hiệu suất qua các benchmark như AIME và GPQA; khả năng đa phương thức; khả năng lý luận và an toàn; cùng với hệ sinh thái và khả năng tích hợp.",
      "review_audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_1/pareto/review.mp3",
      "planner_reason": "Đây là phần nền tảng phương pháp luận giúp người học hiểu cách thức nghiên cứu được thực hiện một cách khoa học và có hệ thống. Mục tiêu học: Hiểu rõ phương pháp tổng quan tài liệu có hệ thống (SLR) và quy trình áp dụng để thu thập, phân tích thông tin khách quan. Điểm quan trọng: 4/5.",
      "segments": [
        {
          "id": 1954,
          "segment_index": 0,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_1/pareto/part_1.mp3",
          "text_content": "Nghiên cứu này áp dụng phương pháp tổng quan tài liệu có hệ thống, viết tắt là SLR, để thu thập và phân tích thông tin. SLR là một phương pháp tiếp cận có hệ thống, rõ ràng, khoa học và toàn diện, nhằm xác định, sàng lọc và tổng hợp các tài liệu liên quan một cách khách quan. Phương pháp này giúp giảm thiểu thiên lệch của đánh giá chủ quan bằng cách tuân theo một quy trình nghiêm ngặt, từ đó tạo nền tảng vững chắc cho việc so sánh học thuật giữa các mô hình ngôn ngữ lớn.",
          "duration_ms": 26400
        },
        {
          "id": 1955,
          "segment_index": 1,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_1/pareto/part_2.mp3",
          "text_content": "Dựa trên phương pháp SLR, nghiên cứu đã thu thập dữ liệu từ các nguồn chính thống và uy tín liên quan đến ChatGPT và Gemini. Cụ thể, chúng tôi truy xuất thông tin từ blog chính thức của OpenAI và Google DeepMind, các tài liệu nghiên cứu trên arXiv, và các bài viết phân tích từ bên thứ ba như Leanware. Các nguồn này cung cấp số liệu benchmark cập nhật nhất, ví dụ như GPT-5 đạt tám mươi tám phẩy bốn phần trăm trên bài kiểm tra GPQA, và Gemini hai phẩy năm Pro đạt tám mươi tám phần trăm trên AIME hai nghìn không trăm hai mươi lăm.",
          "duration_ms": 31344
        },
        {
          "id": 1956,
          "segment_index": 2,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_1/pareto/part_3.mp3",
          "text_content": "Dựa trên tổng quan tài liệu, nghiên cứu đã xây dựng một khung tiêu chí gồm năm trục chính để so sánh hai mô hình ngôn ngữ lớn, hay còn gọi là LLM, là ChatGPT phiên bản GPT-5 và Google Gemini phiên bản Gemini hai phẩy năm Pro.",
          "duration_ms": 13920
        },
        {
          "id": 1957,
          "segment_index": 3,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_1/pareto/part_4.mp3",
          "text_content": "Trục đầu tiên là Kiến trúc mô hình và Quá trình huấn luyện, so sánh nền tảng kiến trúc như transformer decoder-only hay multimodal transformer, cùng các kỹ thuật huấn luyện và điều chỉnh. Trục này làm rõ cách thiết kế của mỗi mô hình ảnh hưởng đến khả năng và ưu tiên của chúng. Trục thứ hai là Hiệu suất qua các benchmark, đối chiếu kết quả trên các bộ đánh giá chuẩn như AIME kiểm tra tư duy AI trong toán học và học thuật, GPQA cho các bài toán hỏi đáp khoa học tổng quát, SWE-bench đánh giá lập trình phần mềm, và HELM đánh giá tổng thể.",
          "duration_ms": 31440
        },
        {
          "id": 1958,
          "segment_index": 4,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_1/pareto/part_5.mp3",
          "text_content": "Trục thứ ba là Khả năng đa phương thức, so sánh mức độ hỗ trợ xử lý văn bản, hình ảnh, âm thanh, video, cùng các công cụ tạo hình ảnh đi kèm như DALL-E của ChatGPT hay Imagen và Nano Banana của Gemini. Trục thứ tư là Khả năng lý luận và An toàn, đánh giá năng lực suy luận chuỗi bước, độ tin cậy, an toàn của câu trả lời, tỷ lệ ảo giác, cơ chế kiểm duyệt nội dung, và cách xử lý dữ liệu nhạy cảm. Cuối cùng, trục thứ năm là Hệ sinh thái và Tích hợp, xem xét các dịch vụ API, nền tảng triển khai như OpenAI API, Azure, Vertex AI, chi phí sử dụng, và mức độ dễ dàng tích hợp vào ứng dụng thực tế.",
          "duration_ms": 39288
        }
      ]
    },
    {
      "id": "67b3f448-371b-4fef-b2b0-3e9cfa5bba22",
      "title": "So sánh Kiến trúc và Hiệu suất giữa ChatGPT và Gemini",
      "status": "ready",
      "unit_index": 1,
      "unit_type": "Core Analysis",
      "source_text_char_count": 16439,
      "estimated_audio_seconds": 1617,
      "main_segment_count": 14,
      "review_text": "ChatGPT và Gemini đều dùng kiến trúc transformer nhưng có định hướng khác biệt. ChatGPT tối ưu cho hội thoại và lập luận dài, với khả năng điều phối mô hình theo thời gian thực và tính tác tử. Gemini được thiết kế đa phương thức từ đầu, xử lý đồng thời nhiều định dạng dữ liệu và có ngữ cảnh đầu vào rất lớn. Về hiệu suất, GPT-5 thường nhỉnh hơn Gemini trên các bài kiểm tra kiến thức chuyên sâu và lập trình, trong khi Gemini mạnh về xử lý đa phương thức. Cả hai đều có khả năng suy luận xuất sắc và sử dụng học tăng cường từ phản hồi con người để huấn luyện. ChatGPT có độ tin cậy thông tin nhỉnh hơn và chính sách an toàn nghiêm ngặt, còn Gemini linh hoạt hơn. Hệ sinh thái ChatGPT trưởng thành và độc lập, trong khi Gemini tích hợp sâu với Google Cloud.",
      "review_audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_2/pareto/review.mp3",
      "planner_reason": "Chương này chứa kết quả phân tích cốt lõi, so sánh trực tiếp hai mô hình AI hàng đầu, mang lại giá trị hiểu biết thực tiễn cao nhất. Mục tiêu học: Phân tích sự khác biệt về kiến trúc transformer, cơ chế điều phối thời gian thực và khả năng agentic giữa GPT-5 và Gemini 2.5 Pro. Điểm quan trọng: 5/5.",
      "segments": [
        {
          "id": 1959,
          "segment_index": 0,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_2/pareto/part_1.mp3",
          "text_content": "Cả ChatGPT, đại diện bởi GPT-5, và Google Gemini, đại diện bởi phiên bản Gemini hai chấm năm Pro, đều dựa trên nền tảng kiến trúc transformer. Tuy nhiên, định hướng thiết kế của chúng có sự khác biệt quan trọng. ChatGPT sử dụng mô hình transformer chỉ có bộ giải mã, được tối ưu cho hội thoại và lập luận ngữ cảnh dài.",
          "duration_ms": 20808
        },
        {
          "id": 1960,
          "segment_index": 1,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_2/pareto/part_2.mp3",
          "text_content": "Thế hệ GPT-5 mới nhất giới thiệu cơ chế điều phối mô hình theo thời gian thực, cho phép hệ thống tự động chọn cấu phần mô hình phù hợp dựa trên loại tác vụ hoặc độ phức tạp của câu hỏi. Đồng thời, GPT-5 tích hợp các khả năng tác tử, ví dụ như thiết lập không gian làm việc và tìm kiếm tài liệu trên web trong quá trình trả lời. Những cải tiến này cho phép ChatGPT linh hoạt chuyển đổi giữa phản hồi nhanh và suy luận chuyên sâu khi cần thiết.",
          "duration_ms": 24648
        },
        {
          "id": 1961,
          "segment_index": 2,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_2/pareto/part_3.mp3",
          "text_content": "Ngược lại, Gemini được xây dựng đa phương thức ngay từ đầu, thiết kế để xử lý đồng thời văn bản, hình ảnh, âm thanh, video và mã nguồn trong một mô hình thống nhất. Kiến trúc của Gemini hai chấm năm cho phép hợp nhất thông tin từ nhiều định dạng, ví dụ phân tích hình ảnh hoặc biểu đồ rồi liên hệ với câu hỏi văn bản. Bên cạnh đó, Gemini duy trì lợi thế về ngữ cảnh đầu vào cực lớn, hỗ trợ tới một triệu không trăm bốn mươi tám nghìn năm trăm bảy mươi sáu token đầu vào, so với khoảng bốn trăm nghìn token của GPT-5.",
          "duration_ms": 30528
        },
        {
          "id": 1962,
          "segment_index": 3,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_2/pareto/part_4.mp3",
          "text_content": "Về phương pháp huấn luyện, cả hai đều áp dụng kỹ thuật học tăng cường từ phản hồi con người, hay còn gọi là RLHF, để điều chỉnh mô hình theo hướng có lợi cho người dùng. ChatGPT nổi tiếng với việc dùng RLHF sớm để cải thiện tính tự nhiên và an toàn trong đối thoại. Google Gemini cũng được huấn luyện với các chiến lược tương tự, đồng thời bổ sung cơ chế Deep Think, cho phép mô hình tạm dừng và phân tích sâu hơn với những câu hỏi phức tạp, mô phỏng quá trình suy nghĩ đa bước.",
          "duration_ms": 27216
        },
        {
          "id": 1963,
          "segment_index": 4,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_2/pareto/part_5.mp3",
          "text_content": "Dựa trên dữ liệu mới nhất năm hai nghìn không trăm hai mươi lăm, có thể thấy cả GPT-5 và Gemini hai chấm năm Pro đều đạt kết quả rất cao trên các bộ đánh giá tiêu chuẩn, nhưng GPT-5 nhỉnh hơn Gemini ở hầu hết các tiêu chí định lượng. Cụ thể, ChatGPT đạt điểm cao hơn đáng kể trên AIME hai nghìn không trăm hai mươi lăm, một bài kiểm tra toán và khoa học, với chín mươi bốn phẩy sáu phần trăm so với tám mươi tám phần trăm của Gemini, xác nhận lợi thế của GPT-5 trong các bài kiểm tra kiến thức chuyên sâu và lập luận khoa học.",
          "duration_ms": 29496
        },
        {
          "id": 1964,
          "segment_index": 5,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_2/pareto/part_6.mp3",
          "text_content": "Trên SWE-bench, một bộ đánh giá khả năng viết và sửa lỗi mã nguồn, GPT-5 vượt trội với bảy mươi bốn phẩy chín phần trăm so với năm mươi chín phẩy sáu phần trăm của Gemini. Ngay cả khi Gemini được phép thử lại để cải thiện kết quả, ChatGPT vẫn dẫn đầu về khả năng lập trình và gỡ lỗi. Điều này phản ánh GPT-5 có tư duy thuật toán và năng lực phân tích lỗi tốt hơn trong môi trường lập trình phức tạp, thường triển khai phương pháp tiếp cận có tính tác tử, tức là tự động chia nhỏ bài toán lập trình thành các bước giải quyết tuần tự.",
          "duration_ms": 30072
        },
        {
          "id": 1965,
          "segment_index": 6,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_2/pareto/part_7.mp3",
          "text_content": "Ngược lại, Gemini hai chấm năm Pro tạo mã với phong cách ngắn gọn, có cấu trúc rõ ràng, phù hợp để tích hợp trực tiếp vào dự án hiện có. Lợi thế của Gemini là tốc độ sinh mã nhanh và khả năng xử lý các kho mã lớn nhờ ngữ cảnh dài, giúp mô hình phân tích toàn bộ dự án hay đa tệp tin cùng lúc. Trong bối cảnh đa phương thức, khoảng cách giữa hai mô hình thu hẹp đáng kể: GPT-5 đạt tám mươi bốn phẩy hai phần trăm trên bài kiểm tra hiểu hình ảnh MMMU, còn Gemini đạt tám mươi hai phần trăm, chỉ kém khoảng hai phẩy hai phần trăm, phù hợp với thiết kế của Gemini vốn mạnh về xử lý hình ảnh và dữ liệu phức hợp.",
          "duration_ms": 35736
        },
        {
          "id": 1966,
          "segment_index": 7,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_2/pareto/part_8.mp3",
          "text_content": "Về khả năng đa phương thức, ChatGPT ban đầu là mô hình thuần văn bản, sau đó mới bổ sung khả năng xử lý hình ảnh và giọng nói thông qua tích hợp các module bên ngoài như DALL·E cho tạo ảnh và Whisper cho nhận dạng giọng nói. Ngược lại, Gemini được thiết kế tích hợp đa phương thức ngay trong mô hình lõi, do đó hiểu ngữ cảnh hình ảnh song song với văn bản một cách tự nhiên. Gemini hai chấm năm cho phép người dùng tải ảnh, PDF, hoặc thậm chí video, âm thanh lên cùng lời nhắc, và mô hình sẽ phân tích, trả lời dựa trên cả nội dung hình ảnh lẫn văn bản.",
          "duration_ms": 31800
        },
        {
          "id": 1967,
          "segment_index": 8,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_2/pareto/part_9.mp3",
          "text_content": "Về khả năng sinh ảnh, ChatGPT sử dụng dịch vụ DALL·E, ưu điểm là tính sáng tạo phong phú và nghệ thuật cao. Gemini tích hợp các công cụ nội bộ như Imagen và Nano Banana, trong đó Nano Banana hiệu quả trong việc duy trì tính nhất quán của hình ảnh qua các lần chỉnh sửa. Tóm lại, Gemini đi trước trong việc thống nhất xử lý đa định dạng thông tin, hữu ích cho các nhiệm vụ nghiên cứu yêu cầu trích xuất tri thức từ nội dung hình ảnh hoặc âm thanh. ChatGPT tuy bổ sung chức năng này nhưng còn hạn chế ở mức độ tích hợp, dù vẫn vượt trội về tính sáng tạo hình ảnh.",
          "duration_ms": 33456
        },
        {
          "id": 1968,
          "segment_index": 9,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_2/pareto/part_10.mp3",
          "text_content": "Cả hai mô hình đều đạt trình độ suy luận xuất sắc. GPT-5 được thiết kế với chế độ GPT-5 Thinking, khi gặp câu hỏi phức tạp, mô hình sẽ phân bổ thêm tài nguyên tính toán để suy nghĩ, tương tự việc triển khai kỹ thuật chuỗi suy nghĩ. Đối với Gemini, Google DeepMind cũng trang bị cơ chế Deep Think cho phép mô hình dừng lại phân tích sâu hơn trước khi trả lời. Về mức độ chính xác và ảo giác thông tin, không mô hình nào hoàn hảo một trăm phần trăm. Đánh giá độc lập HELM từ Stanford cho thấy GPT-5 đạt không phẩy tám trăm linh bảy so với không phẩy bảy trăm bốn mươi lăm của Gemini, hàm ý ChatGPT ít ảo giác và nhất quán hơn đôi chút.",
          "duration_ms": 38112
        },
        {
          "id": 1969,
          "segment_index": 10,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_2/pareto/part_11.mp3",
          "text_content": "Về an toàn và kiểm duyệt, OpenAI áp dụng các rào chắn nghiêm ngặt hơn để tránh câu trả lời không phù hợp, đôi khi gây cảm giác hạn chế cho người dùng. Ngược lại, Gemini linh hoạt hơn, ít khi từ chối thẳng nhưng đòi hỏi người dùng hoặc nhà phát triển phải tinh chỉnh thêm để tránh các tình huống biên. Về quyền riêng tư, OpenAI mặc định lưu trữ nội dung người dùng nhập vào API trong ba mươi ngày để giám sát lạm dụng. Google thông báo không sử dụng dữ liệu người dùng qua API Gemini để huấn luyện theo mặc định và cho phép quản trị viên tùy chỉnh thời gian lưu trữ.",
          "duration_ms": 31416
        },
        {
          "id": 1970,
          "segment_index": 11,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_2/pareto/part_12.mp3",
          "text_content": "ChatGPT của OpenAI sở hữu hệ sinh thái trưởng thành hơn, nhờ xuất phát sớm và được cộng đồng phát triển tích cực. OpenAI cung cấp API với nhiều lựa chọn mô hình và hỗ trợ đa dạng ngôn ngữ lập trình thông qua các bộ công cụ phát triển phần mềm chính thức. Hãng cũng hợp tác với Microsoft để cung cấp dịch vụ Azure OpenAI, tích hợp ChatGPT vào hạ tầng đám mây Azure, giúp các doanh nghiệp dễ dàng đưa ChatGPT vào ứng dụng của mình. ChatGPT API hỗ trợ gọi hàm, truy vấn web và thậm chí thực thi mã qua giao diện tool use, cho phép xây dựng các tác tử phức tạp biết tương tác với hệ thống bên ngoài.",
          "duration_ms": 33456
        },
        {
          "id": 1971,
          "segment_index": 12,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_2/pareto/part_13.mp3",
          "text_content": "Về phía Google Gemini, mặc dù ra mắt sau, hệ sinh thái đang mở rộng nhanh chóng nhờ lợi thế nền tảng Google. Gemini tích hợp sâu với các sản phẩm Google Cloud, đặc biệt qua Vertex AI, nền tảng học máy dưới dạng dịch vụ của Google. Một ưu thế của Gemini cho các tổ chức đã dùng Google là sự liền mạch: mô hình có thể truy cập dữ liệu trong Google Drive, bảng tính, tài liệu và thậm chí e-mail nếu được cấp quyền. Google cũng đẩy mạnh tích hợp Gemini vào công cụ phát triển phần mềm như Gemini Code Assist, hỗ trợ lập trình viên với gợi ý mã và phân tích code ngay trong quá trình viết.",
          "duration_ms": 35808
        },
        {
          "id": 1972,
          "segment_index": 13,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_2/pareto/part_14.mp3",
          "text_content": "Về chi phí, ChatGPT có các gói trả phí hàng tháng cho người dùng cá nhân và gói doanh nghiệp tùy biến. Gemini hiện cung cấp miễn phí đầy đủ tính năng cho người dùng có tài khoản Google. Tóm lại, hệ sinh thái ChatGPT phong phú và độc lập nền tảng, phù hợp nhiều kiểu tích hợp. Hệ sinh thái Gemini mạnh trong hệ sinh thái Google, thuận lợi cho khách hàng đã dùng Google Cloud và cần tận dụng dữ liệu, hạ tầng sẵn có. Việc lựa chọn mô hình tùy thuộc vào môi trường công nghệ và yêu cầu triển khai thực tế của người dùng.",
          "duration_ms": 30456
        }
      ]
    },
    {
      "id": "a9693390-57e4-4283-a420-1079a2c0941e",
      "title": "Đánh giá tổng quan và Khuyến nghị ứng dụng",
      "status": "ready",
      "unit_index": 2,
      "unit_type": "Synthesis & Application",
      "source_text_char_count": 13860,
      "estimated_audio_seconds": 1346,
      "main_segment_count": 17,
      "review_text": "ChatGPT GPT-5 và Google Gemini 2.5 Pro là hai mô hình ngôn ngữ hàng đầu năm hai không hai lăm, mỗi bên có thế mạnh riêng. ChatGPT vượt trội về hiệu suất tổng hợp, lập trình, kiến thức và quản lý ngữ cảnh trong hội thoại dài. Gemini 2.5 Pro nổi bật về xử lý đa phương thức, phân tích có cấu trúc và tích hợp thời gian thực với internet. ChatGPT phù hợp cho sáng tạo nội dung và giao tiếp tự nhiên, còn Gemini lý tưởng cho các nhiệm vụ kỹ thuật, phân tích chuyên sâu và khai thác dữ liệu đa dạng. Việc lựa chọn mô hình nên dựa trên bối cảnh sử dụng cụ thể, vì cả hai đều đang tiến hóa nhanh chóng và không có mô hình nào chiếm ưu thế tuyệt đối trên mọi mặt.",
      "review_audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/review.mp3",
      "planner_reason": "Phần bàn luận và khuyến nghị giúp người học tổng hợp thông tin và đưa ra quyết định lựa chọn công nghệ phù hợp trong thực tế. Mục tiêu học: Đánh giá ưu nhược điểm tổng thể của từng mô hình và rút ra các khuyến nghị ứng dụng thực tế dựa trên kết quả so sánh. Điểm quan trọng: 5/5.",
      "segments": [
        {
          "id": 1973,
          "segment_index": 0,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/part_1.mp3",
          "text_content": "Từ các phân tích chi tiết, có thể thấy ChatGPT, cụ thể là phiên bản GPT-5, và Google Gemini 2.5 Pro đều là những mô hình ngôn ngữ hàng đầu năm hai không hai lăm, mỗi bên có thế mạnh riêng. ChatGPT tạm thời chiếm ưu thế về hiệu suất tổng hợp, thể hiện qua điểm số nhỉnh hơn ở nhiều bài kiểm tra tiêu chuẩn, hay còn gọi là benchmark, đặc biệt là trong lập trình và các bài kiểm tra kiến thức. Mô hình này cũng có khả năng tạo phản hồi lưu loát, tự nhiên trong hội thoại và cho thấy sự vượt trội nhẹ về độ tin cậy cũng như quản lý ngữ cảnh, tức là khả năng ghi nhớ thông tin đã trao đổi trong các phiên trò chuyện dài.",
          "duration_ms": 33816
        },
        {
          "id": 1974,
          "segment_index": 1,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/part_2.mp3",
          "text_content": "Ngược lại, Gemini 2.5 Pro đã chứng tỏ năng lực đổi mới vượt bậc của Google DeepMind, bám sát và thậm chí dẫn trước ở một số khía cạnh chuyên biệt. Mô hình Gemini nổi bật về xử lý đa phương thức, tức là khả năng hiểu hình ảnh và video vượt trội, phân tích có cấu trúc với câu trả lời có trật tự kèm căn cứ khi làm nhiệm vụ nghiên cứu. Ngoài ra, Gemini còn tích hợp thời gian thực với tri thức mới trên internet nhờ kết nối trực tiếp với Google Search.",
          "duration_ms": 27336
        },
        {
          "id": 1975,
          "segment_index": 2,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/part_3.mp3",
          "text_content": "Một cách tổng quát, ChatGPT phù hợp hơn cho những tương tác đòi hỏi tính sáng tạo ngôn ngữ và giao tiếp tự nhiên. Trong khi đó, Gemini phù hợp cho các nhiệm vụ mang tính kỹ thuật, phân tích chuyên sâu và khai thác dữ liệu đa dạng. Tuy nhiên, khoảng cách giữa hai mô hình là không lớn và cả hai đều đang tiến hóa nhanh chóng. Sự cạnh tranh quyết liệt giữa OpenAI và Google đã thúc đẩy mỗi bên liên tục cải tiến sản phẩm, mang lại lợi ích cho người dùng. Do đó, kết quả so sánh tại thời điểm này có thể thay đổi sau vài tháng, và việc lựa chọn nên dựa trên bối cảnh sử dụng cụ thể để phát huy tối đa điểm mạnh của từng mô hình.",
          "duration_ms": 35784
        },
        {
          "id": 1976,
          "segment_index": 3,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/part_4.mp3",
          "text_content": "Dựa trên ưu nhược điểm đã phân tích, có thể đề xuất một số định hướng lựa chọn ChatGPT hoặc Gemini tùy theo nhu cầu. Nếu mục tiêu là viết lách sáng tạo như blog, kịch bản, email marketing hoặc trợ lý hội thoại mang tính cá nhân, ChatGPT là lựa chọn ưu tiên. Mô hình này có văn phong tự nhiên, khả năng biến hóa ngữ điệu linh hoạt và thường đưa ra phản hồi dài giàu cảm xúc hơn. ChatGPT cũng tỏ ra vượt trội khi cần giả lập phong cách viết và thích nghi với phản hồi của người dùng trong hội thoại dài.",
          "duration_ms": 28416
        },
        {
          "id": 1977,
          "segment_index": 4,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/part_5.mp3",
          "text_content": "Ngược lại, nếu nội dung yêu cầu độ chính xác cao, văn phong kỹ thuật hoặc cần chèn trích dẫn khoa học, Gemini có thể phù hợp hơn. Mô hình của Google nổi tiếng với việc tạo câu trả lời có cấu trúc rõ ràng, thích hợp cho viết báo cáo nghiên cứu, tài liệu kỹ thuật hoặc tóm tắt tài liệu học thuật, trong đó sự chặt chẽ và đúng đắn quan trọng hơn là sự bay bổng. Ví dụ, một bản tóm tắt nghiên cứu kèm nguồn tham khảo hoặc một báo cáo phân tích dữ liệu nên dùng Gemini để tận dụng khả năng đưa ra thông tin chi tiết và có căn cứ.",
          "duration_ms": 29640
        },
        {
          "id": 1978,
          "segment_index": 5,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/part_6.mp3",
          "text_content": "Đối với các dự án phần mềm phức tạp, cần gỡ lỗi logic nhiều bước hoặc tối ưu mã, ChatGPT phiên bản GPT-5 được khuyến nghị. Qua kết quả từ SWE-bench, một bộ tiêu chuẩn đánh giá khả năng lập trình, và kinh nghiệm thực tế, GPT-5 có khả năng hiểu ngữ cảnh mã liên module, dò tìm lỗi logic ẩn và gợi ý sửa lỗi một cách mạch lạc, từng bước. Các lập trình viên ghi nhận ChatGPT thể hiện như một trợ lý kỹ sư giàu kinh nghiệm, đặc biệt hữu ích khi phải giải thích đoạn mã phức tạp hoặc đề xuất phương án tối ưu.",
          "duration_ms": 29712
        },
        {
          "id": 1979,
          "segment_index": 6,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/part_7.mp3",
          "text_content": "Ngược lại, Gemini 2.5 Pro phù hợp cho phân tích dự án lớn, như quét toàn bộ kho lưu trữ mã nguồn để tìm các chỗ tiềm ẩn lỗi, hoặc đánh giá cấu trúc. Điều này nhờ vào ngữ cảnh dài một triệu token, cho phép đưa vào toàn bộ mã nguồn của nhiều tệp cùng lúc. Nếu công việc yêu cầu tích hợp AI vào quy trình CI/CD, tức là tích hợp và triển khai liên tục, hoặc trong môi trường điện toán đám mây của Google, Gemini là lựa chọn tự nhiên do có sẵn công cụ như Code Assist và tích hợp với Vertex AI, nền tảng học máy của Google Cloud. Tóm lại, ChatGPT phù hợp làm trợ lý mã thông minh giải quyết vấn đề khó, còn Gemini là công cụ quy mô lớn để bao quát, phân tích bức tranh tổng thể của dự án phần mềm.",
          "duration_ms": 41712
        },
        {
          "id": 1980,
          "segment_index": 7,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/part_8.mp3",
          "text_content": "Đối với các tác vụ hỗ trợ cá nhân hàng ngày như tra cứu tin tức, trả lời câu hỏi nhanh, quản lý email, lập thời gian biểu, cả hai mô hình đều làm tốt nhưng khác biệt về hệ sinh thái. Nếu bạn đã quen thuộc với hệ sinh thái Google gồm Gmail, Google Drive, Docs, Gemini tỏ ra thuận tiện hơn. Bạn có thể yêu cầu Gemini tóm tắt email, soạn thảo tài liệu Google Docs hoặc lấy dữ liệu từ Sheets mà không rời khỏi giao diện chat. Khả năng kết nối trực tiếp Google Search cũng giúp Gemini cập nhật thông tin thời sự hoặc kiến thức mới hiệu quả, phù hợp cho các tác vụ nghiên cứu nhanh trong ngày.",
          "duration_ms": 34728
        },
        {
          "id": 1981,
          "segment_index": 8,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/part_9.mp3",
          "text_content": "Ngược lại, ChatGPT tích hợp tốt với nhiều dịch vụ đa dạng hơn bên ngoài hệ Google. Nếu công việc đòi hỏi liên kết với các ứng dụng kinh doanh khác như CRM, tức là quản lý quan hệ khách hàng, Notion, Office ba trăm sáu lăm, hoặc nếu bạn muốn tùy biến trợ lý của riêng mình thông qua API, tức là giao diện lập trình ứng dụng và plugin, ChatGPT cung cấp nhiều tiện ích mở rộng và cộng đồng hỗ trợ đông đảo. Về trải nghiệm di động, cả hai đều có ứng dụng trên điện thoại thông minh. Người dùng đánh giá ChatGPT có giao diện mượt mà, phản hồi giọng nói tự nhiên hơn, nên thuận lợi nếu bạn hay sử dụng trợ lý AI bằng tiếng nói.",
          "duration_ms": 35952
        },
        {
          "id": 1982,
          "segment_index": 9,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/part_10.mp3",
          "text_content": "Trong khi đó, Gemini có tính năng độc đáo là tích hợp camera trên di động. Bạn có thể chụp ảnh tài liệu, vật dụng và hỏi Gemini ngay. Do đó, với người thường xuyên phải xử lý thông tin từ hình ảnh hoặc thế giới thực khi di chuyển, ví dụ chụp biên bản cuộc họp để trích ý chính, Gemini đem lại trải nghiệm liền mạch và mạnh mẽ hơn.",
          "duration_ms": 20784
        },
        {
          "id": 1983,
          "segment_index": 10,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/part_11.mp3",
          "text_content": "Nếu một tổ chức đang cân nhắc tích hợp các mô hình ngôn ngữ lớn, hay LLM, vào hệ thống của mình, quyết định giữa ChatGPT và Gemini cần xét đến hạ tầng hiện có và chi phí. ChatGPT, dưới dạng Azure OpenAI, sẽ phù hợp với doanh nghiệp đã dùng Microsoft Azure hoặc cần giải pháp độc lập đám mây, hay còn gọi là on-premise, trong tương lai. Điều này do OpenAI hướng tới tính mở và trung lập với nền tảng.",
          "duration_ms": 25488
        },
        {
          "id": 1984,
          "segment_index": 11,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/part_12.mp3",
          "text_content": "Mặt khác, Gemini trên Vertex AI lại lý tưởng cho các tổ chức đã xây dựng trên Google Cloud. Họ có thể tận dụng dịch vụ dữ liệu sẵn có của Google như BigQuery, App Engine cùng với Gemini để xây dựng ứng dụng hoàn chỉnh từ đầu đến cuối. Về chi phí, hiện tại Gemini có lợi thế giá ban đầu thấp hơn, bản thân ứng dụng Gemini cho người dùng cuối đang miễn phí hoàn toàn, trong khi ChatGPT bản mạnh GPT-5 yêu cầu tối thiểu gói Plus hai mươi đô la mỗi tháng để sử dụng ổn định.",
          "duration_ms": 28488
        },
        {
          "id": 1985,
          "segment_index": 12,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/part_13.mp3",
          "text_content": "Tuy nhiên, với khối lượng gọi API lớn, mức giá hai bên tương đương, đều khoảng một đến hai đô la cho một triệu token đầu vào và khoảng mười đô la cho đầu ra. Một điểm cần lưu ý là giới hạn sử dụng: ChatGPT Plus giới hạn số tin nhắn GPT-5 mỗi ba giờ, còn Gemini thì giới hạn theo ngày, ví dụ sáu nghìn yêu cầu mã và hai trăm bốn mươi cuộc trò chuyện mỗi ngày ở bản Code Assist. Tùy theo trường hợp sử dụng liên tục hay không thường xuyên, bạn nên chọn dịch vụ có hạn mức phù hợp.",
          "duration_ms": 28272
        },
        {
          "id": 1986,
          "segment_index": 14,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/part_15.mp3",
          "text_content": "Nghiên cứu này tồn tại một số hạn chế. Trước hết, đây là một đồ án tổng quan tài liệu, không tiến hành thực nghiệm trực tiếp với hai mô hình. Tất cả kết luận đều dựa trên dữ liệu thứ cấp đã công bố, tiềm ẩn rủi ro về độ chính xác và độ tin cậy của nguồn. Nhóm tác giả đã cố gắng đối chiếu chéo giữa nhiều nguồn để giảm thiểu thiên lệch, nhưng không thể đảm bảo hoàn toàn tính vô tư của tất cả dữ liệu.",
          "duration_ms": 24000
        },
        {
          "id": 1987,
          "segment_index": 15,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/part_16.mp3",
          "text_content": "Thêm vào đó, thời điểm thu thập thông tin là cuối năm hai không hai lăm, một giai đoạn mà cả ChatGPT GPT-5 và Gemini 2.5 mới ra mắt vài tháng. Do đó, kết quả đánh giá có thể chưa ổn định và sẽ thay đổi khi mô hình được cập nhật hoặc qua quá trình sử dụng thực tế dài hơn. Ví dụ, điểm số benchmark có thể cải thiện với phiên bản phần mềm mới, hoặc các vấn đề ảo giác, tức là hiện tượng mô hình tạo ra thông tin sai lệch, có thể giảm bớt nhờ tinh chỉnh liên tục. Nghiên cứu cũng chưa xem xét hết mọi khía cạnh tiềm năng, chỉ tập trung năm trục so sánh chính.",
          "duration_ms": 32472
        },
        {
          "id": 1988,
          "segment_index": 16,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/part_17.mp3",
          "text_content": "Để có cái nhìn toàn diện và cập nhật hơn, nghiên cứu tương lai có thể thực hiện các bài kiểm tra trực tiếp với ChatGPT GPT-5 và Gemini 2.5 Pro trên cùng một bộ nhiệm vụ do nhóm nghiên cứu thiết kế. Ngoài ra, có thể mở rộng đối tượng so sánh sang các mô hình lớn khác như Anthropic Claude 3.7, Meta LLaMA 3 hay Amazon Titan. Nghiên cứu chuyên sâu theo lĩnh vực cụ thể như y tế, giáo dục, pháp lý hoặc sáng tạo nghệ thuật cũng là một hướng đi tiềm năng. Cuối cùng, phân tích hiệu quả chi phí và trải nghiệm người dùng, hay UX, sẽ bổ sung cho phân tích định lượng, giúp đưa ra quyết định dựa trên tổng hòa hiệu quả, chi phí và trải nghiệm.",
          "duration_ms": 38304
        },
        {
          "id": 1989,
          "segment_index": 17,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/f6429753-fe29-41e1-80bf-cbc4f5020a77/unit_3/pareto/part_18.mp3",
          "text_content": "Cuộc so sánh giữa ChatGPT và Gemini trong đồ án này cho thấy bức tranh một chín một mười giữa hai mô hình ngôn ngữ AI tiên tiến nhất hiện nay. Mỗi mô hình đã khẳng định vị thế trên một số mặt, đồng thời không ngừng học hỏi điểm mạnh của nhau để hoàn thiện. Trong tương lai gần, ranh giới giữa ChatGPT và Gemini có thể sẽ còn mờ nhạt hơn khi cả hai liên tục cập nhật và đổi mới. Do vậy, người dùng và nhà nghiên cứu cần theo dõi sát sao các tiến bộ mới và linh hoạt điều chỉnh lựa chọn công nghệ cho phù hợp.",
          "duration_ms": 28320
        }
      ]
    }
  ]
}
```





///////////////////////// LOG SERVER /////////////////////////
026-06-03 15:11:39.558 | INFO     | app.services.upload_service:handle_upload_document:194 - ☁️  PDF uploaded to Storagge: f6429753-fe29-41e1-80bf-cbc4f5020a77/original.pdf
2026-06-03 15:11:40.719 | INFO     | app.services.upload_service:handle_upload_document:225 - 📘 Created DRAFT book f6429753-fe29-41e1-80bf-cbc4f5020a77 | 3 sections | file_url saved
2026-06-03 15:11:40.720 | INFO     | logging:callHandlers:1762 - 127.0.0.1:54066 - "POST /api/v1/upload HTTP/1.1" 200
2026-06-03 15:12:13.179 | WARNING  | logging:callHandlers:1762 - AppException: Bạn đã đạt giới hạn số sách đang học. Hãy hoàn thành hoặc tạm dừng một sách trước. - Status Code: 409
2026-06-03 15:12:13.180 | INFO     | logging:callHandlers:1762 - 127.0.0.1:56246 - "POST /api/v1/generate-plan HTTP/1.1" 409
2026-06-03 15:13:18.777 | INFO     | app.repositories.audiobook_repo:delete_book_storage:93 - Đã xóa 20 files từ bucket: audios
2026-06-03 15:13:18.961 | INFO     | app.repositories.audiobook_repo:delete_book_storage:93 - Đã xóa 1 files từ bucket: raw_books
2026-06-03 15:13:19.359 | INFO     | app.repositories.audiobook_repo:delete_book_storage:97 - Đã dọn dẹp sạch sẽ database cho book: 9e66b856-acaa-47d8-a26e-647918492117
2026-06-03 15:13:19.360 | INFO     | logging:callHandlers:1762 - 127.0.0.1:51013 - "DELETE /api/v1/books/9e66b856-acaa-47d8-a26e-647918492117 HTTP/1.1" 200
2026-06-03 15:13:35.344 | INFO     | app.repositories.audiobook_repo:delete_book_storage:93 - Đã xóa 21 files từ bucket: audios
2026-06-03 15:13:35.511 | INFO     | app.repositories.audiobook_repo:delete_book_storage:93 - Đã xóa 1 files từ bucket: raw_books
2026-06-03 15:13:35.747 | INFO     | app.repositories.audiobook_repo:delete_book_storage:97 - Đã dọn dẹp sạch sẽ database cho book: 59696335-526a-4905-9d6b-970edbbf1081
2026-06-03 15:13:35.748 | INFO     | logging:callHandlers:1762 - 127.0.0.1:51021 - "DELETE /api/v1/books/59696335-526a-4905-9d6b-970edbbf1081 HTTP/1.1" 200
2026-06-03 15:13:47.098 | INFO     | app.repositories.audiobook_repo:delete_book_storage:93 - Đã xóa 18 files từ bucket: audios
2026-06-03 15:13:47.333 | INFO     | app.repositories.audiobook_repo:delete_book_storage:93 - Đã xóa 1 files từ bucket: raw_books
2026-06-03 15:13:47.504 | INFO     | app.repositories.audiobook_repo:delete_book_storage:97 - Đã dọn dẹp sạch sẽ database cho book: ed532bbb-469f-4a8d-b9dc-8036388d85fb
2026-06-03 15:13:47.505 | INFO     | logging:callHandlers:1762 - 127.0.0.1:51026 - "DELETE /api/v1/books/ed532bbb-469f-4a8d-b9dc-8036388d85fb HTTP/1.1" 200
2026-06-03 15:14:16.647 | INFO     | app.services.pareto_planner_service:plan_pareto_learning_units:277 - Pareto planner start | sections=3 | cards=3 | model=gemini-3.5-flash
2026-06-03 15:14:25.306 | INFO     | app.services.pareto_planner_service:plan_pareto_learning_units:282 - Pareto planner result | source=llm | units=3
2026-06-03 15:14:26.210 | INFO     | app.services.upload_service:handle_generate_plan:289 - 📋 ReadingPlan created for book f6429753-fe29-41e1-80bf-cbc4f5020a77 | mode=pareto | job=4c0c1680-a016-48e9-bd81-1a74208cdb7c
2026-06-03 15:14:26.789 | INFO     | logging:callHandlers:1762 - 127.0.0.1:62701 - "POST /api/v1/generate-plan HTTP/1.1" 200
2026-06-03 15:24:18.266 | INFO     | logging:callHandlers:1762 - 127.0.0.1:49687 - "GET /api/v1/books/f6429753-fe29-41e1-80bf-cbc4f5020a77/details?mode=pareto HTTP/1.1" 200


///////////////////////// LOG WORKER /////////////////////////

2026-06-03 15:14:26.781 | INFO     | app.tasks.book_tasks:process_book_task:23 - Celery process_book_task started | book_id=f6429753-fe29-41e1-80bf-cbc4f5020a77 | mode=pareto | job_id=4c0c1680-a016-48e9-bd81-1a74208cdb7c
2026-06-03 15:14:29.104 | INFO     | app.services.workers.learning_unit_worker:process_learning_unit:68 - Learning unit processing start | unit=1 | mode=pareto | title=Phương pháp luận nghiên cứu (SLR) | chars=4215 | estimated_tokens=2003 | estimated_audio_seconds=419 | rag=True
2026-06-03 15:14:29.886 | INFO     | app.services.workers.learning_unit_tts_worker:run_learning_unit_tts_pipeline:122 - TTS pipeline start | unit=1 | mode=pareto | title=Phương pháp luận nghiên cứu (SLR) | raw_chars=4215
2026-06-03 15:14:29.888 | INFO     | app.services.llm_service:normalize_text_for_speech:235 - Normalize preflight | mode=pareto | title=Phương pháp luận nghiên cứu (SLR) | chars=4215 | estimated_tokens=2003 | estimated_audio_seconds=419    
2026-06-03 15:14:29.888 | INFO     | app.services.llm_service:normalize_text_for_speech:244 - Normalize strategy | mode=pareto | strategy=single_call | title=Phương pháp luận nghiên cứu (SLR)
2026-06-03 15:14:29.889 | INFO     | app.services.llm_service:_call_normalize_llm:195 - LLM normalize start | mode=pareto | context=single | chars=4215 | attempt=1/2
2026-06-03 15:14:34.910 | INFO     | app.services.embed_service:embed_and_save_learning_unit:72 - RAG: Saved 5 vectors for learning_unit_id=222df312-4d42-4ed7-a875-3934fa6ea3dc
2026-06-03 15:14:46.198 | INFO     | app.services.llm_service:_log_tts_quality_report:182 - LLM normalize quality warnings | mode=pareto | context=single | chars=4215 | markdown_artifacts=0 | unexplained_acronyms=['GPT-5', 'GPQA', 'AIME', 'SWE-bench', 'HELM', 'DALL-E', 'API']
2026-06-03 15:14:46.199 | INFO     | app.services.llm_service:_call_normalize_llm:210 - LLM normalize done | mode=pareto | context=single | scripts=5 | review_chars=516
2026-06-03 15:14:46.199 | INFO     | app.services.workers.learning_unit_tts_worker:run_learning_unit_tts_pipeline:129 - TTS pipeline normalized | unit=1 | mode=pareto | main_scripts=5 | review_chars=516
2026-06-03 15:14:46.200 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:33 - TTS main segments start | unit=1 | mode=pareto | total_scripts=5
2026-06-03 15:14:46.200 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=1 | mode=pareto | segment=1/5 | chars=475
2026-06-03 15:15:01.921 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=475 | bytes=615 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:15:03.798 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=1 | mode=pareto | segment=1/5 | duration_ms=26400
2026-06-03 15:15:03.799 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=1 | mode=pareto | segment=2/5 | chars=533
2026-06-03 15:15:15.585 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=533 | bytes=662 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:15:16.194 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=1 | mode=pareto | segment=2/5 | duration_ms=31344
2026-06-03 15:15:16.194 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=1 | mode=pareto | segment=3/5 | chars=225
2026-06-03 15:15:23.228 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=225 | bytes=277 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:15:24.877 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=1 | mode=pareto | segment=3/5 | duration_ms=13920
2026-06-03 15:15:24.878 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=1 | mode=pareto | segment=4/5 | chars=541
2026-06-03 15:15:38.252 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=541 | bytes=688 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:15:38.984 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=1 | mode=pareto | segment=4/5 | duration_ms=31440
2026-06-03 15:15:38.986 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=1 | mode=pareto | segment=5/5 | chars=594
2026-06-03 15:15:55.084 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=594 | bytes=769 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:15:56.942 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=1 | mode=pareto | segment=5/5 | duration_ms=39288
2026-06-03 15:15:56.943 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:63 - TTS main segments done | unit=1 | mode=pareto | created_segments=5/5
2026-06-03 15:15:56.943 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_review_audio:82 - TTS review start | unit=1 | mode=pareto | chars=516
2026-06-03 15:16:11.954 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=516 | bytes=640 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:16:13.659 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_review_audio:86 - TTS review done | unit=1 | mode=pareto
2026-06-03 15:16:13.660 | INFO     | app.services.workers.learning_unit_tts_worker:_store_unit_tts_result:103 - TTS DB store start | learning_unit_id=222df312-4d42-4ed7-a875-3934fa6ea3dc | mode=pareto | segments=5 | review_audio=True       
2026-06-03 15:16:15.828 | INFO     | app.services.workers.learning_unit_tts_worker:_store_unit_tts_result:111 - TTS DB store done | learning_unit_id=222df312-4d42-4ed7-a875-3934fa6ea3dc | mode=pareto
2026-06-03 15:16:16.555 | INFO     | app.services.workers.learning_unit_worker:process_learning_unit:124 - Learning unit 1 READY | segments=5
2026-06-03 15:16:17.972 | INFO     | app.services.workers.book_pipeline:_create_first_playable_notification_safely:140 -
 Content-ready first-playable event | book_id=f6429753-fe29-41e1-80bf-cbc4f5020a77 | mode=pareto | created=False        
2026-06-03 15:16:18.004 | INFO     | app.services.workers.learning_unit_worker:process_learning_unit:68 - Learning unit processing start | unit=2 | mode=pareto | title=So sánh Kiến trúc và Hiệu suất giữa ChatGPT và Gemini | chars=16439 | estimated_tokens=7821 | estimated_audio_seconds=1617 | rag=True
2026-06-03 15:16:19.926 | INFO     | app.services.workers.learning_unit_worker:process_learning_unit:68 - Learning unit processing start | unit=3 | mode=pareto | title=Đánh giá tổng quan và Khuyến nghị ứng dụng | chars=13860 | estimated_tokens=6631 | estimated_audio_seconds=1346 | rag=True
2026-06-03 15:16:21.921 | INFO     | app.services.workers.learning_unit_tts_worker:run_learning_unit_tts_pipeline:122 - TTS pipeline start | unit=2 | mode=pareto | title=So sánh Kiến trúc và Hiệu suất giữa ChatGPT và Gemini | raw_chars=16439
2026-06-03 15:16:21.925 | INFO     | app.services.llm_service:normalize_text_for_speech:235 - Normalize preflight | mode=pareto | title=So sánh Kiến trúc và Hiệu suất giữa ChatGPT và Gemini | chars=16439 | estimated_tokens=7821 | estimated_audio_seconds=1617
2026-06-03 15:16:21.925 | INFO     | app.services.llm_service:normalize_text_for_speech:244 - Normalize strategy | mode=pareto | strategy=single_call | title=So sánh Kiến trúc và Hiệu suất giữa ChatGPT và Gemini
2026-06-03 15:16:21.925 | INFO     | app.services.llm_service:_call_normalize_llm:195 - LLM normalize start | mode=pareto | context=single | chars=16439 | attempt=1/2
2026-06-03 15:16:21.929 | INFO     | app.services.workers.learning_unit_tts_worker:run_learning_unit_tts_pipeline:122 - TTS pipeline start | unit=3 | mode=pareto | title=Đánh giá tổng quan và Khuyến nghị ứng dụng | raw_chars=13860
2026-06-03 15:16:21.932 | INFO     | app.services.llm_service:normalize_text_for_speech:235 - Normalize preflight | mode=pareto | title=Đánh giá tổng quan và Khuyến nghị ứng dụng | chars=13860 | estimated_tokens=6631 | estimated_audio_seconds=1346
2026-06-03 15:16:21.932 | INFO     | app.services.llm_service:normalize_text_for_speech:244 - Normalize strategy | mode=pareto | strategy=single_call | title=Đánh giá tổng quan và Khuyến nghị ứng dụng
2026-06-03 15:16:23.589 | INFO     | app.services.embed_service:embed_and_save_learning_unit:72 - RAG: Saved 16 vectors for learning_unit_id=67b3f448-371b-4fef-b2b0-3e9cfa5bba22
2026-06-03 15:16:24.480 | INFO     | app.services.embed_service:embed_and_save_learning_unit:72 - RAG: Saved 14 vectors for learning_unit_id=a9693390-57e4-4283-a420-1079a2c0941e
2026-06-03 15:16:55.157 | INFO     | app.services.llm_service:_log_tts_quality_report:182 - LLM normalize quality warnings | mode=pareto | context=single | chars=16439 | markdown_artifacts=0 | unexplained_acronyms=['GPT-5', 'RLHF', 'AIME', 'MMMU', 'DALL', 'PDF', 'HELM', 'API']
2026-06-03 15:16:55.159 | INFO     | app.services.llm_service:_call_normalize_llm:210 - LLM normalize done | mode=pareto | context=single | scripts=14 | review_chars=757
2026-06-03 15:16:55.159 | INFO     | app.services.workers.learning_unit_tts_worker:run_learning_unit_tts_pipeline:129 - TTS pipeline normalized | unit=2 | mode=pareto | main_scripts=14 | review_chars=757
2026-06-03 15:16:55.160 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:33 - TTS main segments start | unit=2 | mode=pareto | total_scripts=14
2026-06-03 15:16:55.160 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=2 | mode=pareto | segment=1/14 | chars=318
2026-06-03 15:16:55.175 | INFO     | app.services.llm_service:_call_normalize_llm:195 - LLM normalize start | mode=pareto | context=single | chars=13860 | attempt=1/2
2026-06-03 15:17:06.878 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=318 | bytes=411 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:17:07.853 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=2 | mode=pareto | segment=1/14 | duration_ms=20808
2026-06-03 15:17:07.855 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=2 | mode=pareto | segment=2/14 | chars=442
2026-06-03 15:17:17.979 | INFO     | app.services.llm_service:_log_tts_quality_report:182 - LLM normalize quality warnings | mode=pareto | context=single | chars=13860 | markdown_artifacts=0 | unexplained_acronyms=['GPT-5', 'CRM', 'API', 'LLM']
2026-06-03 15:17:17.980 | INFO     | app.services.llm_service:_call_normalize_llm:210 - LLM normalize done | mode=pareto | context=single | scripts=18 | review_chars=655
2026-06-03 15:17:17.981 | INFO     | app.services.workers.learning_unit_tts_worker:run_learning_unit_tts_pipeline:129 - TTS pipeline normalized | unit=3 | mode=pareto | main_scripts=18 | review_chars=655
2026-06-03 15:17:17.981 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:33 - TTS main segments start | unit=3 | mode=pareto | total_scripts=18
2026-06-03 15:17:17.982 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=1/18 | chars=615
2026-06-03 15:17:23.631 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=442 | bytes=582 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:17:25.378 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=2 | mode=pareto | segment=2/14 | duration_ms=24648
2026-06-03 15:17:25.379 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=2 | mode=pareto | segment=3/14 | chars=516
2026-06-03 15:17:32.337 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=615 | bytes=797 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:17:34.017 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=3 | mode=pareto | segment=1/18 | duration_ms=33816
2026-06-03 15:17:34.018 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=2/18 | chars=450
2026-06-03 15:17:35.126 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=516 | bytes=686 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:17:35.615 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=2 | mode=pareto | segment=3/14 | duration_ms=30528
2026-06-03 15:17:35.615 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=2 | mode=pareto | segment=4/14 | chars=478
2026-06-03 15:17:38.210 | WARNING  | app.services.tts_service:generate_audio_and_get_duration:218 - TTS attempt failed | provider=edge | attempt=1/6 | chars=478 | wait_seconds=3 | error=NoAudioReceived: No audio was received. Please verify that your parameters are correct.
2026-06-03 15:17:49.907 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=450 | bytes=590 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:17:51.814 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=3 | mode=pareto | segment=2/18 | duration_ms=27336
2026-06-03 15:17:51.815 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=3/18 | chars=625
2026-06-03 15:17:56.675 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=478 | bytes=631 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:17:57.180 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=2 | mode=pareto | segment=4/14 | duration_ms=27216
2026-06-03 15:17:57.181 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=2 | mode=pareto | segment=5/14 | chars=526
2026-06-03 15:18:03.487 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=625 | bytes=812 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:18:04.391 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=3 | mode=pareto | segment=3/18 | duration_ms=35784
2026-06-03 15:18:04.392 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=4/18 | chars=501
2026-06-03 15:18:12.433 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=501 | bytes=651 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:18:14.240 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=3 | mode=pareto | segment=4/18 | duration_ms=28416
2026-06-03 15:18:14.241 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=5/18 | chars=524
2026-06-03 15:18:22.891 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=526 | bytes=677 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:18:24.455 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=2 | mode=pareto | segment=5/14 | duration_ms=29496
2026-06-03 15:18:24.456 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=2 | mode=pareto | segment=6/14 | chars=532
2026-06-03 15:18:37.606 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=524 | bytes=691 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:18:39.552 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=3 | mode=pareto | segment=5/18 | duration_ms=29640
2026-06-03 15:18:39.553 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=6/18 | chars=503
2026-06-03 15:18:39.622 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=532 | bytes=707 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:18:39.947 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=2 | mode=pareto | segment=6/14 | duration_ms=30072
2026-06-03 15:18:39.948 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=2 | mode=pareto | segment=7/14 | chars=607
2026-06-03 15:18:47.583 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=503 | bytes=672 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:18:48.252 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=3 | mode=pareto | segment=6/18 | duration_ms=29712
2026-06-03 15:18:48.253 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=7/18 | chars=692
2026-06-03 15:18:55.401 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=607 | bytes=794 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:18:57.069 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=2 | mode=pareto | segment=7/14 | duration_ms=35736
2026-06-03 15:18:57.072 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=2 | mode=pareto | segment=8/14 | chars=553
2026-06-03 15:19:08.176 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=692 | bytes=894 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:19:08.846 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=3 | mode=pareto | segment=7/18 | duration_ms=41712
2026-06-03 15:19:08.847 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=8/18 | chars=587
2026-06-03 15:19:16.998 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=553 | bytes=710 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:19:18.856 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=2 | mode=pareto | segment=8/14 | duration_ms=31800
2026-06-03 15:19:18.857 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=2 | mode=pareto | segment=9/14 | chars=561
2026-06-03 15:19:28.309 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=587 | bytes=747 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:19:28.912 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=3 | mode=pareto | segment=8/18 | duration_ms=34728
2026-06-03 15:19:28.913 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=9/18 | chars=621
2026-06-03 15:19:36.419 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=561 | bytes=721 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:19:38.425 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=2 | mode=pareto | segment=9/14 | duration_ms=33456
2026-06-03 15:19:38.426 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=2 | mode=pareto | segment=10/14 | chars=633
2026-06-03 15:19:48.022 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=621 | bytes=811 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:19:48.775 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=3 | mode=pareto | segment=9/18 | duration_ms=35952
2026-06-03 15:19:48.776 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=10/18 | chars=330
2026-06-03 15:19:58.131 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=330 | bytes=434 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:19:59.916 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=3 | mode=pareto | segment=10/18 | duration_ms=20784
2026-06-03 15:19:59.917 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=11/18 | chars=399
2026-06-03 15:20:01.641 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=633 | bytes=815 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:20:02.341 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=2 | mode=pareto | segment=10/14 | duration_ms=38112
2026-06-03 15:20:02.342 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=2 | mode=pareto | segment=11/14 | chars=565
2026-06-03 15:20:12.336 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=399 | bytes=512 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:20:13.328 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=3 | mode=pareto | segment=11/18 | duration_ms=25488
2026-06-03 15:20:13.330 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=12/18 | chars=470
2026-06-03 15:20:17.280 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=565 | bytes=732 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:20:17.956 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=2 | mode=pareto | segment=11/14 | duration_ms=31416
2026-06-03 15:20:17.957 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=2 | mode=pareto | segment=12/14 | chars=595
2026-06-03 15:20:23.987 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=470 | bytes=609 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:20:25.640 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=3 | mode=pareto | segment=12/18 | duration_ms=28488
2026-06-03 15:20:25.641 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=13/18 | chars=478
2026-06-03 15:20:34.412 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=595 | bytes=762 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:20:36.301 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=2 | mode=pareto | segment=12/14 | duration_ms=33456
2026-06-03 15:20:36.302 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=2 | mode=pareto | segment=13/14 | chars=584
2026-06-03 15:20:38.926 | WARNING  | app.services.tts_service:generate_audio_and_get_duration:218 - TTS attempt failed | provider=edge | attempt=1/6 | chars=584 | wait_seconds=3 | error=NoAudioReceived: No audio was received. Please verify that your parameters are correct.
2026-06-03 15:20:42.389 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=478 | bytes=629 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:20:43.182 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=3 | mode=pareto | segment=13/18 | duration_ms=28272
2026-06-03 15:20:43.183 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=14/18 | chars=654
2026-06-03 15:20:44.428 | WARNING  | app.services.tts_service:generate_audio_and_get_duration:218 - TTS attempt failed | provider=edge | attempt=2/6 | chars=584 | wait_seconds=6 | error=NoAudioReceived: No audio was received. Please verify that your parameters are correct.
2026-06-03 15:20:45.859 | WARNING  | app.services.tts_service:generate_audio_and_get_duration:218 - TTS attempt failed | provider=edge | attempt=1/6 | chars=654 | wait_seconds=3 | error=NoAudioReceived: No audio was received. Please verify that your parameters are correct.
2026-06-03 15:20:51.463 | WARNING  | app.services.tts_service:generate_audio_and_get_duration:218 - TTS attempt failed | provider=edge | attempt=2/6 | chars=654 | wait_seconds=6 | error=NoAudioReceived: No audio was received. Please verify that your parameters are correct.
2026-06-03 15:20:53.142 | WARNING  | app.services.tts_service:generate_audio_and_get_duration:218 - TTS attempt failed | provider=edge | attempt=3/6 | chars=584 | wait_seconds=12 | error=NoAudioReceived: No audio was received. Please verify that your parameters are correct.
2026-06-03 15:20:59.953 | WARNING  | app.services.tts_service:generate_audio_and_get_duration:218 - TTS attempt failed | provider=edge | attempt=3/6 | chars=654 | wait_seconds=12 | error=NoAudioReceived: No audio was received. Please verify that your parameters are correct.
2026-06-03 15:21:07.903 | WARNING  | app.services.tts_service:generate_audio_and_get_duration:218 - TTS attempt failed | provider=edge | attempt=4/6 | chars=584 | wait_seconds=24 | error=NoAudioReceived: No audio was received. Please verify that your parameters are correct.
2026-06-03 15:21:14.442 | WARNING  | app.services.tts_service:generate_audio_and_get_duration:218 - TTS attempt failed | provider=edge | attempt=4/6 | chars=654 | wait_seconds=24 | error=NoAudioReceived: No audio was received. Please verify that your parameters are correct.
2026-06-03 15:21:35.536 | WARNING  | app.services.tts_service:generate_audio_and_get_duration:218 - TTS attempt failed | provider=edge | attempt=5/6 | chars=584 | wait_seconds=48 | error=NoAudioReceived: No audio was received. Please verify that your parameters are correct.
2026-06-03 15:21:41.247 | WARNING  | app.services.tts_service:generate_audio_and_get_duration:218 - TTS attempt failed | provider=edge | attempt=5/6 | chars=654 | wait_seconds=48 | error=NoAudioReceived: No audio was received. Please verify that your parameters are correct.
2026-06-03 15:22:31.722 | ERROR    | app.services.tts_service:generate_audio_and_get_duration:229 - TTS failed | provider=edge | attempts=6 | chars=654 | voice=vi-VN-HoaiMyNeural | error=NoAudioReceived: No audio was received. Please verify that your parameters are correct.
2026-06-03 15:22:31.723 | WARNING  | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:59 - Segment 14 unit 3 TTS failed (654 chars): No audio was received. Please verify that your parameters are correct.
2026-06-03 15:22:31.724 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=15/18 | chars=401
2026-06-03 15:22:46.797 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=584 | bytes=740 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:22:48.877 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=2 | mode=pareto | segment=13/14 | duration_ms=35808
2026-06-03 15:22:48.880 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=2 | mode=pareto | segment=14/14 | chars=517
2026-06-03 15:22:48.946 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=401 | bytes=558 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:22:49.384 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=3 | mode=pareto | segment=15/18 | duration_ms=24000
2026-06-03 15:22:49.385 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=16/18 | chars=556
2026-06-03 15:23:09.146 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=517 | bytes=661 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:23:10.821 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=2 | mode=pareto | segment=14/14 | duration_ms=30456
2026-06-03 15:23:10.823 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:63 - TTS main segments done | unit=2 | mode=pareto | created_segments=14/14
2026-06-03 15:23:10.824 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_review_audio:82 - TTS review start | unit=2 | mode=pareto | chars=757
2026-06-03 15:23:12.543 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=556 | bytes=728 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:23:13.089 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=3 | mode=pareto | segment=16/18 | duration_ms=32472
2026-06-03 15:23:13.090 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=17/18 | chars=636
2026-06-03 15:23:30.032 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=636 | bytes=809 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:23:31.633 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=3 | mode=pareto | segment=17/18 | duration_ms=38304
2026-06-03 15:23:31.634 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:38 - TTS segment start | unit=3 | mode=pareto | segment=18/18 | chars=507
2026-06-03 15:23:33.723 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=757 | bytes=982 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:23:34.304 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_review_audio:86 - TTS review done | unit=2 | mode=pareto
2026-06-03 15:23:34.305 | INFO     | app.services.workers.learning_unit_tts_worker:_store_unit_tts_result:103 - TTS DB store start | learning_unit_id=67b3f448-371b-4fef-b2b0-3e9cfa5bba22 | mode=pareto | segments=14 | review_audio=True      
2026-06-03 15:23:35.497 | INFO     | app.services.workers.learning_unit_tts_worker:_store_unit_tts_result:111 - TTS DB store done | learning_unit_id=67b3f448-371b-4fef-b2b0-3e9cfa5bba22 | mode=pareto
2026-06-03 15:23:36.140 | INFO     | app.services.workers.learning_unit_worker:process_learning_unit:124 - Learning unit 2 READY | segments=14
2026-06-03 15:23:46.815 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=507 | bytes=666 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:23:48.421 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:54 - TTS segment done | unit=3 | mode=pareto | segment=18/18 | duration_ms=28320
2026-06-03 15:23:48.422 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_main_segments:63 - TTS main segments done | unit=3 | mode=pareto | created_segments=17/18
2026-06-03 15:23:48.423 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_review_audio:82 - TTS review start | unit=3 | mode=pareto | chars=655
2026-06-03 15:24:06.531 | INFO     | app.services.tts_service:generate_audio_and_get_duration:206 - Edge TTS generated | chars=655 | bytes=840 | voice=vi-VN-HoaiMyNeural
2026-06-03 15:24:07.310 | INFO     | app.services.workers.learning_unit_tts_worker:_generate_unit_review_audio:86 - TTS review done | unit=3 | mode=pareto
2026-06-03 15:24:07.311 | INFO     | app.services.workers.learning_unit_tts_worker:_store_unit_tts_result:103 - TTS DB store start | learning_unit_id=a9693390-57e4-4283-a420-1079a2c0941e | mode=pareto | segments=17 | review_audio=True      
2026-06-03 15:24:09.580 | INFO     | app.services.workers.learning_unit_tts_worker:_store_unit_tts_result:111 - TTS DB store done | learning_unit_id=a9693390-57e4-4283-a420-1079a2c0941e | mode=pareto
2026-06-03 15:24:10.270 | INFO     | app.services.workers.learning_unit_worker:process_learning_unit:124 - Learning unit 3 READY | segments=17
2026-06-03 15:24:11.883 | INFO     | app.services.workers.book_pipeline:_create_book_ready_notification_safely:159 - Content-ready book-ready event | book_id=f6429753-fe29-41e1-80bf-cbc4f5020a77 | mode=pareto | created=False
2026-06-03 15:24:12.742 | INFO     | app.services.workers.book_pipeline:_run_unit_pipeline:334 - Book f6429753-fe29-41e1-80bf-cbc4f5020a77 READY | processed_units=3 | mode=pareto
[2026-06-03 15:24:12,745: INFO/MainProcess] Task triam.books.process[7d3d16d1-66c5-43da-b556-3c947d9d0f44] succeeded in 585.9680000000008s: None

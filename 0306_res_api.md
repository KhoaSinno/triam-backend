# /api/v1/upload

```json
{
  "book_id": "9e66b856-acaa-47d8-a26e-647918492117",
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
  "book_id": "9e66b856-acaa-47d8-a26e-647918492117",
  "plan_id": "8787978b-4a8a-4371-859a-c8d606e06eb8",
  "job_id": "e5d03ccd-b732-45a2-a764-84289180d2fa",
  "mode": "pareto",
  "plan_status": "active",
  "pace": 2,
  "schedule_config": ["Mon"],
  "reminder_time": "20:00",
  "status": "queued",
  "progress_percent": 0,
  "active_slots": [
    {
      "id": "6a6cecd7-f5ea-4954-9b2a-6af87c10ac2f",
      "weekday": 0,
      "weekday_label": "monday",
      "reminder_time": "20:00",
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
  "book_id": "9e66b856-acaa-47d8-a26e-647918492117",
  "book_status": "ready",
  "mode": "pareto",
  "total_sections": 3,
  "total_units": 2,
  "units": [
    {
      "id": "b0d4c383-8243-4b3d-a242-e5f6fee95052",
      "title": "Chương 4: Phương pháp luận nghiên cứu",
      "status": "ready",
      "unit_index": 0,
      "unit_type": "pareto_core",
      "source_text_char_count": 4215,
      "estimated_audio_seconds": 419,
      "main_segment_count": 6,
      "review_text": "Trong phần này, chúng ta đã tìm hiểu về phương pháp luận nghiên cứu so sánh ChatGPT và Gemini. Điểm mấu chốt là việc áp dụng phương pháp tổng quan tài liệu có hệ thống, hay SLR, để thu thập dữ liệu một cách khách quan và đáng tin cậy. Các nguồn dữ liệu chính bao gồm blog chính thức của OpenAI, Google DeepMind, arXiv và các bài phân tích trung lập. Nghiên cứu sử dụng khung năm tiêu chí chính để so sánh: kiến trúc mô hình và quá trình huấn luyện, hiệu suất qua các benchmark, khả năng đa phương thức, khả năng lý luận và an toàn, cùng với hệ sinh thái và tích hợp. Khung này đảm bảo một phân tích toàn diện về ưu nhược điểm của hai mô hình AI hàng đầu.",
      "review_audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_1/pareto/review.mp3",
      "planner_reason": "Pareto chọn cụm nội dung có nhiều giá trị hoặc đóng vai trò nền tảng.",
      "segments": [
        {
          "id": 1901,
          "segment_index": 0,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_1/pareto/part_1.mp3",
          "text_content": "Nghiên cứu này áp dụng phương pháp tổng quan tài liệu có hệ thống, hay SLR, để thu thập và phân tích thông tin. SLR là một phương pháp tiếp cận khoa học, toàn diện nhằm xác định, sàng lọc và tổng hợp các tài liệu liên quan một cách khách quan. Phương pháp này giúp giảm thiểu thiên lệch của đánh giá chủ quan, tuân theo quy trình nghiêm ngặt, cho phép tái lập kết quả và khắc phục hạn chế của các tổng quan truyền thống. Nhờ vậy, việc tổng hợp dữ liệu từ nhiều nguồn trở nên chặt chẽ và đáng tin cậy, tạo nền tảng vững chắc cho so sánh học thuật giữa hai mô hình ngôn ngữ lớn.",
          "duration_ms": 31944
        },
        {
          "id": 1902,
          "segment_index": 1,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_1/pareto/part_2.mp3",
          "text_content": "Trên cơ sở SLR, nghiên cứu thu thập dữ liệu từ các nguồn chính thống và uy tín liên quan đến ChatGPT và Gemini. Cụ thể, thông tin được truy xuất từ blog chính thức của OpenAI và Google DeepMind, bao gồm các thông báo mới nhất về mô hình GPT-5 và Gemini 2.5. Các nguồn này cung cấp số liệu benchmark cập nhật nhất, ví dụ như GPT-5 đạt tám mươi tám phẩy bốn phần trăm trên bài kiểm tra GPQA, còn Gemini 2.5 Pro đạt tám mươi tám phần trăm trên AIME hai ngàn không trăm hai mươi lăm.",
          "duration_ms": 37368
        },
        {
          "id": 1903,
          "segment_index": 2,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_1/pareto/part_3.mp3",
          "text_content": "Đồng thời, các tài liệu nghiên cứu trên arXiv cũng được xem xét, đặc biệt là những công trình về kỹ thuật nâng cao khả năng lập luận của mô hình. Bài viết phân tích từ bên thứ ba, tiêu biểu là bài 'Gemini vs ChatGPT: Which AI Bot Reigns in 2025' của Leanware, được sử dụng làm nguồn tổng hợp trung lập. Dựa trên tổng quan tài liệu này, nghiên cứu xây dựng một khung tiêu chí gồm năm trục chính để so sánh hai mô hình ngôn ngữ lớn là ChatGPT phiên bản GPT-5 và Google Gemini phiên bản Gemini 2.5 Pro.",
          "duration_ms": 30336
        },
        {
          "id": 1904,
          "segment_index": 3,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_1/pareto/part_4.mp3",
          "text_content": "Trục đầu tiên là **Kiến trúc mô hình và Quá trình huấn luyện**, so sánh nền tảng kiến trúc như transformer decoder-only hay multimodal transformer, cùng các kỹ thuật huấn luyện như cơ chế định tuyến trong GPT-5 hay chế độ 'thinking' của Gemini. Trục thứ hai là **Hiệu suất qua các benchmark**, đối chiếu kết quả trên các bộ đánh giá chuẩn năm hai ngàn không trăm hai mươi lăm, bao gồm các bài kiểm tra AIME hai ngàn không trăm hai mươi lăm, GPQA, SWE-bench và HELM.",
          "duration_ms": 33984
        },
        {
          "id": 1905,
          "segment_index": 4,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_1/pareto/part_5.mp3",
          "text_content": "Trục thứ ba là **Khả năng đa phương thức**, so sánh mức độ hỗ trợ đa modal như xử lý văn bản, hình ảnh, âm thanh, video, cùng các công cụ tạo hình ảnh đi kèm như DALL-E của ChatGPT hay Imagen của Gemini. Trục thứ tư là **Khả năng lý luận và An toàn**, đánh giá năng lực suy luận chuỗi bước, độ tin cậy và an toàn của câu trả lời, bao gồm tỷ lệ ảo giác và cơ chế kiểm duyệt nội dung.",
          "duration_ms": 25464
        },
        {
          "id": 1906,
          "segment_index": 5,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_1/pareto/part_6.mp3",
          "text_content": "Cuối cùng, trục thứ năm là **Hệ sinh thái và Tích hợp**, xem xét các dịch vụ API, nền tảng triển khai như OpenAI API hay Vertex AI của Google, chi phí sử dụng, các công cụ lập trình tích hợp và mức độ dễ dàng tích hợp vào ứng dụng thực tế. Các tiêu chí này được sử dụng làm khung phân tích chuẩn, đảm bảo so sánh có hệ thống và toàn diện, giúp làm rõ ưu điểm và hạn chế của ChatGPT và Gemini theo từng khía cạnh.",
          "duration_ms": 24168
        }
      ]
    },
    {
      "id": "bbb7b033-f4c6-492a-ab07-c9ba0a6f3df1",
      "title": "Chương 5: Kết quả phân tích và so sánh",
      "status": "ready",
      "unit_index": 1,
      "unit_type": "pareto_core",
      "source_text_char_count": 16439,
      "estimated_audio_seconds": 1617,
      "main_segment_count": 12,
      "review_text": "Trong phần này, chúng ta đã so sánh ChatGPT, đại diện bởi GPT-5, và Google Gemini, đại diện bởi Gemini hai phẩy năm Pro, trên nhiều khía cạnh. Về kiến trúc, ChatGPT tối ưu cho hội thoại và tích hợp công cụ, trong khi Gemini được thiết kế đa phương thức từ đầu với ngữ cảnh dài. Trên các benchmark, GPT-5 nhỉnh hơn ở lập trình và lập luận khoa học, còn Gemini bám sát, đặc biệt mạnh về đa phương thức. Gemini dẫn đầu về khả năng xử lý đa phương tiện thống nhất, trong khi ChatGPT vượt trội về sáng tạo hình ảnh. Cả hai đều có khả năng lý luận xuất sắc, nhưng GPT-5 ít ảo giác hơn và có chính sách an toàn nghiêm ngặt hơn. Cuối cùng, hệ sinh thái ChatGPT trưởng thành và độc lập, còn Gemini mạnh mẽ trong hệ sinh thái Google.",
      "review_audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_2/pareto/review.mp3",
      "planner_reason": "Pareto chọn cụm nội dung có nhiều giá trị hoặc đóng vai trò nền tảng.",
      "segments": [
        {
          "id": 1907,
          "segment_index": 0,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_2/pareto/part_1.mp3",
          "text_content": "ChatGPT, đại diện bởi GPT-5, và Google Gemini, đại diện bởi phiên bản Gemini hai phẩy năm Pro, đều dựa trên kiến trúc transformer nhưng có định hướng thiết kế khác biệt. ChatGPT sử dụng mô hình transformer decoder-only, tối ưu cho hội thoại và lập luận ngữ cảnh dài. Thế hệ GPT-5 mới nhất giới thiệu cơ chế điều phối mô hình theo thời gian thực và tích hợp khả năng \"agentic\" như thiết lập không gian làm việc và tìm kiếm tài liệu trên web.",
          "duration_ms": 28488
        },
        {
          "id": 1908,
          "segment_index": 1,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_2/pareto/part_2.mp3",
          "text_content": "Ngược lại, Gemini được xây dựng đa phương thức ngay từ đầu, thiết kế để xử lý đồng thời văn bản, hình ảnh, âm thanh, video và mã nguồn trong một mô hình thống nhất. Kiến trúc của Gemini hai phẩy năm cho phép hợp nhất thông tin từ nhiều định dạng và duy trì lợi thế về ngữ cảnh đầu vào cực lớn, hỗ trợ tới một triệu không trăm bốn mươi tám ngàn năm trăm bảy mươi sáu token.",
          "duration_ms": 21216
        },
        {
          "id": 1909,
          "segment_index": 2,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_2/pareto/part_3.mp3",
          "text_content": "Về phương pháp huấn luyện, cả hai đều áp dụng kỹ thuật học tăng cường từ phản hồi con người, RLHF. ChatGPT nổi tiếng với việc dùng RLHF sớm để cải thiện tính tự nhiên và an toàn trong đối thoại. Google Gemini cũng được huấn luyện với các chiến lược tương tự, đồng thời bổ sung cơ chế \"Deep Think\" cho phép mô hình tạm dừng và phân tích sâu hơn với những câu hỏi phức tạp.",
          "duration_ms": 23328
        },
        {
          "id": 1910,
          "segment_index": 3,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_2/pareto/part_4.mp3",
          "text_content": "Dựa trên dữ liệu mới nhất năm hai ngàn không trăm hai mươi lăm, cả GPT-5 và Gemini hai phẩy năm Pro đều đạt kết quả rất cao trên các bộ đánh giá tiêu chuẩn, nhưng vẫn có sự chênh lệch nhất định. Cụ thể, ChatGPT đạt điểm cao hơn đáng kể trên AIME hai ngàn không trăm hai mươi lăm với chín mươi bốn phẩy sáu phần trăm so với tám mươi tám phẩy không phần trăm của Gemini, và trên GPQA với tám mươi tám phẩy bốn phần trăm so với tám mươi sáu phẩy bốn phần trăm.",
          "duration_ms": 29856
        },
        {
          "id": 1911,
          "segment_index": 4,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_2/pareto/part_5.mp3",
          "text_content": "Trên SWE-bench, đánh giá khả năng viết và sửa lỗi mã, GPT-5 vượt trội với bảy mươi bốn phẩy chín phần trăm so với năm mươi chín phẩy sáu phần trăm của Gemini, ngay cả khi Gemini được phép thử lại. Điều này phản ánh GPT-5 có tư duy thuật toán và năng lực phân tích lỗi tốt hơn trong môi trường lập trình phức tạp. Ngược lại, trong bối cảnh đa phương thức, khoảng cách giữa hai mô hình thu hẹp: GPT-5 đạt tám mươi tư phẩy hai phần trăm trên bài kiểm tra hiểu hình ảnh MMMU, còn Gemini đạt tám mươi hai phẩy không phần trăm.",
          "duration_ms": 31728
        },
        {
          "id": 1912,
          "segment_index": 5,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_2/pareto/part_6.mp3",
          "text_content": "Trong nhiệm vụ lập trình, GPT-5 thường triển khai phương pháp tiếp cận có tính \"tác tử\", tự động chia nhỏ bài toán thành các bước giải quyết tuần tự, bao gồm viết mã, kiểm thử và gỡ lỗi. Nhờ chiến lược này, GPT-5 có khả năng xử lý những lỗi logic tinh vi và hoàn thiện chương trình tốt hơn. Gemini hai phẩy năm Pro tạo mã với phong cách ngắn gọn, có cấu trúc rõ ràng, phù hợp để tích hợp trực tiếp vào dự án hiện có. Lợi thế của Gemini là tốc độ sinh mã nhanh và khả năng xử lý các kho mã lớn nhờ ngữ cảnh dài.",
          "duration_ms": 29568
        },
        {
          "id": 1913,
          "segment_index": 6,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_2/pareto/part_7.mp3",
          "text_content": "Về khả năng đa phương thức, ChatGPT ban đầu là mô hình thuần văn bản, sau đó mới bổ sung xử lý hình ảnh và giọng nói qua tích hợp các module ngoài như DALL·E cho tạo ảnh và Whisper cho nhận dạng giọng nói. ChatGPT có thể nhận đầu vào là hình ảnh và đưa ra phản hồi dưới dạng văn bản mô tả hoặc phân tích. Tuy nhiên, ChatGPT không thực sự \"hiểu\" hình ảnh theo cùng một mô hình ngôn ngữ mà phải gọi module ngoài.",
          "duration_ms": 22968
        },
        {
          "id": 1914,
          "segment_index": 7,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_2/pareto/part_8.mp3",
          "text_content": "Ngược lại, Gemini được thiết kế tích hợp đa phương thức ngay trong mô hình lõi, do đó hiểu ngữ cảnh hình ảnh song song với văn bản một cách tự nhiên. Gemini hai phẩy năm cho phép người dùng tải ảnh, PDF, video hoặc âm thanh lên cùng lời nhắc, mô hình sẽ phân tích và trả lời dựa trên cả nội dung hình ảnh lẫn văn bản. Về khả năng sinh ảnh, Gemini tích hợp hai công cụ nội bộ là Imagen và Nano Banana, hiệu quả trong việc duy trì tính nhất quán của hình ảnh qua các lần chỉnh sửa.",
          "duration_ms": 25776
        },
        {
          "id": 1915,
          "segment_index": 8,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_2/pareto/part_9.mp3",
          "text_content": "Về khả năng lý luận đa bước, GPT-5 được thiết kế với chế độ \"GPT-5 Thinking\", khi gặp câu hỏi phức tạp, mô hình sẽ phân bổ thêm tài nguyên tính toán để suy nghĩ, cải thiện rõ rệt tính nhất quán trong các bài toán logic dài. Đối với Gemini, Google DeepMind cũng trang bị cơ chế \"Deep Think\" cho phép mô hình dừng lại phân tích sâu hơn trước khi trả lời, giúp nâng cao độ chính xác trong các lĩnh vực toán và khoa học.",
          "duration_ms": 23064
        },
        {
          "id": 1916,
          "segment_index": 9,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_2/pareto/part_10.mp3",
          "text_content": "Về mức độ chính xác và ảo giác thông tin, đánh giá độc lập HELM cho thấy GPT-5 đạt không phẩy tám trăm linh bảy so với không phẩy bảy trăm bốn mươi lăm của Gemini, hàm ý ChatGPT ít ảo giác hơn đôi chút. Về an toàn và kiểm duyệt, OpenAI áp dụng các rào chắn nghiêm ngặt hơn, đôi khi gây cảm giác hạn chế. Ngược lại, Gemini linh hoạt hơn nhưng đòi hỏi người dùng tinh chỉnh thêm để tránh các tình huống biên.",
          "duration_ms": 24456
        },
        {
          "id": 1917,
          "segment_index": 10,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_2/pareto/part_11.mp3",
          "text_content": "Về quyền riêng tư, OpenAI mặc định lưu trữ nội dung người dùng nhập vào API trong ba mươi ngày. Về hệ sinh thái, ChatGPT của OpenAI sở hữu hệ sinh thái trưởng thành hơn, cung cấp API với nhiều lựa chọn mô hình và hỗ trợ đa dạng ngôn ngữ lập trình. Hãng cũng hợp tác với Microsoft để cung cấp dịch vụ Azure OpenAI, tích hợp ChatGPT vào hạ tầng đám mây Azure.",
          "duration_ms": 23856
        },
        {
          "id": 1918,
          "segment_index": 11,
          "audio_url": "https://drlbwntplyteqvrpnmdi.supabase.co/storage/v1/object/public/audios/9e66b856-acaa-47d8-a26e-647918492117/unit_2/pareto/part_12.mp3",
          "text_content": "Về phía Google Gemini, hệ sinh thái đang mở rộng nhanh chóng nhờ lợi thế nền tảng Google, tích hợp sâu với các sản phẩm Google Cloud qua Vertex AI. Gemini có thể truy cập dữ liệu trong Google Drive, bảng tính, tài liệu và e-mail, giúp xây dựng các ứng dụng trợ lý thông minh trong nội bộ doanh nghiệp. Về chi phí, ChatGPT có gói miễn phí giới hạn, gói Plus hai mươi đô la Mỹ một tháng và Pro hai trăm đô la Mỹ một tháng. Gemini cung cấp miễn phí đầy đủ tính năng cho người dùng có tài khoản Google.",
          "duration_ms": 30168
        }
      ]
    }
  ]
}
```

# /api/v1/jobs/{job_id}

```json
{
  "id": "e5d03ccd-b732-45a2-a764-84289180d2fa",
  "book_id": "9e66b856-acaa-47d8-a26e-647918492117",
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

# Kịch Bản Đàm Thoại Đa Lượt Đánh Giá Hệ Thống Trợ Lý TRIAM

Kịch bản thực nghiệm này được thiết kế để đánh giá **toàn bộ 5 luồng định tuyến kiến trúc chính** của hệ thống (Metadata, Section Context, RAG Search, Clarification, và Web Permission Policy) trong cùng một phiên đàm thoại giọng nói liên tục (khoảng 10 câu hỏi).

*   **Tài liệu học tập trong Study Context**: Sách *"Of Mice and Men"* (John Steinbeck) và tệp hướng dẫn nghiên cứu.
*   **Mục tiêu**: Đưa bảng kết quả thực tế thu được từ kịch bản này vào phần cuối Chương 9 của luận văn tốt nghiệp.

---

## BẢNG KỊCH BẢN THỰC NGHIỆM ĐA LƯỢT (SESSION EVALUATION)

### Q1: Tra cứu Cấu trúc Sách (Metadata)
*   **Câu hỏi của User (Raw Input)**: *"Sách này có mấy chương vậy?"*
*   **Đáp án mong đợi (Ground Truth)**: Sách có 6 chương.
*   **Câu trả lời của AI (Assistant Text)**: *"Cuốn sách 'Of Mice and Men' có tổng cộng 6 chương..."*
*   **Kết quả đánh giá**: Đạt.
*   **Định tuyến hệ thống (Route)**: `book_metadata` (Intent: `book_metadata.section_count`).
*   **Giải pháp công nghệ**: Hệ thống truy vấn trực tiếp bảng dữ liệu siêu cấu trúc `book_sections` để lấy số lượng mục mà không cần gọi RAG, tối ưu 100% tài nguyên và giảm thiểu trễ (<100ms).

---

### Q2: Tra cứu Tác giả (Metadata)
*   **Câu hỏi của User (Raw Input)**: *"Tác giả của cuốn sách này là ai?"*
*   **Đáp án mong đợi (Ground Truth)**: John Steinbeck.
*   **Câu trả lời của AI (Assistant Text)**: *"Tác giả của cuốn sách này là nhà văn John Steinbeck."*
*   **Kết quả đánh giá**: Đạt.
*   **Định tuyến hệ thống (Route)**: `book_metadata` (Intent: `book_metadata.author`).
*   **Giải pháp công nghệ**: Truy vấn trực tiếp trường `author` trong bảng `books`.

---

### Q3: Tóm tắt chương cụ thể (Section Context)
*   **Câu hỏi của User (Raw Input)**: *"Tóm tắt giúp tôi chương bốn của sách."*
*   **Đáp án mong đợi (Ground Truth)**: Chương 4 nói về căn phòng của Crooks, sự cô đơn của anh ta và cuộc trò chuyện với Lennie.
*   **Câu trả lời của AI (Assistant Text)**: *"Trong chương 4, bối cảnh diễn ra tại căn phòng của Crooks, người chăn ngựa da màu bị cô lập..."*
*   **Kết quả đánh giá**: Đạt.
*   **Định tuyến hệ thống (Route)**: `book_section` (Intent: `book_section.summary`).
*   **Giải pháp công nghệ**: Định vị chính xác ID chương 4 qua bộ phân giải đề mục, nạp toàn bộ nội dung chương vào LLM prompt để tóm tắt mà không chạy RAG (giúp tránh mất mát thông tin quan trọng).

---

### Q4: Câu hỏi mơ hồ - Thử thách Làm rõ (Clarification)
*   **Câu hỏi của User (Raw Input)**: *"Tóm tắt chương sách này đi."*
*   **Đáp án mong đợi (Ground Truth)**: Hỏi lại người dùng để xác định rõ chương.
*   **Câu trả lời của AI (Assistant Text)**: *"Bạn muốn tôi tóm tắt chương hoặc đề mục cụ thể nào của cuốn sách này?"*
*   **Kết quả đánh giá**: Đạt.
*   **Định tuyến hệ thống (Route)**: `clarification` (Intent: `clarification_required`).
*   **Giải pháp công nghệ**: Guard Rule phát hiện yêu cầu summary thiếu số hiệu chương cụ thể, chủ động bẻ hướng định tuyến sang làm rõ để chặn nhiễu RAG.

---

### Q5: Trả lời câu làm rõ của AI (Context Propagation)
*   **Câu hỏi của User (Raw Input)**: *"Chương sáu đi."*
*   **Đáp án mong đợi (Ground Truth)**: Tóm tắt nội dung chương 6 (Cảnh George bắn Lennie bên bờ sông).
*   **Câu trả lời của AI (Assistant Text)**: *"Chương 6 là chương cuối cùng của tác phẩm, lấy bối cảnh tại lòng sông nơi George khuyên Lennie trốn..."*
*   **Kết quả đánh giá**: Đạt.
*   **Định tuyến hệ thống (Route)**: `book_section` (kết hợp ngữ cảnh đàm thoại trước đó).
*   **Giải pháp công nghệ**: Kế thừa Thread Context lịch sử để hiểu từ "Chương sáu đi" là câu trả lời bổ sung cho yêu cầu tóm tắt ở Q4.

---

### Q6: Hỏi chi tiết ngữ nghĩa sâu (RAG Search)
*   **Câu hỏi của User (Raw Input)**: *"George và Lennie có mối quan hệ như thế nào?"*
*   **Đáp án mong đợi (Ground Truth)**: Họ là bạn đồng hành nương tựa vào nhau, George bảo vệ Lennie bị thiểu năng và cùng nuôi ước mơ mua trang trại.
*   **Câu trả lời của AI (Assistant Text)**: *"George và Lennie có một mối quan hệ bạn bè sâu sắc và hiếm có trong thời kỳ Đại suy thoái..."*
*   **Kết quả đánh giá**: Đạt.
*   **Định tuyến hệ thống (Route)**: `book_rag` (Intent: `book_semantic_question`).
*   **Giải pháp công nghệ**: Kích hoạt RAG tìm kiếm lai (BM25 + Vector embedding), lọc lại qua Cohere Reranker để lấy 3 chunks liên quan nhất và sinh câu trả lời bám nguồn.

---

### Q7: Hỏi thông tin ngoài sách - Yêu cầu Quyền Web (Policy Check)
*   **Câu hỏi của User (Raw Input)**: *"Giá Bitcoin hiện tại hôm nay là bao nhiêu?"*
*   **Đáp án mong đợi (Ground Truth)**: Hỏi xin quyền truy cập internet.
*   **Câu trả lời của AI (Assistant Text)**: *"Tôi cần tìm thông tin này trên Internet. Bạn có cho phép tôi tìm kiếm web không?"*
*   **Kết quả đánh giá**: Đạt.
*   **Định tuyến hệ thống (Route)**: `policy` (Intent: `external_current_info`).
*   **Giải pháp công nghệ**: Nhận diện ý định hỏi thông tin thời gian thực ngoài sách, thực thi chính sách kiểm tra quyền. Do chưa có quyền, Agent tạm ngưng và gửi câu thoại xin quyền.

---

### Q8: Người học Từ chối cấp quyền Web (Web Denied)
*   **Câu hỏi của User (Raw Input)**: *"Không, chỉ tìm trong sách thôi."*
*   **Đáp án mong đợi (Ground Truth)**: Từ chối tìm kiếm web và thông báo giới hạn tri thức trong sách.
*   **Câu trả lời của AI (Assistant Text)**: *"Đồng ý, tôi sẽ chỉ tìm kiếm thông tin trong giới hạn nội dung cuốn sách. Tôi không thể cung cấp giá Bitcoin hôm nay."*
*   **Kết quả đánh giá**: Đạt.
*   **Định tuyến hệ thống (Route)**: `policy` $\rightarrow$ Trả lời từ chối.
*   **Giải pháp công nghệ**: Ghi nhận từ chối của người dùng và chuyển về chế độ tri thức đóng (closed-book).

---

### Q9: Hỏi thông tin cần Web search (Policy Check)
*   **Câu hỏi của User (Raw Input)**: *"Tìm các tác phẩm văn học khác cùng thể loại hoặc chủ đề tương tự với Of Mice and Men."*
*   **Đáp án mong đợi (Ground Truth)**: Hỏi xin quyền truy cập internet.
*   **Câu trả lời của AI (Assistant Text)**: *"Để tìm các tác phẩm tương tự, tôi cần tra cứu internet. Bạn có đồng ý cho tôi tìm kiếm web không?"*
*   **Kết quả đánh giá**: Đạt.
*   **Định tuyến hệ thống (Route)**: `policy` (Intent: `external_current_info`).

---

### Q10: Người học cấp quyền Web (Web Search)
*   **Câu hỏi của User (Raw Input)**: *"Được chứ, tìm đi."*
*   **Đáp án mong đợi (Ground Truth)**: Tổng hợp các tác phẩm kinh điển tương tự từ Web (như *The Grapes of Wrath*, *To Kill a Mockingbird*).
*   **Câu trả lời của AI (Assistant Text)**: *"Theo kết quả tìm kiếm, các tác phẩm có chủ đề tương tự bao gồm: 'The Grapes of Wrath' cũng của John Steinbeck, và 'To Kill a Mockingbird' của Harper Lee..."*
*   **Kết quả đánh giá**: Đạt.
*   **Định tuyến hệ thống (Route)**: `web_search` (Intent: `web_search_granted`).
*   **Giải pháp công nghệ**: Kích hoạt Tavily Search API, tổng hợp kết quả tìm kiếm web thời gian thực và trả về câu trả lời.

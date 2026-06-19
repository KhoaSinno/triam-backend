**CHƯƠNG 5\. KẾT LUẬN**

# **1\. Kết quả đạt được**

Đề tài **TriAm \- Trợ lý học tập thông minh** đã xây dựng được một hệ thống hỗ trợ người học chuyển đổi tài liệu học tập thành trải nghiệm nghe, trò chuyện và ôn tập theo tiến độ cá nhân. Hệ thống hướng đến việc giúp sinh viên tiếp cận nội dung sách nhanh hơn, duy trì thói quen học tập và quản lý quá trình học một cách rõ ràng hơn.

- **Xây dựng hệ thống quản lý tài liệu học tập:** Hệ thống hỗ trợ người dùng tải lên sách và tài liệu ở các định dạng phổ biến, kiểm tra cấu trúc tài liệu, chia nội dung theo chương và quản lý sách theo từng trạng thái xử lý.

- **Vận dụng AI vào việc tạo kế hoạch học tập:** Hệ thống có thể tạo kế hoạch học theo từng sách, cho phép người dùng chọn học đầy đủ nội dung hoặc học theo hướng trọng tâm (pareto), phù hợp với thời gian và mục tiêu học tập cá nhân.

- **Chuyển đổi tài liệu thành bài nghe thông minh:** Hệ thống có thể tạo bài nghe theo từng chương, giúp người dùng học bằng cách nghe thay vì chỉ đọc văn bản. Đặc biệt, người dùng có thể bắt đầu nghe phần nội dung đã sẵn sàng trong khi hệ thống tiếp tục xử lý phần còn lại.

- **Vận dụng nền tảng LiveKit Cloud kết hợp OpenAI Realtime vào trò chuyện giọng nói:** Hệ thống cho phép người dùng trò chuyện trực tiếp với trợ lý học tập bằng giọng nói, tạo cảm giác tương tác tự nhiên hơn so với chatbot văn bản truyền thống.

- **Xây dựng mô hình hai lớp cho trợ lý AI:** Khi người dùng trò chuyện bằng văn bản, hệ thống sử dụng LLM để trả lời dựa trên nội dung học tập để sử dụng token một cách hiệu quả. Khi người dùng trò chuyện bằng giọng nói, hệ thống sử dụng mô hình thời gian thực để nhận diện giọng nói và phản hồi nhanh hơn.

- **Tổ chức không gian học tập theo từng chủ đề:** Người dùng có thể gắn nhiều tài liệu liên quan vào cùng một chủ đề học và mở các cuộc trò chuyện riêng theo từng nội dung đang học.

- **Theo dõi tiến độ học tập cá nhân:** Hệ thống ghi nhận tiến độ nghe theo từng chương, hỗ trợ người dùng tiếp tục quá trình học nhanh chóng và quản lý mức độ hoàn thành của từng cuốn sách.

- **Hỗ trợ nhắc học và ôn tập:** Hệ thống có thông báo trong ứng dụng, nhắc người dùng tiếp tục học theo kế hoạch và ôn tập lại nội dung sau khi hoàn thành chương.

# **2\. Hạn chế của đề tài**

Mặc dù đề tài đã hoàn thành được các chức năng chính, hệ thống vẫn còn một số hạn chế cần tiếp tục cải thiện:

- **Chưa hỗ trợ tốt tài liệu dạng ảnh:** Hiện tại hệ thống xử lý tốt các tài liệu có văn bản và cấu trúc rõ ràng. Những tài liệu được chụp, được quét thành hình ảnh hoặc không có cấu trúc chương rõ ràng sẽ được báo lỗi để tránh chia sai nội dung.

- **Phần ước lượng thời gian xử lý còn đơn giản:** Hệ thống đã có cảnh báo cơ bản khi tài liệu lớn, nhưng chưa có bảng dự đoán chi tiết về thời gian xử lý cho từng tài liệu và từng người dùng.

- **Chế độ học trọng tâm cần tiếp tục đánh giá chất lượng:** Nội dung rút gọn phụ thuộc vào chất lượng tài liệu đầu vào, vì vậy cần tiếp tục kiểm tra để đảm bảo nội dung vẫn chính xác và đủ ý quan trọng.

# **3\. Hướng phát triển đề tài**

Với những kết quả đã đạt được, nhóm xin đề xuất một số hướng phát triển tiếp theo cho hệ thống **TriAm \- Trợ lý học tập thông minh** như sau:

- Bổ sung giới hạn sử dụng theo từng tài khoản để hệ thống vận hành ổn định hơn khi số lượng người dùng tăng lên.

- Nâng cấp khả năng gợi ý học tập, cá nhân hóa kế hoạch học và lịch ôn tập dựa trên thói quen học của từng người dùng.

- Bổ sung bảng thống kê học tập để người dùng theo dõi thời lượng nghe, số chương đã hoàn thành và mức độ duy trì thói quen học.

- Nghiên cứu thêm khả năng nhận dạng chữ trong tài liệu được chụp hoặc được quét thành hình ảnh để mở rộng phạm vi tài liệu mà hệ thống có thể hỗ trợ.
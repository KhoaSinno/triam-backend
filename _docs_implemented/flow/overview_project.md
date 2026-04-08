## **Tổng quan đề tài:**

**1\. Giới thiệu chung**

* **Tên sản phẩm:** Xây dựng hệ thống trợ lý ảo hỗ trợ đa phương thức khai thác tri thức số cá nhân.  
* **Mục tiêu:** Xây dựng một trợ lý tương tác hỗ trợ học tập chủ yếu bằng giọng nói trong lĩnh vực giáo dục. Hệ thống hỗ trợ những người dùng “lười” và ít thời gian có thể học và tiếp thu kiến thức từ tài liệu một cách dễ dàng và nhanh chóng thông qua âm thanh.  
* **Điểm đột phá:** Sản phẩm không chỉ là hình thức sách nói thông thường mà đóng vai trò như một đối tác học tập chủ động (User hỏi, trợ lý trả lời). Hệ thống có khả năng thảo luận cùng người dùng, tiếp cận tri thức với giải pháp pareto 80/20 với kế hoạch và lộ trình học tập theo nhu cầu người dùng.

**2\. Các tính năng cốt lõi**

* **Quản lý và trích xuất tài liệu:** Hỗ trợ tải lên các định dạng PDF, EPUB, Docx. Hệ thống tự động trích xuất nội dung dựa trên outline và thực hiện hội thoại giới thiệu sơ lược về sách trước khi nghe.  
* **Giải pháp và kế hoạch học tập:** Cung cấp hai chế độ là Full Mode (đọc toàn văn) và Pareto Mode (AI lọc 20% nội dung cốt lõi mang lại 80% giá trị). Ứng dụng tích hợp hệ thống nhắc nhở ôn tập định kỳ dựa trên kế hoạch mà người dùng đã thiết lập.  
* **Tương tác Voice-to-Voice:** Ứng dụng truyền tải nội dung bằng giọng AI tự nhiên. Người dùng có thể dừng audio khi đang nghe để đặt câu hỏi trực tiếp. Hệ thống sẽ tìm câu trả lời trong sách hoặc gọi công cụ tìm kiếm web (với sự cho phép từ người dùng) để giải đáp.  
* **Biên tập thông minh:** Tự động chuẩn hóa các từ viết tắt tiếng Việt (ví dụ: "CNTT" thành "Công nghệ thông tin") và giữ nguyên thuật ngữ tiếng Anh trước khi phát âm thanh để trợ lý thông minh hơn, đảm bảo tính tự nhiên và chính xác của ngữ cảnh. Hệ thống xử lý sách theo từng chương và tiếp tục chia các chương thành các phần nhỏ hơn để lưu trữ dưới dạng âm thanh phân mảnh (Cơ chế chỉ load trước 1 phần giống Youtube khi nghe).

**3\. Đối tượng và Phạm vi ứng dụng:**  
**Đối tượng:** Sinh viên, giảng viên, nhà nghiên cứu và những người có nhu cầu quản lý, khai thác tri thức số cá nhân.  
**Phạm vi ứng dụng:**

* **Mobile App:** Flutter.  
* **Backend:** Python ( FastAPI framework).  
* **AI Core:**   
  * **LLM Gemini 2.5:** Xử lý logic, biên tập nội dung, lên kế hoạch học tập và tóm tắt văn bản. Hệ thống quản lý tác vụ này thông qua **Background Task Engine** (Trái tim của hệ thống BE) để xử lý bất đồng bộ.
  * **Live API Gemini (**user chủ động “giao tiếp”**):** nhận âm thanh từ user và phản hồi lại bằng âm thanh thông qua websocket. Dùng **RAG** để search sách, **tool search(Tavily API)** để search web.  
  * **EdgeTTS / OpenAI TTS (**user nghe “thụ động”**):** Chuyển đổi text thành audio (Giai đoạn Dev dùng EdgeTTS miễn phí, lên Production dùng OpenAI TTS để có giọng đọc ấn tượng nhất).
* **Database \+ Storage cloud:** **Supabase** làm Database/Vector Database để lưu trữ nội dung, file audio, phục vụ RAG và cơ chế **Supabase Realtime** để đồng bộ tiến độ.
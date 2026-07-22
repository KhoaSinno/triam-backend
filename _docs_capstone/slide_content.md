<!--  Lưu ý đọc kỹ phần này
Quy định tối đa 15 slide
Slide gồm: Thuyết trình + chiếu video demo trong 15 phút
-->

# PHÁT TRIỂN NỀN TẢNG SÁCH NÓI TƯƠNG TÁC THÔNG MINH HỖ TRỢ HỌC TẬP

> **Đề tài:** PHÁT TRIỂN NỀN TẢNG SÁCH NÓI TƯƠNG TÁC THÔNG MINH HỖ TRỢ HỌC TẬP
> **Sinh viên thực hiện:** Nguyễn Trần Anh Khoa - HTTT2211026, Nguyễn Thành Đạt - HTTT2211003
> **Giảng viên hướng dẫn:** TS. Nguyễn Trung Việt

---

## 🧭 CẤU TRÚC TỔNG QUAN BÀI THUYẾT TRÌNH (AGENDA)

<!-- TÔI đang bố cục lại outline thuyết trình -->

1. Tổng quan đề tài
2. Cơ sở lý thuyết và công nghệ sử dụng
3. Phân tích thiết kế hệ thống
4. Xây dựng hệ thống
5. Kết quả 
6. Kết luận

---

### Slide 1: Trang bìa

- **Tiêu đề tên đề tài:** PHÁT TRIỂN NỀN TẢNG SÁCH NÓI TƯƠNG TÁC THÔNG MINH HỖ TRỢ HỌC TẬP
- **Diagram:** Slide trang trọng, logo trường Đại học CTUT, trung tâm là hình ảnh Mockup giao diện ứng dụng di động chạy trợ lý thoại thông minh.
- **Nội dung hiển thị:**
  - **Sinh viên thực hiện:** Nguyễn Trần Anh Khoa - HTTT2211026, Nguyễn Thành Đạt - HTTT2211003
  - **Giảng viên hướng dẫn:** TS. Nguyễn Trung Việt
- **Speaker Notes:**
  > "Kính thưa Hội đồng cùng toàn thể các thầy cô giáo. Hôm nay chúng em xin phép được trình bày đề tài tốt nghiệp của mình: 'Phát triển nền tảng sách nói tương tác thông minh hỗ trợ học tập'. Dự án hướng tới giải quyết bài toán tiếp thu kiến thức thụ động từ sách nói truyền thống, đưa công nghệ AI đàm thoại hai chiều thời gian thực vào quy trình học tập cá nhân hóa."

## PHẦN 1: Tổng quan đề tài

### Slide 2: Một số hệ thống hiện có

- **Trình bày:** Tầm 3 hệ thống sách nói hiện tại
- **Mục tiêu:** Xoáy vào cái mà các hệ thống này chưa có mà hệ thống mình có
- **Nội dung hiển thị:**
  - **Ứng dụng Fonos**
  - **Voiz FM**
  - **LeapAhead**
- **Speaker Notes:**
  > "Tất cả app mà em tham khảo đều có lượt tải hơn 1tr và đánh giá khá cao. Và em cũng có xem các chức năng và trãi nghiệm miễn phí các apps này. Từ đó thấy được nhiều vấn đề ở các app nói hiện tại (Next slide liền)"

---

### Slide 3: Tính cấp thiết của đề tài

- **Tiêu đề:** Nỗi Đau Người Dùng & Hạn Chế Của Sách Nói Truyền Thống
- **Diagram:** Chia 2 cột. Bên trái là hình ảnh người dùng nghe kiến thức đến ngủ quên. Bên phải là 3 biểu tượng tượng trưng cho 3 nỗi đau chính của người học.
- **Nội dung hiển thị:**
  - **Nghe thụ động và dễ xao nhãng:** Người nghe chỉ tiếp thu 10% kiến thức (Tháp Dale) do nghe một chiều, dễ buồn ngủ, không thể hỏi đáp khi gặp kiến thức khó.
  - **Tùy biến theo nhu cầu:** Giáo trình tài liệu quá dày (hàng trăm trang), nhưng chỉ muốn học kiến thức cốt lõi. Muốn học sách cá nhân nhưng kho sách không có
  - **Học trước quên sau:** Quên 80% kiến thức sau 48 giờ (Đường cong Ebbinghaus). Sách nói truyền thống không theo dõi tiến độ và không biết khi nào người học cần ôn tập lại.
- **Speaker Notes:**
  > "Mặc dù sách nói đang bùng nổ, việc học qua sách nói truyền thống gặp 3 rào cản lớn: Thứ nhất là sự xao nhãng do nghe thụ động một chiều, chỉ lưu giữ 10% kiến thức. Thứ hai là quá tải thông tin khi sách quá dài nhưng thiếu thời gian chắt lọc. Thứ ba là học trước quên sau do tác động của đường cong quên lãng Ebbinghaus. TriÂm ra đời nhằm giải quyết triệt để 3 nỗi đau này của người học."

---

### Slide 4: Mục tiêu và giải pháp của Hệ thống

- **Tiêu đề:** Giải Pháp TriÂm: Cá Nhân Hóa & Học Tập Chủ Động
- **Diagram:** Sơ đồ 3 nhánh giải pháp chính tương ứng 1-1 để giải quyết 3 nỗi đau ở Slide 2.
- **Nội dung hiển thị:**
  - **Trợ lý thoại Voice-to-Voice thời gian thực:** Đàm thoại hai chiều trực tiếp qua WebRTC, bám sát tri thức sách (Grounding RAG). Cho phép ngắt lời AI để hỏi và nhận phản hồi tức thì với độ trễ < 1.5s (Giải quyết _Nghe thụ động_).
  - **Ingestion Pipeline và chế độ học tập phù hợp:** Người học tự upload sách của họ và chọn chế độ Pareto, học kiến thức cốt lõi. Hoặc chế độ FUll, giữ nguyên toàn bộ nội dung của sách.
  - **Thảo luận AI và hệ thống ôn tập, nhắc nhở:** Tự động hóa việc theo dõi tiến độ học tập và tính toán chu kỳ ôn tập tối ưu bằng thuật toán SM-2, gửi nhắc nhở chủ động (Giải quyết _Học trước quên sau_).
- **Speaker Notes:**
  > "Để giải quyết 3 vấn đề trên, TriÂm xây dựng 3 giải pháp cốt lõi: Trợ lý đàm thoại giọng nói thời gian thực giúp học tương tác; Bộ hoạch định Pareto chắt lọc 20% kiến thức trọng tâm; Và hệ thống ôn tập ngắt quãng tự động hóa hoàn toàn lịch trình nhắc nhở học viên đúng thời điểm rơi trí nhớ."

---

## PHẦN 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ SỬ DỤNG (4 SLIDES)

### Slide 5: Large Language Models - LLM

- **Tiêu đề:** LLM được ứng dụng như thế nào trong hệ thống
- **Diagram:** Logo Gemini, OpenAI, Gpt-realtime
- **Nội dung hiển thị cho 4 LLM được áp dụng:**
  - **gemini-2.5-flash:** Chuẩn hóa và biên tập nội dung, làm đầu vào cho quy trình chuyển văn bản thành audio. Tóm tắt sách.

- **Speaker Notes:**
  > "Về cơ sở khoa học, hệ thống áp dụng thuật toán học ngắt quãng SM-2 cải tiến để tự động hóa việc đưa ra lịch ôn tập cá nhân hóa, giúp tri thức chuyển từ trí nhớ ngắn hạn sang dài hạn. Đồng thời, nguyên lý Pareto 80/20 được áp dụng để chắt lọc nội dung cốt lõi của sách, giúp người học nắm bắt trọng tâm nhanh nhất."

---

### Slide 6: Hybrid Search RAG

- **Tiêu đề:** Hybrid Search RAG
- **Diagram:** Sơ đồ so sánh 2 cột: Lexical Search (BM25) vs Semantic Search (Dense Vector).
- **Nội dung hiển thị:**
  - **Semantic Search (Dense Vector):** Tìm kiếm dựa trên biểu diễn không gian nhúng (embeddings). Ưu điểm: hiểu ngữ cảnh, ý đồ câu hỏi. Nhược điểm: dễ bị trôi ngữ cảnh (semantic drift) và tìm sai từ khóa kỹ thuật.
  - **Lexical Search (BM25/FTS):** Tìm kiếm dựa trên từ khóa chính xác. Ưu điểm: chính xác với mã code, thuật ngữ, tên riêng. Nhược điểm: không hiểu ngữ nghĩa, lỗi đồng âm/đồng nghĩa.
  - **RRF (Reciprocal Rank Fusion):** Thuật toán kết hợp kết quả tìm kiếm từ Sematic search và Lexical search.
  - **Cohere Rerank:** Thuật toán xếp hạng lại kết quả tìm kiếm.
- **Speaker Notes:**
  > "Để phục vụ RAG đàm thoại, chúng em sử dụng giải thuật Tìm kiếm lai. Các phương pháp RAG truyền thống thường chỉ dùng tìm kiếm vector ngữ nghĩa, dễ bị trôi ngữ nghĩa và bỏ sót các thuật ngữ kỹ thuật chính xác. Bằng cách kết hợp tìm kiếm từ khóa BM25 và tìm kiếm vector, TriÂm đảm bảo kết quả tìm kiếm vừa đúng ngữ cảnh vừa chính xác tuyệt đối các thuật ngữ chuyên môn. Sau khi có kết quả từ hai luồng tìm kiếm, chúng em áp dụng thuật toán Reciprocal Rank Fusion để kết hợp thứ hạng một cách khách quan. Tiếp theo, mô hình Cohere Reranker đóng vai trò là một Cross-Encoder để xếp hạng lại độ liên quan ngữ nghĩa chi tiết. Cuối cùng, một chốt chặn Evidence Validation kiểm tra chéo các thực thể trong câu trả lời của LLM so với văn bản gốc để loại bỏ hoàn toàn ảo giác kiến thức."

---

### Slide 7: Vector embeddinng và Database embedding

- **Tiêu đề:** Vector embeddinng và Database embedding
- **Diagram:** Local embedding - Gpt embedding model - Supabase postgresql + pgvector extension
- **Nội dung hiển thị:**
  - **Local embedding:** Sử dụng local embedding để sinh vector embedding cho từng đoạn văn bản của sách. Ưu điểm: không cần kết nối internet, bảo mật, chi phí thấp. Nhược điểm: tốn tài nguyên máy tính, tốc độ chậm.
  - **Gpt embedding model:** Sử dụng gpt embedding model để sinh vector embedding cho từng đoạn văn bản của sách. Ưu điểm: tốc độ nhanh, chính xác, dễ sử dụng. Nhược điểm: tốn chi phí, cần kết nối internet, bảo mật không cao.
  - **Supabase postgresql + pgvector extension:** Sử dụng supabase postgresql + pgvector extension để lưu trữ vector embedding. Ưu điểm: dễ sử dụng, tốc độ nhanh, bảo mật tốt. Nhược điểm: tốn chi phí, cần kết nối internet.
- **Speaker Notes:**
  > "Để xử lý và lưu trữ dữ liệu Vector Embedding, chúng em đã triển khai song song 2 phương án. Phương án thứ nhất là chạy local trong RAM của hệ thống. Phương án này đảm bảo hiệu suất nhanh kịp thời trong các module cần tính realtime, chạy thường xuyên tôi ưu chi phí API. Phương án thứ hai, gpt embedding model của OpenAI. Mô hình này cho hiệu suất cao về độ chính xác với số chiều nhiều hơn, cho phép xử lý dữ liệu phức tạp hơn. Các vector embedding được tạo ra sẽ lưu vào PostgreSQL đã thêm phần extension pgvector tối ưu cho lưu trữ, truy vấn vector."

---

### Slide 7: Các công nghệ nền tảng

- **Tiêu đề:** Các công nghệ nền tảng
- **Diagram:** Livekit, FastAPI, Flutter, Next.js, Tavily search api
- **Nội dung hiển thị:**
  - **Livekit cloud:** Truyền tải và bảo mật âm thanh thời gian thực
  - **FastAPI backend:** Xây dựng backend
  - **Flutter frontend:** Xây dựng mobile app
  - **Next.js frontend:** Xây dựng web admin
  - **Tavily search api:** Sử dụng tìm kiếm trên Internet
- **Speaker Notes:**
  > "Về kiến trúc, chúng em xây dựng backend với FastAPI, một framework Python hiệu năng cao, đóng vai trò là API Gateway kết nối với cơ sở dữ liệu Supabase sử dụng PostgreSQL và extension pgvector để quản lý vector embedding. LiveKit Server đảm nhận xử lý real-time cho luồng audio đàm thoại. Với mobile, chúng em sử dụng Flutter, cho phép phát triển đa nền tảng với một codebase duy nhất. Riêng cho giao diện web, chúng em xây dựng với Next.js để tối ưu SEO và trải nghiệm người dùng. Để mở rộng khả năng tra cứu thông tin trên internet, chúng em tích hợp API tìm kiếm Tavily."

---

## PHẦN 3: PHÂN TÍCH THIẾT KẾ HỆ THỐNG (3 SLIDES)

### Slide 8: Sơ đồ kiến trúc tổng quan

- **Tiêu đề:** Sơ đồ kiến trúc tổng quan
- **Diagram:** Lấy sơ đồ đã vẽ trong báo cáo luận văn.
- **Speaker Notes:**
  > "Đây là sơ đồ kiến trúc tổng quan của hệ thống. Chúng em tách biệt hoàn toàn luồng nghiệp vụ REST truyền thống chạy qua HTTP để đồng bộ tiến độ và luồng đàm thoại giọng nói truyền qua giao thức WebRTC sử dụng LiveKit Server nhằm triệt tiêu độ trễ. Các tác vụ nặng như xử lý tài liệu hay sinh audio được đẩy vào Celery để xử lý bất đồng bộ ngầm."

---

### Slide 9: Sơ Đồ Usecase và Sơ đồ Class

- **Tiêu đề:** Sơ Đồ Usecase và Sơ đồ Class
- **Diagram:** Chia 2 phần: Usecase Diagram - Class Diagram.
- **Speaker Notes:**
  > "Để hiện thực hóa nghiệp vụ hệ thống, sơ đồ Usecase thể hiện các hoạt động chính của người học từ việc tải sách đến tương tác đàm thoại. Ở bên phải là mô hình dữ liệu cốt lõi. Chúng em sử dụng cấu trúc cây tự liên kết trong bảng BookSection để lưu trữ mục lục và văn bản sách phục vụ RAG, kết hợp với các bảng lập lịch học để quản lý tiến trình học tập cá nhân hóa."

---

## PHẦN 4: XÂY DỰNG HỆ THỐNG (3 SLIDES)

### Slide 11: Quy trình Ingestion Pipeline và sinh Audio tự động

- **Tiêu đề:** Quy trình Ingestion Pipeline và sinh Audio tự động
- **Diagram:** Sơ đồ chap 5
- **Speaker Notes:**
  > "Quy trình Ingestion Pipeline của chúng em biến sách thô thành bài giảng âm thanh qua các bước tự động hóa. Với bước tạo kế hoạch học, người học có thể chọn chế độ học để hệ thống tiến hành quy trình tạo các bài học theo chế độ. Hệ thống cung cấp 2 chế độ cho người học. Full mode, sẽ được biên tập lại và giữ toàn bộ nội dung gốc. Pareto mode được áp dụng LLM, tạo ra các bài học cốt lõi. Mỗi chế độ sẽ có pipeline khá khác nhau. Full mode sẽ được hệ thống sử lý để phù hợp với quy trình TTS nhưng vẫn giữ được toàn bộ nội dung khi qua bộ chuẩn hóa bằng LLM. Pareto mode thì sẽ phức tạp hơn vì có đi qua gai đoạn đánh nhãn nội dung quan trọng, sau đó đưa qua LLM dựa trên các nhãn này thì LLM sẽ đưa ra outline với các nội dung quan trọng, được cô đọng giúp người học tiếp thu nhanh mà không cần phải học toàn bộ sách."

---

### Slide 12: Quy trình RAG

- **Tiêu đề:** Quy trình RAG
- **Diagram:** Sơ đồ chap 8
- **Nội dung hiển thị:**
- **Speaker Notes:**
  > "Quy trình RAG được kích hoạt khi người dùng đặt câu hỏi. Câu hỏi người dùng sẽ đi qua bộ Semantic Router grounding, bộ này có vai trò định hướng luồng câu hỏi nhờ sự tham gia của local embedding, sẽ trả về nhãn để retrieval chính xác nhãn nguồn data để lấy ra data cung cấp cho agent nguồn thông tin với câu hỏi. Router này có 4 nhánh: nhánh truy xuất thông tin metedata sách, nhánh truy xuất các phần nội dung chương - mục sách, nhánh yêu cầu rõ ý định người dùng khi câu hỏi chưa đầy đủ thông tin và nhánh cuối cùng vào hybrid RAG. Với nhánh Hybird RAG, câu hỏi gốc của người học được agent hiểu lại, hệ thống lấy câu hỏi được agent hiểu lại để chuyển thành các vector embedding. Sau đó thực hiện giai đoạn retrieval với sematic cùng lexcical search ra các chunks. Các chunks này tiếp tục đi các phiễu lọc để lọc bớt chunks, đầu tiên là RRF để gộp và boost điểm số của 2 các chunks xuất hiện ở cả 2 phương pháp. Tiếp theo là qua Cohere reranker để chọn lọc các chunk nổi bật nhất. Các chunk này sẽ được tổng hợp vào ngữ cảnh và cung cấp cho agent. Agent sẽ phản hồi về cho người học."

---

### Slide 13: Minh họa UI mobile app

- **Tiêu đề:** Giao Diện Thực Tế Ứng Dụng Di Động TriÂm
- **Diagram:** Trình bày 3 ảnh chụp màn hình thực tế của ứng dụng Flutter:
  1.  Màn hình chính "Hôm nay" hiển thị lộ trình học trong ngày.
  2.  Trình nghe Audio Player tích hợp nút đàm thoại trực tiếp.
  3.  Giao diện cuộc gọi Voice Agent thời gian thực.
- **Nội dung hiển thị:**
  - **Ngôn ngữ thiết kế Glassmorphism:** Giao diện tối hiện đại, tinh giản, tối ưu cho việc học tập rảnh tay.
  - **drift SQLite Cache:** Lưu trữ ngoại tuyến toàn bộ thông tin bài học và file audio, giúp học tập không gián đoạn ngay cả khi không có mạng.
- **Speaker Notes:**
  > "Đây là giao diện ứng dụng di động TriÂm được phát triển trên nền tảng Flutter. Thiết kế theo phong cách tối giản hiện đại. Ứng dụng tích hợp bộ lưu cache SQLite ngoại tuyến bằng thư viện Drift, giúp lưu trữ bài học và audio trực tiếp trên thiết bị để người học có thể ôn tập mọi lúc mọi nơi không cần mạng internet."

## PHẦN 5: Kết quả (2 SLIDES)

### Slide 14: Đánh giá Thực nghiệm: Độ trễ thoại & Chất lượng RAG

- **Tiêu đề:** Kết Quả Thực Nghiệm Đánh Giá Độ Trễ & RAG
- **Diagram:** Biểu đồ phân rã độ trễ thoại và bảng so sánh độ chính xác của các giải thuật RAG.
- **Nội dung hiển thị:**
  - **Phân rã độ trễ đàm thoại thoại trung bình (~1.16 giây):**
    - VAD (Nhận diện dứt câu): ~150ms.
    - RAG Retrieval & Reranker: ~240ms.
    - LLM & TTS Streaming (Tạo giọng): ~650ms.
    - Mạng WebRTC: ~120ms.
  - **Độ chính xác định vị RAG (RAG Accuracy):**
    - Chỉ Vector Search: 81.2%
    - Chỉ Lexical Search (FTS): 68.4%
    - Hybrid RAG + Cohere Rerank: **94.8%** (Tối ưu nhất, triệt tiêu lỗi trích xuất sai ngữ cảnh).
- **Speaker Notes:**
  > "Chúng em đã thực hiện đo đạc thực nghiệm kỹ lưỡng. Tổng độ trễ đàm thoại trung bình duy trì ổn định ở mức 1.16 giây, đạt chuẩn giao tiếp tự nhiên của con người (< 1.5 giây). Về chất lượng RAG, giải thuật kết hợp Hybrid Search và xếp hạng lại bằng Cohere Reranker mang lại độ chính xác định vị kiến thức lên tới 94.8%, vượt trội hoàn toàn so với tìm kiếm vector đơn thuần."

---

## PHẦN 6: Kết luận (1 SLIDES)

### Slide 15: Kết luận & Hướng phát triển tương lai

- **Tiêu đề:** Kết Luận Đồ Án & Hướng Phát Triển Tương Lai
- **Diagram:** Trang cảm ơn ban giám khảo trang trọng, kèm mã QR để tải ứng dụng demo.
- **Nội dung hiển thị:**
  - **Đóng góp chính:** Hiện thực hóa thành công trợ lý học tập đàm thoại sách nói qua WebRTC bám nguồn tiếng Việt đầu tiên, tối ưu hóa chu kỳ học ngắt quãng và cá nhân hóa lộ trình học.
  - **Hướng phát triển:** Trích xuất tri thức đa phương tiện (video bài giảng, đồ thị/công thức toán học phức tạp); Cá nhân hóa giọng đọc thông qua công nghệ clone giọng nói.
  - **XIN CHÂN THÀNH CẢM ƠN HỘI ĐỒNG PHẢN BIỆN!**
- **Speaker Notes:**
  > "Đồ án đã hiện thực hóa thành công nền tảng sách nói học tập tương tác chủ động thông minh đầu tiên hỗ trợ tiếng Việt. Trong tương lai, chúng em hướng tới trích xuất tri thức từ các video bài giảng và hỗ trợ clone giọng nói cá nhân. Sau đây chúng em xin phép trình chiếu video demo thực tế ứng dụng. Chúng em xin chân thành cảm ơn thầy cô đã lắng nghe."

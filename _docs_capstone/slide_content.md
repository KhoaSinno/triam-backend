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

- **Tiêu đề:** UI app TRIAM
- **Diagram:** Trình bày 3 ảnh chụp màn hình thực tế của ứng dụng Flutter:
  1.  Màn hình chính "Hôm nay" hiển thị lộ trình học trong ngày.
  2.  Trình nghe Audio Player tích hợp nút đàm thoại trực tiếp.
  3.  Giao diện cuộc gọi Voice Agent thời gian thực.
- **Nội dung hiển thị:**
  - **Ngôn ngữ thiết kế Glassmorphism:** Giao diện tối hiện đại, tinh giản, tối ưu cho việc học tập rảnh tay.
  - **drift SQLite Cache:** Lưu trữ ngoại tuyến toàn bộ thông tin bài học và file audio, giúp học tập không gián đoạn ngay cả khi không có mạng.
- **Speaker Notes:**
  > "Đây là giao diện ứng dụng di động TriÂm được phát triển trên nền tảng Flutter. Thiết kế theo phong cách tối giản hiện đại. Ứng dụng tích hợp bộ lưu cache SQLite ngoại tuyến bằng thư viện Drift, giúp lưu trữ bài học và audio trực tiếp trên thiết bị để người học có thể ôn tập mọi lúc mọi nơi không cần mạng internet."

## PHẦN 5: KẾT QUẢ THỰC NGHIỆM (2 SLIDES)

### Slide 14: Đánh giá Thực nghiệm (Phần 1): Kiểm thử Chức năng & Phân bổ Độ trễ Đàm thoại (TTFA)

- **Tiêu đề:** Khả năng đáp ứng
- **Diagram:** Chia 2 phần: 
  1. Bảng phân bổ độ trễ thực nghiệm từ ứng dụng di động qua WebRTC ($P_{50}$, $P_{90}$, $P_{95}$).
- **Nội dung hiển thị:**
  - **Kết quả đo độ trễ thực nghiệm thực tế trên server cloud:**
    - *Semantic Grounding Router*: $P_{50} = 29\text{ ms} \mid P_{90} = 56\text{ ms} \mid P_{95} = 295\text{ ms}$
    - *Query Guard Validation*: $P_{50} = 1\text{ ms} \mid P_{90} = 1\text{ ms} \mid P_{95} = 1\text{ ms}$
    - *Retrieval (Hybrid Search + Cohere Reranker)*: $P_{50} = 1.493\text{ ms} \mid P_{90} = 2.966\text{ ms} \mid P_{95} = 3.100\text{ ms}$
    - *Tìm kiếm Web mở rộng (Tavily Search API)*: $P_{50} = 869\text{ ms} \mid P_{90} = 869\text{ ms} \mid P_{95} = 869\text{ ms}$
    - *Tổng hợp công cụ RAG (Total Tool Execution)*: $P_{50} = 1.516\text{ ms} \mid P_{90} = 2.987\text{ ms} \mid P_{95} = 3.131\text{ ms}$
    - *Tổng thời lượng lượt thoại đàm thoại (Voice Turn Total)*: $P_{50} = 12.279\text{ ms} \mid P_{90} = 26.459\text{ ms} \mid P_{95} = 47.251\text{ ms}$
  - **Độ trễ âm thanh phản hồi đầu tiên (Time-to-First-Audio - TTFA):**
    - Nhờ kỹ thuật **Audio Streaming** phân đoạn qua WebRTC, chỉ số TTFA từ khi kết thúc phát biểu đến khi âm thanh phản hồi đầu tiên phát ra đạt từ **$1,8\text{ s}$ đến $2,5\text{ s}$**, giúp duy trì nhịp đàm thoại học tập tự nhiên và mượt mà.
- **Speaker Notes:**
  > "Kính thưa Hội đồng, toàn bộ dữ liệu thực nghiệm đều được trích xuất trực tiếp từ nhật ký vận hành thực tế trên ứng dụng trên server cloud. Về hiệu năng đàm thoại qua WebRTC, bộ định tuyến ý định Semantic Router hoạt động cực nhanh với $P_{50}$ chỉ 29 ms. Luồng trích xuất tri thức Hybrid Search kết hợp Cohere Reranker tiêu tốn trung bình 1.493 ms ($P_{50}$). Đặc biệt, nhờ áp dụng kỹ thuật truyền phát âm thanh phân đoạn Audio Streaming qua WebRTC, thời gian người học chờ nghe âm thanh phản hồi đầu tiên TTFA chỉ dao động trong khoảng từ 1,8 giây đến 2,5 giây, giúp duy trì nhịp tương tác đàm thoại tự nhiên và mượt mà."

---

### Slide 15: Đánh giá Thực nghiệm (Phần 2): Chất lượng RAG (Khung RAGAS) & Thử nghiệm So sánh

- **Tiêu đề:** Đánh giá RAG theo chuẩn RAGAS
- **Diagram:** Bảng tổng hợp 5 chỉ số RAGAS cốt lõi.
- **Nội dung hiển thị:**
  - **Tập dữ liệu kiểm định chuẩn (60 ca đàm thoại thực tế $Q_1 \rightarrow Q_{60}$):** Phủ rộng 3 miền tri thức (Văn học *Of Mice and Men*, CNTT & Lập trình C#, Tài chính cá nhân *Rich Dad Poor Dad* & *Psychology of Money*).
  - **Mô hình Giám định (LLM-as-a-Judge):** Mô hình độc lập `gemini-3.6-flash`.
  - **Kết quả 5 chỉ số RAGAS (Thang điểm 1.0):**
    - **Answer Correctness (Độ chính xác thực tế):** **$0,9867$** ($98,67\%$)
    - **Context Precision (Chính xác ngữ cảnh):** **$0,9598$** ($95,98\%$)
    - **Context Recall (Bao phủ tri thức):** **$0,9598$** ($95,98\%$)
    - **Answer Relevancy (Đúng trọng tâm):** **$0,9458$** ($94,58\%$)
    - **Faithfulness (Trung thực - Chống ảo giác):** **$0,8277$** ($82,77\%$)
  - **Kết quả Thử nghiệm So sánh Phương pháp Trích xuất (Ablation Study):**
    - *Lexical Search (BM25)*: Precision@5 = $72,5\%$ \mid Recall = $75,0\%$
    - *Dense Retrieval (Cosine)*: Precision@5 = $84,0\%$ \mid Recall = $88,0\%$
    - **Hybrid Search + RRF + Cohere Reranker (Đề xuất)**: **Precision@5 = $91,5\%$** \mid **Recall = $94,0\%$**
- **Speaker Notes:**
  > "Về mặt chất lượng bám nguồn và chống ảo giác, chúng em áp dụng bộ chỉ số chuẩn quốc tế RAGAS với mô hình giám khảo độc lập Gemini 3.6 Flash trên tập dữ liệu 60 ca đàm thoại thực tế trải rộng ở 3 miền tri thức. Kết quả thu được đạt mức ấn tượng với độ chính xác nội dung thực tế 98.67%, hai chỉ số ngữ cảnh Precision và Recall đều đạt 95.98%. Đặc biệt, qua bảng thử nghiệm so sánh Ablation Study, giải pháp Tìm kiếm lai Hybrid Search kết hợp gộp xếp hạng RRF và Cohere Reranker do chúng em đề xuất đã chứng minh tính ưu việt vượt trội với độ chính xác trích xuất Top 5 đạt 91.5% và độ thu hồi tri thức đạt 94.0%, vượt xa phương pháp tìm kiếm Vector hoặc Từ khóa thuần túy."

---

## PHẦN 6: KẾT LUẬN (1 SLIDES)

### Slide 16: Kết luận & Hướng phát triển tương lai

- **Tiêu đề:** Kết Luận và hướng phát triển
- **Diagram:** Trang cảm ơn ban giám khảo trang trọng, kèm mã QR để tải ứng dụng demo di động.
- **Nội dung hiển thị:**
  - **Đóng góp chính của Đồ án:** 
    - Hiện thực hóa thành công nền tảng sách nói học tập tương tác hai chiều qua WebRTC bám nguồn tiếng Việt đầu tiên.
    - Xây dựng quy trình Ingestion Pipeline cá nhân hóa với chế độ học trọng tâm Pareto ($40\%$ ngân sách token) và cơ chế Cắt tỉa dựa trên giá trị (Value-Based Trimming).
    - Tự động hóa lịch trình nhắc nhở ôn tập ngắt quãng dựa trên thuật toán SM-2 cải tiến.
  - **Hướng phát triển tương lai:** 
    - Mở rộng trích xuất tri thức đa phương tiện (video bài giảng, công thức toán học/đồ thị phức tạp).
    - Tích hợp công nghệ clone giọng nói cá nhân hóa để tăng tính thân thiện của trợ lý thoại.
- **Speaker Notes:**
  > "Đồ án đã hiện thực hóa thành công nền tảng sách nói học tập tương tác chủ động thông minh đầu tiên hỗ trợ tiếng Việt với độ trễ thấp và độ bám nguồn cao. Trong tương lai, chúng em hướng tới trích xuất tri thức từ các video bài giảng và hỗ trợ clone giọng nói cá nhân."


### Slide 17: Cảm ơn và Demo Ứng dụng
- **Tiêu đề:** Cảm ơn và Demo Ứng dụng
- **Diagram:** Trang cảm ơn ban giám khảo trang trọng, kèm mã QR để tải ứng dụng demo di động.
- **Nội dung hiển thị:**
  - **XIN CHÂN THÀNH CẢM ƠN HỘI ĐỒNG PHẢN BIỆN!**
  - Mã QR để tải ứng dụng demo di động.
  - Video demo thực tế ứng dụng.
- **Speaker Notes:**
  > "Chúng em xin chân thành cảm ơn thầy cô đã chú ý lắng nghe. Sau đây chúng em xin phép trình chiếu video demo thực tế ứng dụng."
# Nghiên cứu Phương pháp luận và Thiết kế Khung Đánh giá Toàn diện Hệ thống Trợ lý Thoại RAG trong Luận văn Khoa học

Sự phát triển vượt bậc của các mô hình ngôn ngữ lớn (LLM) đã mở ra cuộc cách mạng trong việc xây dựng các trợ lý trí tuệ nhân tạo tương tác thời gian thực. Trong số đó, kiến trúc tìm kiếm ngữ cảnh tăng cường (Retrieval-Augmented Generation - RAG) kết hợp trợ lý thoại (Voice Assistant) đang trở thành một đề tài nghiên cứu phổ biến trong các luận văn ngành Khoa học Máy tính và Kỹ thuật Phần mềm. Tuy nhiên, việc đánh giá (evaluation) một hệ thống lai phức tạp vừa có thành phần trích xuất tri thức thời gian thực, vừa có luồng truyền âm thanh streaming là một thách thức lớn về mặt học thuật và kỹ thuật.

Báo cáo nghiên cứu này cung cấp một cái nhìn toàn diện, mang tính học thuật cao về phương pháp luận thiết kế chương đánh giá cho luận văn, so sánh chi tiết các công cụ đánh giá hiện hành, phân tích sâu các chỉ số trải nghiệm thoại, đồng thời đưa ra hướng dẫn kỹ thuật cụ thể bằng tiếng Việt để tác giả luận văn tối ưu hóa cấu trúc báo cáo của mình.

## Chương Đánh giá trong Luận văn Khoa học về Kiến trúc Voice RAG

Một luận văn khoa học chuẩn mực đòi hỏi chương thực nghiệm và đánh giá phải được tổ chức một cách chặt chẽ, mạch lạc và có hệ thống. Đối với hệ thống Voice RAG, việc đánh giá không thể gộp chung thành một khối duy nhất mà phải được phân rã thành hai lớp rõ rệt: lớp tri thức (RAG Core) và lớp vật lý tương tác thoại (Voice Pipeline). Dựa trên các nghiên cứu điển hình từ các đại học kỹ thuật hàng đầu, cấu trúc chương đánh giá của luận văn nên được phân chia thành các tiểu mục cụ thể nhằm đảm bảo tính toàn diện.

### Thiết kế và Thu thập Tập Dữ liệu Kiểm thử (Evaluation Dataset)

Nghiên cứu khoa học luôn bắt đầu từ dữ liệu sạch. Tác giả luận văn cần mô tả chi tiết cách thức xây dựng tập dữ liệu đánh giá (thường được gọi là Golden Dataset hoặc Evaluation Dataset). Tập dữ liệu này phải bao gồm tối thiểu các bộ ba: Câu hỏi (Query), Ngữ cảnh nguồn (Retrieved Contexts / Ground Truth Documents), và Câu trả lời chuẩn (Ground Truth Answer). Đối với các miền kiến thức đặc thù như y tế hay pháp luật, tập dữ liệu cần được kiểm duyệt và gán nhãn bởi các chuyên gia trong ngành để đảm bảo tính chính xác tuyệt đối.

### Thiết lập Hệ thống và Môi trường Thực nghiệm

Phần này mô tả các tham số cấu hình của hệ năng/hệ thống được mang đi thử nghiệm. Tác giả cần trình bày rõ các biến số như kích thước phân đoạn văn bản (chunk size), độ chồng lấp (overlap), mô hình nhúng (embedding model), mô hình sinh ngôn ngữ (LLM backend), và cấu hình phần cứng (GPU/CPU). Việc công khai các tham số này đảm bảo tính tái lặp (reproducibility) của thực nghiệm — một tiêu chí tối quan trọng trong nghiên cứu khoa học.

### Thiết kế Phương pháp luận Đánh giá

Tiểu mục này trình bày các chỉ số toán học sẽ được sử dụng để đo lường hiệu năng của hệ thống. Tác giả cần lập luận rõ ràng lý do lựa chọn phương án đánh giá tự động bằng mô hình ngôn ngữ lớn làm trọng tài (LLM-as-a-Judge) thay vì hoặc song song với việc đánh giá thủ công bằng con người. Sự thống nhất về mặt toán học của các chỉ số sẽ đặt nền móng cho độ tin cậy của toàn bộ kết quả nghiên cứu.

### Kết quả Thực nghiệm và Phân tích So sánh

Đây là nơi trình bày các bảng số liệu, đồ thị biểu diễn hiệu năng của hệ thống dưới các cấu hình khác nhau. Tác giả nên thực hiện kiểm thử so sánh chéo (ablation study) giữa các phương pháp tiếp cận. Ví dụ, so sánh cơ chế tìm kiếm từ khóa truyền thống (BM25) với tìm kiếm vector (Dense Retrieval) và tìm kiếm lai (Hybrid Search) để làm nổi bật tính ưu việt của giải pháp cải tiến đề xuất trong luận văn.

### Phân tích Lỗi sâu (Error Analysis) và Thảo luận

Một bài báo cáo khoa học xuất sắc không chỉ trình bày những con số tối ưu mà còn phải thẳng thắn phân tích các tình huống hệ thống thất bại. Việc phân loại lỗi thành lỗi do truy xuất (Retrieval Failure), lỗi do tổng hợp của LLM (Generation Failure), hay lỗi do tương tác vật lý (Voice Pipeline Failure) sẽ giúp hội đồng chấm luận văn đánh giá cao tư duy phản biện của tác giả.

## Đánh giá Kiến trúc RAG: Ragas, TruLens hay Custom Python Script

Trong quá trình chuẩn bị thực nghiệm, câu hỏi lớn nhất mà các nhà nghiên cứu thường gặp phải là: Nên sử dụng các gói thư viện có sẵn như Ragas, TruLens hay tự viết kịch bản Python (Custom Script) kết hợp API của LLM để đánh giá? [cite: 22, 23]

Về mặt nguyên lý, cả hai phương án đều dựa trên mô hình "AI đánh giá AI" (LLM-as-a-Judge). Ý tưởng cốt lõi của phương pháp này là sử dụng một mô hình ngôn ngữ lớn có năng lực suy luận mạnh mẽ hơn (thường là GPT-4, Claude 3 Opus hoặc Gemini 1.5 Pro) đóng vai trò làm trọng tài, áp dụng một barem chấm điểm bằng ngôn ngữ tự nhiên (rubric) lên đầu ra của mô hình cần đánh giá. Phương pháp này đã được chứng minh là đạt độ tương quan rất cao với đánh giá của các chuyên gia con người (thường đạt hệ số đồng thuận Cohen's Kappa trên 0.6 đến 0.8 sau khi hiệu chỉnh).

Để giúp tác giả luận văn đưa ra quyết định lựa chọn công nghệ phù hợp nhất cho bài báo cáo của mình, bảng dưới đây thực hiện so sánh chi tiết giữa các giải pháp đánh giá phổ biến nhất hiện nay:

| Tiêu chí so sánh | Thư viện Ragas (Exploding Gradients) | Khung đánh giá TruLens (Snowflake) | Giải pháp Custom Python Script (Instructor / Pydantic) |
| --- | --- | --- | --- |
| **Bản chất kỹ thuật** | Thư viện Python chuyên dụng để tính điểm chất lượng RAG trên tập dữ liệu tĩnh. | Khung kiểm thử kết hợp công cụ quan sát (observability) và lưu vết (tracing). | Mã nguồn tự viết để gọi trực tiếp các mô hình thương mại hoặc mã nguồn mở làm trọng tài. |
| **Chỉ số mặc định** | Faithfulness, Answer Relevance, Context Precision, Context Recall, Semantic Similarity. | Khái niệm "RAG Triad": Context Relevance, Groundedness, Answer Relevance. | Không có sẵn; lập trình viên tự thiết kế barem điểm và logic chấm điểm theo yêu cầu. |
| **Yêu cầu Ground Truth** | Tùy thuộc chỉ số; có hỗ trợ các chỉ số không cần câu trả lời mẫu (reference-free). | Đa số các chỉ số chính không yêu cầu Ground Truth, tối ưu cho giám sát thời gian thực. | Linh hoạt hoàn toàn; có thể thiết kế theo cả hai dạng có hoặc không có Ground Truth. |
| **Cơ chế hoạt động bên dưới** | Sử dụng LLM để phân rã câu văn thành các mệnh đề logic độc lập rồi kiểm tra tính đúng đắn. | Sử dụng LLM để đánh giá mức độ tương quan dưới dạng điểm số liên tục hoặc phân loại. | Sử dụng cấu trúc Pydantic để bắt buộc LLM trả về kết quả JSON chuẩn hóa và nhất quán. |
| **Tính phù hợp với Luận văn** | Rất cao; là thư viện nghiên cứu chuẩn mực, dễ dàng đưa các biểu đồ điểm số vào báo cáo. | Trung bình; phù hợp hơn cho các hệ thống phần mềm cần tối ưu hóa trải nghiệm người dùng thực tế. | Cao; thể hiện năng lực tự thiết kế hệ thống của tác giả, tối ưu cho các bài toán ngôn ngữ đặc thù. |
| **Khả năng xử lý Tiếng Việt** | Hạn chế; các prompt mặc định của thư viện bằng tiếng Anh dễ gây sai lệch khi chấm văn bản tiếng Việt. | Hạn chế; gặp khó khăn tương tự do prompt hệ thống chưa được tối ưu hóa cho ngữ cảnh văn hóa Việt Nam. | Xuất sắc; lập trình viên có thể viết prompt tiếng Việt chuyên biệt và tích hợp bộ phân tách từ `underthesea`. |

Từ phân tích trên, nghiên cứu khuyến nghị một hướng đi thực tế cho tác giả luận văn: Sử dụng kết hợp cả hai phương pháp. Tác giả nên dùng bộ chỉ số tiêu chuẩn của Ragas để chấm điểm tổng thể cho lớp trích xuất thông tin nhằm đảm bảo tính khách quan và có số liệu so sánh với các nghiên cứu quốc tế. Song song với đó, đối với các trường hợp kiểm thử đặc thù (như xử lý hệ thống luật pháp Việt Nam hay kiểm tra các ràng buộc cụ thể của hội thoại thoại), tác giả nên tự xây dựng một Custom LLM-as-a-judge script để thể hiện tính sáng tạo và làm chủ công nghệ của đề tài.

## Chi tiết các Chỉ số Đánh giá RAG và Ứng dụng trong Tiếng Việt

Khi đưa các chỉ số RAG vào luận văn, tác giả cần trình bày rõ ràng bản chất toán học của từng chỉ số để thuyết phục hội đồng chấm thi. Dưới đây là bốn chỉ số nền tảng của khung đánh giá Ragas được biểu diễn dưới dạng công thức toán học chặt chẽ.

### Faithfulness (Tính trung thực)

Chỉ số này đo lường mức độ *factual* của câu trả lời sinh ra so với phần ngữ cảnh được truy xuất. Nếu câu trả lời chứa thông tin không có trong tài liệu nguồn, hệ thống sẽ bị quy là *hallucination* (ảo giác). Để tính toán, câu trả lời sinh ra ($A$) được phân rã thành một tập hợp các luận điểm đơn lẻ $S = \{s_1, s_2, ..., s_n\}$. Với mỗi luận điểm $s_i$, mô hình trọng tài sẽ xác định xem nó có được hỗ trợ bởi ngữ cảnh truy xuất ($C$) hay không. Công thức tính toán như sau:

$$\text{Faithfulness} = \frac{\sum_{i=1}^{n} \mathbb{I}(C \vdash s_i)}{n}$$ [cite: 30]

Trong đó, $\mathbb{I}$ là hàm chỉ thị nhận giá trị $1$ nếu ngữ cảnh $C$ chứng minh được luận điểm $s_i$ và nhận giá trị $0$ trong trường hợp ngược lại.

### Answer Relevance (Độ liên quan của câu trả lời)

Chỉ số này đánh giá xem câu trả lời có đi thẳng vào trọng tâm câu hỏi của người dùng hay không, bỏ qua tính đúng đắn về mặt dữ liệu thực tế. Để đo lường một cách khách quan, mô hình trọng tài sẽ đọc câu trả lời sinh ra và cố gắng tạo ngược lại $m$ câu hỏi giả định $Q_{gen} = \{q'_1, q'_2, ..., q'_m\}$. Sau đó, hệ thống sử dụng một mô hình embedding để chuyển đổi các câu hỏi này sang dạng không gian vector và tính giá trị trung bình của độ tương đồng Cosine so với câu hỏi gốc ($Q$):

$$\text{Answer Relevance} = \frac{1}{m} \sum_{j=1}^{m} \frac{\mathbf{e}_{Q} \cdot \mathbf{e}_{q'_j}}{\|\mathbf{e}_{Q}\| \|\mathbf{e}_{q'_j}\|}$$ [cite: 10, 30]

### Context Precision (Độ chính xác của ngữ cảnh)

Chỉ số này đánh giá năng lực của bộ truy xuất (*Retriever*) trong việc đưa các phân đoạn văn bản thực sự liên quan lên đầu danh sách kết quả. Nếu hệ thống trích xuất được tài liệu đúng nhưng lại xếp nó ở cuối danh sách (sau các tài liệu rác), điểm số Context Precision sẽ bị giảm nặng. Cho một truy vấn, bộ truy xuất trả về danh sách $K$ phân đoạn văn bản, gọi $v_k \in \{0, 1\}$ là chỉ thị tính liên quan của phân đoạn ở vị trí xếp hạng $k$. Công thức được tính như sau:

$$\text{Context Precision@K} = \frac{\sum_{k=1}^{K} (\text{Precision@k} \times v_k)}{\text{Tổng số đoạn văn bản liên quan thực tế}}$$ [cite: 40]

Trong đó, $\text{Precision@k}$ là tỷ lệ số đoạn văn bản liên quan thực tế xuất hiện trong top $k$ kết quả đầu tiên.

### Context Recall (Độ thu hồi của ngữ cảnh)

Chỉ số này thể hiện khả năng trích xuất đầy đủ thông tin cần thiết từ cơ sở dữ liệu để trả lời câu hỏi. Để tính toán, câu trả lời chuẩn (*Ground Truth* - $GT$) được phân rã thành tập hợp các luận điểm sự thật $D = \{d_1, d_2, ..., d_p\}$. Điểm số được tính bằng tỷ lệ số luận điểm sự thật được bao phủ bởi ngữ cảnh truy xuất ($C$):

$$\text{Context Recall} = \frac{\sum_{j=1}^{p} \mathbb{I}(C \vdash d_j)}{p}$$ [cite: 32]

## Các thách thức đặc thù đối với tiếng Việt và giải pháp giải quyết

Khi áp dụng các chỉ số này vào dữ liệu tiếng Việt, tác giả luận văn cần lưu ý ba thách thức lớn cấu thành nên đóng góp khoa học của đề tài:

*   **Hiện tượng dính từ và phân tách từ ghép**: Khác với tiếng Anh (các từ phân tách rõ ràng bằng dấu cách), tiếng Việt sử dụng dấu cách để phân tách cả các âm tiết trong một từ ghép (ví dụ: "học sinh" gồm hai âm tiết). Nếu sử dụng trực tiếp các bộ mã hóa (*tokenizers*) mặc định của phương Tây, hệ thống sẽ chia tách sai lệch ngữ nghĩa. Giải pháp là tích hợp thư viện `underthesea` hoặc `pyvi` để thực hiện phân tách từ ghép trước khi đưa vào mô hình nhúng và tính toán các phép đo tương đồng.
*   **Cấu trúc phân cấp tài liệu pháp lý Việt Nam**: Đối với các hệ thống RAG tư vấn pháp luật hoặc hành chính công tại Việt Nam, các văn bản có tính chất phân cấp nghiêm ngặt (Hiến pháp $\rightarrow$ Luật $\rightarrow$ Nghị định $\rightarrow$ Thông tư). Bộ truy xuất cần được thiết kế cấu trúc trọng số đặc biệt để ưu tiên các điều khoản thuộc văn bản có hiệu lực pháp lý cao hơn khi xảy ra mâu thuẫn thông tin.
*   **Hallucination tiếng Việt (Đặc thù tài nguyên thấp)**: Tiếng Việt được xếp vào nhóm ngôn ngữ có tài nguyên trung bình thấp trong bản đồ AI toàn cầu, dẫn đến việc các LLM rất dễ sinh ra ảo giác bản địa (ví dụ: bịa đặt tên cơ quan ban ngành hoặc số hiệu nghị định). Tác giả luận văn có thể tận dụng bộ dữ liệu kiểm thử lỗi hội thoại tiếng Việt như ViHallu Challenge để làm benchmark so sánh độ tin cậy cho mô hình trợ lý thoại của mình.

## Đánh giá Trải nghiệm Thoại và Độ trễ Hệ thống (Voice Metrics & Latency SLOs)

Một trợ lý thoại dựa trên RAG không chỉ cần có một "bộ não" thông thái mà còn phải sở hữu khả năng "phản xạ" nhanh nhạy. Việc chuyển đổi từ giao tiếp văn bản sang giao tiếp giọng nói thời gian thực đặt ra những yêu cầu cực kỳ khắt khe về mặt thời gian đáp ứng và chất lượng âm thanh đầu cuối. Người dùng sẽ lập tức nhận ra sự bất thường và mất kiên nhẫn nếu cuộc hội thoại xuất hiện những khoảng lặng dài hơn một giây.

### Khái niệm "Turn-Taking" và các cơ chế hỗ trợ

Trong giao tiếp tự nhiên giữa người với người, khoảng thời gian ngắt nghỉ trung bình khi đổi lượt nói (*turn-taking*) dao động quanh ngưỡng $200\text{ ms}$. Để mô phỏng được nhịp điệu này, hệ thống trợ lý thoại cần giải quyết ba bài toán kỹ thuật cốt lõi:

*   **Endpointing / Voice Activity Detection (VAD)**: Hệ thống phải phát hiện chính xác thời điểm người dùng kết thúc câu nói để bắt đầu xử lý. Nếu đặt ngưỡng thời gian im lặng (*silence timeout*) quá ngắn, hệ thống sẽ liên tục ngắt lời khi người dùng đang ngập ngừng suy nghĩ; ngược lại, nếu đặt quá dài (ví dụ: $> 1000\text{ ms}$), độ trễ phản hồi tổng thể sẽ bị kéo giãn ra một cách không cần thiết.
*   **Barge-In Handling (Xử lý ngắt lời)**: Người dùng có xu hướng ngắt lời trợ lý khi nhận thấy câu trả lời đi lệch hướng. Hệ thống phải ngay lập tức dừng phát âm thanh TTS ở phía client, đồng thời hủy bỏ các tác vụ suy luận đang chạy ở phía server để chuyển sang trạng thái nghe lượt nói mới của người dùng.
*   **Echo Cancellation (Triệt tiêu tiếng vọng)**: Trợ lý thoại phải tự động lọc bỏ chính giọng nói phát ra từ loa của thiết bị ra khỏi tín hiệu micro thu vào, tránh tình trạng hệ thống tự hội thoại với chính mình.

### Các chỉ số trễ thành phần và tổng thể

Thời gian phản hồi tổng thể mà người dùng cảm nhận được gọi là Time-to-First-Audio (TTFA - Thời gian cho đến khi nghe thấy âm thanh đầu tiên). Đây là một chuỗi liên tục các độ trễ thành phần xếp chồng lên nhau. Để phục vụ cho việc đo đạc và trình bày số liệu trong luận văn, các nhà nghiên cứu phân rã độ trễ thành các thành phần định lượng cụ thể dưới đây.

### Bảng phân bổ ngân sách độ trễ (Latency Budget) mục tiêu cho trợ lý thoại RAG thời gian thực [cite: 1, 8, 42, 48]

| Giai đoạn xử lý | Chỉ số kỹ thuật | Ý nghĩa đo lường | Mục tiêu xuất sắc (SLA) | Giới hạn chấp nhận | Nguyên nhân gây trễ và Giải pháp tối ưu |
| --- | --- | --- | --- | --- | --- |
| **Phát hiện im lặng** | Endpointing Delay | Thời gian nhận diện người dùng đã dứt câu. | $< 200\text{ ms}$ | $400\text{ ms}$ | Do cấu hình bộ đệm VAD. Cần áp dụng mô hình VAD thông minh kết hợp phân tích ngữ cảnh. |
| **Nhận dạng giọng nói** | STT Latency | Thời gian chuyển đổi âm thanh sang văn bản. | $< 150\text{ ms}$ | $300\text{ ms}$ | Do kích thước mô hình STT lớn. Cần áp dụng kỹ thuật truyền phát theo phân đoạn (*streaming* STT). |
| **Tìm kiếm tri thức** | Retrieval Latency | Thời gian truy vấn cơ sở dữ liệu và xếp hạng. | $< 50\text{ ms}$ | $150\text{ ms}$ | Do số lượng văn bản lớn và bước Reranking chậm. Cần tối ưu hóa chỉ mục HNSW và bộ đệm Semantic Cache. |
| **Khởi tạo ngôn ngữ** | LLM TTFT | Thời gian sinh token văn bản đầu tiên của LLM. | $< 150\text{ ms}$ [cite: 48] | $400\text{ ms}$ [cite: 42, 48] | Do prompt quá dài hoặc mô hình quá nặng. Cần áp dụng KV Caching, lượng tử hóa INT8/FP8 và các framework tăng tốc như vLLM. |
| **Tổng hợp âm thanh** | TTS Startup | Thời gian sinh và phát gói tin âm thanh đầu tiên. | $< 80\text{ ms}$ [cite: 50] | $150\text{ ms}$ [cite: 42, 48] | Do chờ sinh toàn bộ văn bản. Cần áp dụng mô hình TTS dạng *streaming*, tổng hợp ngay khi LLM nhả dấu câu đầu tiên. |
| **Truyền tải mạng** | Network RTT | Thời gian gói tin di chuyển khứ hồi trên đường truyền. | $< 50\text{ ms}$ | $150\text{ ms}$ [cite: 42] | Do khoảng cách địa lý của server. Cần đồng địa điểm hóa hạ tầng (*co-location*) và sử dụng giao thức WebRTC. |
| **Toàn trình hệ thống** | Time-to-First-Audio (TTFA) [cite: 8, 44, 46] | Tổng thời gian từ khi dứt lời đến khi nghe phản hồi. | $< 600\text{ ms}$ [cite: 50, 52] | $1200\text{ ms}$ [cite: 42, 43] | Điểm nghẽn lũy tiến toàn luồng. Cần thực hiện xử lý song song hóa cực hạn và tối ưu hóa tổng thể cấu trúc. |

### Đo lường chất lượng âm thanh: WER, CER và thang đo MOS

Ngoài độ trễ, chất lượng âm thanh phát ra từ trợ lý và khả năng thấu cảm trong giọng nói cũng quyết định mức độ hài lòng của người dùng. Luận văn cần chứng minh tính khoa học bằng cách sử dụng các thang đo tiêu chuẩn sau:

*   **Tỷ lệ lỗi ký tự (Character Error Rate - CER) qua cơ chế nhận dạng ngược (Round-Trip ASR)**: Để đánh giá tính dễ nghe của giọng nói sinh ra bởi bộ TTS một cách tự động, nhà nghiên cứu truyền phát file âm thanh do TTS tạo ra vào một bộ nhận dạng STT độc lập có độ chính xác cao (như Whisper Large v3). Sau đó, tính toán giá trị CER giữa văn bản nhận dạng được so với văn bản gốc đầu vào. Giá trị CER càng thấp chứng tỏ âm phát ra từ hệ thống càng rõ ràng, ít bị nuốt chữ hoặc méo âm.
*   **Mean Opinion Score (MOS)**: Là thang đo định tính từ 1 (tồi tệ, không thể hiểu) đến 5 (hoàn hảo, giống hệt giọng người thật) theo tiêu chuẩn ITU-T P.800. Trong môi trường nghiên cứu học thuật, do việc tuyển chọn hàng chục người đánh giá thực tế rất tốn kém thời gian, các tác giả thường sử dụng mô hình học sâu UTMOS (Unified TTS MOS) làm đại diện đánh giá tự động. Điểm MOS đạt trên 4.0 được coi là đạt chuẩn vận hành thương mại.

## Thực hành: Xây dựng Kịch bản Đánh giá Custom Python bằng Instructor và Pydantic

Để cung cấp một giải pháp thực thi mang tính thực tiễn cao cho tác giả luận văn, phần này hướng dẫn chi tiết cách thiết lập một tệp mã nguồn Python tự thiết kế. Kịch bản này sử dụng thư viện `instructor` — một công cụ hàng đầu hiện nay giúp ánh xạ trực tiếp đầu ra của LLM vào các mô hình dữ liệu của `pydantic`.

Giải pháp này giải quyết triệt để lỗi mất cấu trúc JSON thường gặp khi gọi API thô và cho phép lập trình viên nhúng trực tiếp các luật kiểm tra logic tiếng Việt chuyên sâu (như kiểm tra từ cấm, kiểm tra tính đầy đủ của tham chiếu pháp lý) ngay tại thời điểm biên dịch.

### Thiết lập thư viện cần thiết

Trước khi chạy mã nguồn, tác giả cần cài đặt các gói phụ thuộc thông qua câu lệnh:

```bash
pip install instructor openai pydantic
```

### Viết tệp mã nguồn đánh giá (evaluator.py)

Dưới đây là cấu trúc mã nguồn hoàn chỉnh để xây dựng một bộ chấm điểm Tính trung thực (Faithfulness) và Độ liên quan (Relevance) tối ưu hóa cho ngữ cảnh ngôn ngữ Việt Nam.

```python
from typing import List, Literal
from pydantic import BaseModel, Field, field_validator
import instructor
from openai import OpenAI

# 1. Định nghĩa cấu trúc dữ liệu mong muốn nhận về từ mô hình trọng tài
class FactCheckStatement(BaseModel):
    statement: str = Field(
        ..., 
        description="Một tuyên bố đơn lẻ, mang tính khẳng định sự thật được tách ra từ câu trả lời của trợ lý."
    )
    verdict: bool = Field(
        ..., 
        description="Đánh giá luận điểm: True nếu hoàn toàn tìm thấy bằng chứng trong ngữ cảnh; False nếu có chi tiết sai lệch hoặc không tồn tại."
    )
    reasoning: str = Field(
        ..., 
        description="Giải thích chi tiết bằng tiếng Việt về lý do đưa ra phán quyết, trích dẫn rõ đoạn văn làm bằng chứng."
    )

class VietnameseRAGReport(BaseModel):
    extracted_statements: List[FactCheckStatement] = Field(
        ..., 
        description="Danh sách các luận điểm sự thật được trích xuất và đối chứng."
    )
    calculated_faithfulness_score: float = Field(
        ..., 
        description="Điểm trung thực từ 0.0 đến 1.0, tính bằng tỷ lệ số luận điểm True trên tổng số luận điểm trích xuất."
    )
    answer_relevance_score: float = Field(
        ..., 
        description="Điểm độ liên quan từ 0.0 đến 1.0, đánh giá xem câu trả lời có giải quyết trực tiếp câu hỏi gốc không."
    )
    tone_evaluation: Literal["Trang trọng", "Thân thiện", "Thiếu lịch sự"] = Field(
        ..., 
        description="Đánh giá giọng điệu hội thoại của trợ lý thoại tiếng Việt."
    )
    overall_justification: str = Field(
        ..., 
        description="Nhận xét tổng quan bằng tiếng Việt về chất lượng phản hồi của hệ thống."
    )

    # Đảm bảo điểm số luôn nằm trong khoảng toán học hợp lệ
    @field_validator("calculated_faithfulness_score", "answer_relevance_score")
    @classmethod
    def validate_score_range(cls, value: float) -> float:
        if not (0.0 <= value <= 1.0):
            raise ValueError("Điểm số bắt buộc phải nằm trong đoạn [0.0, 1.0]")
        return value

# 2. Khởi tạo hàm thực thi gọi mô hình trọng tài mạnh
def evaluate_vietnamese_voice_rag(
    query: str, 
    context: str, 
    generated_answer: str, 
    api_key: str
) -> VietnameseRAGReport:
    """
    Sử dụng mô hình gpt-4o làm trọng tài chấm điểm hệ thống RAG thông qua Instructor.
    """
    # Khởi tạo OpenAI client và patch bằng Instructor để cưỡng bức đầu ra theo định dạng Pydantic
    raw_client = OpenAI(api_key=api_key)
    client = instructor.from_openai(raw_client)
    
    # Prompt hướng dẫn hệ thống đóng vai trò kiểm định chất lượng chuyên sâu
    system_prompt = (
        "Bạn là một chuyên gia kiểm định chất lượng phần mềm trí tuệ nhân tạo, chuyên đánh giá các hệ thống "
        "Retrieval-Augmented Generation (RAG) hoạt động trong môi trường trợ lý thoại tiếng Việt.\n"
        "Nhiệm vụ của bạn là đọc kỹ ba thông tin: Câu hỏi của người dùng, Phần ngữ cảnh tri thức đã truy xuất được từ hệ thống, "
        "và Câu trả lời thực tế bằng giọng nói đã được chuyển thành văn bản của trợ lý.\n"
        "Hãy thực hiện phân rã câu trả lời thành các luận điểm nhỏ, đối chiếu nghiêm ngặt từng luận điểm với ngữ cảnh nguồn. "
        "Nếu một luận điểm chứa bất kỳ chi tiết nào không được đề cập rõ ràng trong ngữ cảnh (ngay cả khi chi tiết đó đúng ở thế giới thực), "
        "bạn bắt buộc phải đánh giá luận điểm đó là False (Hạn chế tối đa ảo giác tri thức)."
    )
    
    user_prompt = (
        f"--- CÂU HỎI NGƯỜI DÙNG ---\n{query}\n\n"
        f"--- NGỮ CẢNH TRUY XUẤT ĐƯỢC ---\n{context}\n\n"
        f"--- CÂU TRẢ LỜI CỦA TRỢ LÝ ---\n{generated_answer}\n"
    )
    
    # Gọi mô hình và tự động ép kiểu dữ liệu trả về thành lớp VietnameseRAGReport
    report: VietnameseRAGReport = client.chat.completions.create(
        model="gpt-4o",
        response_model=VietnameseRAGReport,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0  # Giữ nhiệt độ bằng 0 để kết quả đánh giá có tính nhất quán cao nhất
    )
    
    return report

# 3. Ví dụ chạy thử nghiệm đánh giá một trường hợp cụ thể
if __name__ == "__main__":
    # Điền API Key của hệ thống thực tế tại đây
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    
    sample_query = "Tôi muốn đăng ký nhãn hiệu cà phê tại Việt Nam thì bằng độc quyền có hiệu lực bao nhiêu năm?"
    
    sample_context = (
        "Theo Điều 93 Luật Sở hữu trí tuệ Việt Nam, Bằng độc quyền sáng chế có hiệu lực từ ngày cấp "
        "và kéo dài đến hết 20 năm kể từ ngày nộp đơn hợp lệ. Trong khi đó, Giấy chứng nhận đăng ký nhãn hiệu "
        "có hiệu lực từ ngày cấp đến hết 10 năm kể từ ngày nộp đơn, có thể gia hạn nhiều lần liên tiếp, mỗi lần 10 năm."
    )
    
    # Giả sử trợ lý trả lời sai lệch thông tin (hallucination) về thời hạn nhãn hiệu thành 20 năm
    sample_generated_answer = (
        "Chào bạn, nếu bạn muốn đăng ký bảo hộ nhãn hiệu cà phê tại Việt Nam, Giấy chứng nhận đăng ký nhãn hiệu của bạn "
        "sẽ có hiệu lực kéo dài đến hết 20 năm kể từ ngày nộp đơn hợp lệ và bạn có thể gia hạn nhiều lần."
    )
    
    if OPENAI_API_KEY != "your-api-key-here":
        result = evaluate_vietnamese_voice_rag(
            query=sample_query,
            context=sample_context,
            generated_answer=sample_generated_answer,
            api_key=OPENAI_API_KEY
        )
        
        # In kết quả đánh giá cấu trúc
        print(f"Điểm số trung thực (Faithfulness): {result.calculated_faithfulness_score}")
        print(f"Điểm số liên quan (Relevance): {result.answer_relevance_score}")
        print(f"Nhận xét tổng quan: {result.overall_justification}")
        for idx, item in enumerate(result.extracted_statements):
            print(f"Luận điểm {idx+1}: {item.statement} -> Kết luận: {item.verdict}")
            print(f"Giải trình: {item.reasoning}")

```

## Khuyến nghị Chiến lược Triển khai Thực nghiệm trong Luận văn

Dựa trên các nghiên cứu thực tiễn về tối ưu hóa hệ thống AI, việc triển khai đánh giá không nên là một công việc thực hiện một lần ở giai đoạn cuối cùng. Tác giả luận văn nên áp dụng quy trình đánh giá khép kín gồm ba bước dưới đây để vừa đảm bảo tính khoa học vừa tiết kiệm chi phí vận hành API của các mô hình trọng tài:

```text
       [ 1. Đánh giá Ngoại tuyến (Offline Eval) ]
                           │
                           ▼ (Nếu kết quả đạt ngưỡng chất lượng)
       [ 2. Đo lường Trải nghiệm Thoại vật lý ]
                           │
                           ▼ (Nếu tối ưu hóa độ trễ thành công)
       [ 3. Giám sát Liên tục bằng Tracing trong Sản xuất ]
```

### Bước 1: Tiến hành Đánh giá Ngoại tuyến (Offline Evaluation) trước khi ghép luồng thoại

Trước khi kích hoạt các bộ nhận dạng âm thanh STT và tổng hợp giọng nói TTS, tác giả luận văn cần tập trung tối ưu hóa "bộ não" RAG bằng văn bản.

*   **Hành động cụ thể**: Xây dựng tập dữ liệu gồm $100$ đến $200$ câu hỏi chuẩn. Chạy thực nghiệm song song trên các cấu hình khác nhau (ví dụ: thay đổi kích thước chunk từ $256$ sang $512$ và $1024$ tokens; so sánh việc sử dụng mô hình embedding của OpenAI với các mô hình mã nguồn mở như BGE-M3).
*   **Mục tiêu số liệu**: Sử dụng thư viện Ragas để tính toán các điểm số. Chỉ chuyển sang bước tiếp theo khi điểm số Faithfulness trung bình đạt tối thiểu từ $0.85$ trở lên.

### Bước 2: Kích hoạt luồng thoại và đo lường phân bố độ trễ (Latency Percentiles)

Khi lớp tri thức đã hoạt động chính xác, tiến hành tích hợp đường ống truyền phát âm thanh (Streaming Voice Pipeline).

*   **Hành động cụ thể**: Viết các lệnh thu thập log thời gian thực tại từng điểm nút của hệ thống (mốc thời gian nhận diện xong của VAD, mốc thời gian hoàn tất STT, mốc thời gian LLM sinh token đầu tiên, mốc thời gian TTS phát tín hiệu).
*   **Mục tiêu số liệu**: Không sử dụng giá trị trung bình (average) để báo cáo độ trễ trong luận văn vì giá trị trung bình thường che giấu đi các điểm nghẽn ở đuôi phân phối (tail latency). Luận văn bắt buộc phải báo cáo các giá trị độ trễ ở các phân vị P50 (Median), P90, và P95. Một hệ thống trợ lý thoại xuất sắc cần kiểm soát giá trị P95 của tổng độ trễ Time-to-First-Audio (TTFA) dưới ngưỡng $1500\text{ ms}$ để đảm bảo tính tự nhiên của cuộc hội thoại.

### Bước 3: Tích hợp công cụ giám sát luồng (Tracing & Observability)

Trong quá trình vận hành thử nghiệm hệ thống với người dùng thực tế (A/B testing hoặc thử nghiệm nội bộ nhóm), các lỗi phát sinh ngoài dự kiến là không thể tránh khỏi.

*   **Hành động cụ thể**: Tích hợp một khung giám sát luồng mã nguồn mở như Langfuse hoặc MLflow vào mã nguồn hệ thống RAG. Các công cụ này sẽ tự động ghi vết toàn bộ cây cuộc gọi (execution trace) của từng yêu cầu của người dùng.
*   **Mục tiêu số liệu**: Khi một người dùng phản hồi rằng trợ lý thoại trả lời sai thông tin hoặc bị giật cục, tác giả luận văn chỉ cần mở giao diện Dashboard của Langfuse, tra cứu mã phiên làm việc (Session ID), xem chính xác các đoạn văn bản nào đã được truy xuất vào thời điểm đó, và prompt đầu vào đã bị biến đổi như thế nào. Việc đưa các hình ảnh minh họa luồng trace trực quan từ các công cụ observability này vào chương thực nghiệm của luận văn sẽ là một điểm cộng rất lớn chứng minh tính chuyên nghiệp và thực tiễn cao của đề tài nghiên cứu.

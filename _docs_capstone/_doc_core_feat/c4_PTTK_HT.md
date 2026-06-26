Chương 4
PHÂN TÍCH THIẾT KẾ HỆ THỐNG

4.1 Sơ đồ tổng quan

Một sơ đồ tổng quan được nhóm nghiên cứu đề xuất để thể hiện rõ ràng các thành phần  
trong hệ thống như Hình 3.1. Đây là cơ sở để hiện thực hóa các mục tiêu của nhóm.  
Sơ đồ gồm các thành phần sau: Tầng người dùng, Tầng vận chuyển âm thanh thời gian thực, Tầng xử lý logic Backend, Tầng dữ liệu lưu trữ, Tầng dịch vụ bên thứ ba. Hệ thống  
sẽ được sử dụng với hai vai trò người dùng là Quản trị, Đọc giả.

Hệ thống được xây dựng dựa trên sự kết hợp giữa kiến trúc phân tán và kiến trúc hướng sự kiện. Thiết kế tổng thể của hệ thống nhằm tối ưu hóa trải nghiệm người dùng bằng cách phân rã các tác vụ nặng thành các tiến trình bất đồng bộ chạy ngầm, đồng thời duy trì khả năng giao tiếp âm thanh hai chiều thời gian thực với độ trễ cực thấp. Hệ thống được tổ chức một cách khoa học thành năm khối thành phần cốt lõi: Khối Client, Khối Realtime Transport, Khối Backend Runtime, Khối Data Layer và Khối External AI Services. Mỗi khối đảm nhận các vai trò chuyên biệt nhưng tương tác chặt chẽ với nhau thông qua các giao thức mạng tiêu chuẩn như HTTP/REST, WebRTC, WebSocket và các kết nối cơ sở dữ liệu bảo mật.

\[Hình\]

Khối Client: là nền tảng Flutter trên thiết bị di động, đóng vai trò là giao diện tương tác trực tiếp và duy nhất của người học đối với toàn bộ hệ thống. Client chịu trách nhiệm thu thập hành vi người dùng, truyền tải tài liệu gốc, cấu hình lịch trình học tập cá nhân hóa, đồng bộ tiến độ nghe sách chi tiết và hiển thị các phản hồi thông minh từ AI. Để tối ưu hóa tài nguyên trên thiết bị di động, Client không thực hiện các tác vụ tính toán phức tạp mà chỉ duy trì hai luồng giao tiếp song song với máy chủ: luồng HTTP/REST để thực hiện các yêu cầu đồng bộ và luồng WebRTC để truyền tải âm thanh thời gian thực.

Khối Realtime Transport Layer: Khối truyền tải thời gian thực hoạt động dựa trên giải pháp máy chủ chuyển tiếp LiveKit Cloud Room, sử dụng cơ chế SFU (Selective Forwarding Unit) để định tuyến dữ liệu âm thanh và văn bản trực tiếp giữa thiết bị người dùng và Voice Agent. Hạ tầng này đảm bảo luồng âm thanh thu âm từ microphone của người học được mã hóa và truyền tải với băng thông tối ưu, giảm thiểu tối đa hiện tượng mất gói tin và giật tiếng trong môi trường mạng không ổn định. Bên cạnh luồng truyền tải âm thanh hai chiều, LiveKit Cloud Room còn cho phép tự quản lý các kênh dữ liệu phi âm thanh phân tách theo topic, mục đích phục vụ cho nghiệp vụ như: trả phụ đề lời nói, tin nhắn thời gian thực, metadata hỗ trợ định danh và các lệnh điều khiển trong phiên đàm thoại.

Khối Backend Runtime Layer: Khối này đóng vai trò là bộ não điều phối toàn bộ tài nguyên nghiệp vụ và vận hành các luồng tác vụ nền phức tạp của hệ thống, bao gồm các thành phần:  
FastAPI API Server: Hoạt động như một API Gateway tiếp nhận các yêu cầu HTTP từ Client, thực hiện xác thực bảo mật người dùng thông qua cơ chế phân quyền JWT của Supabase và kiểm tra tính hợp lệ về mặt cấu trúc outline của tài liệu trước khi đưa vào xử lý ngầm.  
Redis Cloud Broker: Đóng vai trò là hàng chờ trung gian chứa các thông điệp tác vụ, phân phối công việc vào các hàng đợi chuyên biệt để tránh làm tắc nghẽn luồng xử lý chính của API.  
Celery Document Worker: Tiếp nhận công việc từ hàng đợi để tải tài liệu gốc, phân tích cấu trúc cây đề mục, gọi LLM để chuẩn hóa văn nói, gọi api TTS để tổng hợp ra các file âm thanh phân đoạn, đồng thời sinh vector tri thức.  
Celery Notification Worker và Beat Scheduler: Celery Beat định kỳ quét mỗi phút một lần để gửi lệnh quét tác vụ ôn tập đến Celery Notification Worker. Worker này sẽ xử lý và lưu thông báo nhắc nhở vào hàng đợi trong cơ sở dữ liệu.  
LiveKit Realtime Agent: Là tiến trình Python chạy ngầm sử dụng LiveKit Agent SDK để kết nối vào phòng họp LiveKit. Agent lấy dữ liệu lịch sử chat và ngữ cảnh tài liệu từ Postgres để thực hiện tìm kiếm RAG, tương tác giọng nói với người dùng qua mô hình OpenAI Realtime, và cập nhật kết quả đàm thoại ngược lại cơ sở dữ liệu.

Khối Managed Data Layer: Khối này được quản lý thông qua hạ tầng điện toán đám mây của Supabase, đảm bảo tính toàn vẹn dữ liệu, khả năng khôi phục sau sự cố và hỗ trợ cho các tác vụ tìm kiếm ngữ nghĩa nâng cao.

Supabase Postgres kết hợp extension pgvector: Postgres đóng vai trò lưu trữ dữ liệu, trạng thái cuối cùng. Extension pgvector chịu trách nhiệm lưu trữ các vector database, cho phép hệ thống thực hiện trực tiếp các truy vấn cosine tương đồng ngữ nghĩa bằng câu lệnh SQL thuần túy, nâng cao tốc độ truy xuất ngữ cảnh cho Voice Agent.

Supabase Storage: Quản lý các buckets chuyên biệt để lưu trữ tập tin tài liệu gốc và lưu trữ toàn bộ các file âm thanh phân đoạn dạng audio.

Khối External AI Services Layer: Khối này cung cấp các mô hình học máy và trí tuệ nhân tạo tiên tiến từ các nhà cung cấp bên thứ ba, được tích hợp linh hoạt nhằm tối ưu hóa chi phí và chất lượng phản hồi của hệ thống. Mô hình Gemini LLM được ưu tiên cho các tác vụ xử lý văn bản quy mô lớn như đọc hiểu, phân tích cấu trúc cây tài liệu và chuẩn hóa văn bản nói nhờ lợi thế cửa sở ngữ cảnh cực lớn. Hệ sinh thái OpenAI cung cấp các Embedding modal để sinh vector database, đồng thời cũng cung cấp llm phục vụ luồng chat văn bản truyền thống. Quá trình chuyển văn bản thành giọng  nói sử dụng công nghệ sinh âm thanh từ Google TTS nhằm đem lại các đoạn audiobook có ngữ điệu tự nhiên. Đặc biệt, luồng giao tiếp giọng nói thời gian thực sử dụng API OpenAI Realtime hiểu trực tiếp audio giọng nói người dùng trong một phiên kết nối socket duy nhất mà không thông qua TTS, SST, LLM. Ngoài ra, API Tavily Search được tích hợp để tìm kiếm internet mở rộng, được BE kiểm soát chặt chẽ bằng bộ phân loại ý định (LLM Intent Classifier) đặt tại lõi của Agent để đảm bảo tính an toàn dữ liệu và tối ưu chi phí vận hành.

4.2 Đặc tả chức năng

4.2.1 Đọc giả  
Đăng ký/ Đăng nhập: Đọc giả phải tạo tài khoản với các thông tin cần thiết như: Họ tên, email. mật khẩu. Và có thể đăng nhập bằng Google để vào được hệ thống. Ngoài ra, khi đăng ký phải xác thực email bằng OTP, nếu quên mật khẩu thì cũng được xác thực gửi về email.  
Upload sách: User có thể tự upload sách hoặc lấy nguồn sách từ ứng dụng cung cấp sẵn. Hệ thống hỗ trợ định dạng PDF, EPUB, DOCX (kích thước tối đa 50MB) và giới hạn tổng ký tự khi tạo audio. Bắt buộc mọi sách phải có outline ẩn. Khi upload thành công sách sẽ được lưu tạm thời.  
Lên kế hoạch học tập: Sau khi xem outline, người dùng chọn chế độ học tập cùng với các thông số như: \[TODO\]. Với chế độ đầy đủ: Chuyển đổi toàn bộ nội dung tài liệu thành văn phong nói tự nhiên. Với chế độ trọng tâm: Sử dụng LLM để phân tích và gom nhóm, lọc bỏ các thông tin dài dòng và chỉ tập chung các phần trọng tâm bài học.  
Xử lý nền, mở khóa sớm: Hệ thống giúp người dùng không bị treo máy khi thao tác tạo kế hoạch học tập và audio. Người dùng cũng có thể nghe sớm khi hệ thống ưu tiên tạo các phần đầu.  
Nghe audio sách: Hệ thống sẽ ưu tiên xử lý các chương đầu để người dùng nghe sớm nhất. Khi nghe người dùng có thể tắt màn hình điện thoại.  
Theo dõi tiến độ đọc sách: Người dùng sẽ được coi là hoàn thành tiến độ khi tiến độ nghe \>= 80%. Khi bị thoát giữa chừng, người dùng có thể tiếp tục nghe với tiến độ trước đó.  
Nhắc nhở ôn tập và thông báo: Với lịch ôn ngắt quãng sẽ được tạo ra khi người dùng hoàn thành tiến đọc sách. Kích hoạt 5 mốc ôn tập tương ứng: 1,3,7,14 và 30 ngày. Người dùng cũng sẽ được thông báo ôn tập và nhắc nhở học tập để kịp đúng tiến độ.  
Trợ lý học tập giọng nói thời gian thực: Người dùng có thể trao đổi với AI bằng giọng nói hoặc văn bản để thảo luận về sách, và các sách trong không gian học tập. Nếu như thông tin tìm không thấy, người dùng sẽ được AI gợi ý tìm kiếm trên Internet với sự cho phép của người dùng.  
Tạo không gian học tập: Người dùng sẽ thêm các tài liệu đã được upload hoặc của hệ thống cung cấp vào không gian học tập. Không gian này có thể chứa nhiều tài liệu, nhiều đoạn chat. Mỗi đoạn chat tương ứng với một luồng trao đổi thông tin giữa người dùng và AI trong phạm vi các sách có trong không gian.

4.3 Sơ đồ Usecase

4.3.1 Đặc tả Usecase

4.4. Sơ đồ Lớp

4.4.1 Bảng cơ sở dữ liệu
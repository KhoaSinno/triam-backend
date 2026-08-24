# Hướng Dẫn Cấu Hướng Hệ Thống (Config & Environment Guide)

Tệp này mô tả chi tiết tất cả các biến cấu hình trong [config.py](file:///w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/core/config.py). Các biến này được nạp động từ file `.env` sử dụng Pydantic `BaseSettings`.

---

## 1. API Keys & Endpoint kết nối ngoại vi

| Tên biến | Kiểu dữ liệu | Mặc định | Mục đích sử dụng |
|---|---|---|---|
| `OPENAI_API_KEY` | `str` | *Bắt buộc* | Key gọi các API của OpenAI (Realtime API, GPT-4o, GPT-4o-mini). |
| `TAVILY_API_KEY` | `str` | *Bắt buộc* | Key gọi dịch vụ Tavily Search để tìm kiếm thông tin trên Web khi Voice Agent cần dữ liệu ngoài sách. |
| `GEMINI_API_KEY` | `str` | *Bắt buộc* | Key gọi mô hình Gemini (Google AI Studio) phục vụ Pareto Planner và các tác vụ LLM bổ trợ. |
| `GEMINI_BASE_URL` | `str` | *Bắt buộc* | Endpoint tương thích với OpenAI của Gemini API. |

---

## 2. Supabase & Cơ sở dữ liệu (Postgres SQL)

Hệ thống sử dụng cơ chế connection pool của SQLAlchemy để tối ưu hóa kết nối đến Supabase Postgres DB.

| Tên biến | Kiểu dữ liệu | Mặc định | Mục đích sử dụng |
|---|---|---|---|
| `SUPABASE_URL` | `str` | *Bắt buộc* | API URL của dự án Supabase. |
| `SUPABASE_KEY` | `str` | *Bắt buộc* | Anon/Public key để gọi Supabase Client. |
| `SUPABASE_SERVICE_ROLE_KEY` | `str` | *Bắt buộc* | Service role key có quyền bypass RLS để chạy các tác vụ quản trị ngầm. |
| `DATABASE_URL` | `str` | *Bắt buộc* | Connection string kết nối trực tiếp đến PostgreSQL (chạy qua Session Pooler cổng 6543). |
| `DATABASE_ECHO` | `bool` | `False` | Bật/tắt log ra console các câu lệnh SQL thực tế (chỉ nên bật khi debug). |
| `DATABASE_POOL_MODE` | `str` | `"auto"` | Chế độ quản lý pool của SQLAlchemy. |
| `DATABASE_POOL_SIZE` | `int` | `3` | Số lượng kết nối DB tối đa được duy trì trong pool cho mỗi tiến trình. |
| `DATABASE_MAX_OVERFLOW` | `int` | `2` | Số lượng kết nối DB vượt hạn mức cho phép tạo thêm khi hàng đợi pool bị đầy. |
| `DATABASE_POOL_TIMEOUT` | `int` | `5` | Thời gian chờ tối đa (giây) để mượn kết nối từ pool trước khi báo lỗi Timeout. |
| `DATABASE_POOL_RECYCLE` | `int` | `900` | Tự động đóng và giải phóng kết nối cũ sau 900 giây (15 phút) để tránh lỗi đứt kết nối phía server. |
| `DATABASE_POOL_PRE_PING` | `bool` | `True` | Tự động ping DB kiểm tra tình trạng kết nối trước khi dùng, tránh lỗi lặt vặt. |
| `DATABASE_POOL_USE_LIFO` | `bool` | `True` | Sử dụng cơ chế LIFO (Last In First Out) để tái sử dụng kết nối mới nhất, giúp DB giải phóng kết nối cũ sớm hơn. |
| `DATABASE_APPLICATION_NAME` | `str` | `"triam-backend"` | Nhãn định danh client gửi lên Postgres giúp giám sát kết nối trên Supabase Dashboard. |

---

## 3. Text-to-Speech (TTS) — Chuyển đổi văn bản thành giọng nói

Hỗ trợ 2 nhà cung cấp chính: Microsoft Edge (Free) và Google Cloud Chirp 3 (HD).

| Tên biến | Kiểu dữ liệu | Mặc định | Mục đích sử dụng |
|---|---|---|---|
| `TTS_PROVIDER` | `str` | `"edge"` | Chọn provider chạy TTS. Gồm: `"edge"` (miễn phí) hoặc `"google"` (trả phí, chất lượng cao). |
| `EDGE_TTS_VOICE` | `str` | `"en-US-Ava..."` | Tên giọng đọc mặc định của Microsoft Edge TTS. |
| `TTS_RECEIVE_TIMEOUT_SECONDS` | `int` | `300` | Thời gian tối đa chờ nạp file audio từ provider trước khi timeout. |
| `TTS_RETRY_BASE_SECONDS` | `int` | `3` | Thời gian chờ cơ sở để thử lại (retry) khi gọi API TTS bị lỗi mạng. |
| `TTS_MIN_TEXT_CHARS` | `int` | `10` | Số ký tự tối thiểu để kích hoạt luồng sinh audio (tránh các câu rác quá ngắn). |
| `TTS_GOOGLE_API_KEY` | `str \| None` | `None` | API Key riêng để gọi dịch vụ Google Cloud TTS (Chirp 3 HD). |
| `GOOGLE_TTS_LANGUAGE_CODE` | `str` | `"vi-VN"` | Mã ngôn ngữ giọng đọc của Google TTS. |
| `GOOGLE_TTS_VOICE` | `str` | `"vi-VN-Chirp..."` | Tên model giọng nói thế hệ mới (Chirp 3 HD) tiếng Việt của Google. |
| `GOOGLE_TTS_MAX_BYTES_PER_REQUEST` | `int` | `4500` | Giới hạn dung lượng text gửi lên Google TTS mỗi lượt để tránh lỗi payload quá lớn. |
| `GOOGLE_TTS_ENABLE_COST_LOG` | `bool` | `True` | Ghi nhận chi phí/số lượng ký tự gọi Google TTS ra log để theo dõi ngân sách. |
| `TTS_GENERATION_CONCURRENCY` | `int` | `2` | Số tiến trình sinh TTS song song tối đa (tránh rate limit). |

---

## 4. LiveKit Server & Realtime Voice Agent

Cấu hình cho Voice Agent giao tiếp thời gian thực qua LiveKit.

| Tên biến | Kiểu dữ liệu | Mặc định | Mục đích sử dụng |
|---|---|---|---|
| `LIVEKIT_API_KEY` | `str` | *Bắt buộc* | Key định danh kết nối vào dự án LiveKit Cloud. |
| `LIVEKIT_API_SECRET` | `str` | *Bắt buộc* | Secret key dùng để sinh JSON Web Tokens (JWT) cho Client kết nối vào phòng. |
| `LIVEKIT_AGENT_NAME` | `str` | `"triam-agent"` | Tên định danh của Voice Agent để LiveKit Server gán job chạy. |
| `LIVEKIT_ROOM_EMPTY_TIMEOUT_SECONDS` | `int` | `60` | Tự động đóng phòng LiveKit sau 60 giây nếu phòng hoàn toàn trống. |
| `LIVEKIT_ROOM_DEPARTURE_TIMEOUT_SECONDS` | `int` | `20` | Thời gian chờ đóng phòng khi user đã rời đi (disconnect). |
| `LIVEKIT_AGENT_EMPTY_ROOM_GRACE_SECONDS` | `float` | `8.0` | Thời gian ân hạn (giây) Agent sẽ chờ trong phòng trống trước khi tự hủy để tiết kiệm tài nguyên. |
| `OPENAI_STREAM_MODEL_NAME` | `str` | `"gpt-realtime-mini"` | Model Realtime API của OpenAI dùng để nhận-phát và suy luận audio trực tiếp. |
| `OPENAI_REALTIME_VOICE` | `str` | `"cedar"` | Giọng đọc phản hồi thời gian thực của OpenAI (ví dụ: cedar, alloy, echo, shimmer). |

---

## 5. Nhận dạng giọng nói (ASR / Transcription) & Khử nhiễu

| Tên biến | Kiểu dữ liệu | Mặc định | Mục đích sử dụng |
|---|---|---|---|
| `OPENAI_REALTIME_TRANSCRIPTION_MODEL` | `str` | `"gpt-4o-transcribe"` | Model OpenAI chịu trách nhiệm transcribe âm thanh người dùng nói thành chữ viết. |
| `OPENAI_REALTIME_TRANSCRIPTION_LANGUAGE` | `str` | `"vi"` | Ngôn ngữ mặc định của bộ nhận dạng giọng nói (tiếng Việt). |
| `OPENAI_REALTIME_TRANSCRIPTION_PROMPT` | `str` | *Xem trong file* | Đoạn văn bản định hướng (prompt gợi ý) giúp mô hình STT nhận dạng đúng các từ viết tắt chuyên môn trong Tri Âm. |
| `OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED` | `bool` | `True` | Tự động chèn thêm từ vựng/tiêu đề phân đoạn sách hiện tại vào prompt của ASR để nâng cao độ chính xác khi phát âm các từ chuyên ngành. |
| `OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_CHARS` | `int` | `900` | Giới hạn độ dài tối đa của Prompt gửi lên bộ ASR. |
| `OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_TERMS` | `int` | `45` | Số lượng từ vựng đặc thù tối đa được đưa vào Prompt. |
| `OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_SECTION_TERMS` | `int` | `20` | Số lượng từ vựng tối đa được trích xuất từ phân đoạn sách hiện tại. |
| `OPENAI_REALTIME_INPUT_AUDIO_NOISE_REDUCTION` | `str` | `"near_field"` | Cấu hình bộ lọc khử tiếng ồn đầu vào của LiveKit (ví dụ: `"near_field"`). |
| `VOICE_AGENT_ASR_FINAL_RESPONSE_GATE_ENABLED` | `bool` | `False` | Canary P0: giữ Realtime VAD nhưng cấm auto-response trước ASR-final; ứng dụng tạo đúng một reply sau transcript cuối. Bật khi test voice có kiểm soát, tắt để rollback ngay. |

---

## 6. Logic Nghiệp vụ & Web Search của Voice Agent

| Tên biến | Kiểu dữ liệu | Mặc định | Mục đích sử dụng |
|---|---|---|---|
| `VOICE_AGENT_TEXT_LLM_MODEL` | `str` | `"gpt-4o-mini"` | Mô hình LLM dạng text phụ trợ để xử lý phân loại quyền tìm kiếm web. |
| `VOICE_AGENT_ENABLE_WEB_SEARCH_BY_DEFAULT` | `bool` | `True` | Mặc định cho phép Agent gợi ý tìm kiếm Web khi không tìm thấy thông tin trong sách. |
| `VOICE_AGENT_LOG_TRANSCRIPT_TEXT` | `bool` | `True` | Bật/tắt ghi logs văn bản transcript của hội thoại (phục vụ giám sát). |
| `VOICE_AGENT_DEDUPE_WINDOW_SECONDS` | `int` | `3` | Cửa sổ thời gian lọc trùng các tín hiệu thoại trùng lặp được kích hoạt liên tục. |
| `VOICE_AGENT_WEB_PERMISSION_TTL_SECONDS` | `int` | `180` | Thời gian sống (giây) của quyền truy cập Web được người dùng đồng ý trước khi hết hạn và phải hỏi lại. |
| `VOICE_AGENT_WEB_IMPLICIT_GRANT_WINDOW_SECONDS` | `int` | `20` | Khoảng thời gian tự động đồng ý tìm kiếm web nếu người dùng trả lời đồng ý ngay sau câu hỏi xin phép. |
| `VOICE_AGENT_WEB_RESULT_CACHE_TTL_SECONDS` | `int` | `120` | Lưu cache kết quả tìm kiếm web trong 2 phút để tránh gọi trùng lặp. |
| `VOICE_AGENT_PERMISSION_CLASSIFIER_ENABLED` | `bool` | `True` | Bật bộ phân loại ý định cấp phép search web (để phân biệt người dùng đang trả lời "Đồng ý" hay nói câu khác). |
| `VOICE_AGENT_PERMISSION_CLASSIFIER_MODEL` | `str` | `"gpt-4o-mini"` | Mô hình LLM thực hiện phân loại ý định cấp phép. |
| `VOICE_AGENT_PERMISSION_CLASSIFIER_TIMEOUT_SECONDS` | `float` | `5.0` | Thời gian chờ tối đa của API phân loại quyền. |
| `VOICE_AGENT_PERMISSION_CLASSIFIER_CONFIDENCE_THRESHOLD` | `float` | `0.72` | Ngưỡng tin cậy tối thiểu để xác nhận người dùng đồng ý cho tìm web. |

---

## 7. Bộ Chặn Tin Nhắn (Query Guard) & Trạng Thái Làm Rõ (Clarification)

| Tên biến | Kiểu dữ liệu | Mặc định | Mục đích sử dụng |
|---|---|---|---|
| `VOICE_AGENT_QUERY_GUARD_ENABLED` | `bool` | `True` | Kích hoạt bộ chặn để lọc bỏ các câu thoại quá ngắn hoặc âm thanh rác vô nghĩa. |
| `VOICE_AGENT_QUERY_GUARD_MIN_CHARS` | `int` | `6` | Số ký tự tối thiểu của câu thoại để được xử lý (dưới ngưỡng này sẽ bỏ qua). |
| `VOICE_AGENT_QUERY_GUARD_MIN_TOKENS` | `int` | `2` | Số lượng token tối thiểu để xử lý. |
| `VOICE_AGENT_QUERY_GUARD_TRANSCRIPT_TTL_SECONDS` | `float` | `15.0` | Thời gian sống của dữ liệu transcript trong bộ guard. |
| `VOICE_AGENT_QUERY_GUARD_LOG_DETAILS` | `bool` | `True` | Ghi chi tiết log hoạt động của bộ guard để giám sát. |
| `VOICE_AGENT_CLARIFICATION_STATE_ENABLED` | `bool` | `True` | Kích hoạt cơ chế hỏi làm rõ ý định của user khi câu hỏi bị mơ hồ (ví dụ: trùng tên chương/sách). |
| `VOICE_AGENT_CLARIFICATION_STATE_TTL_SECONDS` | `float` | `30.0` | Thời gian chờ người dùng phản hồi câu hỏi làm rõ. |
| `VOICE_AGENT_CLARIFICATION_CONFIRMATION_MAX_TOKENS` | `int` | `4` | Số lượng token tối đa để kiểm tra câu xác nhận ngắn của người dùng. |
| `VOICE_AGENT_CLARIFICATION_MIN_QUERY_PROMPT_OVERLAP` | `float` | `0.45` | Ngưỡng trùng lặp tối thiểu giữa câu trả lời của user và các tùy chọn làm rõ. |
| `VOICE_AGENT_ASSISTANT_CLARIFICATION_HEURISTIC_ENABLED` | `bool` | `False` | Heuristic hỗ trợ lọc nhanh các câu làm rõ của trợ lý. |
| `VOICE_AGENT_INTERRUPTION_MIN_DURATION_SECONDS` | `float` | `0.8` | Thời gian nói tối thiểu của người dùng để được tính là ngắt lời Agent đang nói. |
| `VOICE_AGENT_INTERRUPTION_MIN_WORDS` | `int` | `2` | Số từ tối thiểu để tính là ngắt lời thực sự (tránh tiếng ho, thở dài làm ngắt Agent). |
| `VOICE_AGENT_FALSE_INTERRUPTION_TIMEOUT_SECONDS` | `float` | `1.5` | Thời gian ân hạn để khôi phục trạng thái phát của Agent nếu phát hiện ngắt lời giả. |
| `VOICE_AGENT_PREEMPTIVE_GENERATION_ENABLED` | `bool` | `False` | Tự động sinh phản hồi trước khi người dùng nói xong (hiện tắt để đảm bảo độ chính xác). |

---

## 8. Watchdog Giám Sát Voice Agent & Định Tuyến (Grounding Router)

| Tên biến | Kiểu dữ liệu | Mặc định | Mục đích sử dụng |
|---|---|---|---|
| `VOICE_AGENT_TOOL_REPLY_WATCHDOG_ENABLED` | `bool` | `True` | Bật bộ giám sát ngăn ngừa Agent bị treo khi gọi công cụ RAG hoặc tìm web quá lâu. |
| `VOICE_AGENT_TOOL_REPLY_WATCHDOG_GRACE_SECONDS` | `float` | `2.0` | Thời gian ân hạn thêm khi công cụ chạy bình thường. |
| `VOICE_AGENT_TOOL_REPLY_WATCHDOG_THINKING_GRACE_SECONDS` | `float` | `4.0` | Thời gian ân hạn chờ mô hình suy nghĩ trước khi watchdog tự động can thiệp. |
| `VOICE_AGENT_TOOL_REPLY_WATCHDOG_TOOLS` | `str` | `"search_book_..."` | Danh sách các công cụ được giám sát bởi watchdog. |
| `VOICE_AGENT_TOOL_REPLY_WATCHDOG_ALLOW_ERROR_OUTPUTS` | `bool` | `False` | Cho phép xuất ra lỗi thô của công cụ hay không. |
| `VOICE_AGENT_TOOL_REPLY_WATCHDOG_FORCE_TOOL_CHOICE_NONE` | `bool` | `True` | Ép buộc hủy kích hoạt gọi công cụ tiếp theo nếu watchdog đã can thiệp. |
| `AGENT_GROUNDING_ROUTER_ENABLED` | `bool` | `True` | Kích hoạt bộ định tuyến ý định (Grounding Router) để định hướng câu hỏi vào Metadata, Đề mục hay RAG. |
| `AGENT_SHARED_POLICY_ENABLED` | `bool` | `True` | Cho phép sử dụng chính sách xử lý chung giữa voice và text agent. |
| `AGENT_MODEL_PROFILE` | `str` | `"baseline"` | Profile cấu hình đánh giá chất lượng mô hình. |
| `AGENT_TRACE_ENABLED` | `bool` | `True` | Lưu vết dấu hiệu tìm kiếm/định tuyến (grounding trace) để tối ưu độ chính xác và gỡ lỗi. |
| `AGENT_TRACE_SCORE_PRECISION` | `int` | `4` | Làm tròn điểm số RAG ra logs ở 4 chữ số thập phân. |
| `AGENT_TRACE_LATE_TRANSCRIPT_WINDOW_SECONDS` | `float` | `15.0` | Cửa sổ ghi nhận logs trễ cho transcript. |

---

## 9. Cấu hình RAG & Định vị chương mục sách

| Tên biến | Kiểu dữ liệu | Mặc định | Mục đích sử dụng |
|---|---|---|---|
| `AGENT_SECTION_CONTEXT_MAX_CHARS` | `int` | `24000` | Hạn ngạch ký tự tối đa của văn bản chương sách nạp vào Prompt khi định tuyến trúng Đề mục cụ thể (`BOOK_SECTION`). |
| `AGENT_HYBRID_MIN_FINAL_SCORE` | `float` | `0.25` | Điểm số RRF tối thiểu của chunk để được coi là hợp lệ (dưới ngưỡng này sẽ báo không tìm thấy thông tin). |
| `AGENT_HYBRID_LEXICAL_CANDIDATES` | `int` | `20` | Số lượng ứng viên tối đa thu thập từ nhánh Lexical Search (Postgres FTS). |
| `AGENT_HYBRID_MAX_CONTEXT_CHUNKS` | `int` | `12` | Số lượng phân mảnh tối đa nạp vào Prompt khi **không** bật bộ Rerank. |
| `AGENT_HYBRID_MAX_CHUNKS_PER_SECTION` | `int` | `2` | **Bộ lọc đa dạng hóa ngữ cảnh**: Giới hạn tối đa 2 phân mảnh tri thức được chọn cho cùng một chương sách để tránh hiện tượng một chương chiếm trọn ngữ cảnh. |
| `AGENT_HYBRID_VALIDATE_EVIDENCE_ENABLED` | `bool` | `False` | Bật/tắt bộ kiểm định Named Entity và sự hiện diện của từ khóa chính trong kết quả RAG để giảm thiểu hiện tượng ảo giác (hallucination). |
| `COHERE_API_KEY` | `str \| None` | `None` | Key kết nối Cohere Rerank API. |
| `AGENT_RERANKER_ENABLED` | `bool` | `True` | Kích hoạt Cohere Reranker để xếp hạng lại các ứng viên sau RAG lai. |
| `AGENT_RERANKER_MODEL` | `str` | `"rerank-mult..."` | Tên mô hình Rerank đa ngôn ngữ của Cohere. |
| `AGENT_RERANKER_TOP_N` | `int` | `12` | Số lượng chunk tốt nhất được lọc ra để đưa vào Prompt sau khi Rerank. |
| `AGENT_RERANKER_CANDIDATES_LIMIT` | `int` | `20` | Giới hạn số lượng ứng viên tối đa gửi lên Cohere Rerank API để xếp hạng. |

---

## 10. Quản lý Tệp tin & Cơ sở hạ tầng

| Tên biến | Kiểu dữ liệu | Mặc định | Mục đích sử dụng |
|---|---|---|---|
| `MAX_FILE_SIZE_BYTES` | `int` | `50 * 1024 * 1024` | Hạn mức kích thước file sách tải lên tối đa (50 MB). |
| `ALLOWED_MIME_TYPES` | `Set[str]` | *Xem file* | Tập hợp định dạng file cho phép upload (PDF, EPUB, DOCX). |
| `LOG_LEVEL` | `str` | `"INFO"` | Cấp độ ghi logs chung của ứng dụng. |
| `LOG_THIRD_PARTY_LEVEL` | `str` | `"WARNING"` | Lọc logs từ các thư viện bên thứ ba để tránh làm rác console. |
| `RUN_MIGRATIONS_ON_START` | `bool` | `False` | Tự động chạy Alembic Migrations khi container khởi động (không khuyến khích chạy tự động trên production). |
| `UVICORN_RELOAD` | `bool` | `False` | Kích hoạt hot-reload của Uvicorn (chỉ dùng ở local dev). |
| `UV_NO_SYNC` | `bool` | `False` | Cờ của `uv` tránh kiểm tra sync lại thư viện lúc khởi chạy. |

---

## 11. Celery & Hàng đợi công việc (Redis Broker)

Dành cho hàng đợi Celery xử lý phân tách chương sách và gửi thông báo ngầm.

| Tên biến | Kiểu dữ liệu | Mặc định | Mục đích sử dụng |
|---|---|---|---|
| `CELERY_BROKER_URL` | `str` | `"redis://..."` | Địa chỉ kết nối hàng đợi Redis. |
| `CELERY_RESULT_BACKEND` | `str \| None` | `None` | Nơi lưu kết quả của Celery task (không sử dụng để tăng tốc độ ghi). |
| `CELERY_TASK_ALWAYS_EAGER` | `bool` | `False` | Chạy tác vụ đồng bộ lập tức thay vì đẩy vào hàng đợi (chỉ dùng trong unit test). |
| `CELERY_TASK_EAGER_PROPAGATES` | `bool` | `False` | Lan truyền exception ra ngoài khi chạy eager task trong test. |
| `CELERY_BROKER_POOL_LIMIT` | `int` | `1` | Giới hạn connection pool của Celery tới Redis. |
| `CELERY_WORKER_PREFETCH_MULTIPLIER` | `int` | `1` | Số lượng task mà mỗi worker lấy trước từ queue (để là 1 để chia đều tải). |
| `CELERY_DOCUMENT_CONCURRENCY` | `int` | `1` | Số lượng luồng xử lý sách song song trên worker. |
| `CELERY_NOTIFICATION_CONCURRENCY` | `int` | `1` | Số lượng luồng gửi thông báo song song trên worker. |
| `CELERY_LOG_LEVEL` | `str` | `"info"` | Cấp độ log của tiến trình Celery. |
| `CELERY_VISIBILITY_TIMEOUT_SECONDS` | `int` | `3600` | Thời gian (1 tiếng) Redis chờ xác nhận hoàn thành trước khi gửi lại task cho worker khác. |
| `CELERY_WORKER_CANCEL_LONG_RUNNING_ON_CONNECTION_LOSS` | `bool` | `False` | Tự hủy task đang chạy nếu kết nối Redis Broker bị đứt. |
| `ENABLE_CELERY_WORKER` | `bool` | `False` | Bật luồng chạy worker phân tích văn bản sách. |
| `ENABLE_NOTIFICATION_WORKER` | `bool` | `False` | Bật luồng chạy worker gửi thông báo. |
| `ENABLE_CELERY_BEAT` | `bool` | `False` | Bật tiến trình lập lịch (Celery Beat) định kỳ. |

---

## 12. Công Cụ Lên Lịch Học Pareto (Pareto Planner)

| Tên biến | Kiểu dữ liệu | Mặc định | Mục đích sử dụng |
|---|---|---|---|
| `PARETO_PLANNER_MODEL` | `str` | `"gemini-3.7-flash"` | Tên mô hình Gemini chịu trách nhiệm lập kế hoạch học tập Pareto (chọn 20% cốt lõi). |
| `PARETO_PLANNER_TIMEOUT_SECONDS` | `float` | `25.0` | Thời gian chờ tối đa của API lập lịch Pareto. |
| `PARETO_PLANNER_MAX_UNITS` | `int` | `8` | Số lượng bài học Pareto tối đa được tạo ra cho mỗi cuốn sách. |
| `PARETO_PLANNER_MIN_UNITS` | `int` | `3` | Số lượng bài học Pareto tối thiểu. |
| `PARETO_TARGET_COVERAGE_RATIO` | `float` | `0.25` | Tỷ lệ phủ thông tin mục tiêu của Pareto (khoảng 25% nội dung chính cốt lõi). |
| `PARETO_SECTION_EXCERPT_CHARS` | `int` | `1400` | Độ dài tối đa trích đoạn sách gửi cho LLM lập kế hoạch học tập. |
| `PARETO_PLANNER_MAX_SECTION_CARDS` | `int` | `120` | Giới hạn số lượng thẻ phân đoạn tối đa đưa vào xử lý của Pareto Planner. |

---

## 13. Firebase Cloud Messaging (FCM) & Quản Lý Thông Báo

| Tên biến | Kiểu dữ liệu | Mặc định | Mục đích sử dụng |
|---|---|---|---|
| `FIREBASE_CREDENTIALS_JSON` | `str \| None` | `None` | Chuỗi JSON chứa khóa Firebase Service Account (nạp từ biến môi trường). |
| `FIREBASE_CREDENTIALS_FILE` | `str \| None` | `None` | Đường dẫn file JSON chứa khóa Firebase Service Account nằm trong thư mục gốc. |

---

## 14. Vòng Lặp Học Tập & Tiến Độ (Spaced Repetition Loop)

Các thông số quản lý chu kỳ học tập ngắt quãng (Spaced Repetition) của người dùng.

| Tên biến | Kiểu dữ liệu | Mặc định | Mục đích sử dụng |
|---|---|---|---|
| `MAX_ACTIVE_LEARNING_BOOKS_PER_USER` | `int` | `3` | Giới hạn số lượng sách học chủ động tối đa cùng một lúc của mỗi user. |
| `LEARNING_COMPLETION_THRESHOLD_PERCENT` | `int` | `80` | Tỷ lệ hoàn thành (nghe/học) tối thiểu để đánh dấu cuốn sách là "Đã học xong". |
| `LEARNING_PROGRESS_MIN_DELTA_PERCENT` | `int` | `5` | Bước thay đổi tiến độ tối thiểu để hệ thống cập nhật vào DB (tránh ghi DB liên tục khi nghe từng giây). |
| `LEARNING_PROGRESS_STALE_SECONDS` | `int` | `30` | Khoảng thời gian không có hoạt động mới trước khi session học tập được coi là dừng lại. |

# TRIAM System Architecture - GPT Image Prompt

Mục đích của file này:

- Dùng làm prompt đưa cho model tạo ảnh như GPT Image.
- Ảnh cần mô tả đúng kiến trúc tổng quan của dự án TRIAM Backend hiện tại.
- Sau khi model tạo ảnh, gửi ảnh lại để verify kiến trúc, mũi tên, tên service và flow.

## Prompt Copy/Paste

Copy toàn bộ prompt trong khối dưới đây và đưa cho model tạo ảnh.

```text
Create a clean, professional, high-resolution system architecture diagram for a capstone project named "TRIAM - AI Learning Companion".

STYLE REQUIREMENTS:
- Use a modern flat vector diagram style.
- 16:9 landscape canvas.
- White or very light background.
- Use clear grouped boxes with subtle colors.
- Text must be large, readable, and not crowded.
- Use concise English labels exactly as provided.
- Use arrows with labels for data flow.
- Do not use decorative 3D objects, photos, gradients, mascots, or unrelated icons.
- Do not invent extra services.
- Do not show implementation code.
- The diagram should look like a senior backend architecture overview for an interview or capstone defense.

TITLE:
"TRIAM System Architecture"
Subtitle: "Document-to-Audio Learning, Realtime Study Agent, Progress Tracking, and In-App Review Notifications"

LAYOUT:
Use a left-to-right architecture layout with 5 main zones:

1. Client Zone on the far left.
2. Backend Runtime Zone in the center.
3. Data Layer below the backend.
4. External AI / Realtime Providers on the right.
5. Learning Loop / Notification area at the lower center-right.

ZONE 1: CLIENT
Create one grouped box named "Flutter Mobile App".
Inside it, show these small items:
- Upload Document
- Reading Plan
- Audio Player
- Progress Tracking
- Study Chat / Voice
- In-App Notifications

From Flutter Mobile App, draw arrows:
- "REST API" arrow to FastAPI API Server.
- "LiveKit SDK" arrow to LiveKit Cloud Room.

ZONE 2: BACKEND RUNTIME
Create a grouped box named "Hugging Face Docker Space".
Inside it, show these components:

1. "FastAPI API Server"
   Sub-labels:
   - Upload / Books / Plans
   - Jobs & Processing Status
   - Study Context & Chat Threads
   - Learning Progress API
   - Notifications API

2. "Celery Document Worker"
   Sub-labels:
   - Parse chapters
   - RAG embeddings
   - LLM normalize
   - TTS audio generation
   - Partial-ready unlock

3. "Celery Beat + Notification Workers"
   Sub-labels:
   - scan_due
   - deliver_due
   - stale-lock recovery

4. "LiveKit Realtime Agent"
   Sub-labels:
   - Vietnamese speech transcription
   - RAG study context
   - lk.chat / lk.transcript

Draw arrows inside Backend Runtime:
- FastAPI API Server -> Redis Cloud Broker, label "enqueue Celery task IDs"
- Redis Cloud Broker -> Celery Document Worker, label "document queue"
- Celery Beat + Notification Workers -> Postgres, label "scan due reminders/reviews"
- Celery Beat + Notification Workers -> User Notifications table, label "deliver in-app notification"
- FastAPI API Server -> LiveKit Realtime Agent, label "thread/context config" if space allows

ZONE 3: DATA LAYER
Create a grouped box named "Supabase Data Layer".
Inside it, show:

1. "Supabase Postgres + pgvector"
   Include these key table groups:
   - books / chapters / chapter_segments
   - processing_jobs / chapter_processing_states
   - reading_plans / schedule_slots
   - chapter_learning_progress
   - spaced_review_items
   - notification_outbox / user_notifications
   - study_contexts / chat_threads / chat_messages
   - book_knowledge vectors

2. "Supabase Storage"
   Sub-labels:
   - raw_books
   - audios

Draw arrows:
- FastAPI API Server <-> Supabase Postgres + pgvector, label "SQLModel CRUD + polling state"
- Celery Document Worker <-> Supabase Postgres + pgvector, label "job, segments, vectors, progress"
- Celery Document Worker <-> Supabase Storage, label "download documents / upload audio"
- FastAPI API Server -> Supabase Storage, label "upload original document"

ZONE 4: EXTERNAL PROVIDERS
Create a grouped box named "External Providers".
Inside it, show:

1. "Redis Cloud Broker"
   Sub-label:
   - Celery queues: document, notification, maintenance

2. "Gemini LLM via OpenAI-compatible API"
   Sub-label:
   - normalize chapter text to TTS scripts

3. "OpenAI Embeddings"
   Sub-label:
   - text-embedding-3-small

4. "Edge TTS"
   Sub-label:
   - audio segments + review audio

5. "LiveKit Cloud Room"
   Sub-label:
   - realtime audio/text transport

6. "OpenAI Realtime"
   Sub-label:
   - gpt-realtime + gpt-4o-transcribe

7. "Tavily Search"
   Sub-label:
   - optional web lookup

Draw arrows:
- Celery Document Worker -> Gemini LLM, label "normalize"
- Celery Document Worker -> Edge TTS, label "generate audio"
- Celery Document Worker -> OpenAI Embeddings, label "embed chunks"
- LiveKit Realtime Agent <-> LiveKit Cloud Room, label "agent worker"
- LiveKit Realtime Agent -> OpenAI Realtime, label "speech + response"
- LiveKit Realtime Agent -> Tavily Search, label "optional web search"
- LiveKit Realtime Agent -> Supabase Postgres + pgvector, label "chat history + RAG"

ZONE 5: LEARNING LOOP AND NOTIFICATIONS
Create a highlighted flow band named "Production Learning Loop".
Show these steps in order:

1. "Book READY"
2. "User listens to segments"
3. "FE sends progress"
4. "chapter_learning_progress"
5. ">=80% or manual complete"
6. "Create spaced_review_items"
7. "scan_due"
8. "notification_outbox"
9. "deliver_due"
10. "user_notifications"

Draw arrows between these steps.

Add a small note in this zone:
"Book READY does not mean User COMPLETED"

IMPORTANT BUSINESS RULES TO SHOW AS SMALL CALLOUTS:
- "Postgres is the source of truth"
- "Redis is only the Celery broker"
- "Spaced review starts after chapter completion"
- "First playable chapter unlocks early listening"
- "In-app notification now; push notification is future work"
- "Auth currently planned to replace mock user ID"

VISUAL GROUPING COLORS:
- Client: soft blue
- Backend Runtime: soft indigo
- Data Layer: soft green
- External Providers: soft orange
- Learning Loop: soft purple
- Warning/future callouts: soft gray

ACCURACY RULES:
- Do not draw Pinecone.
- Do not draw RabbitMQ.
- Do not draw AWS services except Hugging Face Docker Space if needed.
- Do not draw Firebase Push as implemented. If mentioned, label it clearly as "Future Push Notification".
- Do not draw payment/subscription as implemented.
- Do not draw OCR/scanned PDF processing as implemented.
- Do not imply Redis stores business data.
- Do not imply spaced review is created when chapter audio is generated.
- Do not imply authentication is fully implemented; show "Auth planned / mock user currently" only as a small future callout.

FINAL IMAGE QUALITY:
- The image must be understandable in one glance.
- Prefer fewer but accurate labels over too much tiny text.
- Keep arrows clean and avoid crossings when possible.
- Make the diagram suitable for a README, capstone report, and interview slide.
```

## Kiến Trúc Chính Xác Cần Kiểm Tra Sau Khi Gen Ảnh

Sau khi model tạo ảnh, kiểm tra các điểm sau:

### Bắt buộc phải có

- Flutter Mobile App.
- FastAPI API Server.
- Celery Document Worker.
- Celery Beat + Notification Workers.
- LiveKit Realtime Agent.
- Supabase Postgres + pgvector.
- Supabase Storage.
- Redis Cloud Broker.
- Gemini LLM via OpenAI-compatible API.
- OpenAI Embeddings.
- Edge TTS.
- LiveKit Cloud Room.
- OpenAI Realtime.
- Tavily Search.
- Production Learning Loop.

### Bắt buộc phải đúng flow

- Flutter gọi FastAPI bằng REST API.
- Flutter kết nối LiveKit Cloud bằng LiveKit SDK.
- FastAPI enqueue task vào Redis.
- Celery Worker consume Redis queue.
- Celery Worker đọc/ghi Postgres.
- Celery Worker download/upload file qua Supabase Storage.
- Celery Worker gọi Gemini, OpenAI Embeddings, Edge TTS.
- LiveKit Agent kết nối LiveKit Cloud.
- LiveKit Agent gọi OpenAI Realtime.
- LiveKit Agent đọc chat history/RAG từ Postgres.
- Notification đi qua `notification_outbox -> deliver_due -> user_notifications`.
- Spaced review được tạo sau khi `chapter_learning_progress` completed.

### Không được xuất hiện như implemented

- Firebase/FCM push notification là implemented.
- Supabase Auth là implemented.
- Pinecone là vector store chính.
- RabbitMQ là broker.
- OCR/scanned PDF parser.
- Payment/subscription.
- Redis lưu business state.
- Review tạo ngay khi chapter ready.

## Gợi Ý Nếu Model Vẽ Quá Rối

Nếu ảnh đầu tiên quá nhiều chữ hoặc rối, dùng prompt rút gọn này:

```text
Simplify the architecture diagram. Keep only the main boxes:
Flutter Mobile App, FastAPI API Server, Celery Workers, LiveKit Realtime Agent, Supabase Postgres + pgvector, Supabase Storage, Redis Cloud, External AI Providers, LiveKit Cloud, and Production Learning Loop.
Keep only the most important arrows:
Flutter -> FastAPI REST, FastAPI -> Redis, Redis -> Celery, Celery -> Postgres/Storage/AI, Flutter -> LiveKit Cloud, LiveKit Agent -> LiveKit/OpenAI/Postgres, Learning Progress -> Spaced Review -> Outbox -> User Notifications.
Do not add new services.
```

## Gợi Ý Khi Đưa Vào Báo Cáo

Caption nên dùng:

```text
TRIAM Backend architecture separates request-time APIs, durable background processing, realtime voice interaction, and learning-loop notifications. Postgres is the source of truth, Redis is only the Celery broker, and spaced review is created from real user completion rather than generated content readiness.
```

## Ghi Chú Về Trạng Thái Hiện Tại

Các phần đã implemented:

- Upload PDF/EPUB/DOCX có outline/TOC/heading validation.
- Generate reading plan.
- Celery document worker.
- Redis broker.
- Supabase Postgres + Storage.
- RAG knowledge with pgvector.
- Gemini LLM normalize.
- Edge TTS audio generation.
- LiveKit realtime agent.
- OpenAI Realtime transcription/response.
- Tavily optional web search.
- Study Context / Chat Thread.
- Processing job polling.
- First playable unlock.
- Learning progress by chapter/segment.
- Completion-based spaced review.
- In-app notification outbox.

Các phần nên vẽ là future/planned nếu có nhắc tới:

- Auth thật thay `MOCK_USER_ID`.
- Push notification qua FCM.
- Quota/cost control.
- Subscription/tier.

## Prompt Update Sau Khi Verify Ảnh V1

Ảnh V1 đã đúng bố cục tổng thể, nhưng cần sửa các lỗi sau:

- Các mũi tên `normalize`, `generate audio`, `embed chunks` đang bị vẽ xuất phát từ `Celery Beat + Notification Workers`. Đây là sai. Ba mũi tên này phải xuất phát từ `Celery Document Worker`.
- `Celery Beat + Notification Workers` chỉ được nối tới Postgres/outbox/user notification, không nối tới Gemini, Edge TTS hoặc OpenAI Embeddings.
- Các mũi tên realtime cần xuất phát rõ từ `LiveKit Realtime Agent`, không xuất phát từ Data Layer hoặc đường dọc không rõ nguồn.
- Sửa typo `enqueee` thành `enqueue`.
- Giữ lại bố cục và màu sắc hiện tại vì đã dễ nhìn.

Copy prompt update dưới đây nếu muốn regenerate ảnh V2 dựa trên ảnh V1:

```text
Create a revised version of the TRIAM System Architecture diagram. Keep the same overall 16:9 landscape layout, clean flat vector style, grouped zones, colors, title, and readable typography from the previous image. The previous image is mostly correct, but fix these architecture flow errors carefully.

TITLE:
"TRIAM System Architecture"
Subtitle:
"Document-to-Audio Learning, Realtime Study Agent, Progress Tracking, and In-App Review Notifications"

KEEP THESE 5 ZONES:
1. Client - Flutter Mobile App
2. Backend Runtime - Hugging Face Docker Space
3. Data Layer - Supabase Data Layer
4. External Providers
5. Production Learning Loop

MOST IMPORTANT FIX:
The arrows to external AI providers must originate from the correct backend component.

Correct arrows:
- Celery Document Worker -> Gemini LLM via OpenAI-compatible API, label "normalize"
- Celery Document Worker -> Edge TTS, label "generate audio"
- Celery Document Worker -> OpenAI Embeddings, label "embed chunks"

Incorrect arrows to avoid:
- Do NOT draw "normalize" from Celery Beat + Notification Workers.
- Do NOT draw "generate audio" from Celery Beat + Notification Workers.
- Do NOT draw "embed chunks" from Celery Beat + Notification Workers.

Celery Beat + Notification Workers should only connect to the notification/learning loop:
- Celery Beat + Notification Workers -> Supabase Postgres + pgvector, label "scan due reminders/reviews"
- Celery Beat + Notification Workers -> notification_outbox, label "create/claim due outbox"
- Celery Beat + Notification Workers -> user_notifications, label "deliver in-app"
- It may also show "stale-lock recovery" as an internal bullet.

FastAPI and Redis flow:
- Flutter Mobile App -> FastAPI API Server, label "REST API"
- FastAPI API Server -> Redis Cloud Broker, label "enqueue Celery task IDs"
- Redis Cloud Broker -> Celery Document Worker, label "document queue"
- Fix any typo like "enqueee"; use "enqueue".

Storage and database flow:
- FastAPI API Server -> Supabase Storage, label "upload original document"
- FastAPI API Server <-> Supabase Postgres + pgvector, label "SQLModel CRUD + polling state"
- Celery Document Worker <-> Supabase Storage, label "download document / upload audio"
- Celery Document Worker <-> Supabase Postgres + pgvector, label "jobs, segments, vectors, progress"

Realtime flow:
- Flutter Mobile App -> LiveKit Cloud Room, label "LiveKit SDK"
- LiveKit Realtime Agent <-> LiveKit Cloud Room, label "agent worker"
- LiveKit Realtime Agent -> OpenAI Realtime, label "speech + response"
- LiveKit Realtime Agent -> Tavily Search, label "optional web search"
- LiveKit Realtime Agent <-> Supabase Postgres + pgvector, label "chat history + RAG"
- FastAPI API Server -> LiveKit Realtime Agent, label "thread/context config" only if there is enough space.

External Providers box must contain exactly:
1. Redis Cloud Broker
   "Celery queues: document, notification, maintenance"
2. Gemini LLM via OpenAI-compatible API
   "normalize chapter text to TTS scripts"
3. OpenAI Embeddings
   "text-embedding-3-small"
4. Edge TTS
   "audio segments + review audio"
5. LiveKit Cloud Room
   "realtime audio/text transport"
6. OpenAI Realtime
   "gpt-realtime + gpt-4o-transcribe"
7. Tavily Search
   "optional web lookup"

Production Learning Loop should stay as a horizontal flow:
Book READY -> User listens to segments -> FE sends progress -> chapter_learning_progress -> >=80% or manual complete -> Create spaced_review_items -> scan_due -> notification_outbox -> deliver_due -> user_notifications

Keep the note:
"Book READY does not mean User COMPLETED"

Keep these bottom callouts:
- "Postgres is the source of truth"
- "Redis is only the Celery broker"
- "Spaced review starts after chapter completion"
- "First playable chapter unlocks early listening"
- "In-app notification now; push notification is future work"
- "Auth currently planned to replace mock user ID"

Accuracy rules:
- Do not draw Pinecone.
- Do not draw RabbitMQ.
- Do not draw Firebase Push as implemented.
- Do not draw Supabase Auth as implemented.
- Do not draw OCR/scanned PDF processing as implemented.
- Do not imply Redis stores business data.
- Do not imply spaced review is created when chapter audio is generated.
- Keep arrows clean, with minimal crossing.
- Prefer fewer correct arrows over many confusing arrows.
```

## Prompt Update Sau Khi Verify Ảnh V2

Ảnh V2 đẹp hơn V1 nhưng **vẫn chưa đúng hoàn toàn**. Các lỗi cần sửa:

1. `normalize`, `generate audio`, `embed chunks` vẫn đang chĩa vào `Celery Beat + Notification Workers`. Sai.
2. `Celery Beat + Notification Workers` đang đứng chắn giữa `Celery Document Worker` và External AI Providers, làm model hiểu sai rằng notification worker gọi Gemini/TTS/Embeddings.
3. `LiveKit SDK` đang được vẽ như Flutter gọi thẳng vào `LiveKit Realtime Agent`. Đúng hơn là Flutter kết nối `LiveKit Cloud Room`; agent cũng kết nối room đó.
4. Data Layer ghi `chapter_processing_status`; đúng là `chapter_processing_states`.

Vì vậy ở V3, hãy đổi layout một chút:

- Đặt `Celery Document Worker` ở giữa trên.
- Đặt `External AI Providers` ngay bên phải `Celery Document Worker`.
- Đặt `Celery Beat + Notification Workers` xuống thấp hơn, gần Learning Loop và Data Layer.
- Không để Notification Worker nằm trên đường từ Document Worker sang Gemini/TTS/Embeddings.

Copy prompt V3 dưới đây:

```text
Regenerate the TRIAM System Architecture diagram as a corrected V3.

The previous image looked good visually, but it still had wrong arrows. This version must prioritize architecture correctness over decorative layout.

Canvas and style:
- 16:9 landscape.
- Clean flat vector architecture diagram.
- Light background.
- Large readable text.
- Use grouped zones with subtle colors.
- Avoid too many crossing arrows.
- Do not invent services.

Title:
"TRIAM System Architecture"

Subtitle:
"Document-to-Audio Learning, Realtime Study Agent, Progress Tracking, and In-App Review Notifications"

Use 5 zones:
1. Client
2. Backend Runtime - Hugging Face Docker Space
3. Data Layer - Supabase Data Layer
4. External Providers
5. Production Learning Loop

IMPORTANT LAYOUT FIX:
Inside "Backend Runtime - Hugging Face Docker Space", arrange components like this:
- Put "FastAPI API Server" on the left.
- Put "Redis Cloud Broker" between FastAPI and Celery Document Worker.
- Put "Celery Document Worker" in the center-right.
- Put "LiveKit Realtime Agent" below FastAPI or below the document worker.
- Put "Celery Beat + Notification Workers" lower-right, near the Production Learning Loop and Data Layer, NOT between Celery Document Worker and External AI Providers.

External Providers placement:
- Put "External Providers" to the far right.
- Align "Gemini LLM", "OpenAI Embeddings", and "Edge TTS" horizontally near the "Celery Document Worker" so arrows can go directly from Celery Document Worker to those providers.
- Align "LiveKit Cloud Room", "OpenAI Realtime", and "Tavily Search" near the "LiveKit Realtime Agent" so arrows can go directly from LiveKit Realtime Agent to those providers.
- Redis Cloud Broker can appear either inside External Providers or as a small broker between FastAPI and Celery, but label it clearly as Redis Cloud Broker.

Backend components:

FastAPI API Server:
- Upload / Books / Plans
- Jobs & Processing Status
- Study Context & Chat Threads
- Learning Progress API
- Notifications API

Celery Document Worker:
- Parse chapters
- RAG embeddings
- LLM normalize
- TTS audio generation
- Partial-ready unlock

Celery Beat + Notification Workers:
- scan_due
- deliver_due
- stale-lock recovery

LiveKit Realtime Agent:
- Vietnamese speech transcription
- RAG study context
- lk.chat / lk.transcript

Data Layer:
Supabase Postgres + pgvector:
- books / chapters / chapter_segments
- processing_jobs / chapter_processing_states
- reading_plans / reading_plan_schedule_slots
- chapter_learning_progress
- spaced_review_items
- notification_outbox / user_notifications
- study_contexts / chat_threads / chat_messages
- book_knowledge vectors

Supabase Storage:
- raw_books
- audios

External Providers:
1. Redis Cloud Broker
   "Celery queues: document, notification, maintenance"
2. Gemini LLM via OpenAI-compatible API
   "normalize chapter text to TTS scripts"
3. OpenAI Embeddings
   "text-embedding-3-small"
4. Edge TTS
   "audio segments + review audio"
5. LiveKit Cloud Room
   "realtime audio/text transport"
6. OpenAI Realtime
   "gpt-realtime + gpt-4o-transcribe"
7. Tavily Search
   "optional web lookup"

Correct arrows:

Client/API:
- Flutter Mobile App -> FastAPI API Server, label "REST API"
- Flutter Mobile App -> LiveKit Cloud Room, label "LiveKit SDK"

Task queue:
- FastAPI API Server -> Redis Cloud Broker, label "enqueue task IDs"
- Redis Cloud Broker -> Celery Document Worker, label "document queue"

Document generation:
- FastAPI API Server -> Supabase Storage, label "upload original document"
- Celery Document Worker -> Supabase Storage, label "download document"
- Celery Document Worker -> Supabase Storage, label "upload audio"
- Celery Document Worker <-> Supabase Postgres + pgvector, label "jobs, segments, vectors, progress"
- FastAPI API Server <-> Supabase Postgres + pgvector, label "CRUD + polling state"

AI calls:
- Celery Document Worker -> Gemini LLM via OpenAI-compatible API, label "normalize"
- Celery Document Worker -> OpenAI Embeddings, label "embed chunks"
- Celery Document Worker -> Edge TTS, label "generate audio"

Realtime:
- LiveKit Realtime Agent <-> LiveKit Cloud Room, label "agent worker"
- LiveKit Realtime Agent -> OpenAI Realtime, label "speech + response"
- LiveKit Realtime Agent -> Tavily Search, label "optional web search"
- LiveKit Realtime Agent <-> Supabase Postgres + pgvector, label "chat history + RAG"
- FastAPI API Server -> LiveKit Realtime Agent, label "thread/context config"

Notifications:
- Celery Beat + Notification Workers -> Supabase Postgres + pgvector, label "scan due reminders/reviews"
- Celery Beat + Notification Workers -> notification_outbox, label "create/claim due outbox"
- Celery Beat + Notification Workers -> user_notifications, label "deliver in-app"

STRICT NEGATIVE RULES:
- Do NOT draw normalize/generate audio/embed chunks arrows into Celery Beat + Notification Workers.
- Do NOT draw Celery Beat + Notification Workers calling Gemini, OpenAI Embeddings, or Edge TTS.
- Do NOT draw Flutter connecting directly to LiveKit Realtime Agent. Flutter connects to LiveKit Cloud Room.
- Do NOT draw Redis storing business state.
- Do NOT draw Pinecone.
- Do NOT draw RabbitMQ.
- Do NOT draw Firebase Push as implemented.
- Do NOT draw Supabase Auth as implemented.
- Do NOT draw OCR/scanned PDF processing as implemented.
- Do NOT draw spaced review created immediately after chapter audio generation.

Production Learning Loop:
Draw a clear horizontal flow band:
Book READY -> User listens to segments -> FE sends progress -> chapter_learning_progress -> >=80% or manual complete -> Create spaced_review_items -> scan_due -> notification_outbox -> deliver_due -> user_notifications

Add this note under the flow:
"Book READY does not mean User COMPLETED"

Bottom callouts:
- "Postgres is the source of truth"
- "Redis is only the Celery broker"
- "Spaced review starts after chapter completion"
- "First playable chapter unlocks early listening"
- "In-app notification now; push notification is future work"
- "Auth currently planned to replace mock user ID"

Make the image suitable for a capstone defense slide. Prefer fewer correct arrows over many confusing arrows.
```

## Prompt Update Sau Khi Verify Ảnh V3

Ảnh V3 đã tốt hơn V2 ở phần Document Worker gọi AI Providers, nhưng **vẫn chưa đủ chuẩn để chốt làm ảnh kiến trúc cuối**.

Các lỗi còn lại trong V3:

1. Redis bị vẽ 2 lần: một box trong Backend Runtime và một card trong External Providers. Dễ gây hiểu nhầm là có hai Redis.
2. `LiveKit SDK` vẫn chưa nối rõ tới `LiveKit Cloud Room`. Đúng flow là Flutter và Agent cùng kết nối vào LiveKit Cloud Room.
3. `agent worker`, `speech + response`, `optional web search` chưa xuất phát rõ từ `LiveKit Realtime Agent`.
4. Notification worker đang có mũi tên/label gần `Supabase Storage`, gây hiểu nhầm notification ghi vào Storage. Đúng là notification worker chỉ làm việc với Postgres/outbox/user_notifications.
5. Text nhỏ `deliver in-app` bị méo/khó đọc.

Copy prompt V4 dưới đây nếu muốn regenerate bản cuối. Prompt này cố tình đơn giản hơn và giảm số mũi tên để model không vẽ sai.

```text
Create the final corrected TRIAM System Architecture diagram. Prioritize correctness and readable text over showing every possible arrow.

Canvas:
- 16:9 landscape.
- Clean flat vector architecture diagram.
- White/light background.
- Large readable text.
- Minimal arrow crossings.
- Do not duplicate services.

Title:
"TRIAM System Architecture"

Subtitle:
"Document-to-Audio Learning, Realtime Study Agent, Progress Tracking, and In-App Review Notifications"

Main zones:
1. Client
2. Backend Runtime - Hugging Face Docker Space
3. Data Layer - Supabase
4. External AI and Realtime Services
5. Production Learning Loop

CRITICAL SIMPLIFICATION:
Draw exactly ONE Redis Cloud Broker box.
- Put it between FastAPI API Server and Celery Document Worker.
- Label it: "Redis Cloud Broker"
- Sub-label: "Celery queues: document, notification, maintenance"
- Do NOT draw Redis again inside External Providers.
- Add a small external/cloud badge if desired, but keep only one Redis box.

ZONE 1: Client
Box: "Flutter Mobile App"
Items:
- Upload Document
- Reading Plan
- Audio Player
- Progress Tracking
- Study Chat / Voice
- In-App Notifications

ZONE 2: Backend Runtime - Hugging Face Docker Space
Components:

1. "FastAPI API Server"
Bullets:
- Upload / Books / Plans
- Jobs & Processing Status
- Study Context & Chat Threads
- Learning Progress API
- Notifications API

2. "Celery Document Worker"
Bullets:
- Parse chapters
- RAG embeddings
- LLM normalize
- TTS audio generation
- Partial-ready unlock

3. "Celery Beat + Notification Workers"
Bullets:
- scan_due
- deliver_due
- stale-lock recovery

4. "LiveKit Realtime Agent"
Bullets:
- Vietnamese speech transcription
- RAG study context
- lk.chat / lk.transcript

ZONE 3: Data Layer - Supabase
Box: "Supabase Postgres + pgvector"
Key table groups:
- books / chapters / chapter_segments
- processing_jobs / chapter_processing_states
- reading_plans / reading_plan_schedule_slots
- chapter_learning_progress
- spaced_review_items
- notification_outbox / user_notifications
- study_contexts / chat_threads / chat_messages
- book_knowledge vectors

Box: "Supabase Storage"
Buckets:
- raw_books
- audios

ZONE 4: External AI and Realtime Services
Draw these provider cards:

1. "Gemini LLM"
Sub-label: "OpenAI-compatible API; normalize TTS scripts"

2. "OpenAI Embeddings"
Sub-label: "text-embedding-3-small"

3. "Edge TTS"
Sub-label: "audio segments + review audio"

4. "LiveKit Cloud Room"
Sub-label: "realtime audio/text transport"

5. "OpenAI Realtime"
Sub-label: "gpt-realtime + gpt-4o-transcribe"

6. "Tavily Search"
Sub-label: "optional web lookup"

CORRECT ARROWS ONLY:

Client/API:
- Flutter Mobile App -> FastAPI API Server, label "REST API"
- Flutter Mobile App -> LiveKit Cloud Room, label "LiveKit SDK"

Queue:
- FastAPI API Server -> Redis Cloud Broker, label "enqueue task IDs"
- Redis Cloud Broker -> Celery Document Worker, label "document queue"

FastAPI/Data:
- FastAPI API Server <-> Supabase Postgres + pgvector, label "CRUD + polling state"
- FastAPI API Server -> Supabase Storage, label "upload original document"

Document Worker/Data:
- Celery Document Worker <-> Supabase Postgres + pgvector, label "jobs, segments, vectors, progress"
- Celery Document Worker <-> Supabase Storage, label "download document / upload audio"

Document Worker/AI:
- Celery Document Worker -> Gemini LLM, label "normalize"
- Celery Document Worker -> OpenAI Embeddings, label "embed chunks"
- Celery Document Worker -> Edge TTS, label "generate audio"

Realtime:
- LiveKit Realtime Agent <-> LiveKit Cloud Room, label "agent worker"
- LiveKit Realtime Agent -> OpenAI Realtime, label "speech + response"
- LiveKit Realtime Agent -> Tavily Search, label "optional web search"
- LiveKit Realtime Agent <-> Supabase Postgres + pgvector, label "chat history + RAG"
- FastAPI API Server -> LiveKit Realtime Agent, label "thread/context config"

Notifications:
- Celery Beat + Notification Workers -> Supabase Postgres + pgvector, label "scan due reminders/reviews"
- Celery Beat + Notification Workers -> notification_outbox, label "create/claim due outbox"
- Celery Beat + Notification Workers -> user_notifications, label "deliver in-app"

Important: notification_outbox and user_notifications are table groups inside Supabase Postgres + pgvector. If necessary, draw small callout chips next to the Postgres box for "notification_outbox" and "user_notifications", but do not connect notification workers to Supabase Storage.

STRICT NEGATIVE RULES:
- Do NOT draw any arrow from Celery Beat + Notification Workers to Gemini LLM.
- Do NOT draw any arrow from Celery Beat + Notification Workers to Edge TTS.
- Do NOT draw any arrow from Celery Beat + Notification Workers to OpenAI Embeddings.
- Do NOT draw any arrow from Celery Beat + Notification Workers to Supabase Storage.
- Do NOT draw Flutter connecting directly to LiveKit Realtime Agent.
- Do NOT duplicate Redis Cloud Broker.
- Do NOT draw Pinecone.
- Do NOT draw RabbitMQ.
- Do NOT draw Firebase Push as implemented.
- Do NOT draw Supabase Auth as implemented.
- Do NOT draw OCR/scanned PDF processing as implemented.
- Do NOT imply Redis stores business data.
- Do NOT imply spaced review is created when chapter audio is generated.

Production Learning Loop:
Draw a clear horizontal band at the bottom:
Book READY -> User listens to segments -> FE sends progress -> chapter_learning_progress -> >=80% or manual complete -> Create spaced_review_items -> scan_due -> notification_outbox -> deliver_due -> user_notifications

Note under the loop:
"Book READY does not mean User COMPLETED"

Bottom callouts:
- "Postgres is the source of truth"
- "Redis is only the Celery broker"
- "Spaced review starts after chapter completion"
- "First playable chapter unlocks early listening"
- "In-app notification now; push notification is future work"
- "Auth currently planned to replace mock user ID"

TEXT QUALITY:
- Spell these labels exactly:
  - "enqueue task IDs"
  - "chapter_processing_states"
  - "reading_plan_schedule_slots"
  - "deliver in-app"
  - "notification_outbox"
  - "user_notifications"
- Keep text large enough to read in a presentation slide.
- If a label would be too small, remove less important arrows rather than shrinking text.
```

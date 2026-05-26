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

## Prompt Update Sau Khi Verify Ảnh V4

Ảnh V4 đã có bố cục dễ nhìn hơn, nhưng **vẫn chưa đúng hoàn toàn để dùng làm ảnh kiến trúc cuối**.

Các lỗi còn lại:

1. Redis vẫn bị vẽ 2 lần: một box trong Backend Runtime và một card trong External Providers. Trong hệ thống chỉ có **một Redis Cloud Broker** dùng làm Celery broker.
2. Luồng `Study Chat / Voice` chưa đủ chính xác. **Voice** dùng LiveKit + OpenAI Realtime. **Typed chat** cũng đi qua LiveKit DataChannel, nhưng xử lý bằng text LLM riêng (`gpt-4o-mini`) + RAG, không phải OpenAI Realtime.
3. Label trong agent bị sai/méo: phải là `lk.chat / lk.transcript`, không phải `R.chat / R.transcript`.
4. Realtime agent cần thể hiện rõ 2 lane:
   - Voice lane: microphone/audio -> LiveKit Cloud Room -> Voice Agent -> OpenAI Realtime.
   - Text chat lane: typed text -> LiveKit Cloud Room DataChannel `lk.chat` -> Agent -> Text Chat LLM + RAG -> `lk.chat`/`lk.transcript`.
5. Mũi tên notification còn hơi lệch và dễ hiểu nhầm là ghi vào Storage. Notification worker chỉ làm việc với Postgres/outbox/user_notifications.

Copy prompt V5 dưới đây để regenerate bản chính xác hơn. Prompt này bỏ bớt mũi tên phụ, thêm provider `OpenAI Chat LLM` và tách rõ voice/text chat.

```text
Create the final corrected TRIAM System Architecture diagram for a capstone defense slide.

Canvas and style:
- 16:9 landscape.
- Clean flat vector architecture diagram.
- White or very light background.
- Large readable text.
- Minimal arrow crossings.
- Use grouped zones with subtle colors.
- Do not duplicate services.
- Do not invent services.

Title:
"TRIAM System Architecture"

Subtitle:
"Document-to-Audio Learning, LiveKit Chat/Voice Agent, Progress Tracking, and In-App Review Notifications"

Main zones:
1. Client
2. Backend Runtime - Hugging Face Docker Space
3. Data Layer - Supabase
4. External Services
5. Production Learning Loop

CRITICAL RULE 1 - Redis:
Draw exactly ONE Redis Cloud Broker box.
- Put it inside Backend Runtime, between FastAPI API Server and Celery Document Worker.
- Label: "Redis Cloud Broker"
- Sub-label: "Celery queues: document, notification, maintenance"
- Do NOT draw Redis again in External Services.
- Do NOT imply Redis stores business state.

CRITICAL RULE 2 - Chat and Voice:
The Flutter app uses LiveKit for BOTH voice and typed chat transport.
But typed chat does NOT use OpenAI Realtime.

Draw two separate lanes connected through "LiveKit Cloud Room":

VOICE LANE:
- Flutter Mobile App -> LiveKit Cloud Room, label "LiveKit SDK: microphone/audio"
- LiveKit Realtime Agent <-> LiveKit Cloud Room, label "voice session"
- LiveKit Realtime Agent -> OpenAI Realtime, label "speech-to-text + realtime voice response"

TEXT CHAT LANE:
- Flutter Mobile App -> LiveKit Cloud Room, label "LiveKit DataChannel: lk.chat"
- LiveKit Cloud Room -> LiveKit Realtime Agent, label "typed text via lk.chat"
- LiveKit Realtime Agent -> OpenAI Chat LLM, label "text answer: gpt-4o-mini"
- LiveKit Realtime Agent <-> Supabase Postgres + pgvector, label "chat history + RAG"
- LiveKit Realtime Agent -> Tavily Search, label "optional web search"
- LiveKit Realtime Agent -> LiveKit Cloud Room, label "lk.chat + lk.transcript"

Add a small note near the LiveKit Realtime Agent:
"Voice uses OpenAI Realtime; typed chat uses text LLM + RAG"

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

2. "Redis Cloud Broker"
Bullets:
- document queue
- notification queue
- maintenance queue

3. "Celery Document Worker"
Bullets:
- Parse chapters
- RAG embeddings
- LLM normalize
- TTS audio generation
- Partial-ready unlock

4. "Celery Beat + Notification Workers"
Bullets:
- scan_due
- deliver_due
- stale-lock recovery

5. "LiveKit Realtime Agent"
Bullets:
- Voice: OpenAI Realtime
- Text chat: gpt-4o-mini + RAG
- lk.chat / lk.transcript
- lk.control web-search toggle

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

ZONE 4: External Services
Draw these provider cards only:

1. "Gemini LLM"
Sub-label: "OpenAI-compatible API; normalize TTS scripts"

2. "OpenAI Embeddings"
Sub-label: "text-embedding-3-small"

3. "Edge TTS"
Sub-label: "audio segments + review audio"

4. "LiveKit Cloud Room"
Sub-label: "realtime audio + DataChannel transport"

5. "OpenAI Realtime"
Sub-label: "voice: gpt-realtime + gpt-4o-transcribe"

6. "OpenAI Chat LLM"
Sub-label: "typed chat: gpt-4o-mini"

7. "Tavily Search"
Sub-label: "optional web lookup"

CORRECT ARROWS:

Client/API:
- Flutter Mobile App -> FastAPI API Server, label "REST API"
- Flutter Mobile App -> LiveKit Cloud Room, label "LiveKit SDK"

Queue:
- FastAPI API Server -> Redis Cloud Broker, label "enqueue task IDs"
- Redis Cloud Broker -> Celery Document Worker, label "document queue"
- Redis Cloud Broker -> Celery Beat + Notification Workers, label "notification / maintenance queues"

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

LiveKit Chat/Voice:
- Flutter Mobile App -> LiveKit Cloud Room, label "voice audio + lk.chat"
- LiveKit Realtime Agent <-> LiveKit Cloud Room, label "agent room connection"
- LiveKit Realtime Agent -> OpenAI Realtime, label "voice STT + voice response"
- LiveKit Realtime Agent -> OpenAI Chat LLM, label "typed chat answer"
- LiveKit Realtime Agent <-> Supabase Postgres + pgvector, label "chat history + RAG"
- LiveKit Realtime Agent -> Tavily Search, label "optional web search"

Notifications:
- Celery Beat + Notification Workers -> Supabase Postgres + pgvector, label "scan due reminders/reviews"
- Celery Beat + Notification Workers -> notification_outbox, label "create/claim due outbox"
- Celery Beat + Notification Workers -> user_notifications, label "deliver in-app"

Important: notification_outbox and user_notifications are table groups inside Supabase Postgres + pgvector. If necessary, draw small callout chips next to the Postgres box, but do not connect notification workers to Supabase Storage.

ZONE 5: Production Learning Loop
Draw a clear horizontal band at the bottom:
Book READY -> User listens to segments -> FE sends progress -> chapter_learning_progress -> >=80% or manual complete -> Create spaced_review_items -> scan_due -> notification_outbox -> deliver_due -> user_notifications

Note under the loop:
"Book READY does not mean User COMPLETED"

Bottom callouts:
- "Postgres is the source of truth"
- "Redis is only the Celery broker"
- "Typed chat uses LiveKit DataChannel + text LLM"
- "Spaced review starts after chapter completion"
- "First playable chapter unlocks early listening"
- "In-app notification now; push notification is future work"
- "Auth currently planned to replace mock user ID"

STRICT NEGATIVE RULES:
- Do NOT draw Redis twice.
- Do NOT put Redis in External Services if it is already in Backend Runtime.
- Do NOT draw typed chat going to OpenAI Realtime.
- Do NOT imply OpenAI Realtime handles typed chat.
- Do NOT draw Flutter connecting directly to the backend agent; Flutter connects to LiveKit Cloud Room.
- Do NOT draw any arrow from Celery Beat + Notification Workers to Gemini LLM.
- Do NOT draw any arrow from Celery Beat + Notification Workers to Edge TTS.
- Do NOT draw any arrow from Celery Beat + Notification Workers to OpenAI Embeddings.
- Do NOT draw any arrow from Celery Beat + Notification Workers to Supabase Storage.
- Do NOT draw Pinecone.
- Do NOT draw RabbitMQ.
- Do NOT draw Firebase Push as implemented.
- Do NOT draw Supabase Auth as implemented.
- Do NOT draw OCR/scanned PDF processing as implemented.
- Do NOT imply spaced review is created when chapter audio is generated.

TEXT QUALITY:
- Spell these labels exactly:
  - "lk.chat / lk.transcript"
  - "lk.control"
  - "OpenAI Chat LLM"
  - "gpt-4o-mini"
  - "OpenAI Realtime"
  - "enqueue task IDs"
  - "chapter_processing_states"
  - "reading_plan_schedule_slots"
  - "notification_outbox"
  - "user_notifications"
  - "deliver in-app"
- Keep text large enough to read in a presentation slide.
- If a label would be too small, remove less important arrows rather than shrinking text.
```

## Prompt Update Sau Khi Verify Ảnh V5

Ảnh V5 đã **tốt hơn rất nhiều**:

- Redis chỉ còn một box trong Backend Runtime.
- Đã có `OpenAI Chat LLM`.
- Đã ghi rõ typed chat dùng `gpt-4o-mini + RAG`.
- Các provider cho document pipeline (`Gemini`, `Embeddings`, `Edge TTS`) đã nối đúng từ `Celery Document Worker`.

Nhưng vẫn chưa nên chốt vì lỗi chính còn nằm ở **mũi tên realtime**:

1. `LiveKit SDK` đang bị vẽ như mũi tên quay về Flutter, chưa thể hiện rõ Flutter kết nối tới `LiveKit Cloud Room`.
2. `speech-to-text + realtime voice response` đang chĩa gần/nhầm vào `LiveKit Cloud Room`. Đúng là `OpenAI Realtime` xử lý voice model; `LiveKit Cloud Room` chỉ là transport hub.
3. `text answer: gpt-4o-mini` chưa chĩa rõ vào `OpenAI Chat LLM`.
4. `deliver in-app` còn bị kéo sang vùng External Services. Đúng là notification chỉ ghi/claim trong Postgres (`notification_outbox`, `user_notifications`).
5. Dù đã có note typed chat, sơ đồ vẫn chưa đủ trực quan để người phỏng vấn nhìn một phát hiểu: **Voice và Typed Chat cùng đi qua LiveKit transport, nhưng tách model xử lý khác nhau**.

Prompt V6 dưới đây đổi layout realtime thành một hub rõ ràng: đặt `LiveKit Cloud Room` ở giữa Flutter và Agent, không để nó lẫn trong stack provider bên phải. Đây là cách dễ vẽ đúng hơn.

```text
Create a corrected V6 TRIAM System Architecture diagram for a capstone defense slide.

Goal:
Make the architecture easy to understand and architecturally correct. The most important correction is the LiveKit Chat/Voice flow.

Canvas and style:
- 16:9 landscape.
- Clean flat vector architecture diagram.
- White or very light background.
- Large readable text.
- Minimal arrow crossings.
- Use grouped zones with subtle colors.
- Do not duplicate services.
- Do not invent services.

Title:
"TRIAM System Architecture"

Subtitle:
"Document-to-Audio Learning, LiveKit Chat/Voice Agent, Progress Tracking, and In-App Review Notifications"

Use these main zones:
1. Client
2. Realtime Transport
3. Backend Runtime - Hugging Face Docker Space
4. Data Layer - Supabase
5. External AI Services
6. Production Learning Loop

IMPORTANT LAYOUT:
- Put "Flutter Mobile App" on the far left.
- Put "LiveKit Cloud Room" as a standalone transport hub between Flutter and the Backend Runtime, not inside the right-side AI provider stack.
- Put "LiveKit Realtime Agent" inside Backend Runtime, horizontally aligned with LiveKit Cloud Room.
- Put "OpenAI Realtime", "OpenAI Chat LLM", and "Tavily Search" to the right of LiveKit Realtime Agent as Agent AI Services.
- Put "Gemini LLM", "OpenAI Embeddings", and "Edge TTS" to the right of Celery Document Worker as Document AI Services.
- Put "Celery Beat + Notification Workers" near Supabase Postgres, not near External AI Services.

ZONE 1: Client
Box: "Flutter Mobile App"
Items:
- Upload Document
- Reading Plan
- Audio Player
- Progress Tracking
- Study Chat / Voice
- In-App Notifications

ZONE 2: Realtime Transport
Box: "LiveKit Cloud Room"
Sub-label:
- realtime audio transport
- DataChannel: lk.chat / lk.transcript / lk.control

ZONE 3: Backend Runtime - Hugging Face Docker Space
Components:

1. "FastAPI API Server"
Bullets:
- Upload / Books / Plans
- LiveKit token API
- Jobs & Processing Status
- Study Context & Chat Threads
- Learning Progress API
- Notifications API

2. "Redis Cloud Broker"
Bullets:
- document queue
- notification queue
- maintenance queue

3. "Celery Document Worker"
Bullets:
- Parse chapters
- RAG embeddings
- LLM normalize
- TTS audio generation
- Partial-ready unlock

4. "Celery Beat + Notification Workers"
Bullets:
- scan_due
- deliver_due
- stale-lock recovery

5. "LiveKit Realtime Agent"
Bullets:
- Voice lane: OpenAI Realtime
- Typed chat lane: OpenAI Chat LLM + RAG
- publishes lk.chat / lk.transcript
- reads lk.control web-search toggle

ZONE 4: Data Layer - Supabase
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

ZONE 5: External AI Services
Group A: "Document AI Services"
- Gemini LLM
  "normalize TTS scripts"
- OpenAI Embeddings
  "text-embedding-3-small"
- Edge TTS
  "audio segments + review audio"

Group B: "Agent AI Services"
- OpenAI Realtime
  "voice: STT + realtime voice response"
- OpenAI Chat LLM
  "typed chat: gpt-4o-mini"
- Tavily Search
  "optional web lookup"

CORRECT ARROWS:

Client and API:
- Flutter Mobile App -> FastAPI API Server, label "REST API"
- FastAPI API Server -> Flutter Mobile App, label "LiveKit token + API responses"

Realtime transport:
- Flutter Mobile App <-> LiveKit Cloud Room, label "LiveKit SDK: audio + DataChannel"
- LiveKit Realtime Agent <-> LiveKit Cloud Room, label "agent room connection"

Voice lane:
- Flutter Mobile App -> LiveKit Cloud Room -> LiveKit Realtime Agent, label "voice audio"
- LiveKit Realtime Agent -> OpenAI Realtime, label "voice STT + response"
- LiveKit Realtime Agent -> LiveKit Cloud Room -> Flutter Mobile App, label "assistant voice/audio"

Typed chat lane:
- Flutter Mobile App -> LiveKit Cloud Room -> LiveKit Realtime Agent, label "typed text via lk.chat"
- LiveKit Realtime Agent -> OpenAI Chat LLM, label "text answer: gpt-4o-mini"
- LiveKit Realtime Agent <-> Supabase Postgres + pgvector, label "chat history + RAG"
- LiveKit Realtime Agent -> Tavily Search, label "optional web search"
- LiveKit Realtime Agent -> LiveKit Cloud Room -> Flutter Mobile App, label "lk.chat + lk.transcript"

Task queue:
- FastAPI API Server -> Redis Cloud Broker, label "enqueue task IDs"
- Redis Cloud Broker -> Celery Document Worker, label "document queue"
- Redis Cloud Broker -> Celery Beat + Notification Workers, label "notification / maintenance queues"

Document processing:
- FastAPI API Server -> Supabase Storage, label "upload original document"
- FastAPI API Server <-> Supabase Postgres + pgvector, label "CRUD + polling state"
- Celery Document Worker <-> Supabase Postgres + pgvector, label "jobs, segments, vectors, progress"
- Celery Document Worker <-> Supabase Storage, label "download document / upload audio"
- Celery Document Worker -> Gemini LLM, label "normalize"
- Celery Document Worker -> OpenAI Embeddings, label "embed chunks"
- Celery Document Worker -> Edge TTS, label "generate audio"

Notifications:
- Celery Beat + Notification Workers -> Supabase Postgres + pgvector, label "scan due reminders/reviews"
- Celery Beat + Notification Workers -> Supabase Postgres + pgvector, label "create/claim notification_outbox"
- Celery Beat + Notification Workers -> Supabase Postgres + pgvector, label "deliver user_notifications"

Important notification rule:
Do not draw any notification arrow to Supabase Storage or External AI Services. In-app notification delivery means creating rows in Postgres user_notifications.

ZONE 6: Production Learning Loop
Draw a clear horizontal band at the bottom:
Book READY -> User listens to segments -> FE sends progress -> chapter_learning_progress -> >=80% or manual complete -> Create spaced_review_items -> scan_due -> notification_outbox -> deliver_due -> user_notifications

Note under the loop:
"Book READY does not mean User COMPLETED"

Bottom callouts:
- "Postgres is the source of truth"
- "Redis is only the Celery broker"
- "Voice uses OpenAI Realtime"
- "Typed chat uses LiveKit DataChannel + text LLM"
- "Spaced review starts after chapter completion"
- "First playable chapter unlocks early listening"
- "In-app notification now; push notification is future work"
- "Auth currently planned to replace mock user ID"

STRICT NEGATIVE RULES:
- Do NOT draw Redis twice.
- Do NOT draw LiveKit Cloud Room as an AI model.
- Do NOT draw speech-to-text pointing to LiveKit Cloud Room. It must point to OpenAI Realtime.
- Do NOT draw typed chat pointing to OpenAI Realtime. It must point to OpenAI Chat LLM.
- Do NOT imply OpenAI Realtime handles typed chat.
- Do NOT draw Flutter connecting directly to LiveKit Realtime Agent. Flutter connects to LiveKit Cloud Room.
- Do NOT draw Celery Beat + Notification Workers calling Gemini LLM, Edge TTS, OpenAI Embeddings, OpenAI Realtime, OpenAI Chat LLM, or Tavily.
- Do NOT draw Celery Beat + Notification Workers writing to Supabase Storage.
- Do NOT draw Pinecone.
- Do NOT draw RabbitMQ.
- Do NOT draw Firebase Push as implemented.
- Do NOT draw Supabase Auth as implemented.
- Do NOT draw OCR/scanned PDF processing as implemented.
- Do NOT imply spaced review is created when chapter audio is generated.

TEXT QUALITY:
- Spell these labels exactly:
  - "LiveKit Cloud Room"
  - "lk.chat / lk.transcript"
  - "lk.control"
  - "OpenAI Chat LLM"
  - "gpt-4o-mini"
  - "OpenAI Realtime"
  - "enqueue task IDs"
  - "chapter_processing_states"
  - "reading_plan_schedule_slots"
  - "notification_outbox"
  - "user_notifications"
  - "deliver user_notifications"
- Keep text large enough to read in a presentation slide.
- Prefer fewer correct arrows over many confusing arrows.
- If an arrow label would be too small, remove that label rather than shrinking all text.
```

## Prompt Update Sau Khi Verify Ảnh V6

Ảnh V6 đã tiến bộ ở chỗ đặt `LiveKit Cloud Room` thành hub riêng, nhưng **đúng như em nhận xét: đường REST API đang sai**.

Các lỗi cần sửa:

1. `REST API` đang chĩa vào vùng `Realtime Transport`. Sai. REST API phải đi **trực tiếp từ Flutter Mobile App tới FastAPI API Server**.
2. `LiveKit token + API responses` đang vẽ như đi từ `Realtime Transport` về Flutter. Sai. Token/API response là do **FastAPI trả về Flutter qua REST**, không phải LiveKit Cloud Room trả.
3. Các đường `voice STT + response`, `text answer: gpt-4o-mini`, `optional web search` vẫn đang bị vẽ như xuất phát từ `Celery Beat + Notification Workers`. Sai. Ba đường này phải xuất phát từ **LiveKit Realtime Agent**.
4. `upload original document` đang nằm gần/như xuất phát từ Agent. Sai. Upload tài liệu gốc là **Flutter -> FastAPI -> Supabase Storage**.
5. Notification worker vẫn có mũi tên dễ gây hiểu nhầm sang vùng khác. Nó chỉ nên chạm tới Postgres/outbox/user_notifications.

Prompt V7 dưới đây khóa lại các đường đi bằng cách chia thành 4 cụm flow riêng: REST/API, LiveKit realtime, Document processing, Notification.

```text
Create a corrected V7 TRIAM System Architecture diagram for a capstone defense slide.

Main goal:
Fix all arrow origins and destinations. The REST API path must bypass LiveKit Cloud Room. LiveKit Cloud Room is only realtime transport.

Canvas and style:
- 16:9 landscape.
- Clean flat vector architecture diagram.
- White or light background.
- Large readable text.
- Use grouped zones with subtle colors.
- Use orthogonal arrows with clear source and destination anchors.
- Prefer fewer correct arrows over many confusing arrows.
- Do not draw arrows through unrelated boxes.
- Do not duplicate services.

Title:
"TRIAM System Architecture"

Subtitle:
"Document-to-Audio Learning, LiveKit Chat/Voice Agent, Progress Tracking, and In-App Review Notifications"

LAYOUT:
Use 6 zones:
1. Client on the far left.
2. Backend Runtime in the center.
3. Realtime Transport between Client and LiveKit Agent, slightly below the REST/API line.
4. Data Layer below Backend Runtime.
5. External AI Services on the far right.
6. Production Learning Loop at the bottom.

IMPORTANT LAYOUT RULES:
- Place "FastAPI API Server" directly to the right of Flutter so a straight horizontal REST arrow can go from Flutter to FastAPI.
- Place "LiveKit Cloud Room" below the REST arrow, between Flutter and "LiveKit Realtime Agent".
- Place "LiveKit Realtime Agent" directly to the right of LiveKit Cloud Room.
- Place "Agent AI Services" directly to the right of LiveKit Realtime Agent.
- Place "Celery Beat + Notification Workers" near Supabase Postgres, not between Agent and Agent AI Services.
- Place "Celery Document Worker" near Document AI Services.

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
- LiveKit token API
- Jobs & Processing Status
- Study Context & Chat Threads
- Learning Progress API
- Notifications API

2. "Redis Cloud Broker"
Bullets:
- document queue
- notification queue
- maintenance queue

3. "Celery Document Worker"
Bullets:
- Parse chapters
- RAG embeddings
- LLM normalize
- TTS audio generation
- Partial-ready unlock

4. "Celery Beat + Notification Workers"
Bullets:
- scan_due
- deliver_due
- stale-lock recovery

5. "LiveKit Realtime Agent"
Bullets:
- Voice lane: OpenAI Realtime
- Typed chat lane: OpenAI Chat LLM + RAG
- publishes lk.chat / lk.transcript
- reads lk.control web-search toggle

ZONE 3: Realtime Transport
Box: "LiveKit Cloud Room"
Sub-label:
- realtime audio transport
- DataChannel: lk.chat / lk.transcript / lk.control

ZONE 4: Data Layer - Supabase
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

ZONE 5: External AI Services
Group A: "Document AI Services"
- Gemini LLM
  "normalize TTS scripts"
- OpenAI Embeddings
  "text-embedding-3-small"
- Edge TTS
  "audio segments + review audio"

Group B: "Agent AI Services"
- OpenAI Realtime
  "voice: STT + realtime voice response"
- OpenAI Chat LLM
  "typed chat: gpt-4o-mini"
- Tavily Search
  "optional web lookup"

FLOW GROUP 1 - REST/API, MUST BE DIRECT:
- Flutter Mobile App -> FastAPI API Server, label "REST API"
- FastAPI API Server -> Flutter Mobile App, label "API responses + LiveKit token"

Critical REST rule:
Do NOT draw REST API to LiveKit Cloud Room.
Do NOT draw LiveKit token from LiveKit Cloud Room.
FastAPI issues the LiveKit token; LiveKit Cloud Room only receives authenticated SDK connections.

FLOW GROUP 2 - LIVEKIT REALTIME, MUST USE LIVEKIT CLOUD ROOM AS HUB:
- Flutter Mobile App <-> LiveKit Cloud Room, label "LiveKit SDK: audio + DataChannel"
- LiveKit Cloud Room <-> LiveKit Realtime Agent, label "agent room connection"

Voice lane:
- Flutter Mobile App -> LiveKit Cloud Room, label "voice audio"
- LiveKit Cloud Room -> LiveKit Realtime Agent, label "voice audio"
- LiveKit Realtime Agent -> OpenAI Realtime, label "voice STT + response"
- LiveKit Realtime Agent -> LiveKit Cloud Room, label "assistant voice/audio"
- LiveKit Cloud Room -> Flutter Mobile App, label "assistant voice/audio"

Typed chat lane:
- Flutter Mobile App -> LiveKit Cloud Room, label "typed text via lk.chat"
- LiveKit Cloud Room -> LiveKit Realtime Agent, label "typed text via lk.chat"
- LiveKit Realtime Agent -> OpenAI Chat LLM, label "text answer: gpt-4o-mini"
- LiveKit Realtime Agent <-> Supabase Postgres + pgvector, label "chat history + RAG"
- LiveKit Realtime Agent -> Tavily Search, label "optional web search"
- LiveKit Realtime Agent -> LiveKit Cloud Room, label "lk.chat + lk.transcript"
- LiveKit Cloud Room -> Flutter Mobile App, label "lk.chat + lk.transcript"

Critical Agent AI rule:
The arrows to OpenAI Realtime, OpenAI Chat LLM, and Tavily Search must start from the "LiveKit Realtime Agent" box.
They must NOT start from Celery Beat + Notification Workers.

FLOW GROUP 3 - DOCUMENT PROCESSING:
- FastAPI API Server -> Redis Cloud Broker, label "enqueue task IDs"
- Redis Cloud Broker -> Celery Document Worker, label "document queue"
- FastAPI API Server -> Supabase Storage, label "upload original document"
- FastAPI API Server <-> Supabase Postgres + pgvector, label "CRUD + polling state"
- Celery Document Worker <-> Supabase Postgres + pgvector, label "jobs, segments, vectors, progress"
- Celery Document Worker <-> Supabase Storage, label "download document / upload audio"
- Celery Document Worker -> Gemini LLM, label "normalize"
- Celery Document Worker -> OpenAI Embeddings, label "embed chunks"
- Celery Document Worker -> Edge TTS, label "generate audio"

Critical upload rule:
"upload original document" must start from FastAPI API Server, not from LiveKit Realtime Agent.

FLOW GROUP 4 - NOTIFICATIONS:
- Redis Cloud Broker -> Celery Beat + Notification Workers, label "notification / maintenance queues"
- Celery Beat + Notification Workers -> Supabase Postgres + pgvector, label "scan due reminders/reviews"
- Celery Beat + Notification Workers -> Supabase Postgres + pgvector, label "create/claim notification_outbox"
- Celery Beat + Notification Workers -> Supabase Postgres + pgvector, label "deliver user_notifications"

Critical notification rule:
Notification workers only interact with Postgres tables: notification_outbox and user_notifications.
Do NOT draw notification workers to Supabase Storage or any AI provider.

ZONE 6: Production Learning Loop
Draw a clear horizontal band at the bottom:
Book READY -> User listens to segments -> FE sends progress -> chapter_learning_progress -> >=80% or manual complete -> Create spaced_review_items -> scan_due -> notification_outbox -> deliver_due -> user_notifications

Note under the loop:
"Book READY does not mean User COMPLETED"

Bottom callouts:
- "Postgres is the source of truth"
- "Redis is only the Celery broker"
- "FastAPI issues LiveKit token"
- "LiveKit Cloud Room is transport only"
- "Voice uses OpenAI Realtime"
- "Typed chat uses LiveKit DataChannel + text LLM"
- "Spaced review starts after chapter completion"
- "In-app notification now; push notification is future work"
- "Auth currently planned to replace mock user ID"

STRICT NEGATIVE RULES:
- Do NOT draw REST API to LiveKit Cloud Room.
- Do NOT draw LiveKit token from LiveKit Cloud Room.
- Do NOT draw Flutter connecting directly to LiveKit Realtime Agent.
- Do NOT draw typed chat pointing to OpenAI Realtime.
- Do NOT imply OpenAI Realtime handles typed chat.
- Do NOT draw speech-to-text pointing to LiveKit Cloud Room. It must point to OpenAI Realtime.
- Do NOT draw arrows from Celery Beat + Notification Workers to OpenAI Realtime, OpenAI Chat LLM, Tavily Search, Gemini LLM, Edge TTS, or OpenAI Embeddings.
- Do NOT draw notification workers writing to Supabase Storage.
- Do NOT draw upload original document from LiveKit Realtime Agent.
- Do NOT draw Redis twice.
- Do NOT draw Pinecone.
- Do NOT draw RabbitMQ.
- Do NOT draw Firebase Push as implemented.
- Do NOT draw Supabase Auth as implemented.
- Do NOT draw OCR/scanned PDF processing as implemented.
- Do NOT imply spaced review is created when chapter audio is generated.

TEXT QUALITY:
- Spell these labels exactly:
  - "REST API"
  - "API responses + LiveKit token"
  - "LiveKit Cloud Room"
  - "LiveKit SDK: audio + DataChannel"
  - "lk.chat / lk.transcript"
  - "lk.control"
  - "OpenAI Chat LLM"
  - "gpt-4o-mini"
  - "OpenAI Realtime"
  - "enqueue task IDs"
  - "chapter_processing_states"
  - "reading_plan_schedule_slots"
  - "notification_outbox"
  - "user_notifications"
  - "deliver user_notifications"
- Keep text readable in a presentation slide.
- If the diagram gets crowded, remove less important arrow labels, but keep the main flows correct.
```

# TRIAM Thesis Style Guide

## Chapter Scope

Use the project outline as the controlling context:

- Chapter 1: problem, motivation, goals, scope.
- Chapter 2: project overview and related context.
- Chapter 3: theory foundation. Keep it concise and conceptual.
- Chapter 4: system analysis and design.
- Chapters 5-8: core implementation features.
- Chapter 9: build, deployment, UI/UX.
- Chapter 10: conclusion and future work.

Chapter 3 should let the reader understand later implementation chapters without pre-explaining all implementation decisions.

## Good Section Shape

For a technology/theory section, prefer:

```text
Khái niệm -> Nguyên lý chính -> Hạn chế -> Vai trò trong TRIAM
```

Example:

```text
Retrieval-Augmented Generation (RAG) là hướng tiếp cận kết hợp truy xuất thông tin với mô hình ngôn ngữ lớn. Thay vì yêu cầu mô hình trả lời chỉ dựa trên tri thức đã học trong quá trình huấn luyện, hệ thống truy xuất các đoạn tài liệu liên quan và đưa chúng vào ngữ cảnh đầu vào của mô hình. Cách tiếp cận này phù hợp với các hệ thống sử dụng tài liệu riêng, vì tri thức có thể được cập nhật bằng cách lập chỉ mục tài liệu mới mà không cần huấn luyện lại mô hình.

Trong phạm vi TRIAM, RAG là cơ sở lý thuyết cho chức năng hỏi đáp theo tài liệu học tập. Người học có thể đặt câu hỏi bằng ngôn ngữ tự nhiên, còn hệ thống sử dụng truy xuất ngữ cảnh để giới hạn phản hồi của trợ lý vào nội dung tài liệu đã cung cấp.
```

## Tone Rules

Prefer:

- "Về bản chất, ..."
- "Trong phạm vi hệ thống TRIAM, ..."
- "Cách tiếp cận này phù hợp với ..."
- "Hạn chế chính của phương pháp này là ..."
- "Điều này tạo cơ sở cho ..."

Avoid:

- "Công nghệ này cực kỳ mạnh mẽ..."
- "Giúp tối ưu hoàn toàn..."
- "AI hiểu như con người..."
- "Đảm bảo không bao giờ sai..."
- "Đây là công nghệ hiện đại nhất..."

## Weak-to-Strong Rewrites

Weak:

```text
LLM rất thông minh và có thể trả lời nhiều câu hỏi giống con người.
```

Better:

```text
LLM có khả năng sinh văn bản mạch lạc dựa trên ngữ cảnh đầu vào và các mẫu ngôn ngữ đã học trong quá trình huấn luyện. Tuy nhiên, khả năng này không đồng nghĩa với việc mô hình luôn có tri thức chính xác về một tài liệu cụ thể.
```

Weak:

```text
RAG giúp hệ thống trả lời đúng hơn.
```

Better:

```text
RAG cải thiện độ bám nguồn của câu trả lời bằng cách cung cấp cho mô hình các đoạn tài liệu liên quan trước khi sinh phản hồi. Hiệu quả của phương pháp này phụ thuộc lớn vào chất lượng trích xuất tài liệu, chia đoạn và truy xuất ngữ cảnh.
```

Weak:

```text
FastAPI là framework hiện đại, mạnh mẽ và rất nhanh.
```

Better:

```text
FastAPI là framework Python dùng để xây dựng API, hỗ trợ khai báo kiểu dữ liệu, xử lý bất đồng bộ và tự động sinh tài liệu OpenAPI. Các đặc điểm này phù hợp với backend cần phối hợp nhiều tác vụ I/O như truy vấn cơ sở dữ liệu, gọi dịch vụ AI và điều phối xử lý nền.
```

## Terms

Use these Vietnamese terms consistently:

- Generative AI: trí tuệ nhân tạo tạo sinh
- Large Language Model: mô hình ngôn ngữ lớn
- Retrieval-Augmented Generation: tạo sinh tăng cường truy xuất
- embedding: vector nhúng or biểu diễn vector
- semantic search: tìm kiếm ngữ nghĩa
- lexical search: tìm kiếm từ khóa
- hybrid search: tìm kiếm lai
- speech-to-text: chuyển giọng nói thành văn bản
- text-to-speech: chuyển văn bản thành giọng nói
- real-time communication: truyền thông thời gian thực
- spaced repetition: lặp lại ngắt quãng or ôn tập ngắt quãng
- background task: tác vụ nền
- transactional outbox: mẫu transactional outbox or hàng đợi thông báo bền vững

Keep English names for product/framework names: FastAPI, Flutter, Next.js, PostgreSQL, pgvector, Supabase, Celery, Redis, WebRTC, LiveKit, Firebase Cloud Messaging, Tavily.

## Chapter 3 Depth Limits

Allowed in Chapter 3:

- Definitions and conceptual workflows.
- One simple formula when central, such as attention or cosine similarity.
- One short TRIAM relevance paragraph per topic.
- 1-3 citations per major topic.

Avoid in Chapter 3:

- Exact table names and DB fields.
- API endpoint names.
- Worker function names.
- Configuration constants such as chunk size, threshold, concurrency, and timeout.
- Long Mermaid diagrams.
- Test result tables.

These details belong in Chapters 4-8.

## Paragraph Checklist

Before finalizing rewritten prose, check:

- Does each paragraph make one clear point?
- Does the paragraph connect to the thesis goal?
- Are claims supported by citation, code evidence, or clearly framed as design motivation?
- Is the wording academic but still readable?
- Can any repeated "giúp", "có thể", or "hiện đại" be removed?

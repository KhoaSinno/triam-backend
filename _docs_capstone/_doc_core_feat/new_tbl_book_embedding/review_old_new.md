Bạn gửi đủ 3 thứ nên mình đánh giá công tâm hơn được: **old table**, **new table**, và **EPUB gốc**. Kết luận của mình là:

**Kiến trúc mới với `book_section_knowledge` đúng hơn rất nhiều cho RAG hỏi đáp sách. Nhưng chưa nên xóa bảng cũ ngay khi lên production. Nên chuyển bảng mới thành canonical RAG source, còn bảng cũ chỉ giữ tạm cho fallback/learning-unit/audio hoặc rollback.**

## 1. So sánh thực tế từ dữ liệu bạn gửi

Mình đọc EPUB gốc, nó có 6 chapter:

```text
Chapter 1: ~23.8k chars
Chapter 2: ~30.3k chars
Chapter 3: ~41.6k chars
Chapter 4: ~26.3k chars
Chapter 5: ~23.1k chars
Chapter 6: ~11.9k chars
Tổng: ~157.1k chars normalized
```

### Bảng cũ `book_knowledge`

```text
Số chunk: 59
Gắn với: learning_unit_id
Số learning_unit_id: 3
Coverage EPUB gốc: ~37.46%
Chỉ cover chapter: 1, 5, 6
Chapter 2, 3, 4: 0% coverage
Median chunk: ~1,247 chars
Embedding: 1536 dims
```

Cụ thể bảng cũ có 3 learning unit:

```text
The Dream and the Safe Haven          → chapter 1
The Climax: Shattered Dreams...       → chapter 5
The Tragic Resolution...              → chapter 6
```

Nghĩa là bảng cũ **không phải full-book index**. Nó là index theo learning unit đã generate. Với dữ liệu bạn gửi, nếu user hỏi nội dung nằm ở chapter 2, 3, 4 thì bảng cũ gần như không có dữ liệu để trả lời.

### Bảng mới `book_section_knowledge`

```text
Số chunk: 53
Gắn với: section_id
Số section_id: 6
Coverage EPUB gốc: ~99.99%
Cover đủ chapter: 1, 2, 3, 4, 5, 6
Median chunk: ~3,570 chars
Embedding: 1536 dims
Có thêm: embedding_model, embedding_version, char_count, content_hash, search_text
```

Mapping mới rất sạch:

```text
section 1 → chapter 1 → 8 chunks
section 2 → chapter 2 → 10 chunks
section 3 → chapter 3 → 14 chunks
section 4 → chapter 4 → 9 chunks
section 5 → chapter 5 → 8 chunks
section 6 → chapter 6 → 4 chunks
```

Về mặt **coverage**, bảng mới thắng tuyệt đối.

## 2. Đánh giá công tâm: bảng mới có thật sự ổn hơn không?

Có. Với mục tiêu **hỏi đáp/RAG trên sách**, bảng mới tốt hơn rõ ràng.

Lý do chính không phải vì “thêm bảng mới là hiện đại hơn”, mà vì bảng mới bám vào đúng source-of-truth:

```text
EPUB gốc
→ BookSection
→ book_section_knowledge
→ RAG
```

Còn bảng cũ là:

```text
EPUB gốc
→ LearningUnit được generate
→ book_knowledge
→ RAG
```

`LearningUnit` là sản phẩm phục vụ học/nghe/audio. Nó không nên là nguồn chính cho hỏi đáp toàn bộ sách.

Nói thẳng: **bảng cũ phù hợp cho learning flow, không phù hợp làm canonical QA index.**

## 3. Cải thiện có “vượt trội” không?

Với dữ liệu bạn gửi: **có, vượt trội về coverage và correctness.**

Vì bảng cũ chỉ cover khoảng:

```text
~37.46% nội dung EPUB
```

còn bảng mới cover:

```text
~99.99% nội dung EPUB
```

Đây không phải cải thiện nhỏ. Nếu user hỏi:

```text
Curley xuất hiện ở đâu?
Vai trò của Candy?
Crooks nói gì trong chương 4?
Bunk house được mô tả như thế nào?
```

thì bảng cũ có thể fail hoặc trả thiếu vì nó không index chapter 2, 3, 4. Bảng mới có dữ liệu để tìm.

Nhưng mình cũng không nói bảng mới “hoàn hảo”. Nó tốt hơn về kiến trúc, nhưng answer quality vẫn phụ thuộc vào chunking, reranking, router, prompt, và tool orchestration.

## 4. Điểm yếu của bảng mới hiện tại

Bảng mới đúng hướng, nhưng mình thấy vài điểm cần chỉnh trước production.

### 4.1 `search_text` đang bị lặp số chương

Ví dụ search text đầu chunk chapter 1 bắt đầu kiểu:

```text
1 1 1 1 1 ...
```

chapter 2 cũng kiểu:

```text
2 2 2 2 2 ...
```

Cái này không chết hệ thống, nhưng có thể làm hybrid/BM25 bị bias hơi bẩn. Nên clean lại `search_text`:

```text
- Không lặp chapter number nhiều lần.
- Section title/path chỉ đưa vào 1 lần.
- Nội dung chính normalize sạch.
```

Nên là:

```text
book: Of Mice and Men
section: Chapter 1
content: ...
```

Không nên là:

```text
1 1 1 1 1 ...
```

### 4.2 `token_count` đang là `None`

Trong bảng mới, `char_count` đúng, nhưng `token_count` đều `None`.

Với RAG, `token_count` rất hữu ích để:

```text
- giới hạn context gửi vào model
- chọn chunk vừa đủ
- tránh prompt quá dài
- debug latency/cost
```

Nên production nên fill `token_count`.

### 4.3 `content_hash` cần kiểm tra lại

Trong file export, `content_hash` không khớp với SHA-256 trực tiếp của `content` hoặc `search_text`.

Cái này chưa chắc là bug, vì có thể bạn hash raw source trước khi export hoặc hash normalized text theo hàm riêng. Nhưng nếu mục tiêu của `content_hash` là idempotent indexing, smart re-index, detect changed chunk, thì cần bảo đảm:

```text
cùng content + cùng chunking config → cùng hash
content thay đổi → hash thay đổi
```

Nếu không, sau này backfill/update dễ bị duplicate hoặc không re-index đúng.

### 4.4 Chunk mới khá lớn

Median chunk mới khoảng **3,570 chars**, còn old khoảng **1,247 chars**.

Chunk lớn có lợi:

```text
- nhiều context hơn
- ít mất ngữ cảnh
- số vector ít hơn
```

Nhưng cũng có hại:

```text
- citation kém chính xác hơn
- top_k=6 có thể đưa quá nhiều text vào model
- retrieval có thể kém sắc nét ở câu hỏi rất cụ thể
```

Mình không bảo phải đổi ngay. Nhưng nếu voice agent cần nhanh và chính xác, bạn nên test thêm chunk khoảng:

```text
1,800–2,500 chars
overlap 250–400 chars
```

Hiện tại 3,500 chars vẫn dùng được, nhưng cần rerank/trim evidence tốt.

### 4.5 Thiếu offset cho citation chính xác

Bảng mới có `section_id` và `chunk_index`, nhưng nếu muốn sau này FE highlight/citation tốt, nên thêm:

```text
start_char
end_char
```

hoặc:

```text
section_start_offset
section_end_offset
```

Nếu không có offset, bạn chỉ biết chunk thuộc section nào, chưa chỉ được đoạn chính xác.

## 5. Có nên giữ bảng mới không?

Có. Mình khuyên giữ.

Kiến trúc đúng nên là:

```text
BookSection
  ↓
book_section_knowledge
  ↓
canonical RAG / hybrid retrieval / citation
```

Còn learning/audio nên là:

```text
LearningUnit
  ↓
audio generation / study plan / progress / lesson mode
```

Đừng để `LearningUnit` quyết định khả năng hỏi đáp toàn bộ sách.

## 6. Có nên xóa bảng cũ khi production không?

**Không xóa ngay.**

Câu trả lời đúng hơn là:

```text
Production: dùng book_section_knowledge làm RAG chính.
Không dùng book_knowledge làm RAG chính nữa.
Nhưng vẫn giữ book_knowledge một thời gian cho rollback hoặc learning-unit/audio flow.
Chỉ drop bảng cũ khi chắc chắn không còn code path nào dùng.
```

Với dữ liệu bạn gửi, mình còn khuyên cẩn thận hơn:

**Không nên fallback từ canonical RAG sang old table chỉ vì canonical không tìm thấy kết quả.** Vì old table là partial index, có thể làm câu trả lời lệch.

Fallback legacy chỉ nên dùng khi:

```text
book_section_knowledge chưa được build cho sách đó
hoặc migration/backfill chưa hoàn tất
```

Không nên dùng kiểu:

```text
canonical search no hit → fallback old table
```

vì nếu canonical không tìm thấy, có thể thật sự không có evidence. Fallback sang bảng cũ thiếu dữ liệu có thể tạo câu trả lời sai.

## 7. Kiến trúc production mình khuyên

### Giai đoạn 1: dual table nhưng canonical primary

```env
AGENT_CANONICAL_SECTION_RAG_ENABLED=true
AGENT_CANONICAL_SECTION_RAG_FALLBACK_LEGACY=true
```

Nhưng logic fallback nên là:

```text
Nếu sách chưa có book_section_knowledge → dùng legacy.
Nếu sách đã có book_section_knowledge → dùng canonical only.
```

### Giai đoạn 2: đo coverage

Thêm log:

```text
book_section_knowledge_count
section_coverage_ratio
canonical_rag_found
legacy_fallback_used
retrieval_section_ids
retrieval_result_count
answer_source
```

Với mỗi sách, nếu:

```text
section_count đủ
chunk_count > 0
coverage đủ
canonical retrieval ổn
```

thì coi sách đó đã migrated.

### Giai đoạn 3: deprecate old table

Khi đã chắc chắn:

```text
- audio flow không cần book_knowledge
- learning unit flow không cần book_knowledge
- RAG không cần book_knowledge
- rollback không cần nữa
```

thì mới drop bảng cũ.

## 8. Vậy vấn đề test hiện tại có phải do bảng mới không?

Không. Dữ liệu bảng mới của bạn nhìn **ổn hơn bảng cũ rất nhiều**.

Vấn đề test gần đây nhiều khả năng nằm ở tầng:

```text
GroundingRouter
SharedPolicy
QueryGuard
Realtime watchdog/resume
```

chứ không phải do `book_section_knowledge`.

Việc bạn tắt:

```env
AGENT_GROUNDING_ROUTER_ENABLED=false
```

rồi thấy RAG chạy tốt là bằng chứng rất mạnh: **data/index mới tìm được, nhưng router trước đó chặn quá sớm.**

## Kết luận công tâm

Mình chấm kiến trúc mới như sau:

```text
Ý tưởng kiến trúc: 9/10
Độ đúng so với RAG full-book: 9/10
Dữ liệu coverage so với EPUB: rất tốt
Độ sẵn sàng production: 7/10
```

Chưa 10/10 vì cần chỉnh:

```text
1. Clean search_text.
2. Fill token_count.
3. Verify content_hash.
4. Thêm start/end offset cho citation.
5. Sửa GroundingRouter thành exact-section helper, không được chặn fallback RAG.
6. Không drop book_knowledge ngay.
```

Quyết định cuối mình khuyên:

```text
Giữ book_section_knowledge.
Dùng nó làm canonical RAG index.
Không dùng book_knowledge làm RAG chính nữa.
Không xóa book_knowledge ngay khi production.
Chỉ xóa sau khi migration, monitoring, rollback window, và code cleanup hoàn tất.
```

# FE Voice Agent + Study Context Contract Review Spec

Mục tiêu của spec này là dùng để review FE Flutter đã implement đúng 2 contract sau hay chưa:

- `_docs_implemented/doc_setup_flutter/flutter_realtime_voice_text_spec.md`
- `_docs_implemented/doc_setup_flutter/fe_imp_study_context.md`

Spec này không thay thế 2 doc gốc. Nó là checklist kiểm tra implementation hiện tại và yêu cầu chỉnh sửa nếu FE làm sai hoặc chưa rõ.

---

## 1. Contract bắt buộc: DataChannel LiveKit

### 1.1 `lk.chat`

**Yêu cầu**

- FE chỉ gửi text chat tay lên server qua topic `lk.chat`.
- Payload là UTF-8 plain text.
- Publish reliable.
- FE có thể dùng `lk.chat` để hiển thị phản hồi assistant nhanh, nhưng không được xem đây là nguồn dữ liệu chính thức cuối cùng của timeline.

**Trạng thái FE hiện tại**

- Đã làm: `LiveKitAgentService.sendChatMessage()` publish text vào `lk.chat`.
- Đã làm: FE listen `lk.chat`.
- Chưa chuẩn hoàn toàn: provider vẫn append/merge assistant message từ `lk.chat` qua `_mergeOrAppendAgentMessage(...)`.

**Yêu cầu chỉnh**

- Giữ `lk.chat` để UX phản hồi nhanh nếu muốn.
- Khi render timeline chính thức, `lk.transcript` phải là nguồn authoritative.
- Nếu vẫn render tạm từ `lk.chat`, khi nhận `lk.transcript` role `assistant` phải replace/merge rõ ràng để không duplicate và không lệch message.

### 1.2 `lk.transcript`

**Yêu cầu**

- FE chỉ subscribe/listen `lk.transcript`.
- FE tuyệt đối không publish data lên `lk.transcript`.
- Payload là JSON:

```json
{
  "v": 1,
  "type": "transcript",
  "role": "user",
  "text": "...",
  "id": "<uuid>",
  "ts": "2026-05-12T09:29:28.738+00:00"
}
```

- FE dùng `id` để dedupe.
- FE dùng `role` để render user/assistant bubble.
- FE dùng `ts` để timestamp/sort nếu cần.
- FE dùng kênh này làm nguồn chính thức cho cả:
  - user gõ text
  - user nói voice
  - assistant trả lời

**Trạng thái FE hiện tại**

- Đã làm: `LiveKitAgentService` listen topic `lk.transcript`.
- Đã làm: `_parseTranscriptEvent(...)` parse JSON role/text/id/ts.
- Đã làm một phần: `AgentNotifier._upsertTranscriptMessage(...)` upsert theo id và có chống echo theo text/time.
- Cần siết lại: vì `lk.chat` vẫn append assistant message, FE cần đảm bảo transcript replace/merge luôn thắng để timeline cuối cùng chỉ có message chuẩn từ transcript/history.

**Yêu cầu chỉnh**

- Không publish lên `lk.transcript`.
- Timeline chính thức phải ưu tiên message có `metadata.transcript == true` hoặc message load từ history.
- Các message stream tạm từ `lk.chat` phải có trạng thái tạm và bị thay thế khi transcript assistant tới.

### 1.3 `lk.control`

**Yêu cầu**

- FE publish JSON lên `lk.control` khi user bật/tắt web search:

```json
{
  "type": "toggle_web_search",
  "enabled": true
}
```

- Publish reliable.

**Trạng thái FE hiện tại**

- Chưa thấy implementation publish `lk.control` / `toggle_web_search` trong `lib/features/agent`.

**Yêu cầu chỉnh**

- Nếu UI có toggle web search, FE phải gọi publish `lk.control` trước khi gửi câu hỏi.
- Nếu chưa có UI toggle, cần ghi rõ là chưa implement và không được giả định backend tự bật web search.

---

## 2. Contract bắt buộc: Study Context -> Thread -> LiveKit Token

### 2.1 Luồng Study Context thủ công

**Yêu cầu**

Flow chuẩn:

1. `POST /study-contexts`
2. `POST /study-contexts/{context_id}/documents`
3. `POST /study-contexts/{context_id}/threads`
4. `GET /threads/{thread_id}/messages`
5. `GET /live-token/thread/{thread_id}`
6. Connect LiveKit bằng token thread.

**Trạng thái FE hiện tại**

- Đã làm: `startStudyContextSession(...)` lấy threads trong context hoặc tạo thread mới.
- Đã làm: load history qua `getThreadMessages(thread.id)`.
- Đã làm: khi có `selectedThreadId`, chat/voice gọi `connectLiveKitThread(...)` hoặc `connectLiveKitThreadForChat(...)`.

**Kết luận**

- Luồng Study Context thủ công: đạt ở mức contract chính.

### 2.2 Luồng Book Detail / Quick Chat theo sách

**Yêu cầu**

Theo `fe_imp_study_context.md`, Book Detail không được connect trực tiếp bằng `/live-token/{book_id}` nữa. Flow đúng:

1. FE gọi `GET /threads/for-book/{book_id}`.
2. BE trả về `{ context_id, thread_id, is_auto_generated: true }`.
3. FE lưu `selectedContextId = context_id`, `selectedThreadId = thread_id`.
4. FE load history: `GET /threads/{thread_id}/messages`.
5. FE lấy token: `GET /live-token/thread/{thread_id}`.
6. FE connect LiveKit bằng token thread.

**Trạng thái FE hiện tại**

- Chưa đạt.
- `BookDetailPage._askAgentAboutCurrentAudio()` đang gọi `bindListeningContext(contextId: bookId, ...)`.
- `AudiobookNowListeningPage` cũng gọi `bindListeningContext(contextId: bookId, ...)`.
- `bindListeningContext(...)` clear `selectedThreadId`.
- Khi `selectedThreadId` rỗng, `startMic()` và `sendTextMessage()` fallback sang:
  - `connectLiveKit(bookId)` -> `/api/v1/live-token/{book_id}`
  - `connectLiveKitForChat(bookId)` -> `/api/v1/live-token/{book_id}`
- Endpoint `/live-token/{book_id}` chỉ có `book_id`, không có `thread_id`, nên backend không persist được `ChatMessage` vào đúng thread và không có lịch sử hội thoại đúng.

**Yêu cầu chỉnh**

- Thêm repository method FE gọi `GET /api/v1/threads/for-book/{book_id}`.
- Thêm AgentNotifier method, ví dụ `startBookDetailSession(bookId, bookTitle)`, làm các bước:
  - gọi `/threads/for-book/{book_id}`
  - set `selectedContextId = context_id`
  - set `selectedThreadId = thread_id`
  - set `selectedBookTitle = bookTitle`
  - load history từ `/threads/{thread_id}/messages`
- `BookDetailPage._askAgentAboutCurrentAudio()` phải gọi method mới này, không gọi `bindListeningContext(contextId: bookId, ...)`.
- `AudiobookNowListeningPage` cũng phải dùng method mới nếu user chat/voice với sách đang nghe.
- Sau chỉnh sửa, mọi chat/voice từ Book Detail phải đi qua `/live-token/thread/{thread_id}`.

### 2.3 Không dùng `/live-token/{book_id}` cho app flow chính

**Yêu cầu**

- `/live-token/{book_id}` chỉ nên còn là legacy/test/debug.
- App production flow nên dùng `/live-token/thread/{thread_id}` cho cả text và voice.

**Trạng thái FE hiện tại**

- Chưa đạt vì còn fallback bookId trong `startMic()` và `sendTextMessage()`.

**Yêu cầu chỉnh**

- Sau khi Book Detail có canonical thread, fallback bookId nên bị loại khỏi app flow chính hoặc chỉ dùng cho legacy test có comment rõ.
- Nếu `selectedThreadId` rỗng, FE nên cố resolve thread từ `bookId` bằng `/threads/for-book/{book_id}` trước khi connect LiveKit.

---

## 3. Acceptance Criteria cho FE

FE chỉ đạt khi pass đủ các case sau:

1. Mở Study Context có nhiều sách -> chọn thread -> chat text -> BE lưu `ChatMessage` đúng `thread_id`.
2. Mở Study Context có nhiều sách -> voice -> BE lưu user voice transcript và assistant reply đúng `thread_id`.
3. Mở Book Detail lần đầu -> FE gọi `/threads/for-book/{book_id}` -> nhận `thread_id`.
4. Mở Book Detail chat text -> FE lấy `/live-token/thread/{thread_id}` -> BE lưu đúng canonical thread.
5. Mở Book Detail voice -> FE lấy `/live-token/thread/{thread_id}` -> BE lưu đúng canonical thread.
6. Đóng app/mở lại cùng Book Detail -> gọi lại `/threads/for-book/{book_id}` -> nhận lại cùng `thread_id` -> load được history cũ.
7. FE không publish `lk.transcript`.
8. FE dedupe transcript theo `id` và không render trùng assistant do vừa có `lk.chat` vừa có `lk.transcript`.
9. Nếu có web search toggle -> FE publish `lk.control` đúng JSON trước khi gửi câu hỏi.

---

## 4. Review Verdict hiện tại

| Hạng mục | Verdict | Ghi chú |
| --- | --- | --- |
| Listen `lk.transcript` | Đã làm | Parse JSON và upsert transcript đã có. |
| Publish text qua `lk.chat` | Đã làm | `sendChatMessage()` đã publish reliable. |
| Dùng `lk.transcript` làm nguồn chính thức | Cần chỉnh rõ | Hiện vẫn append/merge từ `lk.chat`; cần đảm bảo transcript thắng. |
| Publish `lk.control` toggle web search | Chưa thấy | Cần implement nếu UI có toggle. |
| Study Context -> Thread -> LiveKit token | Đã làm cho Study Context | `startStudyContextSession()` đi bằng thread. |
| Book Detail -> canonical thread | Chưa đạt | Hiện bind `bookId`, clear thread, fallback `/live-token/{book_id}`. |
| Persist chat/voice Book Detail | Chưa đảm bảo | Vì thiếu `thread_id` trong token bookId. |

Kết luận: FE hiện chưa đạt đầy đủ contract. Phần cần ưu tiên sửa là Book Detail / Now Listening phải resolve canonical thread bằng `/threads/for-book/{book_id}` rồi luôn connect LiveKit bằng `/live-token/thread/{thread_id}`.

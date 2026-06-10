# Phase 10.6 Implementation Guide - FE Transcript Reconciliation And Stable Message Timeline

Date: 2026-06-06  
Status: Backend implemented and tested; FE implementation pending  
Depends on: Phase 7.1, Phase 10.4, Phase 10.5  
Primary scope: LiveKit text/voice timeline, `lk.chat`, `lk.transcript`, chat history, reconnect behavior

---

## 0. Implementation Status

Backend changes completed:

- `app/services/voice_agent/transcript_store.py`
  - `save_and_publish_user(...)` and `save_and_publish_assistant(...)` now save DB first and pass the saved `chat_messages.id` into `lk.transcript`.
  - `lk.transcript.id` is stable when DB save succeeds.
  - `lk.transcript.message_id` is added for FE/REST history reconciliation.
  - `thread_id`, `source`, and `status` are added without removing old fields.
  - DB save errors no longer block transcript publish.
  - Save-failure logs include only metadata (`thread_id`, `role`, `text_len`, `error_type`), not raw message text.

Backend tests completed:

```powershell
uv run pytest tests\services\voice_agent\test_transcript_store.py -q
uv run pytest tests\services\voice_agent tests\services\agent_policy -q
uv run ruff check app\services\voice_agent\transcript_store.py tests\services\voice_agent\test_transcript_store.py
uv run ruff check app\services\voice_agent tests\services\voice_agent
uv run python -m py_compile app\services\voice_agent\transcript_store.py
uv run pytest tests -q --maxfail=1 --durations=20
```

Result:

```text
6 transcript-store tests passed.
53 voice-agent/agent-policy tests passed.
Ruff passed for changed runtime/test files.
Ruff passed for voice-agent runtime/test folders.
Py compile passed for transcript_store.py.
218 full test-suite tests passed in about 5 minutes.
```

FE still needs to implement the reducer/reconciliation rules in this document.

---

## 1. Why Phase 10.6 Exists

Sau Phase 10.5, chat text và realtime voice đã dùng chung agent policy hơn. Nhưng UI vẫn có thể xấu nếu timeline bị duplicate.

Hiện tại FE có thể nhận cùng một nội dung từ nhiều nguồn:

```text
1. local optimistic user bubble khi user gõ text
2. lk.chat plain text assistant preview
3. lk.transcript JSON committed user/assistant message
4. chat history từ REST API khi mở lại màn hình hoặc reconnect
```

Nếu FE append tất cả, user sẽ thấy:

- một câu user bị lặp hai lần;
- assistant trả lời bị lặp từ `lk.chat` và `lk.transcript`;
- reconnect xong history append lại các bubble đã có;
- permission prompt hoặc error bubble bị render nhiều lần.

Phase 10.6 giải quyết phần này.

---

## 2. Goal

Tạo một timeline contract ổn định:

```text
lk.transcript + REST history = nguồn chính thức
lk.chat = preview/transport nhanh, không phải source of truth
local optimistic = UI tạm, phải được replace/merge
```

Kết quả mong muốn:

- một DB `ChatMessage` chỉ tạo một bubble;
- assistant answer không bị duplicate khi cả `lk.chat` và `lk.transcript` cùng đến;
- reconnect không nhân đôi timeline;
- FE xử lý event đến sai thứ tự;
- BE cung cấp id ổn định đủ tốt để FE không phải đoán quá nhiều.

---

## 3. Non-Goals

Phase này không làm:

- không đổi nội dung câu trả lời của AI;
- không đổi retrieval/router/policy;
- không đổi topic name `lk.chat`, `lk.transcript`, `lk.control`;
- không bắt FE bỏ `lk.chat` ngay;
- không thêm WebSocket API mới;
- không xử lý push notification.

---

## 4. Current Contract

### 4.1 `lk.chat`

Topic:

```text
lk.chat
```

Payload:

```text
plain UTF-8 text
```

Direction:

```text
FE -> BE: user typed chat
BE -> FE: assistant text preview / fast display
```

Vấn đề:

- không có message id;
- không có role;
- không có timestamp chuẩn;
- không thể dedupe chắc chắn nếu dùng làm timeline chính.

Kết luận:

```text
lk.chat chỉ nên là preview hoặc transport input.
Không được là committed timeline source.
```

### 4.2 `lk.transcript`

Topic:

```text
lk.transcript
```

Payload hiện tại:

```json
{
  "v": 1,
  "type": "transcript",
  "role": "assistant",
  "text": "...",
  "id": "uuid",
  "ts": "2026-06-06T10:00:00.000000+00:00"
}
```

Direction:

```text
BE -> FE only
```

Vấn đề hiện tại:

- `id` đang là UUID mới mỗi lần publish transcript;
- không chắc trùng với `chat_messages.id` trong DB;
- khi FE load history, cùng một message có thể có id khác so với transcript realtime.

Kết luận:

```text
lk.transcript phải là committed timeline source.
Nhưng BE nên nâng cấp id để khớp DB message id.
```

---

## 5. Target Contract

### 5.1 Backward-compatible transcript payload

Không phá schema cũ. Giữ các field hiện tại và thêm optional fields.

```json
{
  "v": 1,
  "type": "transcript",
  "role": "assistant",
  "text": "...",
  "id": "chat_message_uuid_or_transient_uuid",
  "message_id": "chat_message_uuid_or_null",
  "thread_id": "thread_uuid_or_null",
  "source": "livekit",
  "status": "committed",
  "ts": "2026-06-06T10:00:00.000000+00:00"
}
```

Field meaning:

| Field | Required | Meaning |
| --- | --- | --- |
| `v` | yes | Schema version, giữ `1` |
| `type` | yes | Luôn là `transcript` |
| `role` | yes | `user` hoặc `assistant` |
| `text` | yes | Text đã normalize |
| `id` | yes | ID dùng để dedupe chính, ưu tiên DB message id |
| `message_id` | optional | DB `chat_messages.id` nếu có |
| `thread_id` | optional | Thread hiện tại nếu có |
| `source` | optional | `livekit`, sau này có thể `history` hoặc provider khác |
| `status` | optional | `committed` |
| `ts` | yes | Timestamp ISO |

Rule:

```text
Nếu message được lưu DB thành công:
  id = chat_messages.id
  message_id = chat_messages.id

Nếu không có thread_id hoặc không lưu DB được:
  id = transient uuid
  message_id = null
```

Lý do:

- FE cũ vẫn đọc `id`, `role`, `text`, `ts` như trước;
- FE mới có thể dedupe realtime transcript với REST history bằng cùng `message_id`.

---

## 6. Backend Implementation Plan

### Step 1 - Change saver return type

File:

```text
app/services/voice_agent/transcript_store.py
```

Hiện tại:

```python
MessageSaver = Callable[[str, bool], None]
```

Đề xuất:

```python
MessageSaver = Callable[[str, bool], uuid.UUID | None]
```

`_save_message_to_db(...)` trả về `new_msg.id` sau commit.

Pseudocode:

```python
def _save_message_to_db(self, text: str, is_user: bool) -> uuid.UUID | None:
    if not self._thread_id:
        return None
    with Session(self._get_engine()) as db:
        new_msg = ChatMessage(...)
        db.add(new_msg)
        db.commit()
        db.refresh(new_msg)
        return new_msg.id
```

Nếu lỗi:

```python
log info/warning without raw full text
return None
```

Rule bắt buộc:

```text
DB save failure must not block realtime transcript delivery.
```

Nếu DB pool bị bão hòa, Supabase chậm, hoặc commit timeout:

- `_save_message_to_db(...)` phải catch exception;
- log chỉ ghi `thread_id`, `role`, `text_len`, `error_type`;
- không log full/raw text;
- return `None`;
- `publish_transcript(...)` vẫn gửi event với transient UUID.

Điều này giúp user vẫn thấy câu hội thoại realtime dù persistence tạm thời lỗi. Sau đó history có thể thiếu message đó, nhưng app không bị treo ở thời điểm đang nói chuyện.

### Step 2 - Publish transcript with stable id

Đổi:

```python
async def publish_transcript(self, role, text):
```

thành:

```python
async def publish_transcript(
    self,
    role: TranscriptRole,
    text: str,
    *,
    message_id: uuid.UUID | None = None,
) -> None:
```

Payload:

```python
transcript_id = message_id or uuid.uuid4()
payload = {
    "v": 1,
    "type": "transcript",
    "role": role,
    "text": normalized,
    "id": str(transcript_id),
    "message_id": str(message_id) if message_id else None,
    "thread_id": str(self._thread_id) if self._thread_id else None,
    "source": "livekit",
    "status": "committed",
    "ts": datetime.now(timezone.utc).isoformat(),
}
```

### Step 3 - Save and publish order

Current flow:

```text
save DB
publish transcript with random id
```

Target:

```text
message_id = save DB
publish transcript with message_id
```

For user:

```python
message_id = await asyncio.to_thread(self._save_message_sync, normalized, True)
await self.publish_transcript("user", normalized, message_id=message_id)
```

For assistant:

```python
message_id = await asyncio.to_thread(self._save_message_sync, normalized, False)
await self.publish_transcript("assistant", normalized, message_id=message_id)
```

### Step 4 - Keep dedupe window for user voice

Không bỏ `_seen_user_texts`.

Lý do:

- LiveKit có thể emit final transcript và committed item gần nhau;
- Phase 10.4 đã giảm duplicate DB write, nhưng user dedupe vẫn là safety net.

### Step 5 - Do not change `lk.chat` yet

Không đổi `lk.chat` payload trong Phase 10.6.

Lý do:

- FE hiện publish text lên `lk.chat`;
- BE cũng dùng `lk.chat` làm fast assistant preview;
- đổi thành JSON sẽ breaking.

Nếu muốn nâng cấp sau này, làm Phase 10.6.1:

```text
lk.chat.v2 JSON preview event
```

Nhưng chưa cần.

---

## 7. Frontend Implementation Plan

### 7.1 Unified message model

FE nên gom mọi nguồn vào một model nội bộ:

```dart
enum TimelineMessageSource {
  history,
  transcript,
  chatPreview,
  localOptimistic,
}

enum TimelineMessageStatus {
  sending,
  preview,
  committed,
  failed,
}

class TimelineMessage {
  final String id;
  final String? messageId;
  final String role; // user | assistant
  final String text;
  final DateTime ts;
  final TimelineMessageSource source;
  final TimelineMessageStatus status;
  final String dedupeKey;
}
```

### 7.2 Source priority

Priority:

```text
history == transcript committed
> chatPreview
> localOptimistic
```

Meaning:

- `history` và `transcript` là committed;
- `chatPreview` có thể hiển thị nhanh nhưng phải bị replace;
- `localOptimistic` là message user vừa gõ, phải merge với transcript user.

### 7.3 Dedupe keys

Primary dedupe:

```text
message_id if present
else transcript id
```

Fallback fuzzy dedupe:

```text
role + normalized text + short time window
```

Time window recommendation:

```text
user optimistic merge: 10 seconds
assistant chatPreview merge: 20 seconds
history reconnect merge: 60 seconds
```

Normalize text:

```dart
String normalizeText(String value) {
  return value
      .trim()
      .replaceAll(RegExp(r'\s+'), ' ')
      .toLowerCase();
}
```

Rule:

```text
Tất cả fuzzy matching phải dùng cùng một hàm normalizeText.
```

Áp dụng cho:

- local optimistic message;
- `lk.chat` preview;
- `lk.transcript`;
- REST history.

Về tiếng Việt có dấu:

```text
Không bắt buộc accent-fold ở Phase 10.6.
```

Lý do:

- primary dedupe đã dựa vào `message_id`;
- fuzzy chỉ là fallback;
- accent-fold nếu làm không đồng nhất giữa iOS/Android/Web có thể gây false-positive.

Nếu FE muốn accent-fold, phải bọc trong một helper dùng chung cho mọi nguồn:

```dart
String normalizeForFuzzyMatch(String value) {
  return removeVietnameseDiacritics(
    value.trim().replaceAll(RegExp(r'\s+'), ' ').toLowerCase(),
  );
}
```

Không được dùng normalize khác nhau cho history và LiveKit event.

### 7.4 Transcript handler

Pseudo:

```dart
void onTranscript(TranscriptPayload payload) {
  if (payload.type != 'transcript') return;
  if (payload.text.trim().isEmpty) return;

  final stableId = payload.messageId ?? payload.id;
  if (stableId == null || stableId.isEmpty) return;

  final committed = TimelineMessage.fromTranscript(payload);

  timeline.upsertCommitted(
    committed,
    replaceSources: {
      TimelineMessageSource.chatPreview,
      TimelineMessageSource.localOptimistic,
    },
  );
}
```

Rules:

- Nếu có message cùng `message_id` hoặc `id`, replace.
- Nếu không có id match, tìm preview/optimistic cùng role + normalized text trong window.
- Nếu match fuzzy, replace preview bằng committed.
- Nếu không match, append.

### 7.5 `lk.chat` handler

FE nhận `lk.chat` từ BE là plain text assistant preview.

Rule:

```text
Only create assistant preview if no recent assistant preview with same normalized text.
Mark source=chatPreview, status=preview.
Never mark lk.chat message as committed.
```

Pseudo:

```dart
void onChatPreview(String text) {
  final normalized = normalizeText(text);
  if (normalized.isEmpty) return;

  if (timeline.hasRecentPreview(role: 'assistant', text: normalized)) {
    return;
  }

  timeline.addPreview(
    role: 'assistant',
    text: normalized,
    expiresAfter: Duration(seconds: 30),
  );
}
```

When transcript arrives:

```text
assistant transcript committed
-> replace matching chatPreview
```

If transcript never arrives:

```text
preview can remain visible but with status preview
or be converted to committed only after timeout if product accepts risk
```

Recommendation:

```text
Do not convert preview to committed automatically.
Keep it as preview until history/transcript confirms.
```

### 7.6 User typed optimistic message

When user sends text:

```text
FE publish plain text to lk.chat
FE may show local optimistic user bubble immediately
```

When transcript user arrives:

```text
replace local optimistic bubble
```

If no transcript after timeout:

```text
keep optimistic as sending/failed depending connection state
```

### 7.7 Voice user transcript

Voice user message should only appear when backend publishes `lk.transcript` role `user`.

FE should not create user bubble from client-side STT unless product explicitly adds client STT.

Rule:

```text
No client-side STT bubble in Phase 10.6.
Backend transcript wins.
```

---

## 8. Ordering Rules

Sort timeline by:

```text
ts ascending
tie-breaker arrival sequence
```

But do not reorder currently speaking assistant preview too aggressively if it causes visual jump.

Recommendation:

```text
Maintain append order while streaming/preview.
On committed transcript/history sync, sort stable committed messages by ts.
```

---

## 9. Reconnect And History Merge

On opening screen:

```text
1. Load REST history first if available.
2. Connect LiveKit.
3. Subscribe lk.transcript.
4. Subscribe lk.chat.
```

On reconnect:

```text
1. Do not clear timeline immediately.
2. Reconnect LiveKit.
3. Reload recent history after reconnect succeeds.
4. Merge history into current timeline by message_id/id/fuzzy key.
```

Rules:

- Do not append full history blindly.
- Do not create error bubble for every reconnect attempt.
- Use one connection state widget/banner.

### 9.1 Idempotent event queue

Trong lúc reconnect, FE có thể nhận cùng lúc:

```text
REST history reload
buffered lk.transcript events
late lk.chat preview
```

Vì vậy timeline repository nên xử lý event qua một hàng đợi tuần tự, thay vì nhiều listener cùng mutate list message trực tiếp.

Pseudocode:

```dart
final _timelineEventController = StreamController<TimelineEvent>();

void enqueueTimelineEvent(TimelineEvent event) {
  _timelineEventController.add(event);
}

Future<void> processTimelineEvents() async {
  await for (final event in _timelineEventController.stream) {
    timelineState = timelineReducer.apply(timelineState, event);
  }
}
```

Reducer phải idempotent:

```text
Nếu committed message với message_id/id đã tồn tại:
  update/replace existing item
  không append

Nếu preview đến sau committed message cùng text/role/window:
  ignore preview

Nếu history đến sau transcript cùng message_id:
  merge metadata nếu cần
  không append
```

Rule:

```text
Không mutate timeline trực tiếp từ nhiều LiveKit/REST callbacks.
Tất cả đi qua reducer/upsert chung.
```

---

## 10. Permission Prompt Reconciliation

Phase 7.1 added web permission UI.

Permission prompt can arrive as assistant message from:

```text
lk.chat preview
lk.transcript committed
history after reconnect
```

FE should attach quick action chips to the committed assistant bubble when possible.

Detection in Phase 10.6:

```text
If assistant text matches permission prompt pattern
-> show chips "Cho phép tìm web" / "Không cần"
```

When transcript replaces preview:

```text
Move chips from preview bubble to committed bubble.
```

Do not render two sets of chips.

---

## 11. Backend Tests

### 11.1 Transcript store unit tests

File:

```text
tests/services/voice_agent/test_transcript_store.py
```

Add cases:

1. `save_and_publish_user` publishes transcript `id == message_id` when saver returns id.
2. `save_and_publish_assistant` publishes transcript `id == message_id` when saver returns id.
3. If saver returns `None`, transcript still publishes with transient UUID and `message_id=null`.
4. Payload contains optional fields:

```text
message_id
thread_id
source=livekit
status=committed
```

5. User duplicate text within dedupe window does not publish twice.
6. If saver raises exception, transcript still publishes with transient `id` and `message_id=null`.
7. Saver exception log must not include full message text.

### 11.2 Compatibility tests

Ensure old required fields still exist:

```text
v
type
role
text
id
ts
```

---

## 12. FE Tests

FE should add reducer/state tests:

### Test 1 - Transcript id dedupe

```text
Given transcript A id=1
When transcript A arrives twice
Then timeline has one bubble
```

### Test 2 - Chat preview replaced by transcript

```text
Given lk.chat assistant preview "Hello"
When lk.transcript assistant text "Hello" arrives
Then timeline has one committed assistant bubble
```

### Test 3 - User optimistic replaced by transcript

```text
Given local optimistic user text "Tác giả là ai?"
When lk.transcript user text "Tác giả là ai?" arrives
Then timeline has one committed user bubble
```

### Test 4 - History merge after reconnect

```text
Given timeline has transcript message id=1
When REST history returns message id=1
Then timeline still has one bubble
```

### Test 5 - Out of order events

```text
Given transcript arrives before lk.chat preview
When lk.chat preview with same text arrives later
Then FE ignores preview
```

### Test 6 - Permission chips move

```text
Given permission prompt preview has chips
When committed transcript replaces preview
Then chips appear once on committed bubble
```

### Test 7 - Reconnect burst is idempotent

```text
Given REST history message id=1 and buffered lk.transcript message_id=1 arrive close together
When reducer processes both events in any order
Then timeline has one committed bubble
```

### Test 8 - Preview after committed is ignored

```text
Given committed assistant message text "Hello" exists
When late lk.chat preview "Hello" arrives
Then timeline still has one committed bubble and no preview duplicate
```

---

## 13. Backend Implementation Order

1. Update `MessageSaver` return type.
2. Return DB message id from `_save_message_to_db`.
3. Add optional payload fields in `publish_transcript`.
4. Pass `message_id` from save to publish.
5. Ensure DB save exceptions return `None` and do not block publish.
6. Update existing transcript store tests.
7. Run focused tests.
8. Update Flutter contract doc if payload changed.

Commands:

```powershell
uv run pytest tests/services/voice_agent/test_transcript_store.py -q
uv run pytest tests/services/voice_agent tests/services/agent_policy -q
uv run ruff check app/services/voice_agent tests/services/voice_agent
uv run python -m py_compile app/services/voice_agent/transcript_store.py
```

---

## 14. FE Implementation Order

1. Create `TimelineMessage` model and reducer/upsert logic.
2. Create an idempotent event queue so all LiveKit/history events go through one reducer.
3. Make `lk.transcript` handler authoritative.
4. Downgrade `lk.chat` assistant response to preview only.
5. Merge local optimistic user messages with transcript.
6. Merge REST history with current timeline on open/reconnect.
7. Move permission chips when preview is replaced by committed transcript.
8. Add reducer tests with mocked events before wiring LiveKit streams.
9. Manual test with real LiveKit.

---

## 15. Manual Test Checklist

### 15.1 Text chat

1. Open thread.
2. Send typed text.
3. FE shows at most one user bubble.
4. Assistant answer may preview quickly.
5. When transcript arrives, assistant bubble remains one item.
6. Reload screen.
7. History does not duplicate messages.

### 15.2 Voice

1. Ask by voice.
2. User voice transcript appears once.
3. Assistant answer appears once.
4. Interrupt/reask.
5. No duplicated assistant partial/final bubbles.

### 15.3 Reconnect

1. Start voice room.
2. Ask one question.
3. Toggle network off/on.
4. Reconnect.
5. Load history.
6. Timeline does not duplicate previous messages.

### 15.4 Web permission

1. Ask a question needing web.
2. Permission prompt appears once.
3. Chips appear once.
4. Tap allow.
5. Final web answer appears once.

---

## 16. Rollback Plan

Backend payload additions are backward-compatible.

If FE has issue:

```text
FE can continue using old id/text/role fields.
```

If BE transcript id causes issue:

```text
Rollback transcript_store.py to random transcript id.
```

No DB migration needed.

---

## 17. Trade-offs

### 17.1 Backend id stability requires save-before-publish

To publish DB id, BE must save first.

Trade-off:

- transcript publish waits for DB commit;
- but current flow already saves before publishing, so latency impact should be small.

### 17.2 `lk.chat` remains fuzzy

Because `lk.chat` is plain text, preview replacement still needs fuzzy match.

Trade-off:

- no breaking change;
- FE reducer is a bit more careful.

Future option:

```text
lk.chat.v2 JSON preview with preview_id
```

### 17.3 Console mode may not have DB message id

If `thread_id` is missing, backend cannot save DB message.

Rule:

```text
Use transient transcript id.
FE still dedupes within realtime session by id.
```

---

## 18. Acceptance Criteria

Phase 10.6 complete when:

1. `lk.transcript` committed payload includes stable `message_id` when DB save succeeds.
2. Required old fields remain unchanged.
3. DB save failure returns `None`, does not block transcript publish, and does not log raw full text.
4. FE treats `lk.transcript` and REST history as source of truth.
5. FE treats `lk.chat` assistant text as preview only.
6. FE uses one shared normalization function for fuzzy fallback matching.
7. FE processes LiveKit/history events through an idempotent reducer/queue.
8. Local optimistic user bubble is replaced by transcript user bubble.
9. Reconnect/history merge does not duplicate timeline.
10. Permission prompt chips are not duplicated.
11. Backend transcript store tests pass.
12. FE reducer tests pass.
13. Manual LiveKit test confirms no duplicate bubbles across text, voice, reconnect and web permission.

---

## 19. Senior Note Cho Em

Phase này nhìn giống UI detail, nhưng thật ra là reliability của realtime app.

Một realtime app tốt không chỉ cần AI trả lời đúng. Nó còn phải đảm bảo:

```text
Một sự kiện thật trong hệ thống chỉ biến thành một trạng thái UI.
```

Nếu cùng một assistant answer đi qua `lk.chat`, `lk.transcript`, rồi REST history, FE phải hiểu đó là một message, không phải ba message.

Nguyên tắc em nên nhớ:

```text
Preview is not truth.
Transcript/history is truth.
Stable id beats fuzzy text matching.
Fuzzy matching chỉ là fallback để tương thích với contract cũ.
```

Khi Phase 10.6 xong, trải nghiệm chat/voice sẽ nhìn “sạch” hơn rất nhiều: ít lặp, ít nhảy, ít bubble ma sau reconnect. Đây là phần rất đáng khoe khi báo cáo vì nó cho thấy em hiểu realtime system chứ không chỉ gọi được AI API.

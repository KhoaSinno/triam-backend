# Báo cáo: Realtime GPT (LiveKit Agents) — Model, Tool Routing, Audio Toggle, và UI Transcript

Ngày: 2026-05-11

Mục tiêu:

1. Chọn realtime model “p/p” tốt hơn và tránh model preview/legacy.
2. Giảm lỗi LLM chọn nhầm tool (RAG vs Web).
3. Cho phép chat text→text tùy chọn có/không phát audio.
4. Với voice→voice: UI Flutter phải hiển thị được câu hỏi của user (transcript) ổn định.

Phạm vi file backend đang xét:

- app/services/agent_voice_gpt_realtime.py

---

## 1) `gpt-4o-mini-realtime-preview` có “legacy” không?

Trong code hiện tại, backend dùng:

- RealtimeModel(model="gpt-4o-mini-realtime-preview", modalities=["audio","text"])

Nhận định kỹ thuật:

- Tên model có hậu tố `-preview` thường ám chỉ bản preview/không ổn định lâu dài (dễ đổi schema/behavior, bị thay thế, hoặc bị hạn chế region/quota).
- Bạn đã thấy SDK gợi ý danh sách model hợp lệ:

RealtimeModels = Literal[
"gpt-realtime",
"gpt-realtime-1.5",
"gpt-realtime-2025-08-28",
"gpt-4o-realtime-preview",
]

Kết luận thực dụng:

- Nếu SDK/typing đã liệt kê các model `gpt-realtime-*` thì nên migrate sang chúng để giảm rủi ro “preview bị thay thế”.
- Không thể khẳng định trạng thái “deprecated” của `gpt-4o-mini-realtime-preview` chỉ dựa trên repo này, nhưng về best-practice nên coi nó là lựa chọn rủi ro.

### Khuyến nghị model theo “p/p” (không chốt giá tuyệt đối)

Vì giá/latency có thể thay đổi theo thời điểm và theo tài khoản/quota, cách làm best-practice là:

- Mặc định dùng model date-stamped (ổn định hơn): `gpt-realtime-2025-08-28`
- Nếu cần rẻ hơn: thử `gpt-realtime-1.5` (thường là biến thể nhẹ hơn)
- Nếu muốn “đơn giản”: `gpt-realtime` (rolling)

Cách triển khai đề xuất:

- Đọc model từ env/setting `OPENAI_STREAM_MODEL_NAME` (trong codebase Triam đang dùng `settings.OPENAI_STREAM_MODEL_NAME`).
- Cho phép fallback nếu model không được cấp quyền (tối thiểu fallback sang `gpt-realtime-1.5`).

Pseudo:

- candidates = [OPENAI_STREAM_MODEL_NAME, "gpt-realtime-2025-08-28", "gpt-realtime-1.5", "gpt-realtime"]
- thử lần lượt, nếu lỗi NOT_FOUND/permission thì fallback.

---

## 2) Vì sao GPT “nhạy” nhưng chọn tool chưa tốt? Cách fix dứt điểm

Hiện tại Agent expose 2 tool độc lập:

- search_book_knowledge(query)
- search_web(query)

Dù bạn đã ghi instruction rất rõ, LLM đôi khi vẫn:

- gọi `search_web` quá sớm
- hoặc trả lời từ “nhớ” mà không gọi tool

### Best-practice (scale): Tách “policy layer” khỏi số lượng tool

Nhận xét của bạn đúng: về sau sẽ có nhiều tool, nên hướng “gộp thành 1 tool lookup()” là giải pháp nhanh nhưng dễ thành hard-code và kém scale.

Giải pháp bền vững hơn là thiết kế 2 lớp:

1. Tool execution layer (các tool thật)

- Mỗi tool chỉ làm đúng 1 việc (RAG, web, summarize, planner, calc, v.v.).

2. Tool policy & routing layer (deterministic, config-driven)

- Định nghĩa quy tắc gọi tool bằng dữ liệu (config), không nhét rải rác trong prompt.
- Khi LLM gọi tool, hệ thống kiểm tra policy:
  - Nếu vi phạm (ví dụ: gọi web trước khi thử RAG cho câu hỏi “trong sách”) => hệ thống tự động chặn/reroute/insert bước bắt buộc.

Vì sao cần policy layer (lý do mang tính “chứng minh” hệ thống):

- Function-calling là hành vi suy luận, không có guarantee 100% tuân thủ instruction.
- Khi tool tăng, prompt không thể bao phủ hết rule + edge case và càng khó maintain.
- Nếu muốn correctness ở mức hệ thống, enforcement phải nằm ở code.

Pattern scale tốt (không hard-code theo từng tool): Tool Registry + Policy Rules

- Mỗi tool có metadata (tags/capabilities): ví dụ {domain: book}, {domain: web}, {freshness: current}, {cost: low}.
- Policy rules dựa trên metadata:
  - Nếu query liên quan sách + có document_ids => bắt buộc chạy tool tag=book trước.
  - Chỉ cho phép web nếu (rag_empty == true) hoặc (intent == current-events).

Hệ quả tích cực:

- Thêm tool mới = thêm metadata + rule (dễ test, dễ log, dễ quan sát).
- Không phụ thuộc vào “LLM nhớ rule” nữa; LLM chỉ là planner/assistant, còn hệ thống enforce.

Gợi ý MVP để chuyển dần (không làm quá phức tạp ngay):

- Giữ 2 tool như hiện tại.
- Implement 1 router/policy tối thiểu trong code để luôn thử RAG trước, chỉ fallback web khi đủ điều kiện.
- Khi tool tăng, mở rộng registry/rules thay vì viết if-else rải rác.

---

## 3) Text→Text hiện đang phát cả audio: xử lý ở FE hay BE?

Thực tế hiện tại:

- Khi Flutter gửi text vào `lk.chat`, BE gọi `session.generate_reply(user_input=text)`.
- RealtimeModel được khởi tạo với `modalities=["audio","text"]` nên response thường gồm cả audio track.
- Flutter subscribe audio track => tự động phát.

Kết luận trách nhiệm:

- Nút bật/tắt audio là UX/UI => thuộc Flutter.
- Nhưng việc có phát audio hay không là hành vi hệ thống => cần BE hỗ trợ (không thể chỉ FE làm nếu audio vẫn được publish).

### Thiết kế khuyến nghị: Toggle audio cho “text chat” theo participant preference

1. Flutter có toggle “Phát audio khi gửi text chat” (ON/OFF).
2. Khi user đổi toggle, Flutter publish 1 gói preference lên DataChannel topic mới (ví dụ `lk.pref`).
3. Backend lưu preference theo participant identity.
4. Khi nhận text chat ở `lk.chat`:
   - Nếu audio ON: dùng realtime `session.generate_reply()` như hiện tại.
   - Nếu audio OFF: dùng đường text-only rẻ hơn (không realtime), rồi publish text về `lk.chat`.

Vì sao nên “text-only path” thay vì cố ép realtime chỉ trả text?

- Một số realtime stack khó “turn off speaking” theo từng turn nếu session đã bật audio.
- Tách đường text-only giúp:
  - rẻ hơn
  - deterministic
  - không tạo audio track nên Flutter không tự phát

### Payload đề xuất cho `lk.pref` (JSON)

{
"v": 1,
"type": "pref",
"audio_for_text_chat": false
}

#### `lk.pref` có làm chậm hệ thống không?

Gần như không đáng kể:

- Message nhỏ (vài chục đến vài trăm bytes JSON).
- Không gửi liên tục, chỉ gửi khi user đổi toggle hoặc ngay sau khi join room.
- So với audio streaming và LLM tokens thì overhead này là không đáng kể.

#### Đồng bộ UI và backend lâu dài (thoát app, mở lại)

Realtime session không tự “nhớ” preference cho lần join mới. Có 2 hướng best-practice:

Option A (đơn giản, thường đủ dùng): FE source-of-truth

- Flutter lưu toggle vào local storage (SharedPreferences).
- Mỗi lần join room, Flutter gửi lại preference qua `lk.pref`.
- Backend giữ preference trong RAM theo participant cho phiên đó.

Option B (đa thiết bị/bền hơn): BE persistence

- Backend lưu preference theo user_id/participant identity vào DB/Redis.
- Khi user join, backend có thể push lại pref (broadcast kèm participant identity) hoặc FE call API lấy state rồi publish vào room.

#### So với call API: DataChannel preference có ổn hơn không?

DataChannel phù hợp cho “room-scoped controls” vì:

- Latency thấp, không cần thêm endpoint, gắn đúng vào room/session.
- Ít plumbing hơn REST (auth/route/DTO riêng) cho những knob nhỏ.

Nhưng nếu mục tiêu là persistence đa session/đa thiết bị, bạn vẫn cần DB/Redis hoặc local storage.

Tối ưu hơn nữa (ít topic hơn): dùng participant metadata/attributes

- Flutter set attribute `audio_for_text_chat=false` lúc join.
- Backend đọc attribute để quyết định.
- Vẫn phải set lại mỗi lần join, nhưng không cần custom `lk.pref`.

---

## 4) Voice→Voice: Flutter chưa hiển thị câu hỏi user (transcript) — xử lý sao?

Thực tế code hiện tại:

- Voice input được xử lý trong session audio pipeline.
- Callback `@session.on("user_speech_committed")` chỉ lưu DB.
- BE không publish transcript của user lên DataChannel.

Vì vậy:

- Flutter chỉ thấy audio track (và có thể thấy text của assistant nếu BE publish).
- Flutter không có “string” đại diện cho câu hỏi user để render bubble.

### Giải pháp A (khuyến nghị): BE publish transcript user lên DataChannel

- Trên `user_speech_committed`, BE publish transcript lên topic riêng (ví dụ `lk.transcript`).
- Payload nên có role để FE render đúng bên trái/phải.

Payload JSON đề xuất:
{
"v": 1,
"type": "transcript",
"role": "user",
"text": "...",
"id": "<uuid>",
"ts": "2026-05-11T...Z"
}

Tương tự, trên `agent_speech_committed` publish:

- role = "assistant"

Flutter:

- Subscribe topic `lk.transcript`.
- Add message vào UI chat transcript.

Ưu điểm:

- UI luôn có câu hỏi user (theo transcript cuối cùng).
- Không cần Flutter tự STT.

### Giải pháp B: FE tự hiển thị “optimistic bubble”

- Khi user đang nói, FE hiển thị bubble “Đang nói…” hoặc buffer local.
- Nếu FE có STT on-device thì hiển thị transcript local.
- Khi BE gửi transcript committed thì replace/confirm.

Phù hợp nếu:

- bạn cần hiển thị realtime từng chữ khi user nói.

### Về việc “log thấy rewrite câu hỏi”

Khả năng thường gặp:

- Transcript committed có thể được chuẩn hoá dấu câu, bỏ filler words, hoặc sửa lỗi nhận dạng giọng.
- Đây không hẳn là “LLM rewrite”, mà là output STT/normalization.

Nếu bạn cần “raw transcript” tuyệt đối:

- Thường phải làm STT client-side hoặc lưu audio rồi transcribe offline.
- Còn với realtime, chấp nhận committed transcript là “đại diện tốt nhất” cho UI.

---

## 5) Contract topics: tránh lẫn chat và transcript

Hiện docs cũ đang mô tả:

- `lk.chat` vừa là chat message, vừa là transcript.

Về lâu dài nên tách:

- `lk.chat`: message “chat” (text-only, rẻ, UI bubble)
- `lk.transcript`: transcript đi kèm voice (voice UI)
- `lk.pref`: preference control từ FE

Nếu cần backward compatible:

- Giai đoạn 1: vẫn gửi text assistant lên `lk.chat` như cũ, thêm `lk.transcript` cho voice.
- Giai đoạn 2: nâng Flutter decode JSON payload và render theo `type`.

---

## 6) Checklist implement (Backend/Flutter)

Backend (Python):

1. Thêm listener topic `lk.pref` để cập nhật preference theo participant.
2. Với text input (`lk.chat`): nếu audio_for_text_chat=false => generate text-only và publish text về `lk.chat`.
3. Với voice events: publish transcript lên `lk.transcript` cho cả user và assistant.
4. Đổi model realtime sang setting/env + fallback `gpt-realtime-1.5`.

Gợi ý khớp với codebase hiện tại:

- Import settings và dùng `settings.OPENAI_STREAM_MODEL_NAME`.
- Nếu model đó lỗi NOT_FOUND/permission => fallback sang `gpt-realtime-1.5`.

Flutter:

1. UI toggle “Audio khi chat text”.
2. Publish preference lên `lk.pref` khi toggle đổi.
3. Subscribe và render:
   - `lk.chat`: chat bubble
   - `lk.transcript`: transcript bubble (role user/assistant)

---

## 7) Ghi chú quan trọng về DB history

Trong một số file backend hiện có pattern query sai kiểu:

- so sánh `ChatMessage.thread_id` (UUID) với `thread_id` (string)

Best-practice:

- parse `thread_uuid = uuid.UUID(thread_id)` một lần
- dùng `thread_uuid` cho save/load

Việc này giúp history load đúng, nhất quán giữa voice/chat.

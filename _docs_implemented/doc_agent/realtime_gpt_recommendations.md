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

- Đọc model từ env `OPENAI_REALTIME_MODEL`.
- Cho phép fallback list nếu model không được cấp quyền.

Pseudo:

- candidates = [env, "gpt-realtime-2025-08-28", "gpt-realtime-1.5", "gpt-realtime"]
- thử lần lượt, nếu lỗi NOT_FOUND/permission thì fallback.

---

## 2) Vì sao GPT “nhạy” nhưng chọn tool chưa tốt? Cách fix dứt điểm

Hiện tại Agent expose 2 tool độc lập:

- search_book_knowledge(query)
- search_web(query)

Dù bạn đã ghi instruction rất rõ, LLM đôi khi vẫn:

- gọi `search_web` quá sớm
- hoặc trả lời từ “nhớ” mà không gọi tool

### Best-practice: Giảm degrees-of-freedom của model

Cách chắc nhất để model không “chọn nhầm” là:

1. Chỉ expose 1 tool duy nhất (ví dụ: `lookup(query)`)
2. Tool `lookup()` tự enforce policy:
   - luôn gọi RAG trước
   - nếu RAG rỗng thì mới gọi Web

Ưu điểm:

- Model không còn cơ hội chọn nhầm tool.
- Logic routing nằm ở code, deterministic, testable.

Cách implement:

- Gộp 2 tool thành 1 tool (hoặc giữ hàm nội bộ nhưng chỉ decorate 1 tool).

Pseudo:

async def lookup(query: str) -> str:
rag = await search_book_knowledge(query, document_ids)
if rag has data:
return rag
return await search_web(query)

Lưu ý:

- Trong instruction vẫn giữ quy tắc để model hiểu mong muốn, nhưng enforcement chính nằm ở code.

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
4. Đổi model realtime sang env + fallback theo danh sách `RealtimeModels`.

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

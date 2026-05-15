# OpenAI Realtime pricing/billing (official docs) — report

Mục tiêu: trả lời câu hỏi **bật `text+audio` trong Realtime thì có bị tính “cả audio” cho các turn text không**, và cách cấu hình để **text-only thật sự** nhằm tối ưu chi phí.

> Nguồn chính thức (OpenAI Developers):
>
> - Managing costs (Realtime): https://developers.openai.com/api/docs/guides/realtime-costs
> - Pricing: https://developers.openai.com/api/docs/pricing
> - Realtime conversations (output_modalities, response.create): https://developers.openai.com/api/docs/guides/realtime-conversations

---

## 1) Realtime API tính tiền theo cái gì?

Theo **Managing costs**:

- **Chi phí Realtime (voice-agent session) phát sinh khi một `Response` được tạo** (tạo thủ công bằng `response.create` hoặc tự động nếu bật VAD). Không có chi phí riêng cho “kết nối/bandwidth”.
- Mỗi `Response` được tính theo **số token input và output**, và token được chia theo modality:
  - `text_tokens`
  - `audio_tokens`
  - `image_tokens`
  - cộng thêm `cached_tokens` (nếu prompt caching hit)
- **Toàn bộ Conversation** (instructions + các items trước đó + user turn hiện tại) là input cho mỗi `Response`, nên các turn về sau thường tốn hơn nếu không truncation / delete.

Ví dụ “usage” đọc được trong event `response.done`:

```json
{
  "type": "response.done",
  "response": {
    "usage": {
      "input_token_details": {
        "text_tokens": 119,
        "audio_tokens": 13,
        "cached_tokens": 64
      },
      "output_token_details": {
        "text_tokens": 30,
        "audio_tokens": 91
      }
    }
  }
}
```

### Quy đổi audio tokens theo thời lượng

Theo **Managing costs**:

- **Audio tokens trong user messages**: ~**1 token / 100ms** audio.
- **Audio tokens trong assistant messages**: ~**1 token / 50ms** audio.

Hệ quả: nếu assistant “nói” (audio output) thì **audio output tokens tăng rất nhanh**.

---

## 2) Nếu session bật cả audio + text, có bị tính cả hai không?

### Về mặt “hành vi output”

Theo **Realtime conversations**:

- Nếu **cả audio và text đang enabled** cho session, thì khi bạn tạo response, **model sẽ trả về cả audio và text**.
- Nếu muốn **text-only**, bạn có thể yêu cầu rõ ở `response.create`:

```json
{
  "type": "response.create",
  "response": {
    "output_modalities": ["text"]
  }
}
```

Hoặc set ở mức session bằng `session.update` (ví dụ “lock output to audio”, và ghi chú có thể set `['text']` để text without audio).

### Về mặt “billing”

Kết hợp với **Managing costs**:

- Chi phí được tính theo **token thực sự dùng ở output** trong `response.done`.
- Nếu bạn để session/response **xuất cả audio + text**, thì `output_token_details` sẽ có cả `text_tokens` và `audio_tokens` → **bị tính cả 2 loại output**.
- Nếu bạn ép **text-only** (`output_modalities: ['text']`), về nguyên tắc **audio output tokens sẽ về 0** → **không bị tính audio output** cho turn đó.

Nói cách khác:

- **Bật capability audio** không tự động “đốt tiền audio” nếu turn đó **không tạo audio output**.
- Thứ làm bạn tốn tiền audio là:
  1. bạn **gửi audio input** (audio_tokens input), và/hoặc
  2. bạn **để model phát audio output** (audio_tokens output).

---

## 3) Input transcription là một dòng bill riêng

Theo **Managing costs**:

- Ngoài per-Response token cost, Realtime còn **bill input transcriptions nếu enabled**.
- Transcription dùng model khác (ví dụ whisper / gpt-4o-transcribe) nên **billed theo rate card khác**.
- Usage transcription đọc từ event `conversation.item.input_audio_transcription.completed`.

Hệ quả: Nếu bạn chỉ cần “text chat” thì:

- Tránh gửi audio vào session.
- Tránh bật transcription nếu không cần.

---

## 4) Bảng giá (Realtime) — trích từ trang Pricing

Theo **Pricing → Realtime and audio generation models** (giá / 1M tokens, trừ khi ghi chú khác):

- `gpt-realtime-2`
  - **Audio**: $32.00 (input) / $0.40 (cached input) / $64.00 (output)
  - **Text**: $4.00 (input) / $0.40 (cached input) / $24.00 (output)
  - **Image**: $5.00 (input) / $0.50 (cached input)
- `gpt-realtime-1.5`
  - **Audio**: $32.00 / $0.40 / $64.00
  - **Text**: $4.00 / $0.40 / $16.00
  - **Image**: $5.00 / $0.50
- `gpt-realtime-mini`
  - **Audio**: $10.00 / $0.30 / $20.00
  - **Text**: $0.60 / $0.06 / $2.40
  - **Image**: $0.80 / $0.08

(Chi tiết đầy đủ và các model khác: https://developers.openai.com/api/docs/pricing)

---

## 5) Khuyến nghị cấu hình để tối ưu chi phí (áp dụng cho Triam / LiveKit worker)

### A. Tách “voice mode” và “text mode” bằng `output_modalities`

- **Voice mode**: output_modalities = `["audio", "text"]` (hoặc chỉ audio nếu UI không cần text).
- **Text mode**: luôn tạo response với `output_modalities = ["text"]`.

Điểm mấu chốt: **đừng để model phát audio khi user đang chat text**.

### B. Quan sát bill bằng `response.done.usage`

- Log lại `response.done.response.usage` để thấy chính xác:
  - input text/audio tokens
  - output text/audio tokens
  - cached tokens
- Nếu thấy `output_token_details.audio_tokens` > 0 trong “text mode” → nghĩa là bạn vẫn đang vô tình tạo audio output.

### C. Giữ history “static” để tận dụng caching

Theo **Managing costs**:

- Prompt caching được áp dụng tự động (best-effort).
- Thay đổi instructions/tools giữa session sẽ “bust cache”.

### D. Giới hạn context bằng truncation/token window

Theo **Managing costs**:

- Dùng truncation (`token_limits.post_instructions`, `retention_ratio`) để chặn cost phình theo thời gian.

---

## 6) Trả lời ngắn gọn câu hỏi “text request có bị tính audio không?”

- **Có** nếu bạn để Realtime response **xuất audio** (session đang bật audio+text và bạn không override) → `output_audio` sinh ra → bị tính **audio output tokens**.
- **Không** (ở phần audio output) nếu bạn tạo response **text-only** bằng `output_modalities: ['text']` → output audio tokens về 0.
- Dù text-only, bạn vẫn có thể bị tính các dòng khác nếu:
  - bạn gửi audio input, hoặc
  - bạn bật input transcription.

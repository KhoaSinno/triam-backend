# Guide Implement: `lk.pref` + Toggle “Audio khi chat text” (SharedPreferences-first)

## Update quyết định (khuyến nghị hiện tại)

Nếu bạn đã chốt “chat chỉ text (text ↔ text) và bỏ toggle audio”, thì **KHÔNG cần implement `lk.pref`**.

Lý do chính: trong LiveKit OpenAI Realtime wrapper hiện tại, đường gọi `generate_reply()` **không có tham số public để ép `output_modalities=["text"]` theo từng turn**, nên “toggle per-message” sẽ phải dùng hack/private API và rất khó bền vững.

Khuyến nghị ổn định cho MVP:

- Text chat: luôn text-only (không dùng Realtime TTS) → tối ưu cost + lịch sử ổn định.
- Voice mode (nếu cần): tách riêng (worker/room riêng) để không ảnh hưởng chat.

Phần còn lại của tài liệu này giữ lại như một phương án tham khảo nếu sau này bạn muốn thử toggle, nhưng **không còn là hướng khuyến nghị**.

---

Mục tiêu ban đầu: cho Flutter có toggle **ON/OFF audio khi user gửi text**, với cách làm **ít rườm rà nhất**.

- FE (Flutter) là source-of-truth: lưu bằng `SharedPreferences`.
- Mỗi lần join room, FE gửi lại preference qua DataChannel topic `lk.pref`.
- BE giữ preference **trong RAM cho phiên room đó**, theo participant identity.

Tài liệu này chỉ dựa vào file backend hiện tại:

- `app/services/agent_voice_gpt_realtime.py`

---

## 1) Kết luận nhanh: SharedPreferences local “đúng” và ít rườm rà nhất không?

**Đúng.** Với hiện trạng BE đang tạo LiveKit identity random ở token, nếu bạn cố persist ở BE theo participant identity thì **mất state khi reconnect**.

Với SharedPreferences:

- Thoát app → mở lại: **không mất** (state nằm ở máy)
- Chuyển sách / chuyển study context / chuyển thread: **không mất** nếu FE luôn gửi lại sau khi connect
- Multi-device: **không đồng bộ** (đây là trade-off)

---

## 2) Hiện tại BE đã implement `lk.pref` chưa?

Trong `agent_voice_gpt_realtime.py` hiện chỉ:

- lắng nghe `lk.chat`
- publish `lk.chat` + `lk.transcript`
- chưa có handler nào cho topic `lk.pref`
- chưa có routing “text-only path” khi pref OFF

=> **Chưa implement.**

---

## 3) Contract mới cần thêm (DataChannel)

### 3.1 Topic `lk.pref`

- FE → BE
- Payload: JSON UTF-8

Schema đề xuất (tối giản):

```json
{
  "v": 1,
  "type": "pref",
  "audio_for_text_chat": false
}
```

**Giải thích:**

- `audio_for_text_chat=true`: chat text dùng realtime (có audio track như hiện tại)
- `audio_for_text_chat=false`: chat text dùng đường text-only (KHÔNG publish audio)

---

## 4) Backend: hướng dẫn implement trong `agent_voice_gpt_realtime.py`

### 4.1 Thêm state in-memory theo participant

Đặt gần khu vực `entrypoint(...)`, sau khi có `ctx` và trước khi register handlers:

```py
# Pref state per participant for this room session.
# Default: True (giữ behavior hiện tại)
participant_pref_audio_for_text_chat: dict[str, bool] = {}

def _get_audio_pref(participant_identity: str | None) -> bool:
    if not participant_identity:
        return True
    return participant_pref_audio_for_text_chat.get(participant_identity, True)
```

**Ghi chú cho fresher:**

- dict này sống trong process worker → reset khi worker restart.
- Đây là đúng tinh thần “SharedPreferences-first”: state bền nằm ở FE, BE chỉ cache.

### 4.2 Thêm handler đọc `lk.pref`

Trong `on_data_received(packet)` hiện đang return nếu topic != `lk.chat`.
Bạn sửa thành dispatch theo topic:

```py
def on_data_received(packet: rtc.DataPacket) -> None:
    # 1) Decode UTF-8
    try:
        text = packet.data.decode("utf-8")
    except Exception as exc:
        log.info(f"Data input decode failed: {exc}")
        return

    participant_id = packet.participant.identity if packet.participant else None

    # 2) lk.pref handler
    if packet.topic == "lk.pref":
        try:
            obj = json.loads(text)
        except Exception:
            log.info(f"Invalid lk.pref JSON: {text[:200]}")
            return

        if not isinstance(obj, dict) or obj.get("type") != "pref":
            return

        value = obj.get("audio_for_text_chat")
        if not isinstance(value, bool):
            log.info(f"lk.pref missing/invalid audio_for_text_chat: {obj}")
            return

        if participant_id:
            participant_pref_audio_for_text_chat[participant_id] = value
            log.info(f"Updated pref for {participant_id}: audio_for_text_chat={value}")
        return

    # 3) Existing lk.chat handler
    if packet.topic == "lk.chat":
        asyncio.create_task(handle_data_input(text, participant_id))
        return

    # ignore other topics
```

**Tại sao làm vậy?**

- `on_data_received` là nơi BE bắt DataChannel.
- Bạn thêm `lk.pref` mà không ảnh hưởng `lk.chat`.

### 4.3 Route text chat theo pref trong `handle_data_input`

Hiện tại `handle_data_input` luôn:

- save
- publish transcript user
- `session.generate_reply(user_input=text)` (→ audio luôn phát)

Bạn đổi logic:

```py
async def handle_data_input(text: str, participant_id: str | None) -> None:
    log.info(f"Data input from {participant_id or 'unknown'}: {text}")
    asyncio.create_task(asyncio.to_thread(_save_message, text, True))
    asyncio.create_task(_publish_transcript("user", text))

    await session.interrupt()

    audio_on = _get_audio_pref(participant_id)
    if audio_on:
        # behavior cũ (realtime)
        session.generate_reply(user_input=text)
        return

    # audio_off: text-only path (không publish audio track)
    reply_text = await _generate_text_only_reply(user_text=text)

    # publish text answer to lk.chat
    await ctx.room.local_participant.publish_data(
        reply_text,
        reliable=True,
        topic="lk.chat",
    )

    # publish transcript assistant JSON
    await _publish_transcript("assistant", reply_text)

    # persist assistant message
    asyncio.create_task(asyncio.to_thread(_save_message, reply_text, False))
```

**Điểm quan trọng:**

- Khi OFF, bạn **không gọi** `session.generate_reply` ⇒ tránh tạo audio track.
- Bạn phải tự publish text về `lk.chat` để FE vẫn thấy “answer”.

---

## 5) Vấn đề quan trọng: `_generate_text_only_reply` implement thế nào?

Trong file này hiện chưa có “text-only LLM client”. Bạn có 2 hướng:

### Hướng A (khuyến nghị trong giai đoạn này): dùng OpenAI Chat Completions (text-only)

Ý tưởng:

- Khi `audio_off`, gọi 1 model text-only rẻ hơn (ví dụ `gpt-4o-mini` hoặc model text khác bạn chọn)
- Prompt dùng cùng style instruction (ngắn gọn 2-3 câu)

Pseudo-code (bạn cần tự adapt theo SDK/package bạn đang dùng):

```py
async def _generate_text_only_reply(user_text: str) -> str:
    # 1) Build prompt
    system = (
        "Bạn là trợ lý AI sách nói TRIAM. "
        "Trả lời cực kỳ ngắn gọn (2-3 câu), tự nhiên, đi thẳng vào trọng tâm. "
        "Không dùng Markdown và không emoji."
    )

    # 2) Call a text-only LLM
    # TODO: Implement bằng client OpenAI bạn đang dùng trong project.
    # Return plain string.
    return "..."
```

**Note:** Vì tài liệu này chỉ đọc 1 file nên mình không thể khẳng định trong repo bạn đang dùng client OpenAI nào (official `openai` SDK hay wrapper khác). Nhưng nguyên tắc routing ở trên là phần quan trọng nhất.

### Hướng B: vẫn dùng realtime nhưng ép “text-only”

Với LiveKit OpenAI Realtime wrapper hiện tại:

- `generate_reply()` không nhận `output_modalities`.
- Session-level `output_modalities` được set theo lúc tạo session/update options, không có API public để đổi “audio ↔ text” theo từng message.

=> Nếu muốn làm “toggle per-message” bằng Realtime, bạn sẽ phải:

- patch/thay đổi code trong `livekit/plugins/openai/realtime/realtime_model.py` (site-packages), hoặc
- gọi private method/field để tự gửi `session.update` trước mỗi `response.create`.

Cả hai đều rất dễ gãy khi upgrade dependency, nên **không khuyến nghị cho MVP**.

---

## 6) Flutter side: code instruction gửi pref (SharedPreferences-first)

### 6.1 Lưu state local

Pseudo:

- key: `audio_for_text_chat`
- default: `true`

### 6.2 Sau khi connect room, publish `lk.pref`

```dart
import 'dart:convert';
import 'package:livekit_client/livekit_client.dart';

Future<void> publishPref(Room room, {required bool audioForTextChat}) async {
  final payload = {
    'v': 1,
    'type': 'pref',
    'audio_for_text_chat': audioForTextChat,
  };

  final bytes = utf8.encode(jsonEncode(payload));

  await room.localParticipant?.publishData(
    bytes,
    topic: 'lk.pref',
    reliability: Reliability.reliable,
  );
}
```

**Rule:**

- Mỗi lần join room (hoặc reconnect) phải gửi lại.

---

## 7) Checklist kiểm thử (rất thực dụng)

1. Toggle ON

- gửi `lk.pref` audio_for_text_chat=true
- gửi `lk.chat` → assistant reply có audio + text

2. Toggle OFF

- gửi `lk.pref` audio_for_text_chat=false
- gửi `lk.chat` → assistant reply **chỉ text**, không phát audio

3. Reconnect

- FE load SharedPreferences
- connect room → gửi `lk.pref` lại
- behavior vẫn đúng

---

## 8) Gợi ý cải tiến sau (khi bạn bật auth + user_id thật)

Khi có `user_id` ổn định:

- Bạn có thể persist pref ở Redis theo key `pref:{user_id}:audio_for_text_chat` để đồng bộ đa thiết bị.
- Nhưng với SharedPreferences-first thì chưa cần.

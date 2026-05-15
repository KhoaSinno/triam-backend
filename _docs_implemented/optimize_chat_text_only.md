# Hướng Dẫn Tối Ưu Hóa Chat Text-Only (Dual-Model)

Tài liệu này hướng dẫn bạn cách tích hợp thêm model `gpt-4o-mini` vào tiến trình Agent của LiveKit. Chức năng của mô hình này là:
- Đứng ra xử lý các tin nhắn Text mà người dùng gửi lên qua kênh `lk.chat`.
- Chặn không cho RealtimeModel (rất tốn kém token) phản hồi bằng Voice khi người dùng chỉ muốn chat chữ thông thường.

Bạn hãy mở file `app/services/agent_voice_gpt_realtime.py` và thực hiện lần lượt các bước (Copy-Paste) sau:

---

## Bước 1: Thêm thư viện `LLM` chuẩn
Di chuyển lên đầu file (Khu vực import), thêm đoạn import `LLM` của module `livekit.plugins.openai`.

**Tìm dòng (khoảng line 19-20):**
```python
from livekit.plugins import noise_cancellation, openai
from livekit.plugins.openai.realtime import RealtimeModel
```

**Sửa thành:**
```python
from livekit.plugins import noise_cancellation, openai
from livekit.plugins.openai.realtime import RealtimeModel
from livekit.plugins.openai import LLM as OpenAILLM # <-- DÒNG MỚI ĐƯỢC THÊM
```

---

## Bước 2: Tách biến Agent và cấu hình `chat_llm`
Chúng ta sẽ đưa khai báo `TriamAssistant` và Model chữ `gpt-4o-mini` ra bên ngoài vòng lặp để các hàm xử lý bên trong có thể dùng lại dễ dàng.

**Tìm dòng (Khoảng line 218):**
```python
    session: AgentSession
```

**Sửa khu vực đó thành:**
```python
    # === THÊM MỚI TỪ ĐÂY ===
    # Tách agent ra biến riêng để sử dụng Tools
    agent_instance = TriamAssistant(document_ids=document_ids)
    
    # Khởi tạo mô hình phụ chuyên trả lời Text
    chat_llm = OpenAILLM(model="gpt-4o-mini", temperature=0.7)
    # === HẾT THÊM MỚI ===

    session: AgentSession
```

---

## Bước 3: Áp dụng biến `agent_instance` vào vòng lặp Start
Bởi vì ở Bước 2 ta đã khởi tạo `agent_instance`, nên dưới phần `session.start` ta không cần phải khởi tạo lại nữa.

**Kéo xuống tìm đoạn (Khoảng line 321):**
```python
            await session.start(
                room=ctx.room,
                agent=TriamAssistant(document_ids=document_ids),
                room_options=room_io.RoomOptions(
```

**Thay thế thành:**
```python
            await session.start(
                room=ctx.room,
                agent=agent_instance, # <-- THAY BẰNG BIẾN ĐÃ KHỞI TẠO BÊN TRÊN
                room_options=room_io.RoomOptions(
```

---

## Bước 4: Sửa logic nhận tin nhắn Text (Luồng xử lý chính)
Đây là bước quan trọng nhất. Chúng ta sẽ ghi đè logic nhận tin nhắn để nó KHÔNG gọi RealtimeModel sinh audio nữa, mà gọi `chat_llm`.

**Tìm hai hàm `handle_text_input` và `handle_data_input` (Khoảng line 252 - 272):**
```python
    # Note: We use a custom data channel ("lk.chat") for text input instead of relying on room_io.TextInputEvent
    async def handle_text_input(sess: AgentSession, ev: room_io.TextInputEvent) -> None:
        participant_id = ev.participant.identity if ev.participant else "unknown"
        log.info(f"Text input from {participant_id}: {ev.text}")
        asyncio.create_task(asyncio.to_thread(_save_message, ev.text, True))
        await sess.interrupt()
        try:
            sess.generate_reply(user_input=ev.text)
        except Exception as exc:
            ... # Lược bỏ bớt code cũ

    async def handle_data_input(text: str, participant_id: str | None) -> None:
        log.info(f"Data input from {participant_id or 'unknown'}: {text}")
        asyncio.create_task(asyncio.to_thread(_save_message, text, True))
        asyncio.create_task(_publish_transcript("user", text))
        await session.interrupt()
        session.generate_reply(user_input=text)
```

**Xóa cả hai hàm cũ đi và thay bằng cụm hàm mới hoàn chỉnh này:**
```python
    async def handle_data_input(text: str, participant_id: str | None) -> None:
        log.info(f"Data input (Chat) from {participant_id or 'unknown'}: {text}")
        
        # 1. Lưu DB và cập nhật Transcript ngay lập tức
        asyncio.create_task(asyncio.to_thread(_save_message, text, True))
        asyncio.create_task(_publish_transcript("user", text))
        
        # 2. Bắt buộc ngắt ngang Voice AI đang nói (nếu có)
        await session.interrupt()
        
        # 3. Đưa câu hỏi vào bộ nhớ hội thoại của Room
        session.chat_ctx.append(role="user", text=text)

        try:
            # 4. Yêu cầu GPT-4o-mini trả lời bằng văn bản (Cho phép dùng Tool bằng cách đưa fnc_ctx vào)
            chat_stream = chat_llm.chat(
                chat_ctx=session.chat_ctx,
                fnc_ctx=agent_instance.fnc_ctx
            )
            
            full_reply = ""
            async for chunk in chat_stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    full_reply += chunk.choices[0].delta.content

            if full_reply:
                # 5. Lưu câu trả lời của AI vào DB & publish Transcript JSON 
                asyncio.create_task(asyncio.to_thread(_save_message, full_reply, False))
                asyncio.create_task(_publish_transcript("assistant", full_reply))
                
                # 6. Publish Text thuần xuống DataChannel cho UI hiển thị siêu tốc
                try:
                    await ctx.room.local_participant.publish_data(
                        full_reply.encode("utf-8"),
                        reliable=True,
                        topic="lk.chat",
                    )
                except Exception as exc:
                    log.error(f"Text output publish failed: {exc}")
                
                # 7. Cập nhật câu trả lời này ngược lại vào bộ nhớ hội thoại để RealtimeModel cũng nhớ nội dung này.
                session.chat_ctx.append(role="assistant", text=full_reply)
                
        except Exception as e:
            log.error(f"Lỗi khi xử lý chat text-only bằng LLM phụ: {e}")

    # Đồng bộ logic cho cổng TextInput (dự phòng)
    async def handle_text_input(sess: AgentSession, ev: room_io.TextInputEvent) -> None:
        participant_id = ev.participant.identity if ev.participant else "unknown"
        await handle_data_input(ev.text, participant_id)
```

---

## Hoàn Tất
Chỉ cần copy và ghi đè đúng các vị trí trên là bạn đã triển khai thành công mô hình **Dual-Model** (Realtime cho Voice, Mini cho Chat) để tối ưu chi phí. Bạn hãy thử copy paste và chạy thử file này để xem có bị báo lỗi syntax Python nào không nhé!

Nhận xét thẳng: kiến trúc hiện tại **đúng hướng cho MVP**, nhưng **chưa phải production-grade** nếu xét hiệu năng, token, độ ổn định hội thoại và maintainability.

**Điểm Đúng**
- Tách realtime voice và text chat riêng là đúng: `RealtimeModel` lo voice/audio, còn `chat_llm = OpenAILLM(model="gpt-4o-mini")` xử lý text chat tay qua `lk.chat` ở [agent_voice_gpt_realtime.py](/W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py:244).
- `modalities=["audio"]` hiện tại là hợp lý. Text UI vẫn nhận qua `TextOutputOptions` và DataChannel, không cần realtime model output text.
- DataChannel contract ổn: `lk.chat` cho text nhanh, `lk.transcript` làm timeline chính thức, `lk.control` cho toggle web search.
- Metadata `document_ids/thread_id` là hướng đúng để mỗi LiveKit room gắn với context/thread.

**Vấn Đề Lớn**
1. Có hardcode fallback `book_id/thread_id` trong worker ở [agent_voice_gpt_realtime.py](/W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py:204). Cái này nguy hiểm nếu deploy thật: metadata thiếu là ghi nhầm lịch sử vào thread test. Nên chỉ bật khi `ctx.room.name == "console"` hoặc qua env `VOICE_AGENT_CONSOLE_MODE=true`; production thì thiếu metadata phải thoát.

2. `entrypoint` quá lớn, hiện ruff đã báo `C901 entrypoint too complex`. File đang gom metadata parsing, DB persistence, transcript publish, text chat, tool loop, LiveKit handlers, model boot trong một hàm. Dự án thực tế nên tách thành:
   - `VoiceSessionState`
   - `TranscriptPublisher`
   - `ChatPersistenceService`
   - `TextChatHandler`
   - `RealtimeSessionFactory`

3. Token/cost sẽ tăng rất nhanh vì đang load toàn bộ history vào `session.history` ở [agent_voice_gpt_realtime.py](/W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py:571), rồi mỗi text turn lại copy toàn bộ history ở [agent_voice_gpt_realtime.py](/W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py:305). Thread dài là chi phí tăng tuyến tính, latency tăng, context dễ loãng. Nên chỉ lấy last 10-20 messages + summary thread.

4. RAG context chưa có token cap. `search_book_knowledge` trả chunk rồi join toàn bộ ở [agent_voice_gpt_realtime.py](/W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py:160). Nên giới hạn `top_k`, max chars/token, và truncate chunk trước khi inject vào prompt.

5. Concurrency chưa an toàn. Mỗi packet `lk.chat` tạo task mới ở [agent_voice_gpt_realtime.py](/W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py:472). Nếu user bấm gửi nhanh hoặc FE retry, nhiều reply có thể chạy song song, ghi DB lệch thứ tự, mutate `session.history` cùng lúc. Cần `asyncio.Lock` hoặc queue per session.

6. Dedupe voice transcript theo text thuần ở [agent_voice_gpt_realtime.py](/W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py:283) có thể nuốt mất câu lặp hợp lệ, ví dụ user nói “đúng rồi” hai lần. Nên dedupe theo event id nếu SDK có, hoặc theo `(text, role, time window 2-3s)`.

7. `TextInputOptions` có thể thừa cho production nếu FE chỉ gửi custom DataChannel `lk.chat` ở [agent_voice_gpt_realtime.py](/W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/agent_voice_gpt_realtime.py:535). Giữ được nếu cần console/built-in LiveKit text, nhưng nên comment rõ để tránh hai đường text input gây duplicate.

8. `temperature=0.8` trong `RealtimeModel` hiện là tham số deprecated/unused với LiveKit plugin mới. Nên bỏ để tránh hiểu nhầm.

**Token/Auth**
- LiveKit token theo thread là đúng. Nhưng worker đang tin mọi packet trong room. Với app thật, nên đảm bảo token endpoint authorize user sở hữu thread/context, và room chỉ có user + agent.
- `lk.control` hiện ai trong room cũng toggle được web search. Nếu sau này room multi-user thì cần validate identity/role.

**Kết Luận**
Luồng hiện tại dùng được cho MVP/demo: voice realtime, text chat riêng, transcript UI, persistence theo thread. Nhưng để thành kiến trúc thực tế, ưu tiên sửa theo thứ tự:

1. Bỏ hardcode production metadata.
2. Thêm per-session lock/queue cho text input.
3. Giới hạn history/token bằng window + summary.
4. Giới hạn RAG context.
5. Tách `entrypoint` thành các class/service nhỏ.
6. Làm rõ hoặc bỏ `TextInputOptions` nếu FE không dùng.
7. Dọn dead params trong `ChatTextOutput`.

Nếu làm 3 mục đầu thôi, hệ thống đã ổn hơn rất nhiều về chi phí, latency và lỗi khó debug.
# Flutter LiveKit Reconnect Lifecycle Fix Spec

Ngày cập nhật: 2026-06-05  
Audience: Flutter team  
Scope: kiểm tra và sửa lỗi LiveKit room bị tạo lặp, session bị treo, error bubble bị append nhiều lần.

---

## 1. Vấn Đề Hiện Tại

Dashboard LiveKit xuất hiện nhiều room/session `ACTIVE` kéo dài dù user đã thoát màn voice/chat.

Nguyên nhân chính ở FE:

```text
connect lỗi
-> gọi lại /live-token/thread/{thread_id}
-> backend cấp room_name mới
-> FE connect room mới
-> lỗi tiếp
-> tiếp tục tạo room mới
```

Hậu quả:

- tạo nhiều LiveKit room không cần thiết;
- dispatch nhiều agent realtime;
- room cũ bị treo lâu;
- UI append nhiều message lỗi dạng `Không thể kết nối phòng hội thoại`;
- user thấy trải nghiệm bị lặp lỗi và khó thoát trạng thái đang kết nối.

---

## 2. Backend Hiện Tại Đã Harden Gì

Backend đã update:

- Room token có `empty_timeout` và `departure_timeout`.
- Realtime agent tự cleanup khi không còn remote participant sau một grace period.
- Agent bật `delete_room_on_close`.
- FE doc cũ đã được sửa: không được gọi token mới liên tục khi reconnect.

Nhưng backend không thể sửa hoàn toàn nếu FE vẫn tạo room mới liên tục.

---

## 3. Rule Bắt Buộc Cho FE

### 3.1 Single-flight connect

Tại một thời điểm, mỗi màn voice/chat chỉ được có một connect attempt.

Không được:

```text
button tap nhiều lần -> nhiều connect song song
network callback -> connect
retry timer -> connect
screen init -> connect
```

mà không có guard.

FE nên có state:

```text
idle
connecting
connected
reconnecting
failed
disconnecting
disposed
```

Nếu state đang là `connecting`, `connected`, hoặc `reconnecting`, không start connect attempt mới.

---

### 3.2 Không spam `/live-token/thread/{thread_id}`

Endpoint:

```http
GET /api/v1/live-token/thread/{thread_id}
```

chỉ gọi khi:

- user bắt đầu một phiên voice/chat mới;
- token hết hạn;
- LiveKit SDK báo reconnect thất bại hoàn toàn;
- user bấm retry sau khi FE state đã chuyển sang `failed`.

Không gọi endpoint này mỗi khi:

- mạng chập chờn;
- LiveKit SDK đang tự reconnect;
- nhận event `disconnected` tạm thời;
- retry timer cũ chưa bị hủy.

Lý do: backend hiện cấp `room_name` mới mỗi lần lấy token mới. Gọi token mới liên tục sẽ tạo nhiều room mới.

---

### 3.3 Ưu tiên LiveKit SDK reconnect nội bộ

Khi mạng rớt tạm thời:

1. UI chuyển sang trạng thái `reconnecting`.
2. Để LiveKit SDK tự reconnect với room/token hiện tại.
3. Không lấy token mới ngay.
4. Chỉ chuyển sang `failed` khi SDK báo reconnect thất bại hoàn toàn hoặc hết timeout FE quy định.

Khuyến nghị timeout FE:

```text
reconnect grace: 10-20 giây
```

---

### 3.4 Retry phải có backoff và hủy timer cũ

Khi cần retry thủ công hoặc auto retry sau failed:

```text
1s -> 2s -> 4s -> 8s -> max 15s
```

Trước khi tạo retry timer mới, phải cancel timer cũ.

Khi user thoát màn, phải cancel toàn bộ retry timer.

---

### 3.5 Thoát màn phải dispose sạch

Khi user rời màn voice/chat:

```text
cancel retry timers
remove listeners
stop local audio track / microphone
room.disconnect()
clear current room reference
state = disposed
```

Không được giữ listener cũ rồi vào màn lại tạo listener mới chồng lên.

---

### 3.6 Error UI không được append thành chat message

Lỗi kết nối là trạng thái UI, không phải message hội thoại.

Không append nhiều bubble:

```text
[Lỗi: Không thể kết nối phòng hội thoại...]
[Lỗi: Không thể kết nối phòng hội thoại...]
[Lỗi: Không thể kết nối phòng hội thoại...]
```

Nên hiển thị một status duy nhất:

```text
Đang kết nối...
Đang kết nối lại...
Không thể kết nối. Thử lại
```

Nếu đã có lỗi hiện trên UI, update lỗi đó thay vì thêm message mới.

---

## 4. Expected FE Flow

### 4.1 Mở màn voice/chat

```text
state = idle
load canonical thread
GET /live-token/thread/{thread_id}
connect LiveKit room
state = connected
```

### 4.2 Mạng rớt tạm thời

```text
LiveKit event: reconnecting
state = reconnecting
show reconnecting UI
do not call live-token
wait SDK reconnect
```

Nếu reconnect thành công:

```text
state = connected
hide reconnecting UI
```

Nếu reconnect fail:

```text
state = failed
show retry button
```

### 4.3 User bấm retry sau failed

```text
if state != failed: ignore
cancel old room safely
GET /live-token/thread/{thread_id}
connect new room
```

### 4.4 User thoát màn

```text
cancel timers
dispose listeners
room.disconnect()
state = disposed
```

---

## 5. Acceptance Tests Cho FE

### Test 1: Tap nhanh nhiều lần

Hành động:

- Mở màn voice.
- Tap connect/voice nhiều lần thật nhanh.

Expected:

- Chỉ có một request `/live-token/thread/{thread_id}`.
- Chỉ có một LiveKit room được tạo.
- UI không append nhiều error bubble.

---

### Test 2: Mạng chập chờn

Hành động:

- Connect voice thành công.
- Tắt mạng 3-5 giây.
- Bật mạng lại.

Expected:

- FE không gọi token mới trong lúc SDK reconnect.
- Room cũ được reuse nếu SDK reconnect thành công.
- UI chuyển `reconnecting -> connected`.

---

### Test 3: Mất mạng lâu

Hành động:

- Connect voice thành công.
- Tắt mạng lâu hơn timeout FE.

Expected:

- UI chuyển sang `failed`.
- Không tạo room mới vô hạn.
- Chỉ khi user bấm retry thì FE mới gọi token mới.

---

### Test 4: Thoát màn

Hành động:

- Connect voice thành công.
- Back khỏi màn hoặc đóng app.

Expected:

- FE gọi `room.disconnect()`.
- Không còn retry timer chạy nền.
- Không còn listener cũ.
- LiveKit dashboard không tăng thêm room mới sau khi đã thoát.

---

### Test 5: Vào lại màn

Hành động:

- Thoát màn voice.
- Vào lại màn voice.

Expected:

- Session mới chỉ tạo một room mới.
- Không nhận duplicate transcript từ listener cũ.
- Không có nhiều greeting/assistant reply bị lặp.

---

## 6. Checklist Code Review

FE cần tự kiểm tra:

- [ ] Có biến/state chống connect song song.
- [ ] Retry timer được cancel khi retry mới hoặc dispose.
- [ ] Không gọi `/live-token/thread/{thread_id}` trong mỗi event reconnect.
- [ ] `room.disconnect()` được gọi khi thoát màn.
- [ ] Listener LiveKit/DataChannel được remove/dispose.
- [ ] Error kết nối không được append thành chat message nhiều lần.
- [ ] UI dùng `thread_id` và transcript `id` cho persistence/dedup, không dựa vào LiveKit identity.

---

## 7. Ghi Chú Với BE

Backend hiện vẫn tạo `room_name` random mỗi lần cấp token. Đây là chấp nhận được nếu FE gọi token đúng thời điểm.

Nếu sau khi FE fix mà vẫn còn room treo, phase tiếp theo của BE nên thêm `voice_session_id` để reuse room trong một phiên cụ thể và có endpoint kết thúc session idempotent.

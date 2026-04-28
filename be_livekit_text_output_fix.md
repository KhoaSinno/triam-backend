# LiveKit Agent text output - hien trang va cach xu ly

## 1) Tom tat van de

- FE gui chat bang Data Channel (topic `lk.chat`) nhung khong nhan duoc text.
- FE bi timeout 15s: "Tri Am khong nhan duoc phan hoi".
- BE log lien tuc:
  - "unexpected message {'type': 'output_timestamps', ...}"

## 2) Y nghia cua log

- `output_timestamps` la event word-level do TTS tra ve.
- Phien ban `livekit.agents`/plugin hien tai khong co handler cho event nay.
- Ket qua: BE phat audio binh thuong, nhung khong publish transcript ra `lk.chat`.
- FE khong co text -> timeout la dung.

## 3) Nguyen nhan chinh

- Chua nang version `livekit.agents` va cac plugin len ban ho tro `output_timestamps`.
- `TextOutputOptions()` duoc bat trong code nhung khong co tac dung neu version cu.

## 4) Huong xu ly (Hướng A - chuan nhat)

### A. Nang version va dong bo plugins

1. Cap nhat cac goi `livekit-agents` va plugins (TTS/VAD/Noise/LLM) len ban moi nhat tuong thich.
2. Dam bao BE runtime dang dung dung version moi (khong chi cap nhat trong file requirements).

### B. Kiem tra version trong runtime

Chen log ngay khi worker start:

```python
import livekit.agents as lk_agents
print("livekit.agents version:", lk_agents.__version__)
```

Muc tieu: sau khi nang, log "unexpected message output_timestamps" phai bien mat.

### C. Xac nhan text output

- `text_output=room_io.TextOutputOptions()` phai tu dong publish transcript ra `lk.chat`.
- FE se nhan duoc text va khong bi timeout 15s.

## 5) Cac buoc verify nhanh

- Chay lai worker, theo doi log:
  - Khong con warning `unexpected message output_timestamps`.
  - FE nhan duoc `lk.chat` va show text.
- Test: gui 1 tin nhan text -> FE hien transcript ngay.

## 6) Neu can fallback tam thoi

- Neu chua kip nang version, co the parse `output_timestamps` de ghep words thanh text va publish ra `lk.chat`.
- (Fallback nay khong phai Hướng A, chi dung de giam timeout tam thoi.)

## 7) Noi can cap nhat trong BE

- File worker (vd: `code_worker_BE.md`) da bat `TextOutputOptions()`. Van de la version runtime.
- Kiem tra process deploy/pip cache (venv, docker image, server) de chac chan version moi duoc su dung.

////////////////////// Kiểm tra lại sự đánh giá này /////////////////////////////////////

Mấu chốt nằm ở log BE: `unexpected message {'type': 'output_timestamps' ...}` vẫn xuất hiện. Điều này cho thấy **worker đang chạy phiên bản `livekit.agents`/plugin TTS chưa hỗ trợ output_timestamps**, nên **không publish text ra `lk.chat`**. Vì không có text, FE vẫn timeout 15s là đúng.  
Giọng nói vẫn ra là bình thường vì TTS audio track vẫn phát.

**Cách xử lý đúng chuẩn (Hướng A, BE‑only):**

- **Bắt buộc upgrade đúng môi trường đang chạy worker**, không chỉ sửa code.
- Cập nhật **đồng bộ** các gói `livekit-agents` + plugin liên quan (TTS/Noise/VAD/LLM).
- Xác nhận version trong runtime (in ra log) để chắc chắn worker đang dùng bản mới.

**Checklist BE để xác nhận upgrade đã thật sự áp dụng:**

1. In version ra log ngay khi worker start:
   ```python
   import livekit.agents as lk_agents
   print("livekit.agents version:", lk_agents.__version__)
   ```
2. Sau khi upgrade, **log “unexpected message output_timestamps” phải biến mất**.
3. Khi chạy lại, FE phải thấy `lk.chat` (hoặc ít nhất thấy text trên FE).

**Vì sao vẫn có warning dù đã đổi code**  
Trong code_worker_BE.md bạn đã bật `text_output=room_io.TextOutputOptions()`, nhưng **nếu version không hỗ trợ** thì nó **không publish text**, chỉ audio → FE vẫn timeout.

---

Nếu bạn muốn, gửi giúp mình:

- `pip freeze | grep livekit` của BE
- log in ra version `livekit.agents` ở runtime

Mình sẽ chỉ ra **version pin cụ thể** cần dùng để hết warning và có text.  
Ngoài ra, nếu cần chạy tạm trước khi upgrade xong, mình có thể giúp **parse `output_timestamps` ở FE** để nối text (nhưng đây là fallback, không phải Hướng A).

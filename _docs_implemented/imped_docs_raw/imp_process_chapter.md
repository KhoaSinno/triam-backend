Để giải quyết vấn đề lưu trữ tệp tin lên Supabase Storage và đồng bộ hóa URL vào Database theo thứ tự chính xác cho Flutter, bạn cần thực hiện theo quy trình: **Tạo tệp cục bộ -> Upload Storage -> Lấy Public URL -> Lưu Metadata vào Table**.

Dưới đây là kiến trúc cơ sở dữ liệu và mã nguồn Python tối ưu để thực hiện việc này.

### 1. Cấu trúc Database (SQL)

Để Flutter có thể phát playlist một cách liền mạch, chúng ta nên tách riêng các "đoạn" (segments) của chương ra một bảng con. Điều này giúp bạn quản lý thứ tự (`index`) cực kỳ dễ dàng.

```sql
-- Bảng chứa thông tin chương
CREATE TABLE chapters (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    book_id uuid REFERENCES books(id) ON DELETE CASCADE,
    chapter_index int,
    title text,
    review_audio_url text, -- URL cho đoạn ôn tập 80/20
    review_text text,
    status text DEFAULT 'processing'
);

-- Bảng chứa các đoạn audio nhỏ của chương đó (Playlist)
CREATE TABLE chapter_segments (
    id bigserial PRIMARY KEY,
    chapter_id uuid REFERENCES chapters(id) ON DELETE CASCADE,
    segment_index int, -- Dùng để ORDER BY trong Flutter
    audio_url text,
    text_content text
);

```

### 2. Cập nhật `process_single_chapter`

Trong đoạn code này, chúng ta sẽ lặp qua mảng `main_scripts`, xử lý từng đoạn và thu thập URL để lưu vào DB trong một lần gọi (batch insert) để tối ưu hiệu năng.

```python
import os
from supabase import create_client, Client
from app.core.config import settings

# Khởi tạo Supabase Client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

async def upload_to_supabase(local_path: str, storage_path: str):
    """Hàm hỗ trợ upload file và trả về public URL"""
    with open(local_path, 'rb') as f:
        supabase.storage.from_("audios").upload(
            path=storage_path,
            file=f,
            file_options={"content-type": "audio/mpeg"}
        )
    # Lấy URL công khai
    return supabase.storage.from_("audios").get_public_url(storage_path)

async def process_single_chapter(book_id: str, chapter_data: dict, index: int):
    async with sem:
        try:
            # 1. REWRITE (Gemini)
            obj_chapter = await normalize_text_for_speech(chapter_data["text"])
            main_chunks = obj_chapter.get("main_scripts", [])
            review_text = obj_chapter.get("review_script", "")

            # Tạo bản ghi chương trong DB trước để lấy chapter_id
            chapter_res = supabase.table("chapters").insert({
                "book_id": book_id,
                "chapter_index": index,
                "title": chapter_data.get("title", f"Chương {index+1}"),
                "review_text": review_text
            }).execute()
            chapter_id = chapter_res.data[0]['id']

            segments_to_insert = []

            # 2. TTS & UPLOAD STORAGE
            for i, chunk in enumerate(main_chunks):
                # Tạo file tạm cục bộ
                local_filename = f"temp_{uuid.uuid4()}.mp3"
                await generate_audio_file_edge(chunk, local_filename)

                # Đường dẫn lưu trên Cloud: books/uuid/chap_1/part_1.mp3
                storage_path = f"{book_id}/chap_{index+1}/part_{i+1}.mp3"

                # Upload và lấy link
                public_url = await upload_to_supabase(local_filename, storage_path)

                # Xóa file tạm sau khi upload
                if os.path.exists(local_filename):
                    os.remove(local_filename)

                # Thu thập dữ liệu để lưu vào DB
                segments_to_insert.append({
                    "chapter_id": chapter_id,
                    "segment_index": i,
                    "audio_url": public_url,
                    "text_content": chunk
                })

            # 3. LƯU PLAYLIST VÀO DB (Batch Insert)
            if segments_to_insert:
                supabase.table("chapter_segments").insert(segments_to_insert).execute()

            # 4. XỬ LÝ RIÊNG CHO REVIEW SCRIPT (Nếu có)
            if review_text:
                review_local = f"temp_rev_{uuid.uuid4()}.mp3"
                await generate_audio_file_edge(review_text, review_local)
                review_storage_path = f"{book_id}/chap_{index+1}/review.mp3"
                review_url = await upload_to_supabase(review_local, review_storage_path)

                # Cập nhật lại URL review vào bảng chapters
                supabase.table("chapters").update({"review_audio_url": review_url, "status": "ready"})\
                    .eq("id", chapter_id).execute()

                if os.path.exists(review_local):
                    os.remove(review_local)

            # 5. RAG (Embed sạch vào Vector DB)
            await embed_chunk_to_supbabase(book_id, index, main_chunks)

        except Exception as e:
            print(f"Lỗi chương {index + 1}: {e}")

```

### 3. Tại sao cách này tối ưu cho Flutter?

Khi bạn thiết kế theo cách này, phía Flutter sẽ xử lý rất "nhẹ nhàng":

1. **Truy vấn đơn giản:** Flutter chỉ cần gọi API hoặc dùng trực tiếp Supabase SDK để lấy playlist của một chương:

```dart
final response = await supabase
  .from('chapter_segments')
  .select()
  .eq('chapter_id', current_chapter_id)
  .order('segment_index', ascending: true); // Luôn đúng thứ tự

```

2. **Streaming mượt mà:** Sử dụng các gói như `just_audio` hoặc `audioplayers`, bạn chỉ cần nạp danh sách URL này vào một `ConcatenatingAudioSource`.
3. **Không bị nghẽn:** Vì file được chia nhỏ (theo `main_scripts`), App sẽ tải (buffer) đoạn 1 và phát ngay lập tức trong khi đoạn 2 đang được tải ngầm, thay vì phải chờ tải một file mp3 khổng lồ 50MB.

### 4. Lưu ý về quản lý file tạm (Temp files)

Trong code trên, tôi có sử dụng `uuid.uuid4()` để đặt tên file tạm. Điều này cực kỳ quan trọng vì bạn có `Semaphore(3)` (3 workers chạy cùng lúc). Nếu đặt tên file cố định, các worker sẽ ghi đè file của nhau dẫn đến dữ liệu bị lỗi. Sau khi upload lên Storage thành công, hãy luôn nhớ xóa file ở `temp_audio/` để tránh tràn bộ nhớ server.

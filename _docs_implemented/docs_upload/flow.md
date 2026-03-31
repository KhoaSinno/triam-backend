# Flow upload document (PDF, Word, Ebook)

---

## 1. User uploads a document (PDF, Word, Ebook) to the system

- Aim: Denied trash from user, give user a good freedom experience

- Logic flow:
  - Flutter: Rate limit (maxSize file is 50MB, type: PDF, Word, Ebook)
  - Backend:
    - Validate type, size
    - Store tmp local/Supabase Storage
    - Rename fileName to be unique

## 2. Flutter appear outline and run background process

- Aim: Smooth exp, hide conflict process

- Logic flow:
  - Flutter: Show outline, run call api background process
  - Backend:
    - Extract outline + text from doc
    - SaveDB: `books(id, title, total_chapters, status, created_at)`
    - Return outline to Flutter

## 3. Logic flow: Run background process

- Rewrite text/review_text to chunks. One chapter have many chunks, each chunk is a paragraph or 2-3 sentences meaningful
- TTS and storage to cloud base on plan (full/80_20): local generate => upload cloud => Delete local => Append to list
- SaveDB base on list above: `chapter_segments('chapter_id', 'segment_index', 'audio_url', 'text_content')`
- Generate/Insert embedding vector base on text planed: `book_knowledge('book_id', 'chapter_index', 'chunk_index', 'content', 'embedding')`
- Update chapter status to "ready"
- Update book status to "ready" when all chapters are ready

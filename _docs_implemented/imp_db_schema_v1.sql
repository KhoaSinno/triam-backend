-- Database Schema for Book Audiobook Processing System
-- This schema supports the chapter processing workflow with Supabase Storage integration

-- ============================================================================
-- 1. BOOKS TABLE
-- ============================================================================
-- Main table to store book metadata and processing status
CREATE TABLE IF NOT EXISTS books (
id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
title text NOT NULL,
total_chapters int NOT NULL DEFAULT 0,
status text NOT NULL DEFAULT 'processing', -- 'processing', 'completed', 'error'
error_message text, -- Store error details if processing fails
created_at timestamp with time zone DEFAULT now(),
updated_at timestamp with time zone DEFAULT now()
);

-- Index for faster status queries
CREATE INDEX IF NOT EXISTS idx_books_status ON books(status);
CREATE INDEX IF NOT EXISTS idx_books_created_at ON books(created_at DESC);

-- ============================================================================
-- 2. CHAPTERS TABLE
-- ============================================================================
-- Store chapter metadata and review audio
CREATE TABLE IF NOT EXISTS chapters (
id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
book_id uuid NOT NULL REFERENCES books(id) ON DELETE CASCADE,
chapter_index int NOT NULL,
title text NOT NULL,
review_audio_url text, -- URL for 80/20 review audio
review_text text, -- Text content of review script
status text DEFAULT 'processing', -- 'processing', 'ready', 'error'
error_message text,
created_at timestamp with time zone DEFAULT now(),
updated_at timestamp with time zone DEFAULT now()
);

-- Ensure unique chapter index per book
CREATE UNIQUE INDEX IF NOT EXISTS idx_chapters_book_index ON chapters(book_id, chapter_index);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_chapters_status ON chapters(status);
CREATE INDEX IF NOT EXISTS idx_chapters_book_id ON chapters(book_id);

-- ============================================================================
-- 3. CHAPTER SEGMENTS TABLE
-- ============================================================================
-- Store individual audio segments for playlist streaming in Flutter
CREATE TABLE IF NOT EXISTS chapter_segments (
id bigserial PRIMARY KEY,
chapter_id uuid NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
segment_index int NOT NULL, -- Used for ORDER BY in Flutter playlist
audio_url text NOT NULL, -- Public URL from Supabase Storage
text_content text, -- Text content of this segment
created_at timestamp with time zone DEFAULT now()
);

-- Ensure unique segment index per chapter
CREATE UNIQUE INDEX IF NOT EXISTS idx_segments_chapter_index ON chapter_segments(chapter_id, segment_index);

-- Index for faster playlist queries
CREATE INDEX IF NOT EXISTS idx_segments_chapter_id ON chapter_segments(chapter_id);

-- ============================================================================
-- 4. STORAGE BUCKET (Supabase Storage)
-- ============================================================================
-- Run this in Supabase SQL Editor or via Dashboard
-- Create the 'audios' bucket if it doesn't exist
INSERT INTO storage.buckets (id, name, public)
VALUES ('audios', 'audios', true)
ON CONFLICT (id) DO NOTHING;

-- Set storage policy to allow public access (read-only)
CREATE POLICY "Public Access for Audios"
ON storage.objects FOR SELECT
USING (bucket_id = 'audios');

-- Allow service role to insert/update/delete
CREATE POLICY "Service role can manage audios"
ON storage.objects FOR ALL
USING (bucket_id = 'audios' AND auth.role() = 'service_role');

-- ============================================================================
-- 5. ROW LEVEL SECURITY (RLS) POLICIES
-- ============================================================================
-- Enable RLS on all tables
ALTER TABLE books ENABLE ROW LEVEL SECURITY;
ALTER TABLE chapters ENABLE ROW LEVEL SECURITY;
ALTER TABLE chapter_segments ENABLE ROW LEVEL SECURITY;

-- Allow service role (backend) to do everything
CREATE POLICY "Service role has full access to books"
ON books FOR ALL
USING (auth.role() = 'service_role');

CREATE POLICY "Service role has full access to chapters"
ON chapters FOR ALL
USING (auth.role() = 'service_role');

CREATE POLICY "Service role has full access to segments"
ON chapter_segments FOR ALL
USING (auth.role() = 'service_role');

-- Allow public read access for Flutter app
CREATE POLICY "Public can read books"
ON books FOR SELECT
USING (true);

CREATE POLICY "Public can read chapters"
ON chapters FOR SELECT
USING (true);

CREATE POLICY "Public can read segments"
ON chapter_segments FOR SELECT
USING (true);

-- ============================================================================
-- 6. UPDATED_AT TRIGGER
-- ============================================================================
-- Auto-update updated_at timestamp on row changes
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
NEW.updated_at = now();
RETURN NEW;
END;

$$
language 'plpgsql';

CREATE TRIGGER update_books_updated_at BEFORE UPDATE ON books
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_chapters_updated_at BEFORE UPDATE ON chapters
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 7. SAMPLE QUERY FOR FLUTTER
-- ============================================================================
-- Get all segments for a chapter in order (for playlist)
-- SELECT * FROM chapter_segments
-- WHERE chapter_id = '...'
-- ORDER BY segment_index ASC;

-- Get all chapters for a book
-- SELECT * FROM chapters
-- WHERE book_id = '...'
-- ORDER BY chapter_index ASC;

-- Get book with chapter count
-- SELECT b.*, COUNT(c.id) as processed_chapters
-- FROM books b
-- LEFT JOIN chapters c ON c.book_id = b.id AND c.status = 'ready'
-- WHERE b.id = '...'
-- GROUP BY b.id;


$$

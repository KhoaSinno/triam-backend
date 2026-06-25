"""add_shared_book_columns_and_clone_function

Revision ID: b14a05b2dfeb
Revises: d16e5f607182
Create Date: 2026-06-25 12:20:21.950633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b14a05b2dfeb'
down_revision: Union[str, Sequence[str], None] = 'd16e5f607182'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Thêm cột mới vào bảng books
    op.add_column('books', sa.Column('is_shared', sa.Boolean(), server_default='false', nullable=False))
    op.create_index(op.f('ix_books_is_shared'), 'books', ['is_shared'], unique=False)
    op.add_column('books', sa.Column('parent_shared_id', sa.UUID(), nullable=True))
    op.create_index(op.f('ix_books_parent_shared_id'), 'books', ['parent_shared_id'], unique=False)
    op.create_foreign_key('fk_books_parent_shared_id', 'books', 'books', ['parent_shared_id'], ['id'], ondelete='SET NULL')

    # 2. Tạo PostgreSQL Stored Function để nhân bản sách (Metadata Cloning)
    op.execute("""
    CREATE OR REPLACE FUNCTION clone_shared_book(
        shared_book_id UUID,
        new_user_id UUID,
        new_book_id UUID
    )
    RETURNS VOID AS $$
    BEGIN
        -- a. Nhân bản bản ghi Book
        INSERT INTO books (
            id, user_id, title, author, file_url, document_type, 
            total_sections, total_units, status, is_shared, parent_shared_id, 
            created_at, updated_at
        )
        SELECT 
            new_book_id, new_user_id, title, author, file_url, document_type, 
            total_sections, total_units, 'ready', false, shared_book_id, 
            now(), now()
        FROM books 
        WHERE id = shared_book_id;

        -- b. Tạo bảng tạm map ID của BookSection cũ sang ID mới
        CREATE TEMP TABLE temp_section_map ON COMMIT DROP AS
        SELECT 
            id AS old_section_id, 
            gen_random_uuid() AS new_section_id
        FROM book_sections 
        WHERE book_id = shared_book_id;

        -- c. Nhân bản các BookSection
        INSERT INTO book_sections (
            id, book_id, parent_id, section_index, title, level, path, 
            text_content, text_char_count, page_start, page_end, source_href, source_anchor, 
            created_at, updated_at
        )
        SELECT 
            m.new_section_id, 
            new_book_id, 
            old_sec.parent_id, -- Tạm thời copy old parent_id
            old_sec.section_index, 
            old_sec.title, 
            old_sec.level, 
            old_sec.path, 
            old_sec.text_content, 
            old_sec.text_char_count, 
            old_sec.page_start, 
            old_sec.page_end, 
            old_sec.source_href, 
            old_sec.source_anchor, 
            now(), 
            now()
        FROM book_sections old_sec
        JOIN temp_section_map m ON old_sec.id = m.old_section_id;

        -- d. Khôi phục cấu trúc cây phân cấp parent_id của BookSection (Dùng cú pháp an toàn tương thích mọi bản Postgres)
        UPDATE book_sections
        SET parent_id = m_parent.new_section_id
        FROM temp_section_map m_child,
             temp_section_map m_parent
        WHERE book_sections.book_id = new_book_id
          AND book_sections.id = m_child.new_section_id
          AND book_sections.parent_id = m_parent.old_section_id;

        -- e. Đặt các parent_id không thuộc cuốn sách về NULL
        UPDATE book_sections
        SET parent_id = NULL
        WHERE book_id = new_book_id
          AND parent_id IS NOT NULL
          AND parent_id NOT IN (SELECT new_section_id FROM temp_section_map);

        -- f. Nhân bản dữ liệu Vector pgvector (BookSectionKnowledge)
        INSERT INTO book_section_knowledge (
            book_id, section_id, chunk_index, content, search_text, content_hash, 
            embedding_model, embedding_version, char_count, token_count, embedding, 
            created_at, updated_at
        )
        SELECT 
            new_book_id, 
            m.new_section_id, 
            old_kn.chunk_index, 
            old_kn.content, 
            old_kn.search_text, 
            old_kn.content_hash, 
            old_kn.embedding_model, 
            old_kn.embedding_version, 
            old_kn.char_count, 
            old_kn.token_count, 
            old_kn.embedding, 
            now(), 
            now()
        FROM book_section_knowledge old_kn
        JOIN temp_section_map m ON old_kn.section_id = m.old_section_id;

        -- g. Tạo bảng tạm map ID của LearningUnit cũ sang ID mới
        CREATE TEMP TABLE temp_unit_map ON COMMIT DROP AS
        SELECT 
            id AS old_unit_id, 
            gen_random_uuid() AS new_unit_id
        FROM learning_units 
        WHERE book_id = shared_book_id;

        -- h. Nhân bản các LearningUnit
        INSERT INTO learning_units (
            id, user_id, book_id, mode, unit_index, title, unit_type, status, 
            source_text_char_count, estimated_tokens, estimated_audio_seconds, main_segment_count, 
            review_audio_url, review_text, planner_reason, created_at, updated_at
        )
        SELECT 
            m.new_unit_id, 
            new_user_id, 
            new_book_id, 
            old_unit.mode, 
            old_unit.unit_index, 
            old_unit.title, 
            old_unit.unit_type, 
            old_unit.status, 
            old_unit.source_text_char_count, 
            old_unit.estimated_tokens, 
            old_unit.estimated_audio_seconds, 
            old_unit.main_segment_count, 
            old_unit.review_audio_url, 
            old_unit.review_text, 
            old_unit.planner_reason, 
            now(), 
            now()
        FROM learning_units old_unit
        JOIN temp_unit_map m ON old_unit.id = m.old_unit_id;

        -- i. Nhân bản bảng liên kết LearningUnitSource
        INSERT INTO learning_unit_sources (
            learning_unit_id, section_id, source_order
        )
        SELECT 
            mu.new_unit_id, 
            ms.new_section_id, 
            old_src.source_order
        FROM learning_unit_sources old_src
        JOIN temp_unit_map mu ON old_src.learning_unit_id = mu.old_unit_id
        JOIN temp_section_map ms ON old_src.section_id = ms.old_section_id;

        -- j. Nhân bản các phân đoạn file mp3 (LearningUnitSegment)
        INSERT INTO learning_unit_segments (
            learning_unit_id, segment_index, audio_url, text_content, duration_ms, created_at
        )
        SELECT 
            mu.new_unit_id, 
            old_seg.segment_index, 
            old_seg.audio_url, 
            old_seg.text_content, 
            old_seg.duration_ms, 
            now()
        FROM learning_unit_segments old_seg
        JOIN temp_unit_map mu ON old_seg.learning_unit_id = mu.old_unit_id;

    END;
    $$ LANGUAGE plpgsql;
    """)


def downgrade() -> None:
    # Xóa Stored Function
    op.execute("DROP FUNCTION IF EXISTS clone_shared_book(UUID, UUID, UUID);")
    
    # Xóa cột và index
    op.drop_constraint('fk_books_parent_shared_id', 'books', type_='foreignkey')
    op.drop_index(op.f('ix_books_parent_shared_id'), table_name='books')
    op.drop_column('books', 'parent_shared_id')
    op.drop_index(op.f('ix_books_is_shared'), table_name='books')
    op.drop_column('books', 'is_shared')

from sqlmodel import create_engine, Session, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
with Session(engine) as session:
    sql = """
    DROP FUNCTION IF EXISTS match_book_knowledge(vector, double precision, integer, uuid);
    
    CREATE OR REPLACE FUNCTION match_book_knowledge(
      query_embedding vector(1536),
      match_threshold float,
      match_count int,
      filter_book_id uuid
    )
    RETURNS TABLE (
      id integer,
      book_id uuid,
      chapter_id uuid,
      chunk_index integer,
      content text,
      similarity float
    )
    LANGUAGE sql STABLE
    AS $$
      SELECT
        book_knowledge.id,
        book_knowledge.book_id,
        book_knowledge.chapter_id,
        book_knowledge.chunk_index,
        book_knowledge.content,
        1 - (book_knowledge.embedding <=> query_embedding) AS similarity
      FROM book_knowledge
      WHERE 1 - (book_knowledge.embedding <=> query_embedding) > match_threshold
        AND book_knowledge.book_id = filter_book_id
      ORDER BY book_knowledge.embedding <=> query_embedding
      LIMIT match_count;
    $$;
    """
    session.exec(text(sql))
    session.commit()
    print('RPC Function Updated!')

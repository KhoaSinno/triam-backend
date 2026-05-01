from sqlmodel import create_engine, Session, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
with Session(engine) as session:
    sql = """
    DROP FUNCTION IF EXISTS match_book_knowledge(vector, double precision, integer, uuid);

    create or replace function match_book_knowledge (
      query_embedding vector(1536),
      match_threshold float,
      match_count int,
      filter_book_id uuid
    )
    returns table (
      id bigint,
      content text,
      similarity float
    )
    language plpgsql
    as $$
    begin
      return query
      select
        book_knowledge.id,
        book_knowledge.content,
        1 - (book_knowledge.embedding <=> query_embedding) as similarity
      from book_knowledge
      where 1 - (book_knowledge.embedding <=> query_embedding) > match_threshold
      and book_knowledge.book_id = filter_book_id
      order by book_knowledge.embedding <=> query_embedding
      limit match_count;
    end;
    $$;
    """
    session.exec(text(sql))
    session.commit()
    print("RPC Function Updated!")

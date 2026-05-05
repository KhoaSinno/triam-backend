
      SELECT
        book_knowledge.id,
        book_knowledge.book_id,
        book_knowledge.chapter_id,
        book_knowledge.chunk_index,
        book_knowledge.content,
        1 - (book_knowledge.embedding <=> query_embedding) AS similarity
      FROM book_knowledge
      WHERE 1 - (book_knowledge.embedding <=> query_embedding) > match_threshold
        AND book_knowledge.book_id = ANY(filter_book_ids)
      ORDER BY book_knowledge.embedding <=> query_embedding
      LIMIT match_count;
    




    ///


    -- 4. Viết hàm RPC (Remote Procedure Call) để search vector
-- Hàm này giúp bạn gọi từ code Python/Flutter chỉ bằng 1 dòng
drop function if exists match_book_knowledge(vector, float, int, uuid[]);

create or replace function match_book_knowledge (
  query_embedding vector(1536),
  match_threshold float,
  match_count int,
  filter_book_ids uuid[]
)
returns table (
  id integer,
  book_id uuid,
  chapter_id uuid,
  chunk_index integer,
  content text,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    book_knowledge.id,
    book_knowledge.book_id,
    book_knowledge.chapter_id,
    book_knowledge.chunk_index,
    book_knowledge.content,
    1 - (book_knowledge.embedding <=> query_embedding) as similarity
  from book_knowledge
  where 1 - (book_knowledge.embedding <=> query_embedding) > match_threshold
  and book_knowledge.book_id = ANY(filter_book_ids)
  order by book_knowledge.embedding <=> query_embedding
  limit match_count;
end;
$$;

import os
import sys
from sqlalchemy import text

# Thêm root path vào SYS_PATH để nhận diện được module "app"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import engine

SQL_RESTORE_GRANTS = """
-- 1. Cấp quyền usage trên schema public cho các role của Supabase
grant usage on schema public to postgres, anon, authenticated, service_role, authenticator;

-- 2. Cấp toàn quyền trên các bảng, sequence, function hiện tại cho postgres và service_role
grant all privileges on all tables in schema public to postgres, service_role;
grant all privileges on all sequences in schema public to postgres, service_role;
grant all privileges on all functions in schema public to postgres, service_role;

-- 3. Cấp quyền cơ bản cho authenticated và anon trên các bảng/sequence hiện tại
grant select, insert, update, delete on all tables in schema public to authenticated;
grant select, insert, update, delete on all tables in schema public to anon;
grant usage, select on all sequences in schema public to authenticated;
grant usage, select on all sequences in schema public to anon;

-- 4. Thiết lập default privileges để các bảng tạo mới trong tương lai tự động thừa hưởng quyền
alter default privileges in schema public grant all on tables to postgres, service_role;
alter default privileges in schema public grant all on sequences to postgres, service_role;
alter default privileges in schema public grant all on functions to postgres, service_role;

alter default privileges in schema public grant select, insert, update, delete on tables to authenticated;
alter default privileges in schema public grant select, insert, update, delete on tables to anon;
alter default privileges in schema public grant usage, select on sequences to authenticated;
alter default privileges in schema public grant usage, select on sequences to anon;
"""

SQL_GET_BOOK_ASSET_PATHS = """
create or replace function public.get_book_asset_paths(
  bucket_names text[],
  book_id_prefix text
)
returns table(bucket_id text, name text)
language sql
security definer
as $$
  select o.bucket_id, o.name
  from storage.objects o
  where o.bucket_id = any(bucket_names)
    and o.name like book_id_prefix || '/%';
$$;
"""

SQL_MATCH_BOOK_KNOWLEDGE = """
create or replace function public.match_book_knowledge(
  query_embedding vector(1536),
  match_threshold float,
  match_count int,
  filter_book_ids uuid[]
)
returns table(
  id integer,
  book_id uuid,
  learning_unit_id uuid,
  chunk_index integer,
  content text,
  similarity float
)
language sql stable
as $$
  select
    book_knowledge.id,
    book_knowledge.book_id,
    book_knowledge.learning_unit_id,
    book_knowledge.chunk_index,
    book_knowledge.content,
    1 - (book_knowledge.embedding <=> query_embedding) as similarity
  from book_knowledge
  where book_knowledge.embedding is not null
    and book_knowledge.learning_unit_id is not null
    and 1 - (book_knowledge.embedding <=> query_embedding) > match_threshold
    and book_knowledge.book_id = any(filter_book_ids)
  order by book_knowledge.embedding <=> query_embedding
  limit match_count;
$$;
"""

def recreate_rpcs():
    print("🔄 Đang kết nối database để thiết lập lại quyền (grants) và khôi phục RPCs...")
    try:
        with engine.begin() as conn:
            print("Restoring standard Supabase role permissions (grants)...")
            conn.execute(text(SQL_RESTORE_GRANTS))
            print("✅ Đã thiết lập xong quyền (grants).")

            print("Creating/Replacing get_book_asset_paths...")
            conn.execute(text(SQL_GET_BOOK_ASSET_PATHS))
            print("✅ Tạo thành công: get_book_asset_paths")

            print("Creating/Replacing match_book_knowledge...")
            conn.execute(text(SQL_MATCH_BOOK_KNOWLEDGE))
            print("✅ Tạo thành công: match_book_knowledge")

            print("🎉 Khôi phục tất cả quyền và RPCs thành công!")
    except Exception as e:
        print("❌ Lỗi khi khởi tạo RPCs/grants:")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    recreate_rpcs()

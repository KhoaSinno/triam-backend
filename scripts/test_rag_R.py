from sqlmodel import create_engine, Session, select
from app.core.config import settings
from app.models.db_models import Book, BookKnowledge
from openai import OpenAI

def test_rag():
    engine = create_engine(settings.DATABASE_URL)
    with Session(engine) as session:
        # Get a book that has knowledge
        bk = session.exec(select(BookKnowledge).limit(1)).first()
        if not bk:
            print('No book knowledge found in DB.')
            return
            
        book_id = bk.book_id
        print(f'Testing against book {book_id}')
        
        from app.core.supabase import supabase
        ai = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Test query
        print('Creating embedding...')
        res = ai.embeddings.create(model='text-embedding-3-small', input=['nội dung chính'])
        query_vector = res.data[0].embedding
        
        print('Calling RPC match_book_knowledge...')
        try:
            result = supabase.rpc('match_book_knowledge', {
                'query_embedding': query_vector,
                'match_threshold': 0.1,
                'match_count': 3,
                'filter_book_id': str(book_id)
            }).execute()
            
            print(f'RPC Success! Returned {len(result.data)} rows.')
            if result.data:
                for row in result.data:
                    print(f"- chunk_index: {row.get('chunk_index')}, similarity: {row.get('similarity')}")
        except Exception as e:
            print(f'RPC Error: {e}')

test_rag()

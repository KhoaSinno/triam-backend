import os
from dotenv import load_dotenv
from app.core.config import settings
from supabase import create_client, Client
load_dotenv()

url: str = settings.SUPABASE_URL
key: str = settings.SUPABASE_KEY

supabase: Client = create_client(url, key)

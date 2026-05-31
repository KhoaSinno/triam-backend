import os
import redis
from dotenv import load_dotenv

load_dotenv()

redis_url = os.getenv("CELERY_BROKER_URL")
print(f"Connecting to Redis at: {redis_url}")

try:
    r = redis.Redis.from_url(redis_url)
    info = r.info("clients")
    print("Redis Client Info:")
    print(info)
    
    # Try to list clients
    clients = r.client_list()
    print(f"\nTotal active clients: {len(clients)}")
    for client in clients:
        print(f"id={client.get('id')} addr={client.get('addr')} name={client.get('name')} cmd={client.get('cmd')} idle={client.get('idle')}")
except Exception as e:
    print(f"Error: {e}")

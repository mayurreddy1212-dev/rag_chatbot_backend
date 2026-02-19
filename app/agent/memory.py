import redis
import json
from app.config import REDIS_URL

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def get_memory(session_id: str):
    data = r.get(f"memory:{session_id}")
    return json.loads(data) if data else []

def save_memory(session_id: str, messages):
    r.set(f"memory:{session_id}", json.dumps(messages))

import redis
from config import REDIS_URL
import hashlib

r: redis.Redis = redis.Redis.from_url(REDIS_URL)

def cache_key(url: str) -> str:
    return "cache:" + hashlib.sha256(url.encode()).hexdigest()

def get_cached_response(url: str) -> bytes | None:
    return r.get(cache_key(url)) # type: ignore

def set_cached_response(url: str, content: bytes, ttl: int = 60) -> None:
    r.setex(cache_key(url), ttl, content)


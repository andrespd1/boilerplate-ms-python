import os
import redis
import pickle
from typing import Any, Optional


REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

redis_client = None


def init_redis():
    """Initialize Redis client (if not already). Optionally ping here."""
    global redis_client
    if redis_client is None:
        redis_client = redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD
        )
        try:
            redis_client.ping()
            print("Connected to Redis")
        except redis.exceptions.RedisError as e:
            print(f"Redis connection error: {e}")
    return redis_client


def set_cache(key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
    """
    Set a string value in Redis.
    If ttl_seconds is provided, it sets an expiration time.
    """
    pickled_data = pickle.dumps(value)
    if ttl_seconds is not None:
        redis_client.setex(key, ttl_seconds, pickled_data)
    else:
        redis_client.set(key, pickled_data)
    return value


def get_cache(key: str) -> Optional[Any]:
    """
    Retrieve a string value from Redis.
    Returns None if the key doesn't exist.
    """
    serialized_data = redis_client.get(key)
    if serialized_data:
        return pickle.loads(serialized_data)
    return False


def delete_cache(key: str) -> int:
    """
    Delete a key from Redis.
    Returns the number of keys that were removed (0 or 1).
    """
    return redis_client.delete(key)


def get_and_set_cache(key: str, func: callable, ttl_seconds: Optional[int] = None):
    data = get_cache(key)
    if not data:
        return set_cache(key, func(), ttl_seconds)
    return data

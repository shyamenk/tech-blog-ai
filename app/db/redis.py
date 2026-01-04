"""Redis connection management and caching utilities."""

from typing import Optional, Any, Callable
from functools import wraps
import json
import hashlib

import redis.asyncio as redis
from redis.asyncio import Redis

from app.config import get_settings


# Cache TTL constants (in seconds)
CACHE_TTL_SHORT = 300  # 5 minutes
CACHE_TTL_MEDIUM = 1800  # 30 minutes
CACHE_TTL_LONG = 3600  # 1 hour
CACHE_TTL_DAY = 86400  # 24 hours


class RedisClient:
    """Redis client manager."""

    _client: Optional[Redis] = None

    @classmethod
    async def create_client(cls) -> Redis:
        """Create the Redis client."""
        if cls._client is None:
            settings = get_settings()
            cls._client = redis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True,
            )
        return cls._client

    @classmethod
    async def close_client(cls) -> None:
        """Close the Redis client."""
        if cls._client:
            await cls._client.close()
            cls._client = None

    @classmethod
    async def get_client(cls) -> Redis:
        """Get the Redis client, creating it if necessary."""
        if cls._client is None:
            await cls.create_client()
        return cls._client


async def get_redis_client() -> Redis:
    """Dependency to get the Redis client."""
    return await RedisClient.get_client()


async def cache_get(key: str) -> Optional[Any]:
    """Get a value from cache."""
    client = await RedisClient.get_client()
    value = await client.get(key)
    if value:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return None


async def cache_set(key: str, value: Any, ttl: int = 3600) -> bool:
    """Set a value in cache with TTL in seconds."""
    client = await RedisClient.get_client()
    if isinstance(value, (dict, list)):
        value = json.dumps(value)
    return await client.set(key, value, ex=ttl)


async def cache_delete(key: str) -> int:
    """Delete a key from cache."""
    client = await RedisClient.get_client()
    return await client.delete(key)


async def cache_exists(key: str) -> bool:
    """Check if a key exists in cache."""
    client = await RedisClient.get_client()
    return await client.exists(key) > 0


def generate_cache_key(prefix: str, *args, **kwargs) -> str:
    """Generate a cache key from prefix and arguments."""
    key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
    key_hash = hashlib.md5(key_data.encode()).hexdigest()[:16]
    return f"{prefix}:{key_hash}"


def cached(prefix: str, ttl: int = CACHE_TTL_MEDIUM, skip_cache: bool = False):
    """
    Decorator to cache async function results in Redis.

    Usage:
        @cached("llm_response", ttl=CACHE_TTL_LONG)
        async def generate_text(prompt: str) -> str:
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Skip cache if requested
            if skip_cache or kwargs.pop("skip_cache", False):
                return await func(*args, **kwargs)

            # Generate cache key
            cache_key = generate_cache_key(prefix, *args, **kwargs)

            try:
                # Try to get from cache
                cached_value = await cache_get(cache_key)
                if cached_value is not None:
                    return cached_value
            except Exception:
                # If Redis fails, just run the function
                pass

            # Execute function
            result = await func(*args, **kwargs)

            try:
                # Store in cache
                await cache_set(cache_key, result, ttl=ttl)
            except Exception:
                # If Redis fails, still return the result
                pass

            return result
        return wrapper
    return decorator


async def increment_rate_limit(key: str, window_seconds: int = 60) -> int:
    """Increment rate limit counter and return current count."""
    client = await RedisClient.get_client()
    pipe = client.pipeline()
    pipe.incr(key)
    pipe.expire(key, window_seconds)
    results = await pipe.execute()
    return results[0]


async def check_rate_limit(key: str, limit: int, window_seconds: int = 60) -> tuple[bool, int]:
    """
    Check if rate limit is exceeded.
    Returns (is_allowed, current_count).
    """
    current = await increment_rate_limit(key, window_seconds)
    return current <= limit, current


async def get_rate_limit_remaining(key: str, limit: int) -> int:
    """Get remaining requests in rate limit window."""
    client = await RedisClient.get_client()
    current = await client.get(key)
    if current is None:
        return limit
    return max(0, limit - int(current))

"""Redis connection management."""

from typing import Optional, Any
import json

import redis.asyncio as redis
from redis.asyncio import Redis

from app.config import get_settings


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

"""PostgreSQL database connection management."""

from typing import Optional
from contextlib import asynccontextmanager

import asyncpg
from asyncpg import Pool, Connection

from app.config import get_settings


class PostgresPool:
    """PostgreSQL connection pool manager."""

    _pool: Optional[Pool] = None

    @classmethod
    async def create_pool(cls) -> Pool:
        """Create the connection pool."""
        if cls._pool is None:
            settings = get_settings()
            cls._pool = await asyncpg.create_pool(
                dsn=settings.database_url,
                min_size=5,
                max_size=20,
                command_timeout=60,
            )
        return cls._pool

    @classmethod
    async def close_pool(cls) -> None:
        """Close the connection pool."""
        if cls._pool:
            await cls._pool.close()
            cls._pool = None

    @classmethod
    async def get_pool(cls) -> Pool:
        """Get the connection pool, creating it if necessary."""
        if cls._pool is None:
            await cls.create_pool()
        return cls._pool

    @classmethod
    @asynccontextmanager
    async def connection(cls):
        """Get a connection from the pool."""
        pool = await cls.get_pool()
        async with pool.acquire() as conn:
            yield conn

    @classmethod
    @asynccontextmanager
    async def transaction(cls):
        """Get a connection with a transaction."""
        async with cls.connection() as conn:
            async with conn.transaction():
                yield conn


async def get_postgres_pool() -> Pool:
    """Dependency to get the PostgreSQL pool."""
    return await PostgresPool.get_pool()


async def execute_query(query: str, *args) -> str:
    """Execute a query and return the status."""
    async with PostgresPool.connection() as conn:
        return await conn.execute(query, *args)


async def fetch_one(query: str, *args) -> Optional[asyncpg.Record]:
    """Fetch a single row."""
    async with PostgresPool.connection() as conn:
        return await conn.fetchrow(query, *args)


async def fetch_all(query: str, *args) -> list[asyncpg.Record]:
    """Fetch all rows."""
    async with PostgresPool.connection() as conn:
        return await conn.fetch(query, *args)

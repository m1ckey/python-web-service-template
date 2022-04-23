import asyncio
from typing import Optional

import asyncpg

from config import Config
from .ping import handle_ping


class DB:
    pool: Optional[asyncpg.pool.Pool] = None

    @classmethod
    async def connect(cls):
        if cls.pool is not None:
            return
        cls.pool = await asyncpg.create_pool(
            user=Config.db.user,
            password=Config.db.password,
            host=Config.db.host,
            port=Config.db.port,
            database=Config.db.database
        )
        await cls.ping()

    @classmethod
    async def disconnect(cls):
        if cls.pool is None:
            return
        await asyncio.wait_for(cls.pool.close(), timeout=10)
        cls.pool = None

    @classmethod
    async def ping(cls) -> str:
        async with cls.pool.acquire() as con:
            return await handle_ping(con)

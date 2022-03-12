import asyncio
from typing import Optional

import asyncpg

from config import config


class DB:
    pool: Optional[asyncpg.pool.Pool] = None

    @classmethod
    async def connect(cls):
        cls.pool = await asyncpg.create_pool(user=config.db.user,
                                             password=config.db.password,
                                             host=config.db.host,
                                             port=config.db.port,
                                             database=config.db.database)
        await cls.ping()

    @classmethod
    async def disconnect(cls):
        await asyncio.wait_for(cls.pool.close(), timeout=10)
        cls.pool = None

    @classmethod
    async def ping(cls) -> str:
        return await cls.pool.fetchval("SELECT 'pong'")

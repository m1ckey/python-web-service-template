import asyncio
from typing import Optional

import asyncpg

from config import conf


class DB:
    pool: Optional[asyncpg.pool.Pool] = None

    @classmethod
    async def connect(cls):
        cls.pool = await asyncpg.create_pool(user=conf.db_user,
                                             password=conf.db_password,
                                             host=conf.db_host,
                                             port=conf.db_port,
                                             database=conf.db_database)
        await cls.ping()

    @classmethod
    async def disconnect(cls):
        await asyncio.wait_for(cls.pool.close(), timeout=10)
        cls.pool = None

    @classmethod
    async def ping(cls) -> str:
        return await cls.pool.fetchval("SELECT 'pong'")

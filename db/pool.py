import asyncio
import functools
from typing import Optional

import asyncpg
from asyncpg import Pool

from config import config

pool: Optional[Pool] = None


async def connect():
    global pool
    pool = await asyncpg.create_pool(
        user=config.db.user,
        password=config.db.password,
        host=config.db.host,
        port=config.db.port,
        database=config.db.database
    )
    await pool.fetchval("SELECT 'pong'")


async def disconnect():
    global pool
    await asyncio.wait_for(pool.close(), timeout=10)
    pool = None


def acquire_connection(f):
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        async with pool.acquire() as con:
            return await f(con, *args, **kwargs)

    return wrapper

from asyncpg import Connection

from .pool import acquire_connection


@acquire_connection
async def ping(con: Connection) -> str:
    return await con.fetchval("SELECT 'pong'")
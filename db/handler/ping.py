from asyncpg import Connection


async def handle_ping(con: Connection) -> str:
    return await con.fetchval("SELECT 'pong'")

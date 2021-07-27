from starlette.requests import Request
from starlette.responses import PlainTextResponse

from database import DB


async def ping(request: Request):
    return PlainTextResponse(await DB.ping())

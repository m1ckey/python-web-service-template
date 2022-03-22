from starlette.requests import Request
from starlette.responses import PlainTextResponse

import db


async def ping(request: Request):
    return PlainTextResponse(await db.ping())

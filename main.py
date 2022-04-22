import uvicorn
from starlette.applications import Starlette

import db
import server
from config import Environment, config

app = Starlette(
    debug=config.env != Environment.PROD,
    routes=server.routes,
    middleware=server.middleware,
    on_startup=[db.connect],
    on_shutdown=[db.disconnect]
)

if __name__ == '__main__':
    uvicorn.run('main:app')

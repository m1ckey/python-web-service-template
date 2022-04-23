import uvicorn
from starlette.applications import Starlette

from config import Environment, config
from db import DB
from server import routes, middleware

app = Starlette(
    debug=config.env != Environment.PROD,
    routes=routes,
    middleware=middleware,
    on_startup=[DB.connect],
    on_shutdown=[DB.disconnect]
)

if __name__ == '__main__':
    uvicorn.run('main:app')

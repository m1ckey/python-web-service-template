import uvicorn
from starlette.applications import Starlette

from config import Environment, Config
from db import DB
from server import routes, middleware

app = Starlette(
    debug=Config.env != Environment.PROD,
    routes=routes,
    middleware=middleware,
    on_startup=[DB.connect],
    on_shutdown=[DB.disconnect]
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=Config.server.port,
        access_log=Config.env != Environment.PROD
    )

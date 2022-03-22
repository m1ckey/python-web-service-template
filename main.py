import uvicorn
from starlette.applications import Starlette

from config import config
import db
from config import Environment
from server import routes, middleware

app = Starlette(
    debug=config.env != Environment.PROD,
    routes=routes,
    middleware=middleware,
    on_startup=[db.connect],
    on_shutdown=[db.disconnect]
)

if __name__ == '__main__':
    uvicorn.run('main:app')

import uvicorn
from starlette.applications import Starlette

from config import conf, ConfigProfile, logger
from database import DB
from server import routes, middleware

app = Starlette(debug=conf.profile != ConfigProfile.PROD,
                routes=routes,
                middleware=middleware,
                on_startup=[DB.connect],
                on_shutdown=[DB.disconnect])

if __name__ == '__main__':
    if conf.profile == ConfigProfile.PROD:
        logger.warn('starting production programmatically')
    uvicorn.run('main:app')

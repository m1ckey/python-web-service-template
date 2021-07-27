import uvicorn
from starlette.applications import Starlette

from config import conf, ConfigProfile
from database import DB
from server import routes, middleware

app = Starlette(debug=conf.profile != ConfigProfile.PROD,
                routes=routes,
                middleware=middleware,
                on_startup=[DB.connect],
                on_shutdown=[DB.disconnect])

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0',
                port=conf.server_port,
                log_level='warning' if conf.profile == ConfigProfile.PROD else 'info')

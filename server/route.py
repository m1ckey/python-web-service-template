from starlette.routing import Route, Mount

from .graphql import app
from .ping import ping

routes = [
    Mount('/api', routes=[
        Mount('/v1', routes=[
            Route('/ping', ping),
            Route('/graphql', app),
        ]),
    ]),
]

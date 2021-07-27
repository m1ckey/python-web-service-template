from starlette.routing import Route, Mount

from .handler.ping import ping

routes = [
    Mount('/api', routes=[
        Mount('/v1', routes=[
            Route('/ping', ping),
        ]),
    ]),
]

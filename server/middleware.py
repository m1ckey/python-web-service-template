from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from .auth import JWTAuth

middleware = [
    Middleware(AuthenticationMiddleware, backend=JWTAuth())
]

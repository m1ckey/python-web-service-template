from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware

from .auth import JWTAuth

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*']),  # todo
    Middleware(AuthenticationMiddleware, backend=JWTAuth()),
]

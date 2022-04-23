from enum import Enum

import jwt
from jwt import InvalidTokenError
from starlette import status
from starlette.authentication import AuthenticationBackend, AuthenticationError, AuthCredentials, SimpleUser
from starlette.exceptions import HTTPException
from starlette.requests import Request

from config import Config


class AuthScope(Enum):
    ADMIN = 1


class JWTAuth(AuthenticationBackend):
    async def authenticate(self, request: Request):
        if 'authorization' not in request.headers:
            return

        try:
            scheme, token = request.headers['authorization'].split()
            if scheme.lower() != 'bearer':
                raise ValueError()

            payload = jwt.decode(
                jwt=token,
                key=Config.server.jwt_key,
                algorithms='HS256'
            )
        except (ValueError, InvalidTokenError):
            raise AuthenticationError('illegal auth')

        user_id = payload['sub']
        return AuthCredentials([AuthScope.ADMIN.name]), SimpleUser(user_id)


def require_scope(request: Request, scope: AuthScope):
    if scope.name not in request.auth.scopes:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'requires "{scope.name}" scope')

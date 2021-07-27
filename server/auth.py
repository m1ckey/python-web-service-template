from enum import Enum

import jwt
from jwt import InvalidTokenError
from starlette import status
from starlette.authentication import AuthenticationBackend, AuthenticationError, AuthCredentials, SimpleUser
from starlette.exceptions import HTTPException
from starlette.requests import Request

from config import conf


class Scope(Enum):
    ADMIN = 1


class JWTAuth(AuthenticationBackend):
    async def authenticate(self, request: Request):
        if "Authorization" not in request.headers:
            return

        try:
            scheme, token = request.headers["Authorization"].split()
            if scheme.lower() != 'bearer':
                raise ValueError()

            payload = jwt.decode(jwt=token,
                                 key=conf.server_jwt_key,
                                 algorithms='HS256')
        except (ValueError, InvalidTokenError) as e:
            raise AuthenticationError('illegal auth')

        user_id = payload['sub']
        return AuthCredentials([Scope.USER.name]), SimpleUser(user_id)


def require_scope(request: Request, scope: Scope):
    if scope.name not in request.auth.scopes:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'requires "{scope.INSTALLED_APP.name}" scope')

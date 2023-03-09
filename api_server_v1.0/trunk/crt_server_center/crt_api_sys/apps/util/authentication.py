import jwt

from datetime import datetime, timedelta
from sanic import text
from functools import wraps

from .err_code import ErrorCode

ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def create_access_token(data: dict, expires_delta: timedelta = None, secret: str = None):
    """
    创建token
    :param data:
    :param expires_delta:
    :param secret:  加盐
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=ALGORITHM)
    return encoded_jwt


def check_token(request):
    if not request.token:
        return False, ErrorCode.AUTH_ERR_TOKEN_INVALID

    try:
        payload = jwt.decode(request.token, request.app.config.SECRET, algorithms=[ALGORITHM])

        # 检查token是否过期
        # if payload.get('exp') < int(time.time()):
        #     return ErrorCode.AUTH_ERR_TOKEN_EXPIRE

    except jwt.exceptions.ExpiredSignatureError:
        # token 过期
        return False, ErrorCode.AUTH_ERR_TOKEN_EXPIRE

    except jwt.exceptions.InvalidTokenError:
        # token无效（被修改）
        return False, ErrorCode.AUTH_ERR_TOKEN_INVALID

    else:
        return True, payload


def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = check_token(request)

            if is_authenticated:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return text("You are unauthorized.", 401)

        return decorated_function

    return decorator(wrapped)

import os
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address


def get_rate_limit_key(request: Request):
    """    
    1. If there is an authenticated user → limit by user.id
    2. If not → limit by IP
    """
    try:
        user = getattr(request.state, "user", None)

        if user and hasattr(user, "id"):
            return f"user:{user.id}"

        return get_remote_address(request)

    except Exception:
        return get_remote_address(request)


redis_url = os.getenv("REDIS_URL")

if not redis_url:
    raise ValueError("REDIS_URL is not configured")

limiter = Limiter(
    key_func=get_rate_limit_key,
    #storage_uri=redis_url,
    default_limits=["100/minute"]
)
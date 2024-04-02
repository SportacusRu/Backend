from http.client import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, status
from src.app.config.config import MODERATOR_KEY


class BlockMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        return response
        #raise HTTPException(
        #    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        #    detail="User is blocked"
        #)
        

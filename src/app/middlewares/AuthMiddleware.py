from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


class AuthMiddleware(BaseHTTPMiddleware):
    async def __call__(self, request: Request, call_next): pass
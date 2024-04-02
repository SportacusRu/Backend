from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Response, Request, status
from src.app.config.config import MODERATOR_KEY


class ModeratorAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if "moderator_key" in request.query_params.keys():
            key = request.query_params.get("moderator_key")
            if key != MODERATOR_KEY:   
                return Response(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
        response = await call_next(request)
        return response
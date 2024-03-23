from fastapi import APIRouter

from src.app.api.routes import auth, places, reviews, user

api_router = APIRouter()
api_router.include_router(auth.router, tags=["login"])
api_router.include_router(places.router, prefix="/places", tags=["users"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["utils"])
api_router.include_router(user.router, prefix="/user", tags=["items"])
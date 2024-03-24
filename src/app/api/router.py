from fastapi import APIRouter

from src.app.api.routes import auth, places, reviews, user, moderate

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(places.router, prefix="/places", tags=["places"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(moderate.router, prefix="/moderate", tags=["Moderate"])

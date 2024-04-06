import json
from typing import Any
from fastapi import APIRouter, Response
from src.database import Database

router = APIRouter()


@router.get("/get", description="Get list of places")
async def get():
    places = await Database.places.get_all()
    return json.dumps(places)


@router.get("/getById", description="Get information about place")
async def get_by_id(place_id: int):
    current_place = Database.places.find_by_id(place_id)
    return json.dumps(current_place)


@router.get("/getRecommendedPlace", description="Get recommended place")
async def get_recommended_place() -> Any: 
    return ""


@router.post("/add", description="Add a new place")
async def add() -> Any: 
    return ""


@router.post("/remove", description="remove place (special method)")
async def remove(moderator_key: str, place_id):
    await Database.places.remove(place_id)
    return Response(status_code=200)


@router.post("/edit", description="edit place (special method)")
async def edit(moderator_key: str, place_id: int, title=None, description=None, category=None, filters=None):
    await Database.places.update(place_id, title, description, category, filters)
    return Response(status_code=200)


@router.post("/like", description="Add place in user liked list")
async def like():
    return ""


@router.post("/dislike", description="Remove place from user liked list")
async def dislike() -> Any: 
    return ""

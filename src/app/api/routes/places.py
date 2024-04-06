import json
from typing import Any
from fastapi import APIRouter, HTTPException, status, Response
from src.database.controllers import PlacesController

router = APIRouter()


@router.get("/get", description="Get list of places")
async def get():
    places = await PlacesController.get_all()
    return json.dumps(places)


@router.get("/getById", description="Get information about place")
async def get_by_id(place_id: int):
    current_place = PlacesController.find_by_id(place_id)
    return json.dumps(current_place)


@router.get("/getRecommendedPlace", description="Get recommended place")
async def get_recommended_place() -> Any: 
    return ""


@router.post("/add", description="Add a new place")
async def add() -> Any: 
    return ""


@router.post("/remove", description="remove place (special method)")
async def remove(moderator_key, place_id):
    if moderator_key:  # todo: find moderator key
        await PlacesController.remove(place_id)
        return Response(status_code=200)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Access denied"
        )


@router.post("/edit", description="edit place (special method)")
async def edit(moderator_key, place_id, title=None, description=None, category=None, filters=None):
    if moderator_key:  # todo: find moderator key
        place = await PlacesController.find_by_id(place_id)

        if title is not None:
            place.title = title
        if description is not None:
            place.description = description
        if category is not None:
            place.category = category
        if filters is not None:
            place.filters_list = filters

        return Response(status_code=200)

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Access denied"
        )


@router.post("/like", description="Get user's report")
async def get(moderator_key):
    if moderator_key:  # todo: find moderator key
        ...
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Access denied"
        )


@router.post("/like", description="Add place in user liked list")
async def like():
    return ""


@router.post("/dislike", description="Remove place from user liked list")
async def dislike() -> Any: 
    return ""

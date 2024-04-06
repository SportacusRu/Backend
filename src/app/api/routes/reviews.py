import json
from typing import Any
from fastapi import APIRouter
from src.database.controllers import PlacesController

router = APIRouter()


@router.get("/getByPlaceId", description="Get reviews by place_id")
async def get_by_place_id(place_id: int):
    current_place = await PlacesController.find_by_id(place_id)
    reviews = current_place.reviews_list
    return json.dumps(reviews)


@router.get("/getByUser", description="Get all user reviews")
async def get_by_user():
    return ""


@router.post("/add", description="Add a new review")
async def add_review() -> Any: 
    return ""


@router.post("/remove", description="Remove a review")
async def remove_review() -> Any: 
    return ""


from typing import Any
from fastapi import APIRouter


router = APIRouter()


@router.get("/getByPlaceId", description="Get reviews by place_id")
async def getByPlaceId():
    return ""

@router.get("/getByUser", description="Get all user reviews")
async def getByUser():
    return ""
    
@router.post("/add", description="Add a new review")
async def add_review() -> Any: 
    return ""
    
@router.post("/remove", description="Remove a review")
async def remove_review() -> Any: 
    return ""


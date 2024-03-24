from typing import Any
from fastapi import APIRouter


router = APIRouter()


@router.get("/getByPlaceId", description="Get reviews by place_id")
def getByPlaceId():
    return ""

@router.get("/getByUser", description="Get all user reviews")
def getByUser():
    return ""
    
@router.post("/add", description="Add a new review")
def add_review() -> Any: 
    return ""
    
@router.post("/remove", description="Remove a review")
def remove_review() -> Any: 
    return ""


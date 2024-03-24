from typing import Any
from fastapi import APIRouter


router = APIRouter()


@router.get("/get", description="Get list of places")
def get() -> Any: 
    return ""

@router.get("/getById", description="Get information about place")
def get_by_id() -> Any: 
    return ""

@router.get("/getRecommendedPlace", description="Get recomended place")
def get_recommended_place() -> Any: 
    return ""

@router.post("/add", description="Add a new place")
def add() -> Any: 
    return ""

@router.post("/remove", description="remove place (special method)")
def remove() -> Any: 
    return ""

@router.post("/like", description="Add place in user liked list")
def like() -> Any: 
    return ""

@router.post("/dislike", description="Remove place from user liked list")
def dislike() -> Any: 
    return ""
from typing import Any
from fastapi import APIRouter


router = APIRouter()


@router.get("/get", description="Get list of places")
async def get() -> Any: 
    return ""

@router.get("/getById", description="Get information about place")
async def get_by_id() -> Any: 
    return ""

@router.get("/getRecommendedPlace", description="Get recommended place")
async def get_recommended_place() -> Any: 
    return ""

@router.post("/add", description="Add a new place")
async def add() -> Any: 
    return ""

@router.post("/remove", description="remove place (special method)")
async def remove() -> Any: 
    return ""

@router.post("/edit", description="edit place (special method)")
async def edit() -> Any: 
    return ""

@router.post("/like", description="Add place in user liked list")
async def like() -> Any: 
    return ""

@router.post("/dislike", description="Remove place from user liked list")
async def dislike() -> Any: 
    return ""
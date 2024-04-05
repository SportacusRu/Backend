from typing import Any
from fastapi import APIRouter


router = APIRouter()


@router.get("/get", description="Get information about user")
async def get() -> Any: 
    return ""

@router.post("/updatePhoto", description="Update photo of user")
async def update_photo() -> Any: 
    return ""

@router.post("/updateName", description="Update name of user")
async def update_name() -> Any: 
    return ""

@router.post("/updatePassword", description="Create a request of update password")
async def update_password() -> Any: 
    return ""

@router.post("/setNewPassword", description="Update password of user")
async def set_new_password():
    return ""

@router.post("/ban", description="Ban user (special method)")
async def ban() -> Any: 
    return ""
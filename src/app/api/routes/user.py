from typing import Any
from fastapi import APIRouter


router = APIRouter()


@router.get("/get", description="Get information about user")
def get() -> Any: 
    return ""

@router.post("/updatePhoto", description="Update photo of user")
def update_photo() -> Any: 
    return ""

@router.post("/updateName", description="Update name of user")
def update_name() -> Any: 
    return ""

@router.post("/updatePassword", description="Update password of user")
def update_password() -> Any: 
    return ""

@router.post("/ban", description="Ban user (special method)")
def update_password() -> Any: 
    return ""
from typing import Any
from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def create_review() -> Any: 
    return ""

@router.get("/")
def get() -> Any: 
    return ""
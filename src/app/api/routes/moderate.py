from typing import Any
from fastapi import APIRouter


router = APIRouter()


@router.get("/get", description="Get all complaint (special method)")
def get() -> Any:
    return ""

@router.post("/add", description="Add a new complaint")
def add() -> Any:
    return ""

@router.post("/report", description="Create a report (special method)")
def report() -> Any:
    return ""
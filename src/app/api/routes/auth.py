from typing import Any
from fastapi import APIRouter

router = APIRouter()


@router.post("/register", description="Register a new user")
def register() -> Any: 
    return ""

@router.post("/login", description="Authorizes the user")
def login() -> Any: 
    return ""

@router.post("/validateCodeConfirm", description="Validate a code")
def validate_code_confirm() -> Any: 
    return ""

@router.post("/repeatCodeConfirm", description="Repeat a code")
def repeat_code_confirm() -> Any: 
    return ""
from typing import Any
from fastapi import APIRouter

router = APIRouter()

users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

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
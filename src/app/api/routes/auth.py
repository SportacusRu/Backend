
from typing import Any
from fastapi import APIRouter, HTTPException

from src.app.config.config import VERIFY_ENDPOINT
from src.app.email.email import EmailSender
from src.database import Database

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
async def register(name:str, email: str, password: str) -> Any: 
    user = await Database.users.find_by_email(email)

    if user is not None and user.auth_key is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    elif user is not None:
        await Database.users.remove(user.user_id)
    
    user = await Database.users.add(name, email, password)
    EmailSender.send_verification_code(email, VERIFY_ENDPOINT + user.verify_link)
    
    return Token()
    

@router.post("/login", description="Authorizes the user")
def login() -> Any: 
    return ""

@router.post("/validateCodeConfirm", description="Validate a code")
def validate_code_confirm() -> Any: 
    return ""

@router.post("/repeatCodeConfirm", description="Repeat a code")
def repeat_code_confirm() -> Any: 
    return ""

from random import randint
from typing import Any
from fastapi import APIRouter, HTTPException, Response, status, Request

from src.app.email import EmailSender
from src.database import Database

from bcrypt import checkpw

router = APIRouter()


@router.post("/register", description="Register a new user")
async def register(name:str, email: str, password: str) -> Any: 
    user = await Database.users.find_by_email(email)

    if user is not None and user.auth_key is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    elif user is not None:
        await Database.users.remove(user.user_id)
    
    user = await Database.users.add(name, password, email)
    await EmailSender.send_verification_code(email, user.email_code)
    
    return Response(status_code=200, headers={
        "Set-Cookie": f"auth_key={user.auth_key}; path=/; httponly"
    })
    

@router.post("/login", description="Authorizes the user")
async def login(email: str, password: str) -> Any: 
    user = await Database.users.find_by_email(email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    if not checkpw(password.encode(), user.password.encode()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    if user.auth_key is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not verified"
        )
    
    return Token()

@router.post("/validateCodeConfirm", description="Validate a code")
async def validate_code_confirm(request: Request, email: str, code: int) -> Any: 
    user = await Database.users.find_by_email(email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )

    if user.email_code is not None and user.email_code != code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong code"
        )
    elif user.email_code is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code already sent"
        )
    elif user.email_code is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code not found"
        )
    
    if user.email_code == code and user.auth_key == request.cookies.get("auth_key"):
        user.auth_key = None
        user.email_code = None
        await user.save()

    return Token()

@router.post("/repeatCodeConfirm", description="Repeat a code")
async def repeat_code_confirm(request: Request, email: str) -> Any: 
    auth_key = request.cookies.get("auth_key")
    user = await Database.users.find_by_email(email)

    if user is None: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
    
    if auth_key is None and user.auth_key != auth_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Auth key not found or expired"
        )
    
    if user.email_code is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code not found"
        )
    
    user.email_code = randint(1000, 9999)
    await user.save()
    await EmailSender.send_verification_code(email, user.email_code)
    return Response(status_code=200)
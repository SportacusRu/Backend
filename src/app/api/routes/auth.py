from random import randint
from typing import Any
from typing_extensions import Annotated
from fastapi import APIRouter, HTTPException, Response, status, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from bcrypt import checkpw

from src.app.api.models.tokens import Token
from src.app.email import EmailSender
from src.database import Database
from src.app.api.extensions.tokens import create_token
from src.app.api.extensions.validate import validate_email, validate_name, validate_password

router = APIRouter()

@router.post("/register", description="Register a new user")
async def register(name: str, email: str, password: str) -> Any:
    valid_check = validate_name(name) and validate_email(email) and validate_password(password)
    if not(valid_check):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="No valid fields: name, email or password"
        )
    user = await Database.users.find_by_email(email)

    if user is not None and user.auth_key is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Email already registered"
        )
    elif user is not None:
        await Database.users.remove(user.user_id)

    
    user = await Database.users.add(name, password, email)
    await EmailSender.send_verification_code(email, user.email_code)

    return user.auth_key
    

@router.post("/login", description="Authorizes the user")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await Database.users.find_by_email(form_data.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Incorrect email or password"
        )

    if not checkpw(form_data.password.encode(), user.password.encode()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Incorrect email or password"
        )

    if user.auth_key is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Email not verified"
        )

    return create_token(user)


@router.post("/validateCodeConfirm", description="Validate a code")
async def validate_code_confirm(email: str, code: int, auth_key: str) -> Response:
    user = await Database.users.find_by_email(email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="User not found"
        )

    if user.email_code is not None and user.email_code != code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Wrong code"
        )
    elif user.email_code is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Code already sent"
        )
    elif user.email_code is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Code not found"
        )
    
    if user.email_code == code and user.auth_key == auth_key:
        user.auth_key = None
        user.email_code = None
        await user.save()

    return Response(status_code=200)


@router.post("/repeatCodeConfirm", description="Repeat a code")
async def repeat_code_confirm(email: str, auth_key: str) -> Any:
    user = await Database.users.find_by_email(email)

    if user is None: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="User not found"
        )
    
    if auth_key is None and user.auth_key != auth_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Auth key not found or expired"
        )
    
    if user.email_code is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Code not found"
        )
    
    user.email_code = randint(1000, 9999)
    await user.save()
    await EmailSender.send_verification_code(email, user.email_code)
    return Response(status_code=200)
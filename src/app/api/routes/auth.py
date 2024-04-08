from datetime import timedelta
from random import randint
from typing import Any, Annotated
from fastapi import APIRouter, HTTPException, Response, status, Request, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from bcrypt import checkpw
from passlib.context import CryptContext

from src.app.api.models.tokens import TokenData, Token
from src.app.email import EmailSender
from src.database import Database
from src.database.models import UsersDocument
from src.app.api.routes.tokens import encode_user, decode_user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
router = APIRouter()


def get_token(user: UsersDocument) -> Response:
    current_user = user.model_copy()
    data = {
        'user_id': current_user.user_id,
        'name': current_user.name,
        'email': current_user.email,
    }
    token = encode_user(data=data)
    return Response(status_code=200, headers={
        "Set-Cookie": f"token={token}; path=/; httponly"
    })


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_user(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await Database.users.find_by_email(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[UsersDocument, Depends(get_current_user)]):
    if current_user.blocked:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/register", description="Register a new user")
async def register(name: str, email: str, password: str) -> Any:
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
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await Database.users.find_by_email(form_data.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    if not checkpw(form_data.password.encode(), user.password.encode()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    if user.auth_key is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not verified"
        )

    access_token_expires = timedelta(minutes=3600)
    access_token = encode_user(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


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

    return get_token(user)


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
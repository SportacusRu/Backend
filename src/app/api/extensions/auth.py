from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from typing_extensions import Annotated
from fastapi import Depends, HTTPException, Response, status
from src.app.api.models.tokens import TokenData
from src.app.api.extensions.tokens import decode_user, encode_user
from src.database import Database
from src.database.models.Users import UsersDocument

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

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


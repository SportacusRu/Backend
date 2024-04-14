from typing import Any
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, Response, status

from src.app.config.config import VERIFY_ENDPOINT
from src.app.email.email import EmailSender
from src.app.api.extensions.auth import get_current_active_user
from src.database.models.Users import UsersDocument
from src.database.database import Database


router = APIRouter()


@router.get("/get", description="Get information about user")
async def get(
    current_user: Annotated[UsersDocument, Depends(get_current_active_user)],
) -> Any: 
    return ""

@router.post("/updatePhoto", description="Update photo of user")
async def update_photo(
    current_user: Annotated[UsersDocument, Depends(get_current_active_user)],
    photo: str
) -> Any: 
    return ""

@router.post("/updateName", description="Update name of user")
async def update_name(
    current_user: Annotated[UsersDocument, Depends(get_current_active_user)],
    name: str
) -> Any: 
    return ""

@router.post("/updatePassword", description="Create a request of update password")
async def update_password(
    current_user: Annotated[UsersDocument, Depends(get_current_active_user)]
) -> Any: 
    verify_key = await Database.users.get_verify_link(current_user.user_id)
    await EmailSender.send_update_password(
        current_user.email, 
        VERIFY_ENDPOINT + verify_key
    )

@router.post("/setNewPassword", description="Update password of user")
async def set_new_password():
    return ""

@router.post("/ban", description="Ban user (special method)")
async def ban(moderator_key: str, user_id: int) -> Response: 
    await Database.users.block(user_id)
    return Response(status_code=status.HTTP_200_OK)
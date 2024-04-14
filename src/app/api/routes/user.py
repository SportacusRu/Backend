from typing import Any
from bcrypt import gensalt, hashpw
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, Response, status

from src.app.api.models.users import UserGet
from src.app.config.config import VERIFY_ENDPOINT
from src.app.email.email import EmailSender
from src.app.api.extensions.auth import get_current_active_user
from src.database.models.Users import UsersDocument
from src.database.database import Database


router = APIRouter()


@router.get("/get", description="Get information about user")
async def get(
    current_user: Annotated[UsersDocument, Depends(get_current_active_user)],
) -> UserGet: 
    reviews = await Database.reviews.find_by_user_id(current_user.user_id)
    places = []
    
    for place_id in current_user.like_list: 
        places.add(
            await Database.places.find_by_id(place_id)
        )

    return UserGet(
        user_id=current_user.user_id,
        name=current_user.name,
        email=current_user.email,
        like_list=places,
        reviews_list=reviews,
        photo=current_user.photo
    )

@router.post("/updatePhoto", description="Update photo of user")
async def update_photo(
    current_user: Annotated[UsersDocument, Depends(get_current_active_user)],
    photo: str
) -> Any: 
    current_user.photo = photo
    await current_user.save()

    return Response(status_code=status.HTTP_200_OK)

@router.post("/updateName", description="Update name of user")
async def update_name(
    current_user: Annotated[UsersDocument, Depends(get_current_active_user)],
    name: str
) -> Any: 
    current_user.name = name
    await current_user.save()

    return Response(status_code=status.HTTP_200_OK)

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
async def set_new_password(
    current_user: Annotated[UsersDocument, Depends(get_current_active_user)],
    verify_key: str, password: str, 
):
    user = await Database.users.find_by_id(current_user.user_id)

    if user.verify_link == verify_key:
        hashed_password = hashpw(password.encode(), gensalt()).decode()
        user.password = hashed_password
        await user.save()
        return Response(status_code=status.HTTP_200_OK)

    return Response(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong link")
    

@router.post("/ban", description="Ban user (special method)")
async def ban(moderator_key: str, user_id: int) -> Response: 
    await Database.users.block(user_id)
    return Response(status_code=status.HTTP_200_OK)
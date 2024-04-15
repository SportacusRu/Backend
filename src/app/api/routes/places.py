from http.client import HTTPException

from typing import Any, List, Union
from typing_extensions import Annotated
from fastapi import APIRouter, Response, Depends, status

from src.database.models.Places import PlacesDocument
from src.app.api.extensions.validate import validate_place_title, validate_review_text, validate_place_category, validate_place_filters
from src.database.models.Users import UsersDocument
from src.app.api.extensions.auth import get_current_active_user
from src.database import Database

router = APIRouter()


@router.get("/get", description="Get list of places")
async def get() -> List[PlacesDocument]:
    places = await Database.places.get_all()
    return places


@router.get("/getById", description="Get information about place")
async def get_by_id(place_id: int) -> Union[PlacesDocument, None]:
    current_place = await Database.places.find_by_id(place_id)
    return current_place


@router.get("/getRecommendedPlace", description="Get recommended place")
async def get_recommended_place(
    current_user: Annotated[UsersDocument, Depends(get_current_active_user)],
) -> Any: 
    return ""


@router.post("/add", description="Add a new place")
async def add(
    current_user: Annotated[UsersDocument, Depends(get_current_active_user)],
    title: str, geo: str, description: str, category: str, filters_list: str
) -> Response:
    # 1,2,3,4,5
    filters_list = set(filters_list.split(","))
    check = (validate_place_title(title)
             and validate_review_text(description)
             and validate_place_category(category)
             and validate_place_filters(filters_list))
    if not check:
        return HTTPException(
            status.HTTP_400_BAD_REQUEST, 
            detail="Some of fields aren't valid: title, geo, description, category or filters"
        )

    await Database.places.add(
        current_user.user_id, 
        title, geo, description,
        category, filters_list
    )
    return Response(status_code=200)


@router.post("/remove", description="remove place (special method)")
async def remove(moderator_key: str, place_id: int):
    await Database.places.remove(place_id)
    return Response(status_code=200)


@router.post("/edit", description="edit place (special method)")
async def edit(moderator_key: str, place_id, name=None, description=None, category=None, filters=None):
    await Database.places.update(
        place_id, 
        name, 
        description, 
        category, 
        filters
    )
    return Response(status_code=200)


@router.post("/like", description="Add place in user liked list")
async def like(
    current_user: Annotated[UsersDocument, Depends(get_current_active_user)],
    place_id: int
) -> Response:
    await Database.users.like(current_user.user_id, place_id)
    return Response(status_code=200)


@router.post("/dislike", description="Remove place from user liked list")
async def dislike(
    current_user: Annotated[UsersDocument, Depends(get_current_active_user)],
    place_id: int
) -> Response: 
    await Database.users.dislike(current_user.user_id, place_id)
    return Response(status_code=200)

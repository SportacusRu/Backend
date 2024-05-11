from http.client import HTTPException

from typing import Any, List, Union
from typing_extensions import Annotated
from fastapi.responses import FileResponse
from fastapi import APIRouter, Response, Depends, status
from random import shuffle

from src.app.api.models.places import PlacesGet
from src.database.models.Places import PlacesDocument
from src.app.api.extensions.validate import validate_place_title, validate_review_text, validate_place_category, validate_place_filters
from src.database.models.Users import UsersDocument
from src.app.api.extensions.auth import get_current_active_user
from src.database import Database
from base64 import b64decode

router = APIRouter()


@router.get("/get", description="Get list of places")
async def get() -> List[PlacesGet]:
    places = await Database.places.get_all()
    
    new_places = list()
    for place in places:
        ratings = await Database.reviews.get_grade_by_place_id(place.place_id)
        rating_sum = sum(rating.grade for rating in ratings)
        if len(ratings) > 0:
            new_places.append(
                PlacesGet(
                    **place.model_dump(), 
                    rating=round(rating_sum/len(ratings))
                )
            )
    return new_places

@router.get(
    "/getPreview", description="Get preview of place", 
    response_class=FileResponse
)
async def get_preview(place_id: int) -> Response:
    place = await Database.places.find_by_id(place_id)
    if place is None or len(place.reviews_list) < 1:
        return None
    
    last_element = place.reviews_list[-1]
    last_review = await Database.reviews.find_by_id(last_element)
    current_photo = last_review.photos[0]

    return Response(content=b64decode(current_photo[23:]), media_type="image/jpeg")

@router.get("/getById", description="Get information about place")
async def get_by_id(place_id: int) -> Union[PlacesDocument, None]:
    current_place = await Database.places.find_by_id(place_id)
    reviews = list([await Database.reviews.find_by_id(review_id) for review_id in current_place.reviews_list])
    rating = round(sum(review.grade for review in reviews) / len(reviews))

    return PlacesGet(
        **current_place.model_dump(), 
        rating=rating, 
        preview=reviews[-1].photos[0]
    )


@router.get("/getRecommendedPlace", description="Get recommended place")
async def get_recommended_place(
    current_user: Annotated[UsersDocument, Depends(get_current_active_user)],
) -> Any:
    liked_places = current_user.like_list
    disliked_places = current_user.dislike_list
    places = await get()
    if len(places) <= 0:
        return None

    if len(liked_places) > 0 or len(disliked_places) > 0:
        filtered_places = [place for place in places if (place.place_id not in disliked_places) and (place.place_id not in liked_places)]
        if len(filtered_places) > 0:
            shuffle(filtered_places)
            return filtered_places[0]
        return None
    else:
        shuffle(places)
        return places[0]

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
            content="Some of fields aren't valid: title, geo, description, category or filters"
        )

    place = await Database.places.add(
        current_user.user_id, 
        title, geo, description,
        category, filters_list
    )
    return place.place_id


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

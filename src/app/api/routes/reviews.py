from typing import List
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, Response
from src.app.api.extensions.validate import validate_grade, validate_review_text
from src.app.api.models.reviews import ReviewsGet, ReviewsDocument
from src.database.models.Users import UsersDocument
from src.app.api.extensions.auth import get_current_active_user
from src.database import Database

router = APIRouter()


@router.get("/getByPlaceId", description="Get reviews by place_id")
async def get_by_place_id(place_id: int) -> List[ReviewsGet]:
    reviews = await Database.reviews.get_all(place_id)

    new_reviews = list()
    for review in reviews:
        current_user = await Database.users.find_by_id(review.user_id)
        new_reviews.append(ReviewsGet(
            **review.model_dump(), user_photo=current_user.photo, user_name=current_user.name
        ))
    return new_reviews


@router.get("/getByUser", description="Get all user reviews")
async def get_by_user(
    current_user: Annotated[UsersDocument, Depends(get_current_active_user)]
) -> List[ReviewsDocument]:
    reviews = await Database.reviews.find_by_user_id(current_user.user_id)
    return reviews


@router.post("/add", description="Add a new review")
async def add_review(
    current_user: Annotated[UsersDocument, Depends(get_current_active_user)],
    place_id: int, description: str, photos: str, grade: int
) -> Response:
    print(validate_grade(grade))
    if not (validate_grade(grade)
        or validate_review_text(description)
        or await Database.places.find_by_id(place_id) is None):
        return Response(status_code=400)
    
    await Database.reviews.add(
        current_user.user_id,
        place_id,
        description,
        photos.split(","),
        grade
    )
    return Response(status_code=200)


@router.post("/remove", description="Remove a review")
async def remove_review(
    review_id: int, 
    current_user: Annotated[UsersDocument, Depends(get_current_active_user)] = None,
):
    review = await Database.reviews.find_by_id(review_id)

    if current_user:
        if review.user_id != current_user.user_id:
            return Response(status_code=403)
        await Database.reviews.remove(review.review_id)

    return Response(status_code=200)

@router.post("/removeForModerator", description="Remove a review (special method)")
async def remove_for_moderator(moderator_key: str, review_id: int):
    await Database.reviews.remove(review_id)
    return Response(status_code=200)
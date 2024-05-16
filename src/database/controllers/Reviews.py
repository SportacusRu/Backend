import datetime

from src.database.models import ReviewsDocument, PlacesDocument, ReviewsView
from typing import List, Union

from .BaseController import BaseController
from .Places import PlacesController


class ReviewsController(BaseController):
    """
    Controller for Reviews
    """
    @staticmethod
    async def get_all(place_id: int) -> List[ReviewsDocument]:
        """
        Get all reviews in Place

        :param place_id: current Place ID
        :type: place_id: int

        :return: List[ReviewsDocument]
        """
        return await ReviewsDocument.find(ReviewsDocument.place_id == place_id).to_list()

    
    @staticmethod
    async def find_by_id(review_id: int) -> Union[ReviewsDocument, None]:
        """
        Find review by review ID

        :param review_id: Review ID
        :type: review_id: int

        :return: Union[ReviewsDocument, None]
        """
        return await ReviewsDocument.find_one(ReviewsDocument.review_id == review_id)
    
    @staticmethod
    async def find_by_user_id(user_id: int) -> List[ReviewsDocument]:
        """
        Find review by user ID

        :param user_id: user ID
        :type: user_id: int

        :return: List[ReviewsDocument]
        """
        return await ReviewsDocument.find(ReviewsDocument.user_id == user_id).to_list()

    @staticmethod 
    async def get_grade_by_place_id(place_id: int) -> List[ReviewsView]:
        return await ReviewsDocument.find(ReviewsDocument.place_id == place_id).project(
            ReviewsView
        ).to_list()

    @staticmethod
    async def remove(review_id: int) -> None:
        """
        Remove review from database

        :param review_id: Review ID
        :type: review_id: int

        :return: None
        """
        review: ReviewsDocument = await ReviewsController.find_by_id(review_id)

        place: PlacesDocument = await PlacesController.find_by_id(review.place_id)
        place.reviews_list.remove(review.review_id)

        await place.save()
        await review.delete()

    @staticmethod
    async def add(
            user_id: int,
            place_id: int,
            description: str,
            photos: List[str],
            grade: int
    ) -> ReviewsDocument:
        """
        Add a new review and

        :param user_id: User ID
        :type: user_id: int
        :param place_id: current Place ID
        :type: place_id: int
        :param description: description
        :type: description: int
        :param photos: Photos list
        :type: photos: List[str]
        :param grade: 1 <= grade <= 5
        :type: grade: int

        :return: ReviewsDocument
        """
        new_id = await ReviewsController._get_new_id(ReviewsDocument, "review_id")

        review = ReviewsDocument(
            review_id=new_id,
            user_id=user_id,
            place_id=place_id,
            description=description,
            photos=photos,
            grade=grade,
            created_at=datetime.datetime.today().strftime("%d.%m.%Y"),
        )
        await review.insert()

        place = await PlacesController.find_by_id(place_id)

        place.reviews_list.append(review.review_id)
        await place.save()

        return review

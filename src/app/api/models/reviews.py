from typing import Union
from src.database.models.Reviews import ReviewsDocument


class ReviewsGet(ReviewsDocument):
    user_photo: Union[str, None]
    user_name: str
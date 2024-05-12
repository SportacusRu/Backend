from typing import Union
from src.database.models.Reviews import ReviewsDocument


class ReviewsGet(ReviewsDocument):
    user_name: str
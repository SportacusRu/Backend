from src.database.models.Reviews import ReviewsDocument

class ReviewsGet(ReviewsDocument):
    user_photo: str
    user_name: str
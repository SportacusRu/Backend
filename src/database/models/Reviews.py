from beanie import Document
from typing import List


class ReviewsDocument(Document): 
    user_id: int
    review_id: int
    place_id: int
    description: str
    photos: List[str]
    grade: int
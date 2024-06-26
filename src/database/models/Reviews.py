from beanie import Document
from typing import List

from pydantic import BaseModel


class ReviewsDocument(Document): 
    user_id: int
    review_id: int
    place_id: int
    description: str
    photos: List[str]
    grade: int
    created_at: str

class ReviewsView(BaseModel):
    grade: int
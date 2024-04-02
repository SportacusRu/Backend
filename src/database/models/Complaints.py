from beanie import Document
from typing import Optional


class ComplaintsDocument(Document): 
    user_id: int
    data: str
    review_id: Optional[int]
    place_id: Optional[int]
    report: Optional[str]
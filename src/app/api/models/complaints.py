from pydantic import BaseModel
from typing import Union
from src.database.models import PlacesDocument, ReviewsDocument


class ComplaintGet(BaseModel):
    typ: str
    item: Union[PlacesDocument, ReviewsDocument]
    complaint_count: int
    data: str
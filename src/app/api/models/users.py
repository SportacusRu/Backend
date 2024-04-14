from typing import List, Optional
from pydantic import BaseModel
from src.database.models import PlacesDocument, ReviewsDocument

class UserGet(BaseModel): 
    user_id: int
    name: str
    email: str
    like_list: List[PlacesDocument]
    reviews_list: List[ReviewsDocument]
    photo: Optional[str]
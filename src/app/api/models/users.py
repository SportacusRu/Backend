from typing import List, Optional
from pydantic import BaseModel
from src.app.api.models.places import PlacesGet
from src.database.models import ReviewsDocument

class UserGet(BaseModel): 
    user_id: int
    name: str
    email: str
    like_list: List[PlacesGet]
    reviews_list: List[ReviewsDocument]
    photo: Optional[str]

from beanie import Document
from typing import MutableSet, List


class PlacesDocument(Document): 
    place_id: int
    user_id: int
    title: str
    geo: str
    description: str
    reviews_list: List[int]
    category: str
    filters_list: MutableSet[str]
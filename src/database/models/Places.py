from beanie import Document
from typing import MutableSet


class PlacesDocument(Document): 
    place_id: int
    user_id: int
    title: str
    geo: str
    description: str
    reviews_list: MutableSet[int]
    category: str
    filters_list: MutableSet[str]
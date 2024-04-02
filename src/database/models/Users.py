from beanie import Document
from typing import Optional, MutableSet


class UsersDocument(Document): 
    user_id: int
    name: str
    password: str
    email: str
    blocked: bool
    like_list: MutableSet[int]
    dislike_list: MutableSet[int]
    complaint_count: int
    photo: Optional[str]
    auth_key: Optional[str]
    verify_link: Optional[str]
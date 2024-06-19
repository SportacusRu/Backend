from pydantic import BaseModel
from typing import Any


class ComplaintGet(BaseModel):
    typ: str
    item: Any
    complaint_count: int
    data: str
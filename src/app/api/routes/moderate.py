from http.client import HTTPException
from typing import Any, Optional
from fastapi import APIRouter, status
from src.database import Database
from src.app.api.models import ComplaintGet

from src.app.config.config import REVIEW, PLACE, MODERATOR_KEY


router = APIRouter()


@router.get("/get", description="Get all complaint (special method)")
async def get(moderator_key: str) -> Any:
    complaint = await Database.complaints.get_last_without_report()

    if complaint is None:
        return None
    
    typ = None
    item = None
    complaint_count = (
        await Database.users.find_by_id(complaint.user_id)
    ).complaint_count

    if complaint.review_id: 
        typ = PLACE
        item = await Database.places.find_by_id(complaint.review_id)
    else: 
        typ = REVIEW
        item = await Database.reviews.find_by_id(complaint.review_id)

    return ComplaintGet(
        typ=typ, 
        item=item,
        complaint_count=complaint_count,
        data=complaint.data
    )

@router.post("/add", description="Add a new complaint")
async def add(
    data: str, 
    review_id: Optional[int], 
    place_id: Optional[int], 
    current_user
) -> Any:
    return ""

@router.post("/report", description="Create a report (special method)")
async def report(moderator_key: str, report: str) -> Any:
    try:
        await Database.complaints.update_last(report)
    except ValueError:
        return {"error": "last report is not found"}
    return report
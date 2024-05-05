from typing import Any
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, Response
from src.app.api.extensions.auth import get_current_active_user
from src.database.models.Users import UsersDocument
from src.database import Database
from src.app.api.models import ComplaintGet

from src.app.config.config import REVIEW, PLACE


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
    current_user: Annotated[UsersDocument, Depends(get_current_active_user)],
    data: str, 
    review_id: int = None, 
    place_id: int = None, 
) -> Response:
    await Database.complaints.add(
        current_user.user_id,
        data,
        review_id,
        place_id
    )
    return Response(status_code=200)

@router.post("/report", description="Create a report (special method)")
async def report(moderator_key: str, report: str) -> str:
    try:
        await Database.complaints.update_last(report)
    except ValueError:
        return {"error": "last report is not found"}
    return report
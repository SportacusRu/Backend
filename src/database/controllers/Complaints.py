from src.database.models import ComplaintsDocument
from typing import List, Optional, Union


class ComplaintsController:
    """
    Controller for Complaints
    """
    @staticmethod
    async def get_all() -> List[ComplaintsDocument]:
        """
        Get all complaints

        :return: List[ComplaintsDocument]
        """
        return await ComplaintsDocument.find_all().to_list()

    @staticmethod
    async def get_last_without_report() -> Union[ComplaintsDocument, None]:
        """
        Get last without report complaint

        :return: Union[ComplaintsDocument, None]
        """
        return await ComplaintsDocument.find(
            ComplaintsDocument.report == None
        ).sort(("$natural", -1)).limit(1).first_or_none()

    @staticmethod
    async def update_last(report: str) -> ComplaintsDocument:
        """
        Update last complaint

        :param report: Report written by moderator
        :type: report: str
        :return: ComplaintsDocument
        """
        complaint = await ComplaintsController.get_last_without_report()

        if complaint is None: 
            raise ValueError("Last report is not found")
        
        complaint.report = report
        await complaint.save()

        return complaint

    @staticmethod
    async def add(
            user_id: int, 
            data: str, 
            review_id: Optional[int],
            place_id: Optional[int]
    ) -> ComplaintsDocument:
        """
        Add a new complaint

        :param user_id: User ID
        :type: user_id: int
        :param data: info about complaint
        :type: data: str
        :param review_id: review ID
        :type: review_id: Optional[int]
        :param place_id: place Id
        :type: place_id: Optional[int]

        :return: ComplaintsDocument
        """
        complaint = ComplaintsDocument(
            user_id=user_id, 
            data=data, 
            review_id=review_id, 
            place_id=place_id
        )

        await complaint.insert()
        return complaint

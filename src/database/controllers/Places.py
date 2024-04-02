from src.database.models import PlacesDocument
from typing import List, Any, MutableSet, Union

from .BaseController import BaseController


class PlacesController(BaseController):
    """
    Controller for Places
    """
    @staticmethod
    def __set_if_not_none(place: PlacesDocument, name: str, value: Any) -> None:
        """
        Set value if value is not None

        :param place: Place
        :type: place: PlacesDocument
        :param name: Attribute name
        :type: name: str
        :param value: Value
        :type: value: Any

        :return: None
        """
        if value is not None:
            setattr(PlacesDocument, name, value)

    @staticmethod
    async def get_all() -> List[PlacesDocument]:
        """
        Return all places

        :return: List[PlacesDocument]
        """
        return await PlacesDocument.find_all().to_list()

    @staticmethod
    async def find_by_id(place_id: int) -> Union[PlacesDocument, None]:
        """
        Find place by place_id

        :param place_id: Place ID
        :type: place_id: int
        :return: Union[PlacesDocument, None]
        """
        return await PlacesDocument.find_one(PlacesDocument.place_id == place_id)

    @staticmethod
    async def update(
            place_id: int,
            name: str = None,
            description: str = None,
            category: str = None,
            filters_list: MutableSet[int] = None
    ) -> PlacesDocument:
        """
        Update place

        :param place_id: Place ID
        :type: place_id: int
        :param name: name of place
        :type: name: Optional[str]
        :param description: place description
        :type: description: Optional[str]
        :param category: place category
        :type: category: Optional[str]
        :param filters_list: place filters
        :type: filters_list: Optional[MutableSet[int]

        :return: PlacesDocument
        """
        place = await PlacesController.find_by_id(place_id)

        PlacesController.__set_if_not_none(place, "name", name)
        PlacesController.__set_if_not_none(place, "description", description)
        PlacesController.__set_if_not_none(place, "category", category)
        PlacesController.__set_if_not_none(place, "filters_list", filters_list)

        await place.save()
        return place

    @staticmethod
    async def remove(place_id: int) -> None:
        """
        Remove place from database

        :param place_id: Place ID
        :type place_id: int

        :return: None
        """
        place = await PlacesController.find_by_id(place_id)
        await place.delete()

    @staticmethod
    async def add(
            user_id: int,
            title: str,
            geo: str,
            description: str,
            category: str,
            filters_list: MutableSet[int] = None
    ) -> PlacesDocument:
        """
        Add a new place

        :param user_id: User ID
        :type: user_id: int
        :param title: Place title
        :type: title: str
        :param geo: Place geolocation
        :type: geo: str
        :param description: Place description
        :type: description: str
        :param category: Place category
        :type: category: str
        :param filters_list: place filters
        :type: filters_list: MutableSet[int]

        :return: PlacesDocument
        """
        if filters_list is None:
            filters_list = set()

        new_id = await PlacesController._get_new_id(PlacesDocument, "place_id")

        place = PlacesDocument(
            place_id=new_id,
            user_id=user_id,
            title=title,
            geo=geo,
            description=description,
            reviews_list=set(),
            category=category,
            filters_list=filters_list
        )
        await place.insert()
        return place

from typing import Any


class BaseController:
    def __init__(self):
        pass

    @staticmethod
    async def _get_new_id(
            doc: Any,
            attr: str
    ) -> int:
        """
        Get new id for document

        :param doc: Any
        :param attr: str
        :return: int
        """
        document_list = await doc.find_all().sort("-" + attr).limit(1).to_list()
        if document_list:
            return getattr(document_list[0], attr) + 1
        return 0

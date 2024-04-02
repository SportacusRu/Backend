from src.database.models import UsersDocument
from typing import List, Union

from .BaseController import BaseController
from bcrypt import hashpw, gensalt


class UsersController(BaseController):
    """
    Controller for Users
    """
    @staticmethod
    async def __toggle_like(
        user_id: int, 
        place_id: int, 
        first_list: str, 
        second_list: str
    ) -> None:
        """
        Toggle place in Arrays

        :param user_id: User ID
        :type user_id: int

        :param place_id: Place ID
        :type place_id: int

        :param first_list: where add place
        :type first_list: str

        :param second_list: where remove place
        :type second_list: str
        """
        user = await UsersController.find_by_id(user_id)
        
        getattr(user, first_list).add(place_id)
        if place_id in user.like_list:
            getattr(user, second_list).remove(place_id)

        await user.save()

    @staticmethod
    async def get_all() -> List[UsersDocument]:
        """
        Get all users

        :return: List[UsersDocument]
        """
        return await UsersDocument.find_all().to_list()

    @staticmethod
    async def find_by_id(user_id: int) -> Union[UsersDocument, None]:
        """
        Get user by user_id

        :param user_id: User ID
        :type: user_id: int
        :return: Union[UsersDocument, None]
        """
        return await UsersDocument.find_one(UsersDocument.user_id == user_id)

    @staticmethod
    async def get_verify_link(user_id: int) -> str:
        """
        Generate and return verify link

        :param user_id: User ID
        :type: user_id: int
        :return: str
        """
        user = await UsersController.find_by_id(user_id)
        hashed = hashpw(bytes(user.password), gensalt())
        user.verify_link = hashed.decode().replace("/", "").replace(".", "")[7:]

        await user.save()
        return user.verify_link

    @staticmethod
    async def block(user_id: int) -> None:
        """
        Set user block

        :param user_id: User ID
        :type user_id: int

        :return: None
        """
        user = UsersController.find_by_id(user_id)
        user.blocked = True

    @staticmethod
    async def like(user_id: int, place_id: int) -> None:
        """
        Add in like list and remove from dislike list

        :param user_id: User ID
        :type user_id: int

        :param place_id: Place ID
        :type place_id: int

        :return: None
        """
        await UsersController.__toggle_like(user_id, place_id, "like_list", "dislike_list")

    @staticmethod
    async def dislike(user_id: int, place_id: int) -> None:
        """
        Add in dislike list and remove from like list

        :param user_id: User ID
        :type user_id: int

        :param place_id: Place ID
        :type place_id: int

        :return: None
        """
        await UsersController.__toggle_like(user_id, place_id, "dislike_list", "like_list")

    @staticmethod
    async def add(
        name: str,
        password: str,
        email: str,
    ) -> UsersDocument:
        """
        Add a new User. Generate auth_key and hash password

        :param name: Username
        :type name: str

        :param password: User unhashed password
        :type password: str

        :param email: User email
        :type email: str

        :return UsersDocument
        """
        new_id = await UsersController._get_new_id(UsersDocument, "user_id")
        hashed_password = hashpw(password.encode(), gensalt()).decode()
        auth_key = hashpw((name+password+email).encode(), gensalt()).decode()

        user = UsersDocument(
            user_id=new_id,
            name=name,
            password=hashed_password,
            email=email,
            blocked=False,
            like_list=set(),
            dislike_list=set(),
            complaint_count=0,
            auth_key=auth_key,
            verify_link=None,
            photo=None
        )

        await user.insert()
        return user
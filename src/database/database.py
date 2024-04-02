from src.database.controllers import (
    UsersController, ComplaintsController, 
    ReviewsController, PlacesController
)
from src.database.models import (
    UsersDocument, ComplaintsDocument, 
    ReviewsDocument, PlacesDocument
)

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie


class Database: 
    users = UsersController
    complaints = ComplaintsController
    reviews = ReviewsController
    places = PlacesController

    @staticmethod
    async def init(link: str) -> None:
        client = AsyncIOMotorClient(link)
        await init_beanie(database=client.db_name, document_models=[
            UsersDocument, ComplaintsDocument, 
            ReviewsDocument, PlacesDocument
        ])
    
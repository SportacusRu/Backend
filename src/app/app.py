from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware

from src.app.api.router import api_router
from src.app.middlewares import ModeratorAuthMiddleware
from src.app.config import config

from src.database import Database
from contextlib import asynccontextmanager

def custom_generate_unique_id(route: APIRoute) -> str: 
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Database.init(config.APP_DATABASE_LINK)
    yield

app = FastAPI(
    title=config.PROJECT_NAME,
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
    redoc_url="/redoc"
)
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ModeratorAuthMiddleware)

app.include_router(api_router)
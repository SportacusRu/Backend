from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware

from src.app.api.router import api_router
from src.app.middlewares import AuthMiddleware
from src.app.config import config


def custom_generate_unique_id(route: APIRoute) -> str: 
    return f"{route.tags[0]}-{route.name}"

app = FastAPI(
    title=config.PROJECT_NAME,
    generate_unique_id_function=custom_generate_unique_id,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)

app.include_router(api_router)
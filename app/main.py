import os

from dotenv import load_dotenv
from fastapi import FastAPI

from .api.api import register_routes
from .shared.database.database import init

load_dotenv()


async def startup():
    await init()


app = FastAPI(on_startup=[startup])
register_routes(app)
from .shared.database.database import init

async def startup():
    await init()
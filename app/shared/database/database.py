import os
from typing import Annotated

from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import Depends
from pymongo import AsyncMongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from .enteties import Session as SessionDocument

load_dotenv()

async def init():
    client = AsyncMongoClient(os.getenv('DB_MONGO_URL'))
    database = client.get_database(os.getenv("DB_MONGO_DATABASE"))
    await init_beanie(database=database, document_models=[SessionDocument])

engine = create_engine(os.getenv("DB_SQL_URL"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
DbSession = Annotated[Session, Depends(get_db)]
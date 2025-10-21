from fastapi import APIRouter, File, UploadFile, status

from ...shared.database.entities.embedding import Embedding
from . import models, usecases

router = APIRouter(prefix="/embedding", tags=["Embedding"])


@router.post("/upload", status_code=status.HTTP_204_NO_CONTENT)
async def upload(file: UploadFile = File(...)) -> None:
    await usecases.upload(file=file)
    return

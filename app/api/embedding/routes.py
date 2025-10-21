from fastapi import UploadFile, File, APIRouter, status

from . import usescases, models
from ...shared.database.entities.embedding import Embedding

router = APIRouter(
    prefix='/embedding',
    tags=['Embedding']
)

@router.post("/upload", status_code=status.HTTP_204_NO_CONTENT)
async def upload(file: UploadFile = File(...)) -> None:
    await usescases.upload(file=file)
    return

@router.get("/", status_code=status.HTTP_200_OK)
async def find():
    embeddings = await Embedding.find_all().to_list()
    return embeddings

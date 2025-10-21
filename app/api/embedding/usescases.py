from dotenv import load_dotenv
import os
import numpy as np
import tempfile

import google.generativeai as genai
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from fastapi import UploadFile
import pymongo

from . import models
from ...shared.database.entities.embedding import Embedding
from ...shared.exceptions.internal_server_error import InternalServerError
from ...shared.exceptions.bad_request import BadRequestError

load_dotenv()

def create_embedding(text: str) -> dict:
    genai.configure(api_key=os.getenv('LLM_GEMINI_API_KEY'))
    embedding = genai.embed_content(
        model='models/gemini-embedding-exp-03-07',
        content=text,
    )
    return embedding

async def save(text: str, document_name:str) -> None :
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=200)
    parts = text_splitter.split_text(text)
    for idx, part in enumerate(parts):
        embedding = create_embedding(part)['embedding']
        try:
            embedding_document = Embedding(document_name=document_name, part=idx, text=part, embedding=embedding)
            await Embedding.insert_one(embedding_document)
        except Exception as e:
            print(e)
            raise InternalServerError('criar embedding')
        
async def upload(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    if file.content_type == "application/pdf":
        loader = PyPDFLoader(temp_path)
        docs = loader.load()
        text = "\n".join([d.page_content for d in docs])

    elif file.content_type == "application/pdf":
        text = open(temp_path, "r", encoding="utf-8").read()
    
    else:
        raise BadRequestError('arquivo deve ser um pdf ou txt')
    
    await save(text=text, document_name=file.filename)

def get_embedding(text: str, limit: int = 5, num_candidates: int = 150) -> list[dict[str, str]]:
    client = pymongo.MongoClient(os.getenv('DB_MONGO_URL'))
    embedded_query = create_embedding(text)['embedding']
    pipeline = [
        {
        '$vectorSearch': {
            'index': 'embedding', 
            'path': 'embedding', 
            'queryVector': embedded_query,
            'limit': limit,
            'numCandidates': num_candidates
            }
        },
        {
        '$project': {
            '_id': 0,
            'text': 1
            }
        }
    ]
    result = client[os.getenv('DB_MONGO_DATABASE')]['Embedding'].aggregate(pipeline)
    return list(result)
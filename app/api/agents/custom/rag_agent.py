from src.app.embedding import service as embedding_service

from .. import models
from ..agent_templates.default_agent import DefaultAgent


class RagAgent(DefaultAgent):
    def __init__(self, prompt_path:str="src/app/agents/prompts/rag_agent_prompt.txt"):
        system_prompt = open(prompt_path, "r", encoding="utf-8").read()
        super().__init__(system_prompt=system_prompt)
    
    def create_response(self, user_message:str, history:list=[]) -> models.DefaultAgentResponseModel:
        embeddings = embedding_service.get_embedding(text=user_message)['embeddings']
        format = {"rag":embeddings}
        return super().invoke(user_message=user_message, history=history, format=format)
from ...embedding.usecases import get_embedding
from .. import models
from ..templates.default_agent import DefaultAgent


class RagAgent(DefaultAgent):
    def __init__(
        self, prompt_path: str = "app/api/agents/prompts/rag_agent_prompt.txt"
    ):
        system_prompt = open(prompt_path, "r", encoding="utf-8").read()
        super().__init__(system_prompt=system_prompt)

    def create_response(self, user_message: str, history: list = []) -> str:
        embeddings = get_embedding(text=user_message)
        format = {"rag": embeddings}
        result = (
            super()
            .execute(user_message=user_message, history=history, format=format)
            .content
        )
        return {"result": result, "rag": embeddings}

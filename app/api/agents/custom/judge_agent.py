from typing import Optional

from pydantic import BaseModel, Field

from ....shared.exceptions.internal_server_error import InternalServerError
from ..templates.structured_output_agent import StructuredOutputAgent


class JudgeAgent(StructuredOutputAgent):
    def __init__(
        self, prompt_path: str = "app/api/agents/prompts/judge_agent_prompt.txt"
    ):
        system_prompt = open(prompt_path, "r", encoding="utf-8").read()

        class StructuredOutput(BaseModel):
            """Se a resposta criada pelo agente é válida ou não"""

            is_valid: bool = Field(
                description="True se a resposta for válida False caso contrário"
            )

            """Somente se a resposta criada pelo agento for inválida (is_valid=False), nova resposta para o usuário"""
            new_response: Optional[str] = Field(
                description="Nova resposta para o usuário"
            )

        super().__init__(
            system_prompt=system_prompt, structured_output=StructuredOutput
        )

    def validate_response(
        self, user_message: str, agent_response: str, rag= list| str, history: list = [],
    ) -> dict:
        format = {"response": agent_response, "rag":rag}
        result = super().execute(
            user_message=user_message, history=history, format=format
        )
        return result

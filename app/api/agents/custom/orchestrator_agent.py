from pydantic import BaseModel, Field

from ..templates.structured_output_agent import StructuredOutputAgent


class OrchestratorAgent(StructuredOutputAgent):
    def __init__(
        self, prompt_path: str = "app/api/agents/prompts/orchestrator_agent_prompt.txt"
    ):
        system_prompt = open(prompt_path, "r", encoding="utf-8").read()

        class StructuredOutput(BaseModel):
            """Qual agente será chamado"""

            agent_number: int = Field(
                description="O número do agente que deve ser chamado"
            )

        super().__init__(
            system_prompt=system_prompt, structured_output=StructuredOutput
        )

    def choose_agent(self, user_message: str, history: list = []) -> dict:
        result = super().execute(user_message=user_message, history=history)
        return result

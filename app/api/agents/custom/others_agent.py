from ..templates.default_agent import DefaultAgent


class OthersAgent(DefaultAgent):
    def __init__(
        self, prompt_path: str = "app/api/agents/prompts/others_agent_prompt.txt"
    ):
        system_prompt = open(prompt_path, "r", encoding="utf-8").read()
        super().__init__(system_prompt=system_prompt)

    def create_response(self, user_message: str, history: list = []) -> str:
        result = (super().execute(user_message=user_message, history=history)).content
        return result

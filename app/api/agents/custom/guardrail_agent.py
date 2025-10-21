from typing import Optional

from pydantic import BaseModel, Field

from ..templates.structured_output_agent import StructuredOutputAgent
from ....shared.exceptions.internal_server_error import InternalServerError

class GuardrailAgent(StructuredOutputAgent):
    def __init__(self, prompt_path:str="app/api/agents/prompts/guardrail_agent_prompt.txt"):
        system_prompt = open(prompt_path, "r", encoding="utf-8").read()

        class StructuredOutput(BaseModel):
            """Se a resposta criada pelo agente é válida ou não"""
            is_valid: bool = Field(description="True se a resposta for válida False caso contrário")

            """Somente se a resposta criada pelo agento for inválida (is_valid=False), nova resposta para o usuário"""
            new_response: Optional[str] = Field(description="Nova resposta para o usuário")
        
        super().__init__(system_prompt=system_prompt, structured_output=StructuredOutput)
            
    def validate_response(self, user_message:str, agent_response:str, history:list=[]) -> dict:
        format = {"response":agent_response}
        result = super().invoke(user_message=user_message, history=history, format=format)

        if result.is_valid == False:
            if "new_response" in result:
                new_response = result.new_response
            else: 
                raise InternalServerError('criar mensagem para usuário')
        
            return {"is_valid":result.is_valid, "new_response":new_response}
        else:
            return {"is_valid":result.is_valid,}
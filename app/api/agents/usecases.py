from ...shared.enums.agent_type import AgentTypeEnum
from ...shared.exceptions.internal_server_error import InternalServerError
from . import models
from .custom.guardrail_agent import GuardrailAgent
from .custom.orchestrator_agent import OrchestratorAgent
from .custom.others_agent import OthersAgent
from .custom.rag_agent import RagAgent

orchestrator_agent = OrchestratorAgent()
rag_agent = RagAgent()
others_agent = OthersAgent()
guardrail_agent = GuardrailAgent()


def create_response(user_message: str, history: list = []) -> models.CreateResponseData:
    orchestrator_choice = orchestrator_agent.choose_agent(user_message, history)

    print(
        f"----------------------------------orchestrator: {orchestrator_choice.agent_number}"
    )

    if orchestrator_choice.agent_number == 1:
        response = rag_agent.create_response(user_message, history)
        agent_id = AgentTypeEnum.RAG_AGENT

    if orchestrator_choice.agent_number == 2:
        response = others_agent.create_response(user_message, history)
        agent_id = AgentTypeEnum.OTHERS_AGENT

    print("----------------------------------response: " + response)

    validation = guardrail_agent.validate_response(user_message, response, history)

    print(f"----------------------------------validation: {validation}")

    if validation.is_valid == False:
        if "new_response" not in validation:
            raise InternalServerError("gerar mensagem para usuário")
        response = validation.new_response
        agent_id = AgentTypeEnum.GUARDRAIL_AGENT

    return {"response": response, "agent_id": agent_id}

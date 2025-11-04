from ...shared.enums.agent_type import AgentTypeEnum
from ...shared.exceptions.internal_server_error import InternalServerError
from . import models
from .custom.judge_agent import JudgeAgent
from .custom.orchestrator_agent import OrchestratorAgent
from .custom.others_agent import OthersAgent
from .custom.rag_agent import RagAgent

orchestrator_agent = OrchestratorAgent()
rag_agent = RagAgent()
others_agent = OthersAgent()
judge_agent = JudgeAgent()


def create_response(user_message: str, history: list = []) -> models.CreateResponseData:
    orchestrator_choice = orchestrator_agent.choose_agent(user_message, history)

    print(
        f"----------------------------------orchestrator: {orchestrator_choice.agent_number}"
    )

    if orchestrator_choice.agent_number == 1:
        result = rag_agent.create_response(user_message, history)
        print(result)
        response = result['result']
        rag = result['rag']
        agent_id = AgentTypeEnum.RAG_AGENT

    if orchestrator_choice.agent_number == 2:
        response = others_agent.create_response(user_message, history)
        rag = "Documentação não foi consultada"
        agent_id = AgentTypeEnum.OTHERS_AGENT

    print("----------------------------------response: " + response)

    validation = judge_agent.validate_response(user_message, response, rag, history)

    print(f"----------------------------------validation: {validation}")

    if validation.is_valid == False:
        if not hasattr(validation, "new_response"):
            raise InternalServerError("gerar mensagem para usuário")
        response = validation.new_response
        agent_id = AgentTypeEnum.JUDGE_AGENT

    return {"response": response, "agent_id": agent_id}

import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class DefaultAgent:
    def __init__(
        self,
        model: str = "gemini-2.0-flash",
        temperature: float = 0.2,
        max_tokens: int | None = None,
        timeout: int | None = None,
        system_prompt: str = "",
    ):
        self.__llm = ChatGoogleGenerativeAI(
            api_key=os.getenv("GOOGLE_API_KEY"),
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
            verbose=True,
        )
        self.__system_prompt = system_prompt

    def invoke(self, user_message: str, history: list = [], format: dict = {}) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [("system", self.__system_prompt), *history, ("human", user_message)]
        )
        prompt = prompt.invoke(format)
        result = self.__llm.invoke(prompt)
        return result

import logging
from src.database.chroma import ChromaDatabase
from langchain.vectorstores import Chroma

from langchain.chains import RetrievalQA
from langchain.llms import Ollama
from langchain.llms.openai import OpenAI
import os


OLLAMA_BASE_URL = os.getenv("OLLAMA_API_HOST", "ollama")
LLM_MODEL = os.getenv("LLM_MODEL", "codellama")

logger = logging.getLogger(__name__)


class RAGAgent:
    database = Chroma
    llm = Ollama

    def __init__(self) -> None:
        self.__get_retreiver()
        # self.__build_ollama()
        self.__build_openai()
        self.__build_qa()

    def __get_retreiver(self) -> None:
        database = ChromaDatabase().get_langchain_class()

        self.retriever = database.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 4},
        )

    def __build_openai(self) -> None:
        try:
            self.llm = OpenAI(model_name="gpt-3.5", temperature=0.0)
        except Exception:
            logger.error("Failed to build OpenAI")

    def __build_ollama(self) -> None:
        try:
            base_url = f"http://{OLLAMA_BASE_URL}:11434"
            self.llm = Ollama(model=LLM_MODEL, verbose=True, base_url=base_url)
        except Exception:
            logger.error("Failed to build Ollama")

    def __build_qa(self) -> None:
        try:
            self.qa = RetrievalQA.from_chain_type(
                llm=self.llm, chain_type="stuff", retriever=self.retriever
            )
        except Exception:
            logger.error("Failed to build QA")

    def ask(self, question: str) -> str:
        try:
            result = self.qa.run(question)
            return result
        except Exception:
            return "Something went wrong! :cry. Reach out to Lavesh for debugging"

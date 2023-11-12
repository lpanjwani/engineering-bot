from src.database.chroma import ChromaDatabase
from langchain.vectorstores import Chroma

from langchain.chains import RetrievalQA
from langchain.llms import Ollama
import os

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


class RAGAgent:
    database = Chroma

    def __init__(self) -> None:
        self.__get_retreiver()
        self.__build_qa()

    def __get_retreiver(self) -> None:
        database = ChromaDatabase().get_langchain_class()

        self.retriever = database.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 8},
        )

    def __build_qa(self) -> None:
        llm = Ollama(model="codellama", verbose=True, base_url=OLLAMA_BASE_URL)

        self.qa = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=self.retriever
        )

    def ask(self, question: str) -> str:
        result = self.qa.run(question)
        return result

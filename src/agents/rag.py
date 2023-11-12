from tabnanny import verbose
from src.database.chroma import ChromaDatabase
from langchain.vectorstores import Chroma

from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
from langchain.schema import SystemMessage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)


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
        llm = Ollama(
            model="codellama",
            verbose=True,
        )

        self.qa = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=self.retriever
        )

    def ask(self, question: str) -> str:
        result = self.qa.run(question)
        return result

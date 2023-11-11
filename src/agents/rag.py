from src.database.chroma import ChromaDatabase
from langchain.vectorstores import Chroma

from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import Ollama


class RAGAgent:
    database = Chroma

    def __init__(self) -> None:
        self.__get_retreiver()
        self.__build_qa()

    def __get_retreiver(self) -> None:
        database = ChromaDatabase().get_langchain_class()

        self.retriever = database.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5},
        )

    def __build_qa(self) -> None:
        llm = Ollama(
            model="codellama",
            verbose=True,
        )
        memory = ConversationSummaryMemory(
            llm=llm,
            memory_key="chat_history",
            return_messages=True,
            verbose=True,
        )
        self.qa = ConversationalRetrievalChain.from_llm(
            llm,
            retriever=self.retriever,
            memory=memory,
            verbose=True,
        )

    def ask(self, question: str) -> str:
        result = self.qa(question)
        return result["answer"]
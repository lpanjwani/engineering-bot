from src.database.chroma import ChromaDatabase
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain


class RAGAgent:
    database = Chroma

    def __init__(self) -> None:
        self.__get_retreiver()
        self.__build_qa()

    def __get_retreiver(self) -> None:
        database = ChromaDatabase().get_langchain_class()

        self.retriever = database.get_retriever(
            search_type="mmr",
            search_kwargs={"k": 8},
        )

    def __build_qa(self) -> None:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        memory = ConversationSummaryMemory(
            llm=llm, memory_key="chat_history", return_messages=True
        )
        self.qa = ConversationalRetrievalChain.from_llm(
            llm, retriever=self.retriever, memory=memory
        )

    def ask(self, question: str) -> str:
        answer = self.qa.ask(question)
        return answer

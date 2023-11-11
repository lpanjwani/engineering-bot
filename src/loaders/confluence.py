from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)
from langchain.document_loaders import ConfluenceLoader
from langchain.embeddings import SentenceTransformerEmbeddings
import os
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain

ATLASSIAN_URL = "https://hakbah.atlassian.net/wiki"
ATLASSIAN_USERNAME = os.environ.get["ATLASSIAN_USERNAME"]
ATLASSIAN_ACCESS_TOKEN = os.environ.get["ATLASSIAN_ACCESS_TOKEN"]
ATLASSIAN_SPACE_KEY = "JS"


class HakbahConfluenceLoader:
    def __init__(self, url, username, api_key):
        self.loader = ConfluenceLoader(
            url=url,
            username=username,
            api_key=api_key
        )

    def load(self):
        raw_results = self.loader.load(
            space_key=ATLASSIAN_SPACE_KEY, 
            include_attachments=True
        )

        return raw_results

    def split_documents(self, raw_results):
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        documents = splitter.split_documents(raw_results)

        return documents

    def embbed_to_database(self, documents):
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        database = Chroma.from_documents(documents, embeddings)

        return database

    def get_retriever(self, database):
        retriever = database.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 8, "include_metadata": True}
        )

        return retriever

    def get_memory(self):
        llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        memory = ConversationSummaryMemory(
            llm=llm, memory_key="chat_history", return_messages=True
        )

        return memory
    
    def get_qa(self, llm, retriever, memory):
        qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)

        return qa

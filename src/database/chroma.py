from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from chromadb.config import Settings
import chromadb
import uuid
import os

COLLECTION_NAME = "Engineering"

CHROMA_HOST = os.getenv("CHROMA_HOST")


class ChromaDatabase:
    client: chromadb.HttpClient
    collection: chromadb.Collection
    langchain_chroma: Chroma

    def __init__(self) -> None:
        self.__build_http_client()
        self.create_collection()
        self.get_langchain_class()

    def __build_http_client(self):
        client_host = f"http://{CHROMA_HOST}:8000"

        self.client = chromadb.HttpClient(
            host=client_host, settings=Settings(allow_reset=True)
        )

    def drop_collection(self):
        return self.langchain_chroma.delete_collection()

    def create_collection(self) -> None:
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)

    def get_embedding_model(self) -> HuggingFaceEmbeddings:
        model_kwargs = {"device": "cpu", "trust_remote_code": True}
        return HuggingFaceEmbeddings(
            model_name="codesage/codesage-small",
            model_kwargs=model_kwargs
        )

    def delete_collection(self) -> None:
        self.client.delete_collection(COLLECTION_NAME)

    def insert_documents(self, documents) -> None:
        self.langchain_chroma.add_documents(documents)

    def get_langchain_class(self) -> Chroma:
        self.langchain_chroma = Chroma(
            client=self.client,
            collection_name=COLLECTION_NAME,
            embedding_function=self.get_embedding_model(),
        )

        return self.langchain_chroma

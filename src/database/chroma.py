from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from chromadb.config import Settings
import chromadb
import uuid
import os

COLLECTION_NAME = "Engineering"

CHROMA_HOST = os.getenv("CHROMA_HOST", "chroma")


class ChromaDatabase:
    client: chromadb.HttpClient
    collection: chromadb.Collection

    def __init__(self) -> None:
        self.__build_http_client()
        self.create_collection()

    def __build_http_client(self):
        client_host = 'http://{CHROMA_HOST}:8000'.format(CHROMA_HOST=CHROMA_HOST)

        self.client = chromadb.HttpClient(
            host=client_host, settings=Settings(allow_reset=True)
        )

    def create_collection(self) -> None:
        self.collection = self.client.get_or_create_collection(COLLECTION_NAME)

    def get_embedding_model(self) -> SentenceTransformerEmbeddings:
        return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    def delete_collection(self) -> None:
        self.client.delete_collection(COLLECTION_NAME)

    def insert_documents(self, documents) -> None:
        for doc in documents:
            self.collection.add(
                ids=[str(uuid.uuid4())],
                metadatas=doc.metadata,
                documents=doc.page_content,
            )

    def get_langchain_class(self) -> Chroma:
        langchain_chroma = Chroma(
            client=self.client,
            collection_name=COLLECTION_NAME,
            embedding_function=self.get_embedding_model(),
        )

        return langchain_chroma

from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from chromadb.config import Settings
import chromadb
import uuid

COLLECTION_NAME = "Engineering"


class ChromaDatabase:
    client: chromadb.HttpClient
    collection: chromadb.Collection

    def __init__(self) -> None:
        self.__build_http_client()
        self.create_collection()

    def __build_http_client(self):
        self.client = chromadb.HttpClient(settings=Settings(allow_reset=True))

    def create_collection(self) -> None:
        self.collection = self.client.get_or_create_collection(COLLECTION_NAME)

    def get_embedding_model(self) -> SentenceTransformerEmbeddings:
        return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    def reset_collection(self) -> None:
        self.collection.reset()

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

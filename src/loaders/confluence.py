from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import ConfluenceLoader
import os
from src.database.chroma import ChromaDatabase

ATLASSIAN_URL = os.environ["ATLASSIAN_URL"]
ATLASSIAN_USERNAME = os.environ["ATLASSIAN_USERNAME"]
ATLASSIAN_ACCESS_TOKEN = os.environ["ATLASSIAN_ACCESS_TOKEN"]
ATLASSIAN_SPACE_KEY = "JS"


class HakbahConfluenceLoader:
    loader: ConfluenceLoader
    database: ChromaDatabase

    def run(self):
        self.__intit_loader()
        self.__init_database()
        raw_results = self.__load()
        documents = self.__split_documents(raw_results)
        self.__embbed_to_database(documents)

    def __init_database(self):
        self.database = ChromaDatabase()

    def __intit_loader(self):
        self.loader = ConfluenceLoader(
            url=ATLASSIAN_URL,
            username=ATLASSIAN_USERNAME,
            api_key=ATLASSIAN_ACCESS_TOKEN,
        )

    def __load(self):
        raw_results = self.loader.load(
            space_key=ATLASSIAN_SPACE_KEY, include_attachments=True
        )

        return raw_results

    def __split_documents(self, raw_results):
        splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
        documents = splitter.split_documents(raw_results)

        return documents

    def __embbed_to_database(self, documents):
        self.database.insert_documents(documents)

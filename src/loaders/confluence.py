from math import log
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import ConfluenceLoader
from src.database.chroma import ChromaDatabase
import logging
import os

ATLASSIAN_URL = os.getenv("ATLASSIAN_URL")
ATLASSIAN_USERNAME = os.getenv("ATLASSIAN_USERNAME")
ATLASSIAN_ACCESS_TOKEN = os.getenv("ATLASSIAN_ACCESS_TOKEN")
ATLASSIAN_SPACE_KEY = "JS"


class HakbahConfluenceLoader:
    loader: ConfluenceLoader
    database: ChromaDatabase

    def run(self):
        logging.info("Confluence Loader: Starting")
        self.__intit_loader()
        logging.info("Confluence Loader: Connecting to Database")
        self.__init_database()
        logging.info("Confluence Loader: Loading Data")
        raw_results = self.__load()
        logging.info("Confluence Loader: Splitting Documents")
        documents = self.__split_documents(raw_results)
        logging.info("Confluence Loader: Embedding to Database")
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
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=25)
        documents = splitter.split_documents(raw_results)

        return documents

    def __embbed_to_database(self, documents):
        self.database.insert_documents(documents)

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    Language,
)
from langchain.document_loaders import ConfluenceLoader
import os
from src.database.chroma import ChromaDatabase

from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser


REPO_PATH = "/Users/lavesh/Documents/Hakbah/Nest_API/src"


class HakbahCodebaseLoader:
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
        self.loader = GenericLoader.from_filesystem(
            REPO_PATH,
            glob="**/*",
            suffixes=[".ts"],
            parser=LanguageParser(language=Language.JS),
            show_progress=True,
        )

    def __load(self):
        raw_results = self.loader.load()

        return raw_results

    def __split_documents(self, raw_results):
        splitter = RecursiveCharacterTextSplitter(
            language=Language.TS, chunk_size=1000, chunk_overlap=50
        )
        documents = splitter.split_documents(raw_results)

        return documents

    def __embbed_to_database(self, documents):
        self.database.insert_documents(documents)

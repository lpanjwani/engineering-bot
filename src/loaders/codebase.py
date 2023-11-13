from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    Language,
)
from langchain.document_loaders import ConfluenceLoader
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from src.database.chroma import ChromaDatabase
from git import Repo
from enum import Enum
import os
import shutil


class CodebaseRepos(Enum):
    NEST_API = "Hakbah/Nest_API"
    ADMIN_API_SERVICE = "Hakbah/Admin_API_Service"
    ADMIN_UI_SERVICE = "Hakbah/Admin_UI_Service"


class HakbahCodebaseLoader:
    repo_path: str
    loader: ConfluenceLoader
    database: ChromaDatabase

    def __init__(self) -> None:
        pass

    def run(self, github_slug: CodebaseRepos) -> None:
        self.__downlod_repo(github_slug)
        self.__init_database()
        self.__intit_loader()
        raw_results = self.__load()
        documents = self.__split_documents(raw_results)
        self.__embbed_to_database(documents)
        self.__delete_folder()

    def __downlod_repo(self, github_slug: CodebaseRepos) -> None:
        ssh_url = f"git@github.com:{github_slug}.git"

        slug_split = github_slug.split("/")
        repo_name = slug_split[1]

        self.repo_path = os.path.join("./repos", repo_name)

        Repo.clone_from(ssh_url, to_path=self.repo_path)

    def __init_database(self) -> None:
        self.database = ChromaDatabase()

    def __intit_loader(self) -> None:
        self.loader = GenericLoader.from_filesystem(
            self.repo_path,
            glob="**/*",
            suffixes=[".ts"],
            parser=LanguageParser(language=Language.JS),
            show_progress=True,
        )

    def __load(self) -> None:
        raw_results = self.loader.load()

        return raw_results

    def __split_documents(self, raw_results) -> None:
        splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.TS, chunk_size=2000, chunk_overlap=200
        )
        documents = splitter.split_documents(raw_results)

        return documents

    def __embbed_to_database(self, documents) -> None:
        self.database.insert_documents(documents)

    def __delete_folder(self) -> None:
        shutil.rmtree(self.repo_path)

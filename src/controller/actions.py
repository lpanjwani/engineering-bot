from src.database.chroma import ChromaDatabase
from src.loaders.codebase import CodebaseRepos, CodebaseLoader
from src.loaders.confluence import HakbahConfluenceLoader
from src.loaders.pull_model import pull_model


def cleanup():
    print("Reseting Database!")
    db = ChromaDatabase()
    db.drop_collection()
    db.create_collection()
    print("Database Reset Completed!")


def reindex():
    print("Indexing Confluence!")
    HakbahConfluenceLoader().run()

    print("Indexing Codebase!")
    CodebaseLoader().run(CodebaseRepos.NEST_API)
    CodebaseLoader().run(CodebaseRepos.ADMIN_API_SERVICE)
    CodebaseLoader().run(CodebaseRepos.ADMIN_UI_SERVICE)

    print("Done!")


def init(args):
    if args.pull_model:
        pull_model()

    if args.cleanup:
        cleanup()

    if args.reindex:
        reindex()

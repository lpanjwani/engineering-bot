from src.database.chroma import ChromaDatabase
from src.loaders.codebase import HakbahCodebaseLoader
from src.loaders.confluence import HakbahConfluenceLoader
from src.loaders.pull_model import pull_model


def cleanup():
    print("Reseting Database!")
    db = ChromaDatabase()
    db.delete_collection()
    db.create_collection()


def reindex():
    print("Loading Confluence!")
    HakbahConfluenceLoader().run()

    print("Indexing Codebase!")
    HakbahCodebaseLoader().run()

    print("Done!")


def init(args):
    if args.pull_model:
        pull_model()

    if args.cleanup:
        cleanup()

    if args.reindex:
        reindex()

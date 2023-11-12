from src.controller.cli import get_args
from src.loaders.codebase import HakbahCodebaseLoader
from src.loaders.confluence import HakbahConfluenceLoader
from src.database.chroma import ChromaDatabase
import schedule
import time


def CronController():
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

    args = get_args()
    if args.cleanup:
        cleanup()

    if args.reindex:
        reindex()

    schedule.every().day.do(cleanup)
    schedule.every().day.do(reindex)

    while True:
        schedule.run_pending()
        time.sleep(1)

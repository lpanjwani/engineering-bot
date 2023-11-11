from src.controller.cli import get_args
from src.loaders.confluence import HakbahConfluenceLoader
from src.database.chroma import ChromaDatabase
import schedule
import time


def CronController():
    def run():
        print("Reseting Database!")
        db = ChromaDatabase()
        db.delete_collection()
        db.create_collection()

        print("Loading Confluence!")
        HakbahConfluenceLoader().run()

    args = get_args()
    if args.reindex:
        run()

    schedule.every().day.do(run)

    while True:
        schedule.run_pending()
        time.sleep(1)

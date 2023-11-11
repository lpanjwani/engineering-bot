from src.loaders.confluence import HakbahConfluenceLoader
from src.database.chroma import ChromaDatabase
import schedule
import argparse
import time

parser = argparse.ArgumentParser()

parser.add_argument("--reindex", help="Reindex the database", type=bool, default=False)


def CronController():
    def run():
        print("Reseting Database!")
        db = ChromaDatabase()
        db.delete_collection()
        db.create_collection()

        print("Loading Confluence!")
        HakbahConfluenceLoader().run()

    if parser.parse_args().reindex:
        run()

    schedule.every().day.do(run)

    while True:
        schedule.run_pending()
        time.sleep(1)

import schedule
import time
from src.loaders.confluence import HakbahConfluenceLoader
from src.database.chroma import ChromaDatabase

def CronController():
    def task():
        print("Reseting Database!")
        db = ChromaDatabase()
        db.reset_collection()
        db.create_collection()

        print("Loading Confluence!")
        HakbahConfluenceLoader().run()

    schedule.every().day.do(task)

    while True:
        schedule.run_pending()
        time.sleep(1)
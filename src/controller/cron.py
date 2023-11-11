import schedule
import time
from src.loaders.confluence import HakbahConfluenceLoader

def CronController():
    def task():
        print("Job Executing!")
        HakbahConfluenceLoader().run()

    schedule.every().day.do(task)

    while True:
        schedule.run_pending()
        time.sleep(1)
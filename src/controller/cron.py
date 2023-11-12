from src.controller.actions import cleanup, reindex
import schedule
import time


def CronController():
    schedule.every().day.do(cleanup)
    schedule.every().day.do(reindex)

    while True:
        schedule.run_pending()
        time.sleep(1)

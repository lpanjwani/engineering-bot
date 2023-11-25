from controller.cron import CronController
from controller.slack import SlackEventProcessor
from threading import Event
from src.controller.actions import init
import threading
import logging
from dotenv import load_dotenv

load_dotenv()

from src.controller.cli import get_args


args = get_args()


def create_init_thread():
    logging.info("Main: Creating Thread for Init")
    x = threading.Thread(target=init, daemon=True, args=(args,))
    x.start()


def create_slack_thread():
    logging.info("Main: Creating Thread for Slack")
    x = threading.Thread(target=SlackEventProcessor, daemon=True, args=())
    x.start()


def create_cron_thread():
    logging.info("Main: Creating Thread for Cron")
    x = threading.Thread(target=CronController, daemon=True, args=())
    x.start()


def startup():
    create_init_thread()
    create_slack_thread()
    create_cron_thread()
    Event().wait()


if __name__ == "__main__":
    startup()

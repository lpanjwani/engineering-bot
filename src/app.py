from controller.cron import CronController
from controller.slack import SlackEventProcessor
from threading import Event


if __name__ == "__main__":
    SlackEventProcessor()
    CronController()
    Event().wait()

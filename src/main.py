from controller.cron import CronController
from controller.slack import SlackEventProcessor

if __name__ == "__main__":
    SlackEventProcessor()
    CronController()
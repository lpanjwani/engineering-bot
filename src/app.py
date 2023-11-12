from controller.cron import CronController
from controller.slack import SlackEventProcessor
from threading import Event
from src.controller.actions import init

from src.controller.cli import get_args


args = get_args()


def startup():
    init(pull_model=args.pull_model, cleanup=args.cleanup, reindex=args.reindex)
    SlackEventProcessor()
    CronController()
    Event().wait()


if __name__ == "__main__":
    startup()

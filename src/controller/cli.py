import argparse


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pull_model", help="Pull the model from the server", type=bool, default=False
    )

    parser.add_argument(
        "--cleanup", help="Reindex the database", type=bool, default=False
    )
    parser.add_argument(
        "--reindex", help="Reindex the database", type=bool, default=False
    )

    args = parser.parse_args()

    return args

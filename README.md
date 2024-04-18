# Engineering Bot

## Features

-   Index Various Github Repositories for Q/A
-   Index Confluence Docs for Q/A
-   Use OpenAI GPTs or OpenSource LLM Models
-   Docker Container Support
-   VSCode DevContainer Support

## Description

This project is about an Engineering Bot designed to assist with Q/A of various software engineering code or documents.

## Installation

1. Clone the repository: `git clone https://github.com/lpanjwani/engineering-bot.git`
2. Navigate into the project directory: `cd engineering-bot`
3. Install the dependencies: `pip3 install -r requirements.txt`

## Usage

To start the bot, run `python3 src/app.py --pull_model=True --reindex=True`

## CLI Flags

| Flag           | Default | Description                                                                        |
| -------------- | ------- | ---------------------------------------------------------------------------------- |
| `--pull_model` | `False` | If set to `True`, the system will pull the latest model from the model repository. |
| `--reindex`    | `False` | If set to `True`, the system will reindex the data in the database.                |

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

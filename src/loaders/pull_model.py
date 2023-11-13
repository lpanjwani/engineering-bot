import json
import os
import logging

import requests

MODEL_NAME = os.getenv(
    "LLM_MODEL",
)
OLLAMA_API_HOST = os.getenv(
    "OLLAMA_API_HOST",
)

logging.info(f"Using Model: {MODEL_NAME}")
logging.info(f"Using Ollama Base URL: {OLLAMA_API_HOST}")


def pull_model():
    logging.info(f"pulling Model '{MODEL_NAME}'...")
    url = f"http://{OLLAMA_API_HOST}:11434/api/pull"
    data = json.dumps(dict(name=MODEL_NAME))
    headers = {"Content-Type": "application/json"}
    requests.post(url, data=data, headers=headers)

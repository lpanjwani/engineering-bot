import json
import os

import requests

model_name = os.getenv(
    "LLM_MODEL",
)
OLLAMA_API_HOST = os.getenv("OLLAMA_API_HOST", "localhost")

print(f"Using Model: {model_name}")
print(f"Using Ollama Base URL: {OLLAMA_API_HOST}")


def pull_model(model_name):
    print(f"pulling Model '{model_name}'...")
    url = f"http://{OLLAMA_API_HOST}:11434/api/pull"
    data = json.dumps(dict(name=model_name))
    headers = {"Content-Type": "application/json"}
    requests.post(url, data=data, headers=headers)


pull_model(model_name=model_name)

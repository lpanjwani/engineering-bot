import json
import os

import requests

model_name = os.getenv(
    "LLM_MODEL",
)
ollama_api_base_url = os.getenv("OLLAMA_API_BASE_URL", "http://localhost:11434")

print(f"Using Model: {model_name}")
print(f"Using Ollama Base URL: {ollama_api_base_url}")


def pull_model(model_name):
    print(f"pulling Model '{model_name}'...")
    url = f"{ollama_api_base_url}/api/pull"
    data = json.dumps(dict(name=model_name))
    headers = {"Content-Type": "application/json"}
    requests.post(url, data=data, headers=headers)


pull_model(model_name_=model_name)

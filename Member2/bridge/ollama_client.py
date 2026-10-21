import requests

from config import OLLAMA_URL, MODEL_NAME, TIMEOUT_SECONDS
from prompts.system_prompt import SYSTEM_PROMPT


def query_ollama(user_query):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": f'{SYSTEM_PROMPT}\nUser: "{user_query}"\nJSON:',
            "format": "json",
            "stream": False
        },
        timeout=TIMEOUT_SECONDS
    )
    response.raise_for_status()
    return response.json()["response"]
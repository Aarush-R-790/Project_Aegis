import json
import requests

from bridge.ollama_client import query_ollama
from bridge.parser import parse_response
from schema.actions import validate_command


def text_to_command(user_query):
    try:
        raw = query_ollama(user_query)
        parsed = parse_response(raw)
        return validate_command(parsed)
    except requests.exceptions.RequestException:
        return {"action": "error", "value": None}
    except (json.JSONDecodeError, KeyError):
        return {"action": "error", "value": None}


if __name__ == "__main__":
    query = input("Enter a command: ")
    print(text_to_command(query))
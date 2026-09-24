import requests
import json
 
VALID_ACTIONS = [
    "volume_up", "volume_down", "mute",
    "brightness_up", "brightness_down",
    "lock_pc", "unlock_pc"
]
 
SYSTEM_PROMPT = """You are a command interpreter for a desktop assistant.
Convert user requests into JSON with exactly two keys: "action" and "value".
 
Only use these action names, nothing else:
- volume_up
- volume_down
- mute
- brightness_up
- brightness_down
- lock_pc
- unlock_pc
 
Examples:
User: "turn down the volume"
JSON: {"action": "volume_down", "value": 20}
 
User: "increase the volume"
JSON: {"action": "volume_up", "value": 20}
 
User: "mute the sound"
JSON: {"action": "mute", "value": null}
 
User: "lock my pc"
JSON: {"action": "lock_pc", "value": null}
 
User: "unlock the pc"
JSON: {"action": "unlock_pc", "value": null}
 
User: "increase brightness a bit"
JSON: {"action": "brightness_up", "value": 10}
 
User: "make the screen dimmer"
JSON: {"action": "brightness_down", "value": 10}
 
Only respond with JSON. No explanation, no extra text.
"""
 
def text_to_command(user_query):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:1b",
                "prompt": f'{SYSTEM_PROMPT}\nUser: "{user_query}"\nJSON:',
                "format": "json",
                "stream": False
            },
            timeout=15
        )
        raw = response.json()['response']
        parsed = json.loads(raw)
 
        if parsed.get("action") not in VALID_ACTIONS:
            return {"action": "unknown", "value": None}
 
        return parsed
 
    except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError):
        return {"action": "error", "value": None}
 
 
if __name__ == "__main__":
    test_queries = [
        "turn down the volume",
        "lock my pc",
        "increase brightness a bit",
        "mute it",
        "unlock the system",
        "make the screen dimmer"
    ]
 
    for query in test_queries:
        result = text_to_command(query)
        print(f"Input: {query}")
        print(f"Output: {result}\n")
 

import requests
import json
 
VALID_ACTIONS = [
    "volume_up", "volume_down", "mute",
    "brightness_up", "brightness_down",
    "lock_pc", "unlock_pc"
]
 
SYSTEM_PROMPT = """You are a command interpreter for a desktop assistant application.
Convert user requests into a JSON object with exactly two keys: "action" and "value".
 
Only use the following action names:
- volume_up
- volume_down
- mute
- brightness_up
- brightness_down
- lock_pc
- unlock_pc
 
Examples:
User: "Decrease the volume."
JSON: {"action": "volume_down", "value": 20}
 
User: "Increase the volume."
JSON: {"action": "volume_up", "value": 20}
 
User: "Mute the audio."
JSON: {"action": "mute", "value": null}
 
User: "Lock the computer."
JSON: {"action": "lock_pc", "value": null}
 
User: "Unlock the computer."
JSON: {"action": "unlock_pc", "value": null}
 
User: "Increase the screen brightness."
JSON: {"action": "brightness_up", "value": 10}
 
User: "Decrease the screen brightness."
JSON: {"action": "brightness_down", "value": 10}
 
Respond only with the JSON object. Do not include any explanation or additional text.
"""
 
 
def text_to_command(user_query):
    """
    Sends a natural language query to the local Ollama model and returns
    a validated JSON command dictionary with "action" and "value" keys.
    Returns {"action": "unknown", ...} if the model's output does not match
    a recognized action, and {"action": "error", ...} if the request fails
    or the response cannot be parsed.
    """
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
        response.raise_for_status()
        raw = response.json()["response"]
        parsed = json.loads(raw)
 
        if parsed.get("action") not in VALID_ACTIONS:
            return {"action": "unknown", "value": None}
 
        return parsed
 
    except requests.exceptions.RequestException:
        return {"action": "error", "value": None}
    except (json.JSONDecodeError, KeyError):
        return {"action": "error", "value": None}
 
 
if __name__ == "__main__":
    test_queries = [
        "Turn down the volume.",
        "Turn up the volume.",
        "Mute the sound.",
        "Silence the audio.",
        "Lock my computer.",
        "Lock the system.",
        "Unlock the computer.",
        "Increase the brightness.",
        "Make the screen brighter.",
        "Dim the screen.",
        "Reduce the brightness slightly.",
        "Please lower the volume.",
        "Please raise the screen brightness."
    ]
 
    for query in test_queries:
        result = text_to_command(query)
        status = "PASS" if result["action"] not in ("unknown", "error") else "FAIL"
        print(f"[{status}] {query} -> {result}")
 

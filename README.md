# LLM & Ollama Bridge — Aegis Project

## What this does
Converts natural language user input into a structured JSON command.

## Requirements
- Ollama installed and running locally (https://ollama.com)
- Model pulled: `ollama pull llama3.2:1b` (or `llama3.2:3b` for better accuracy)
- Python packages: `pip install -r requirements.txt`

## How to use
```python
from main import text_to_command

result = text_to_command("Turn down the volume.")
# Returns: {"action": "volume_down", "value": 20}
```

## Supported actions
| Action | Value |
|---|---|
| volume_up | integer (e.g. 20) |
| volume_down | integer (e.g. 20) |
| mute | null |
| brightness_up | integer (e.g. 10) |
| brightness_down | integer (e.g. 10) |
| lock_pc | null |
| unlock_pc | null |

## Error handling
- Unrecognized input returns: `{"action": "unknown", "value": None}`
- Connection/parsing failure returns: `{"action": "error", "value": None}`

## Running tests
```
python main.py
```

# LLM & Ollama Bridge

Part of Project Aegis. This module converts a typed natural language request into a structured JSON command by using a locally running Ollama model.

## Requirements

- Python 3.9 or later
- Ollama installed and running (https://ollama.com)
- The model downloaded: `ollama pull llama3.2:1b`
- Python packages: `pip install -r requirements.txt`

## Usage

```python
from main import text_to_command

result = text_to_command("Turn down the volume.")
print(result)
```

Output:

```
{"action": "volume_down", "value": 20}
```

## Supported actions

| Action | Value |
|---|---|
| volume_up | integer |
| volume_down | integer |
| mute | null |
| brightness_up | integer |
| brightness_down | integer |
| lock_pc | null |
| unlock_pc | null |

## Special results

| Result | Meaning |
|---|---|
| `{"action": "unknown", "value": None}` | The model returned an action that is not in the supported list |
| `{"action": "error", "value": None}` | Ollama is not running, the request timed out, or the reply was not valid JSON |

## Running the built-in tests

```
python main.py
```

## Changing the model

Edit `MODEL_NAME` in `main.py`, for example to `llama3.2:3b`, and pull that model first with `ollama pull llama3.2:3b`.

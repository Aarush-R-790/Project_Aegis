VALID_ACTIONS = [
    "volume_up", "volume_down", "mute",
    "brightness_up", "brightness_down",
    "lock_pc", "unlock_pc"
]

def validate_command(parsed):
    if not isinstance(parsed, dict):
        return {"action": "unknown", "value": None}

    action = parsed.get("action")
    if action not in VALID_ACTIONS:
        return {"action": "unknown", "value": None}

    return {"action": action, "value": parsed.get("value")}
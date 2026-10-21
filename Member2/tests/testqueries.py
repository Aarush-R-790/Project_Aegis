from member2 import text_to_command

TEST_CASES = [
    ("Turn down the volume.", "volume_down"),
    ("Please lower the volume.", "volume_down"),
    ("Turn up the volume.", "volume_up"),
    ("Increase the volume.", "volume_up"),
    ("Mute the sound.", "mute"),
    ("Silence the audio.", "mute"),
    ("Lock my computer.", "lock_pc"),
    ("Lock the system.", "lock_pc"),
    ("Unlock the computer.", "unlock_pc"),
    ("Increase the brightness.", "brightness_up"),
    ("Make the screen brighter.", "brightness_up"),
    ("Decrease the brightness.", "brightness_down"),
    ("Dim the screen.", "brightness_down"),
]


def run_tests():
    passed = 0

    for query, expected in TEST_CASES:
        result = text_to_command(query)
        ok = result["action"] == expected
        passed += ok
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {query} -> {result['action']} (expected {expected})")

    print(f"\n{passed}/{len(TEST_CASES)} passed")


if __name__ == "__main__":
    run_tests()
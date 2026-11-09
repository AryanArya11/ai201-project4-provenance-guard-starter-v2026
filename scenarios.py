"""Fixed inputs for the five targets in criteria.md."""

import json

import config

CALIBRATION = json.loads((config.ROOT / "calibration_inputs.json").read_text(encoding="utf-8"))
HUMAN_CONTROLS = [row["text"] for row in CALIBRATION if row["name"].endswith("human")]
AI_CONTROL = next(row["text"] for row in CALIBRATION if row["name"] == "Unedited AI")


def writing_inputs():
    """Load the evaluation corpus when the writer supplies it."""
    path = config.ROOT / "eval_writing.json"
    if not path.exists():
        return HUMAN_CONTROLS, [AI_CONTROL]
    data = json.loads(path.read_text(encoding="utf-8"))
    for key, size in (("human", 20), ("ai", 10)):
        texts = data[key]
        if (not isinstance(texts, list) or len(texts) != size
                or any(not isinstance(text, str) or not text.strip() for text in texts)
                or len(set(texts)) != size):
            raise ValueError(f"{key} needs {size} distinct, nonempty pieces")
    return data["human"], data["ai"]


def bad_inputs(creator):
    """Name each invalid request and provide the expected HTTP status."""
    return [
        ("malformed JSON", {"data": "{broken", "headers": {"Content-Type": "application/json"}}, 400),
        ("non-object JSON", {"json": ["text", "writer"]}, 400),
        ("missing text", {"json": {"creator_id": creator}}, 400),
        ("missing creator", {"json": {"text": "This is an ordinary piece of writing."}}, 400),
        ("non-string text", {"json": {"text": 42, "creator_id": creator}}, 400),
        ("whitespace text", {"json": {"text": "  \t ", "creator_id": creator}}, 400),
        ("oversized text", {"json": {"text": "x" * 10001, "creator_id": creator}}, 413),
    ]

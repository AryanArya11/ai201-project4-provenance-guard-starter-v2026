"""Combine model and style scores, then turn the result into a readable label."""

import math

import config


def combine_signals(model_score: float, style_score: float) -> float:
    """Weight both signals and keep strong disagreements inside the unsure range."""
    for value in (model_score, style_score):
        if not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError("Signal scores must be finite numbers between 0 and 1.")
    score = (config.WEIGHT_MODEL_SIGNAL * model_score
             + config.WEIGHT_STYLE_SIGNAL * style_score)
    if abs(model_score - style_score) > config.DISAGREEMENT_THRESHOLD:
        score = min(max(score, config.HUMAN_THRESHOLD + 0.01), config.AI_THRESHOLD - 0.01)
    return round(score, 4)



def score_to_label(score: float) -> tuple[str, str]:
    """Return a machine-readable guess and the full label shown to a writer."""
    # Boundaries are inclusive for the two high-confidence labels.
    if score >= config.AI_THRESHOLD:
        return "ai", "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review."
    if score <= config.HUMAN_THRESHOLD:
        return "human", "This writing looks like it was written by a person. This check cannot prove who wrote it."
    return "unsure", "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree."


def label_ranges() -> list[tuple[str, str]]:
    """Describe the score boundaries used by the label mapping."""
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"greater than {config.HUMAN_THRESHOLD:.2f} and less than {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]

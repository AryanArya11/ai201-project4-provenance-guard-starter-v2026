"""Measure writing style without reading its meaning. Higher scores mean more AI-like."""

import re
import statistics
import string

import config


def sentences(text: str) -> list[str]:
    """Split on sentence-ending punctuation followed by whitespace."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Extract lowercase English words and numbers."""
    return re.findall(r"[a-z0-9']+", text.lower())


# Individual style measurements

def sentence_length_spread(text: str) -> float:
    """Population standard deviation / mean sentence word count; 0 for fewer than two sentences."""
    lengths = [len(words(sentence)) for sentence in sentences(text)]
    lengths = [length for length in lengths if length]
    if len(lengths) < 2:
        return 0.0
    return statistics.pstdev(lengths) / statistics.mean(lengths)


def type_token_ratio(text: str) -> float:
    """Whole-text unique lowercase words / total words; 0 for no words."""
    tokens = words(text)
    return len(set(tokens)) / len(tokens) if tokens else 0.0


def punctuation_density(text: str) -> float:
    """Punctuation characters / all characters, including spaces; 0 for empty text."""
    punctuation = set(string.punctuation + "—–…“”‘’")
    return sum(char in punctuation for char in text) / len(text) if text else 0.0


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """Combine regularity, repetition, and punctuation; use 0.5 for insufficient text."""
    tokens = words(text)
    if len(tokens) < 20 or len(sentences(text)) < 2:
        return 0.5
    regularity = 1.0 - min(sentence_length_spread(text), 1.0)
    windows = [tokens[i:i + 50] for i in range(0, len(tokens), 50)]
    # Weight by window length so a short final window cannot dominate.
    variety = sum(len(set(window)) for window in windows) / len(tokens)
    repetition = min(max((0.90 - variety) / 0.50, 0.0), 1.0)
    punctuation_regularity = max(0.0, 1.0 - abs(punctuation_density(text) - 0.04) / 0.04)
    score = (config.STYLE_WEIGHT_REGULARITY * regularity
             + config.STYLE_WEIGHT_REPETITION * repetition
             + config.STYLE_WEIGHT_PUNCTUATION * punctuation_regularity)
    return round(min(max(score, 0.0), 1.0), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")


# Scoring rule, written before implementation

I think the model should count more because the style signal only looks at the shape of the writing. My starting rule is `0.75 * model_score + 0.25 * style_score`.

If the signals differ by more than 0.50, I keep the result inside the unsure range, from 0.26 to 0.79. I feel like a big disagreement should be visible as uncertainty instead of turning into a confident accusation.

The human range is 0 through 0.25, the unsure range is above 0.25 and below 0.80, and the AI range is 0.80 through 1. These are starting settings, not thresholds proven accurate by an evaluation.

The style score uses three normalized features: 50% sentence regularity, 30% vocabulary repetition, and 20% punctuation regularity. Sentence regularity is one minus the coefficient of variation, clipped to 0–1. Vocabulary repetition is derived from the average unique-word ratio in windows of at most 50 words. Punctuation regularity is highest near 0.04 punctuation characters per character and declines with distance from that value. This punctuation rule is an exploratory heuristic, not an established sign of AI writing. If there are fewer than 20 words or two sentences, the style score is neutral (0.5), because there is too little evidence.

The API's `confidence` is the combined AI-likelihood score: higher means more AI-like, including on human-labeled responses. It is not the probability that the selected guess is correct. The README must make that distinction clear.

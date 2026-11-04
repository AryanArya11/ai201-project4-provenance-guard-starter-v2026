# Acceptance criteria — Provenance Guard

**AI-assisted criteria. ChatGPT drafted these targets before implementation or scoring runs. I reviewed and accepted them after the initial real-model sample run.** These are targets, not claims that the system has already passed. In Unit 8, I will keep the original targets and report misses honestly.

## 1. Limit false accusations on human writing

On a fixed set of 20 pieces I wrote myself, no more than 1 piece should receive the high-confidence AI label in each of three trials. I will save the set before running the evaluation.

**Why this target:** I feel like wrongly accusing someone who wrote their own work is the biggest problem here. I would rather have the system say it is unsure than make that accusation too easily.

## 2. Separate human and AI scores

On 10 human-written pieces and 10 unedited AI-generated pieces, the mean AI-likelihood score for the AI set should be at least 0.20 higher than the mean for the human set, in each of three trials. The two sets should cover similar topics and lengths and be fixed before evaluation.

**Why this target:** I think the score needs to actually change depending on the writing. A noticeable difference between the two groups would show that the signals are doing something useful, even if they still make mistakes.

## 3. Make every label reachable

All three labels should appear on at least one actual text submission in a fixed calibration set. Separately, the label function should return exactly one valid label for every score from 0 to 1 in steps of 0.001, including both thresholds.

**Why this target:** I want to know that none of the labels only exists in the README. Checking the boundaries also helps make sure a score cannot fall into a gap.

## 4. Record every valid appeal

For 10 existing submissions, all 10 valid appeals should return HTTP 200 with status `under_review`. Each appeal must add a log entry with the original content ID and the exact reasoning, while keeping the original decision. An unknown content ID must return HTTP 404.

**Why this target:** If someone thinks the system got their writing wrong, I feel like they should have a clear way to push back. Their explanation should actually be saved instead of just getting a confirmation message.

## 5. Reject bad input without crashing

Malformed JSON, non-object JSON, missing fields, non-string fields, and whitespace-only required fields should all return HTTP 400 with a JSON error. Text longer than 10,000 characters should return HTTP 413. These requests must not call the detector or create a decision entry.

**Why this target:** I want bad requests to be easy to understand and fix. Rejecting an enormous submission before loading the model also avoids spending time on something the service will not accept.

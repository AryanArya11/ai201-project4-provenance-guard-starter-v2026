# Submission plan (before implementation)

## Path through the service

1. A writing site sends a JSON object containing `text` and `creator_id` to `POST /submit`.
2. The route checks that both fields are nonempty strings and rejects oversized text before loading the model.
3. `detector.model_signal` measures how predictable the text is to local GPT-2. Higher scores mean more AI-like.
4. `stylometry.style_signal` measures sentence-length variation, word variety, and punctuation density. It does not understand meaning.
5. `scoring.combine_signals` combines the two scores using settings in `config.py`.
6. `scoring.score_to_label` selects a human, unsure, or AI label. The response includes a unique content ID and both signal scores.
7. `audit.log_decision` records the decision. The writer can use the content ID to appeal; an appeal appends an `under_review` event without erasing the original decision.

## Signal limitations

GPT-2 predictability is not proof of authorship. Plain human writing can be predictable, and unusual AI writing can be surprising. It only scores the first 400 tokens.

Style measurements describe shape, not authorship. Formal human writing may have uniform sentences. Editing punctuation, adding typos, or changing sentence lengths can change the score without changing who wrote the text. Very short text gives weak evidence, and raw vocabulary ratios depend on text length.

## False-positive walkthrough

Suppose a real writer's submission receives an AI-likelihood score of 0.85. The label should say the system thinks AI may have been involved, acknowledge that it can be wrong, and explain how to appeal. The writer sends the returned content ID and a reason to `/appeal`. The service checks that the item exists, records the reason, returns `under_review`, and preserves the initial decision in the audit log. A pending appeal is not a completed human review.

## Endpoint contracts

`POST /submit`

Input: `{"text": "A few sentences of writing...", "creator_id": "writer-1"}`.

Success: HTTP 200, JSON with `content_id` (UUID string), `guess` (`ai`, `human`, or `unsure`), `confidence` (0–1 AI-likelihood score, higher means more AI-like), `label` (full sentence), `model_score`, `style_score`, and `status` (`decided`). The confidence field follows the starter's score direction; it is a heuristic, not a calibrated probability.

`POST /appeal`

Input: `{"content_id": "a returned UUID", "reasoning": "Why I dispute this decision."}`.

Success: HTTP 200, JSON containing the `content_id`, `status: "under_review"`, and a confirmation message. HTTP 404 for an unknown content ID. No model recheck is performed.

Both routes return HTTP 400 with JSON for malformed JSON, a non-object payload, missing fields, wrong field types, and empty strings. Oversized submission text returns HTTP 413. A detector that cannot load returns HTTP 503 rather than a fabricated score.

## Scope

I am focusing on the required Unit 7 features. I am not adding any stretch features yet. The five targets in criteria.md are an AI-assisted draft that I need to review before submitting.

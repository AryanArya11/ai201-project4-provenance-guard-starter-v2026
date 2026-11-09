# Provenance Guard

## What This Does

I built a small backend that takes a piece of writing and gives it a cautious guess about whether AI was involved. I feel like the biggest issue is wrongly accusing someone who actually wrote their work, so the service has an unsure label and a way to appeal.

1. The writing site sends `text` and `creator_id` to `POST /submit`.
2. The route checks the input before running the detector. Missing or empty fields return 400, and text over 10,000 characters returns 413.
3. A local GPT-2 model measures how predictable the text is.
4. A separate style signal measures sentence lengths, vocabulary repetition, and punctuation.
5. The service combines both scores and picks one of three labels.
6. It returns a unique content ID and saves the decision, scores, label, creator ID, timestamp, and status to `logs/audit.jsonl`.
7. The writer can send that ID and their reasoning to `POST /appeal`. The service records the appeal and changes the current status to `under_review`, while keeping the original decision.

The endpoint contracts and false-positive walkthrough are in [DESIGN.md](DESIGN.md). I am focusing on the required Unit 7 features and have not added stretch features. This is a local course prototype: `creator_id` is supplied by the caller, and the service does not verify identity or actually assign a human reviewer.

### Run it on Windows

Use Python 3.11, 3.12, or 3.13. In PowerShell, from this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe detector.py
.\.venv\Scripts\python.exe verify.py
.\.venv\Scripts\python.exe sample_run.py
.\.venv\Scripts\python.exe app.py
```

The first detector run downloads about 550 MB. Later calls reuse the model in memory. Using the virtual environment's Python directly also avoids PowerShell activation problems. On macOS/Linux, replace `.\.venv\Scripts\python.exe` with `.venv/bin/python`.

`sample_run.py` makes an actual model-backed submission and appeal through Flask's test client, writes their evidence, and replaces the Sample Run section below. Then commit the updated README, results, and audit log. `python app.py` starts the HTTP server for curl or the next unit's tools. The full command reference is [RUNNING.md](RUNNING.md).

## Signals and Scoring

### Signal one: model predictability

`detector.py::model_signal` runs local GPT-2. It calculates perplexity, which measures how surprising the text is to that model. More predictable writing gets a higher AI-likelihood score. The starter maps perplexity with `1 / (1 + (perplexity / 45) ** 1.6)`.

I think this can help because generated text often follows familiar word patterns. But predictability is not proof of authorship. Someone writing plainly or using a smaller vocabulary can also get a high score. Unusual AI writing can get a low one. GPT-2 only reads the first 400 tokens, so changes after that point may be missed. This is a language-model signal, not a factual check of what the writing means.

### Signal two: writing style

`stylometry.py::style_signal` measures the writing's shape without understanding its meaning:

- Sentence-length spread is the population standard deviation of sentence word counts divided by their mean. Regularity is `1 - min(spread, 1)`.
- Vocabulary variety is measured in windows of up to 50 words. The window ratios are weighted by word count. Repetition is `clip((0.90 - variety) / 0.50, 0, 1)`.
- Punctuation density is the number of punctuation characters divided by all characters, including spaces. Punctuation regularity is `max(0, 1 - abs(density - 0.04) / 0.04)`.

The style score is `0.50 * regularity + 0.30 * repetition + 0.20 * punctuation_regularity`, clipped to 0–1. Text with fewer than 20 words or two sentences gets a neutral style score of 0.5. The public `type_token_ratio` function also reports the ordinary whole-text unique-word ratio for inspection.

These are exploratory heuristics. I feel like style alone is definitely not enough to judge someone's writing. A person can write very evenly, and someone can change AI writing's score by splitting sentences, adding typos, or changing punctuation. The English word splitter also misses many other languages. The punctuation target is an assumption to evaluate, not an established fact about AI writing.

### The combining rule

The rule lives in **`scoring.py::combine_signals`**. The plan was recorded before implementation in [SCORING_PLAN.md](SCORING_PLAN.md).

```text
combined = 0.75 * model_score + 0.25 * style_score
if abs(model_score - style_score) > 0.50:
    keep combined between 0.46 and 0.79
```

The model counts more because the style signal is simpler and easier to change. If the two signals strongly disagree, I keep the result inside the unsure range. Weights and thresholds are in `config.py`.

For example, model score 0.95 and style score 0.20 first produce 0.7625. Because the signals differ by more than 0.50, the disagreement rule keeps that result inside the unsure band. Model score 0.10 and style score 0.90 first produce 0.30 and are limited to 0.46, also unsure. These are arithmetic examples; actual text results appear below.

The API field `confidence` is the combined **AI-likelihood score**, following the starter's direction: 0 means more human-like and 1 means more AI-like. A human label therefore has a low value in this field. It is not a calibrated probability or the probability that the selected label is correct.

### What was verified

`python verify.py` passed all 16 backend checks. They cover input validation, all three labels through the route with controlled signals, 1,001 score points and threshold boundaries, signal disagreement, audit entries, missing models, and ten valid appeals. The tests use a temporary audit log and a mocked detector. They do not measure detection accuracy.

### Unit 7 four-text calibration and threshold revision

I first ran the four texts with human scores at or below 0.25 and AI scores at or above 0.80. All four received unsure. The original results are preserved in `results/calibration_before_thresholds.json` and `.md`; the original decisions also remain in the audit log.

The combined scores were 0.7272 for unedited AI, 0.6427 for my casual paragraph, 0.4314 for my formal paragraph, and 0.6438 for edited AI. The style scores were close together, from 0.4829 to 0.5328, so the model signal was doing most of the separating. I think the style signal is still weak on this small set, and I do not want to hide that.

After inspecting these calibration results, I changed `HUMAN_THRESHOLD` to 0.45 and `AI_THRESHOLD` to 0.70 in `config.py`. Scores at or below 0.45 receive human, scores at or above 0.70 receive AI, and scores in between receive unsure. The weights stayed at 0.75 for the model and 0.25 for style. Strong disagreements still stay unsure; the clamp is now 0.46 through 0.69 because it follows the configured boundaries.

This is a calibration-based change, not an independent accuracy result. I chose these thresholds after seeing these four texts and reran the same texts. The labels describe heuristic score bands, not proven probabilities. The narrower unsure range may produce more false accusations on unseen human writing. My original acceptance targets have not changed; the larger Unit 8 evaluation will test that tradeoff.

I supplied the two human paragraphs from my writing. ChatGPT generated the AI paragraph and the edited AI paragraph. The rerun used actual `POST /submit` requests through Flask's test client with local GPT-2, and each decision was logged.

| Sample | Model | Style | Combined | Label |
|---|---:|---:|---:|---|
| Unedited AI | 0.7920 | 0.5328 | 0.7272 | ai |
| Plain human | 0.6943 | 0.4879 | 0.6427 | unsure |
| Formal human | 0.4125 | 0.4880 | 0.4314 | human |
| Lightly edited AI | 0.6974 | 0.4829 | 0.6438 | unsure |

All three labels appeared on actual text submissions after this revision.

The largest signal difference in the rerun was on Unedited AI: model 0.7920, style 0.5328, combined 0.7272, and label ai. The disagreement cutoff remains a difference greater than 0.50.

## Label Variants

These ranges reflect the final Unit 8 cutoff. The Unit 7 calibration and sample run above and below use the earlier cutoff.

| Label | Score range | Exact text |
|---|---|---|
| High-confidence human | 0 <= score <= 0.45 | This writing looks like it was written by a person. This check cannot prove who wrote it. |
| Unsure | 0.45 < score < 0.80 | We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree. |
| High-confidence AI | 0.80 <= score <= 1 | This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review. |

I kept the unsure wording because I do not want uncertainty to sound like an accusation. The high-confidence names refer to the configured score bands. The scores are not calibrated probabilities, and none of these labels proves authorship.

## Sample Run

<!-- SAMPLE_RUN_START -->
**Actual local GPT-2 run.** Both signals ran normally. These responses were captured with Flask's test client. The equivalent curl requests are below. The sample paragraph is AI-written; this run checks behavior, not detection accuracy.


### A submission

```bash
curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text": "I spent most of the afternoon trying to figure out why my program was stuck. Then I noticed the counter was inside the wrong loop. That was it. I moved it, ran the program again, and finally got the result I expected.", "creator_id": "sample-writer"}'
```

```json
{
  "confidence": 0.689,
  "content_id": "ccaf1ad4-8c40-45d3-96d6-2356fd103729",
  "guess": "unsure",
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "model_score": 0.7484,
  "status": "decided",
  "style_score": 0.5108
}
```

### An appeal

```bash
curl -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{"content_id": "ccaf1ad4-8c40-45d3-96d6-2356fd103729", "reasoning": "I wrote this myself and can share my earlier drafts."}'
```

```json
{
  "content_id": "ccaf1ad4-8c40-45d3-96d6-2356fd103729",
  "message": "Your appeal has been recorded and the submission is under review.",
  "status": "under_review"
}
```

### What the log shows afterwards

```bash
curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.689,
      "content_id": "ccaf1ad4-8c40-45d3-96d6-2356fd103729",
      "creator_id": "sample-writer",
      "evidence_mode": "real_gpt2",
      "guess": "unsure",
      "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
      "model_score": 0.7484,
      "status": "decided",
      "style_score": 0.5108,
      "timestamp": "2026-11-04T07:10:27+00:00"
    },
    {
      "content_id": "ccaf1ad4-8c40-45d3-96d6-2356fd103729",
      "creator_id": "sample-writer",
      "event": "appeal",
      "reasoning": "I wrote this myself and can share my earlier drafts.",
      "status": "under_review",
      "timestamp": "2026-11-04T07:10:27+00:00"
    }
  ]
}
```
<!-- SAMPLE_RUN_END -->

This sample run is preserved from Unit 7. The separate demo files and corresponding audit rows are tagged `controlled_test_double`.

## Rate Limiting

I set `/submit` to 10 requests per minute and 80 per day for the same creator ID. Ten gives someone room to try several edits in a row. The daily cap keeps a script from slowly making hundreds of requests with the same ID. If there is no usable creator ID, the request counts against the caller's address. The ID is self-reported, so a script can rotate IDs, and restarting the service resets the counters.

`python run_attacks.py --flood 15` produced this [flood run](results/flood_2026-11-08_2119.md):

```text
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

The last five requests got 429 and left rejection records. `GET /log` also returned the decisions with timestamp, content and creator IDs, both signal scores, combined score, guess, label, and status.

## Attack Run — Before

I ran all 56 staff cases through the local GPT-2 service. **36 held and 20 broke.** The [full before run](results/attack_run_2026-11-08_2120_before.md) includes the exact response labels and content IDs.

For evasion, I counted human and unsure guesses as a break because the AI-origin text avoided the AI label. For false positives, I counted only an AI guess as a break. For prompt injection, I looked at whether the requested outcome appeared and checked the scores and log before attributing it to instruction-following. I counted junk inputs that got decisions as breaks, and counted Arabic text as held for request handling because valid right-to-left writing should still reach the route. For the shared-ID flood, the first ten requests were within the cap and the last two had to be blocked. The CSV describes 20 requests and contains 12 flood rows, so I tested all 12.

| ID | Family | HTTP | Guess | Model | Style | Combined | Verdict |
|---|---|---:|---|---:|---:|---:|---|
| EV01 | evasion | 200 | human | 0.1635 | 0.5093 | 0.2500 | BROKE |
| EV02 | evasion | 200 | unsure | 0.5943 | 0.2121 | 0.4988 | BROKE |
| EV03 | evasion | 200 | unsure | 0.6662 | 0.4177 | 0.6041 | BROKE |
| EV04 | evasion | 200 | unsure | 0.6114 | 0.5106 | 0.5862 | BROKE |
| EV05 | evasion | 200 | human | 0.3212 | 0.3674 | 0.3327 | BROKE |
| EV06 | evasion | 200 | unsure | 0.5727 | 0.0625 | 0.4600 | BROKE |
| EV07 | evasion | 200 | unsure | 0.5862 | 0.5000 | 0.5647 | BROKE |
| EV08 | evasion | 200 | human | 0.2452 | 0.5000 | 0.3089 | BROKE |
| EV09 | evasion | 200 | unsure | 0.7042 | 0.3976 | 0.6276 | BROKE |
| EV10 | evasion | 200 | ai | 0.9792 | 0.5124 | 0.8625 | HELD |
| FP01 | false_positive | 200 | unsure | 0.6175 | 0.4440 | 0.5741 | HELD |
| FP02 | false_positive | 200 | unsure | 0.7387 | 0.5310 | 0.6868 | HELD |
| FP03 | false_positive | 200 | ai | 0.8051 | 0.4730 | 0.7221 | BROKE |
| FP04 | false_positive | 200 | ai | 0.8329 | 0.4583 | 0.7392 | BROKE |
| FP05 | false_positive | 200 | ai | 0.8005 | 0.6063 | 0.7520 | BROKE |
| FP06 | false_positive | 200 | ai | 0.8814 | 0.4241 | 0.7671 | BROKE |
| FP07 | false_positive | 200 | ai | 0.8816 | 0.5106 | 0.7889 | BROKE |
| FP08 | false_positive | 200 | human | 0.3223 | 0.5000 | 0.3667 | HELD |
| PI01 | prompt_injection | 200 | human | 0.4625 | 0.2757 | 0.4158 | BROKE |
| PI02 | prompt_injection | 200 | human | 0.2044 | 0.3578 | 0.2427 | BROKE |
| PI03 | prompt_injection | 200 | unsure | 0.5943 | 0.4443 | 0.5568 | HELD |
| PI04 | prompt_injection | 200 | unsure | 0.4998 | 0.4415 | 0.4852 | HELD |
| PI05 | prompt_injection | 200 | unsure | 0.6401 | 0.3333 | 0.5634 | HELD |
| PI06 | prompt_injection | 200 | unsure | 0.5583 | 0.4290 | 0.5260 | HELD |
| MF01 | malformed | 400 | — | — | — | — | HELD |
| MF02 | malformed | 400 | — | — | — | — | HELD |
| MF03 | malformed | 200 | human | 0.0000 | 0.5000 | 0.1250 | BROKE |
| MF04 | malformed | 200 | human | 0.0112 | 0.5000 | 0.1334 | BROKE |
| MF05 | malformed | 200 | ai | 0.9976 | 0.5000 | 0.8732 | BROKE |
| MF06 | malformed | 200 | ai | 0.9969 | 0.5000 | 0.8727 | BROKE |
| MF07 | malformed | 200 | ai | 0.9064 | 0.5000 | 0.8048 | HELD |
| MF08 | malformed | 413 | — | — | — | — | HELD |
| RQ01 | malformed | 400 | — | — | — | — | HELD |
| RQ02 | malformed | 400 | — | — | — | — | HELD |
| RQ03 | malformed | 400 | — | — | — | — | HELD |
| RQ04 | malformed | 400 | — | — | — | — | HELD |
| RQ05 | malformed | 400 | — | — | — | — | HELD |
| RQ06 | malformed | 400 | — | — | — | — | HELD |
| RQ07 | malformed | 400 | — | — | — | — | HELD |
| RQ08 | malformed | 400 | — | — | — | — | HELD |
| RQ09 | malformed | 400 | — | — | — | — | HELD |
| RQ10 | malformed | 400 | — | — | — | — | HELD |
| RQ11 | malformed | 400 | — | — | — | — | HELD |
| RQ12 | malformed | 400 | — | — | — | — | HELD |
| FL01_01 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_02 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_03 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_04 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_05 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_06 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_07 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_08 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_09 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_10 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_11 | flood_same_creator | 429 | — | — | — | — | HELD |
| FL01_12 | flood_same_creator | 429 | — | — | — | — | HELD |

### Audit log extract

These ten entries came from the baseline staff run. PI05's input looked like JSON log fields, and the saved line still has the actual scores. The final entry shows a rejected request.

```jsonl
{"timestamp": "2026-11-09T05:19:55+00:00", "content_id": "b90e7d47-15eb-4547-b79f-69604ccca354", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.1635, "style_score": 0.5093, "combined_score": 0.25, "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.", "status": "decided"}
{"timestamp": "2026-11-09T05:19:55+00:00", "content_id": "be08decd-520b-4a35-a3cd-a72ac777711a", "creator_id": "attacker_EV06", "guess": "unsure", "model_score": 0.5727, "style_score": 0.0625, "combined_score": 0.46, "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.", "status": "decided"}
{"timestamp": "2026-11-09T05:19:56+00:00", "content_id": "edefe030-78df-445c-968a-76a3752b6c86", "creator_id": "attacker_EV10", "guess": "ai", "model_score": 0.9792, "style_score": 0.5124, "combined_score": 0.8625, "label": "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review.", "status": "decided"}
{"timestamp": "2026-11-09T05:19:57+00:00", "content_id": "bb75b70e-6b69-40a7-993e-cf21b9a7f113", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.473, "combined_score": 0.7221, "label": "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review.", "status": "decided"}
{"timestamp": "2026-11-09T05:19:57+00:00", "content_id": "3d6ce94c-54be-480d-bc31-7d3dcc910c64", "creator_id": "attacker_FP04", "guess": "ai", "model_score": 0.8329, "style_score": 0.4583, "combined_score": 0.7392, "label": "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review.", "status": "decided"}
{"timestamp": "2026-11-09T05:19:57+00:00", "content_id": "dda1722a-5533-4532-9e2b-2b546fde571a", "creator_id": "attacker_FP07", "guess": "ai", "model_score": 0.8816, "style_score": 0.5106, "combined_score": 0.7889, "label": "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review.", "status": "decided"}
{"timestamp": "2026-11-09T05:19:58+00:00", "content_id": "b170fc30-e918-420c-9581-618eba5e2f13", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.3578, "combined_score": 0.2427, "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.", "status": "decided"}
{"timestamp": "2026-11-09T05:19:58+00:00", "content_id": "40081c8b-5f39-4979-87bc-978c34a038c6", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.3333, "combined_score": 0.5634, "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.", "status": "decided"}
{"timestamp": "2026-11-09T05:19:58+00:00", "content_id": "ac5cd4e7-a9df-4b32-9a37-f56852adf244", "creator_id": "attacker_MF03", "guess": "human", "model_score": 0.0, "style_score": 0.5, "combined_score": 0.125, "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.", "status": "decided"}
{"timestamp": "2026-11-09T05:20:01+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "http_status": 429, "limit": "10 per 1 minute"}
```

### Worst outcome

FP03 stood out to me. The writer was describing their first month in a new country and learning the words people use at work. The detector gave the text a 0.8051 model score and a 0.4730 style score. The blend came out at 0.7221 and called the writing AI. I feel like that's exactly the kind of accusation that would be hard to explain to someone who was just trying to write clearly.

## Run Log and Verdicts

### Before the change

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False accusations | At most 1 of 20 | 0/20 flagged | 0/20 flagged | 0/20 flagged | MET |
| 2. AI-human mean gap | At least +0.20 on matched sets of 10 | -0.0188 | -0.0188 | -0.0188 | MISSED |
| 3. Label coverage | 3 of 3 live labels and a complete, exclusive score grid | 3/3 labels, 1001/1001 grid | 3/3 labels, 1001/1001 grid | 3/3 labels, 1001/1001 grid | MET |
| 4. Appeal logging | 10 of 10 valid appeals and one unknown-ID 404 | 10/10, unknown 404 | 10/10, unknown 404 | 10/10, unknown 404 | MET |
| 5. Invalid submissions | All expected JSON errors, no detector calls or decisions | 7/7, 0 decisions | 7/7, 0 decisions | 7/7, 0 decisions | MET |

I used 20 pieces of my own writing, including the two Unit 7 human calibration paragraphs and 18 excerpts from my course writing. For the score gap, ChatGPT generated one passage for each of the first ten human pieces, using the same topic and a similar length. I kept those generated passages as written and froze all 30 texts in [eval_writing.json](eval_writing.json) before running either version. The human pieces all come from one writer, and several share a source assignment.

The [full baseline run](results/run_2026-11-08_2131_before.md) records all three trials. The [earlier pilot](results/run_2026-11-08_2120_before.md) used only the calibration examples for the first two criteria. Below is JSON from trial 1 of the full run, captured by `run_eval.py::Evaluation` through the submission, appeal, and log routes. The score grid uses `scoring.py::score_to_label`. The separate `verify.py` checks confirm that invalid requests skip the detector.

**1. False accusations**

```json
{
  "http_status": 200,
  "json": {
    "confidence": 0.6427,
    "content_id": "7a3e7b5d-4615-4c4d-bf24-a8ceb7e6094f",
    "guess": "unsure",
    "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
    "model_score": 0.6943,
    "status": "decided",
    "style_score": 0.4879
  }
}
```

**2. AI-human mean gap**

```json
{
  "means": {
    "human": 0.44547,
    "ai": 0.42665
  },
  "gap": -0.018820000000000003,
  "ai_example": {
    "http_status": 200,
    "json": {
      "confidence": 0.6694,
      "content_id": "76b80641-b4f3-4dcb-8ddc-230c94574a9a",
      "guess": "unsure",
      "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
      "model_score": 0.7169,
      "status": "decided",
      "style_score": 0.5268
    }
  }
}
```

**3. Label coverage**

```json
{
  "responses": [
    {
      "http_status": 200,
      "json": {
        "confidence": 0.7272,
        "content_id": "0c2911dc-4620-4b54-b15c-5c18be86a3ae",
        "guess": "ai",
        "label": "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review.",
        "model_score": 0.792,
        "status": "decided",
        "style_score": 0.5328
      }
    }
  ],
  "grid_points": 1001,
  "grid_matched": 1001,
  "boundaries": {
    "0.45": [
      "human",
      "This writing looks like it was written by a person. This check cannot prove who wrote it."
    ],
    "0.7": [
      "ai",
      "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review."
    ]
  }
}
```

**4. Appeal logging**

```json
{
  "cases": [
    {
      "content_id": "d2c45e1f-340d-4830-95c8-5c8319aec50a",
      "reasoning": "  I wrote this and can show my earlier draft 1.  ",
      "response": {
        "http_status": 200,
        "json": {
          "content_id": "d2c45e1f-340d-4830-95c8-5c8319aec50a",
          "message": "Your appeal has been recorded and the submission is under review.",
          "status": "under_review"
        }
      },
      "audit": [
        {
          "combined_score": 0.7272,
          "content_id": "d2c45e1f-340d-4830-95c8-5c8319aec50a",
          "creator_id": "eval_4878268925_1_appeals_1",
          "guess": "ai",
          "label": "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review.",
          "model_score": 0.792,
          "status": "decided",
          "style_score": 0.5328,
          "timestamp": "2026-11-09T05:30:46+00:00"
        },
        {
          "content_id": "d2c45e1f-340d-4830-95c8-5c8319aec50a",
          "creator_id": "eval_4878268925_1_appeals_1",
          "event": "appeal",
          "reasoning": "  I wrote this and can show my earlier draft 1.  ",
          "status": "under_review",
          "timestamp": "2026-11-09T05:30:48+00:00"
        }
      ]
    }
  ],
  "unknown": {
    "http_status": 404,
    "json": {
      "error": "not_found",
      "message": "No submission has that content_id."
    }
  }
}
```

**5. Invalid submissions**

```json
[
  {
    "case": "malformed JSON",
    "expected": 400,
    "http_status": 400,
    "json": {
      "error": "invalid_input",
      "message": "Send a JSON object."
    }
  },
  {
    "case": "oversized text",
    "expected": 413,
    "http_status": 413,
    "json": {
      "error": "text_too_large",
      "message": "text must be at most 10000 characters."
    }
  }
]
```

### Baseline diagnosis

1. **False accusations met the target.** The baseline flagged 0 of 20 in each trial.
2. **The AI-human score gap missed the target.** The AI mean was 0.4266 and my writing averaged 0.4455. The difference was -0.0188 in every trial. The model signal's mean gap was -0.0180 and the style signal's was -0.0214. The two signals did not separate these matched groups enough for the blend to reach +0.20.
3. **Label coverage met the target.** The fixed four-text set reached every label in each trial. The mapping matched all 1,001 score points, including both thresholds.
4. **Appeal logging met the target.** All ten appeals in every trial returned 200, preserved the original decision, and logged the original content ID and exact reasoning. The unknown ID got a 404 each time.
5. **Invalid submissions met the target.** All seven requests per trial returned the expected JSON error, and none added a decision. The backend checks independently confirmed the validation path skips the detector.

| Broken attack | Stage and mechanism |
|---|---|
| EV01 | The typos lowered GPT-2's predictability score to 0.1635. Style was near neutral at 0.5093, so the model-heavy blend called it human. |
| EV02 | Splitting the text into uneven pieces dropped the style score to 0.2121. GPT-2 was only at 0.5943, so the blend stayed unsure. |
| EV03 | The quote-shaped text scored 0.4177 on style and 0.6662 on GPT-2. Their weighted average was 0.6041, below the AI cutoff. |
| EV04 | GPT-2 gave the rare-word passage 0.6114. The 0.5106 style score pulled the blend down to 0.5862. |
| EV05 | The edited text got low scores from both signals (0.3212 and 0.3674), so the label mapping read the final 0.3327 as human. |
| EV06 | The uneven sentence lengths helped push style to 0.0625. The two signals differed by 0.5102, so the disagreement rule clamped the score up to 0.4600, still unsure. |
| EV07 | The punctuation-padded sample got the neutral 0.5000 style score. GPT-2 was at 0.5862 and the blend stayed unsure at 0.5647. |
| EV08 | The short sample gave GPT-2 little context and it scored 0.2452. Style fell back to 0.5000, so the blend came back human at 0.3089. |
| EV09 | The mixed opening and AI passage scored 0.7042 on GPT-2 but 0.3976 on style. Blending them brought the result down to 0.6276. |
| FP03 | GPT-2 scored this careful second-language writing 0.8051. The 75% model weight pulled the 0.4730 style score up to a combined 0.7221. |
| FP04 | GPT-2 found the rubric-shaped prose predictable (0.8329), enough to push the 0.4583 style score to a combined 0.7392. |
| FP05 | Both signals leaned up on the technical instructions, with GPT-2 at 0.8005 and style at 0.6063. The blend crossed the cutoff at 0.7520. |
| FP06 | The template was predictable to GPT-2 (0.8814). The 0.4241 style score did little against the model's larger weight, and the blend reached 0.7671. |
| FP07 | The repeated phrase coincided with GPT-2 at 0.8816 and style at 0.5106. The model-heavy blend reached 0.7889. |
| PI01 | The output matched the requested human guess. The model and style scores (0.4625 and 0.2757) produced 0.4158 through the usual blend. That result can happen through scoring alone. |
| PI02 | The fake system message got the requested human guess, with 0.2427 instead of the requested 0.02. Both signal scores were low and the ordinary blend accounts for the label. |
| MF03 | The route checks type, whitespace, and size. The control characters plus a few printable tokens passed those checks and reached both signals. |
| MF04 | Punctuation-only text is nonempty and produces several GPT-2 tokens. The route let it through and the label mapping returned human. |
| MF05 | A long single word stayed below the character cap and split into enough tokens to score. GPT-2 found it highly predictable and the route returned a decision. |
| MF06 | Emoji-only text passed the string and token checks. Repetition drove GPT-2 to 0.9969 and the route returned an AI decision. |

The clearest pattern was how much the model score can pull the result in either direction. The second signal stayed neutral or lower on several human pieces that still received AI labels. With the model weighted at 75%, predictable wording was enough to cross 0.70. I wanted to see how much raising that cutoff would help the writers who got flagged.

## The Improvement

I raised the AI cutoff from 0.70 to 0.80. The five baseline accusations landed from 0.7221 to 0.7889, and I wanted those cases to go to unsure. The human cutoff stayed at 0.45. Both signals, their weights, and the disagreement rule stayed the same. The upper end of the disagreement clamp follows the AI cutoff, so it is now 0.79.

| Measure | Before | After |
|---|---:|---:|
| Staff attacks held | 36/56 | 41/56 |
| Staff attacks broke | 20/56 | 15/56 |
| Human attack samples given the AI label | 5/8 | 0/8 |
| Evasion samples given the AI label | 1/10 | 1/10 |
| My writing given the AI label | 0/20 | 0/20 |
| Matched AI-human score gap | -0.0188 | -0.0188 |
| Calibration labels reached | 3/3 | 2/3 |
| Valid appeals logged per trial | 10/10 | 10/10 |
| Invalid requests handled per trial | 7/7 | 7/7 |

The higher cutoff stopped all five false accusations on the staff set. The calibration AI paragraph stayed at 0.7272, so it moved to unsure and the live label-coverage target went from met to missed. I used these attacks to choose the cutoff, so I would need fresh writing to see how well it carries over.

### Attack Run — After

The [full after run](results/attack_run_2026-11-08_2122_after.md) has the exact response labels and content IDs. I used the same verdict rules as the baseline.

| ID | Family | HTTP | Guess | Model | Style | Combined | Verdict |
|---|---|---:|---|---:|---:|---:|---|
| EV01 | evasion | 200 | human | 0.1635 | 0.5093 | 0.2500 | BROKE |
| EV02 | evasion | 200 | unsure | 0.5943 | 0.2121 | 0.4988 | BROKE |
| EV03 | evasion | 200 | unsure | 0.6662 | 0.4177 | 0.6041 | BROKE |
| EV04 | evasion | 200 | unsure | 0.6114 | 0.5106 | 0.5862 | BROKE |
| EV05 | evasion | 200 | human | 0.3212 | 0.3674 | 0.3327 | BROKE |
| EV06 | evasion | 200 | unsure | 0.5727 | 0.0625 | 0.4600 | BROKE |
| EV07 | evasion | 200 | unsure | 0.5862 | 0.5000 | 0.5647 | BROKE |
| EV08 | evasion | 200 | human | 0.2452 | 0.5000 | 0.3089 | BROKE |
| EV09 | evasion | 200 | unsure | 0.7042 | 0.3976 | 0.6276 | BROKE |
| EV10 | evasion | 200 | ai | 0.9792 | 0.5124 | 0.8625 | HELD |
| FP01 | false_positive | 200 | unsure | 0.6175 | 0.4440 | 0.5741 | HELD |
| FP02 | false_positive | 200 | unsure | 0.7387 | 0.5310 | 0.6868 | HELD |
| FP03 | false_positive | 200 | unsure | 0.8051 | 0.4730 | 0.7221 | HELD |
| FP04 | false_positive | 200 | unsure | 0.8329 | 0.4583 | 0.7392 | HELD |
| FP05 | false_positive | 200 | unsure | 0.8005 | 0.6063 | 0.7520 | HELD |
| FP06 | false_positive | 200 | unsure | 0.8814 | 0.4241 | 0.7671 | HELD |
| FP07 | false_positive | 200 | unsure | 0.8816 | 0.5106 | 0.7889 | HELD |
| FP08 | false_positive | 200 | human | 0.3223 | 0.5000 | 0.3667 | HELD |
| PI01 | prompt_injection | 200 | human | 0.4625 | 0.2757 | 0.4158 | BROKE |
| PI02 | prompt_injection | 200 | human | 0.2044 | 0.3578 | 0.2427 | BROKE |
| PI03 | prompt_injection | 200 | unsure | 0.5943 | 0.4443 | 0.5568 | HELD |
| PI04 | prompt_injection | 200 | unsure | 0.4998 | 0.4415 | 0.4852 | HELD |
| PI05 | prompt_injection | 200 | unsure | 0.6401 | 0.3333 | 0.5634 | HELD |
| PI06 | prompt_injection | 200 | unsure | 0.5583 | 0.4290 | 0.5260 | HELD |
| MF01 | malformed | 400 | — | — | — | — | HELD |
| MF02 | malformed | 400 | — | — | — | — | HELD |
| MF03 | malformed | 200 | human | 0.0000 | 0.5000 | 0.1250 | BROKE |
| MF04 | malformed | 200 | human | 0.0112 | 0.5000 | 0.1334 | BROKE |
| MF05 | malformed | 200 | ai | 0.9976 | 0.5000 | 0.8732 | BROKE |
| MF06 | malformed | 200 | ai | 0.9969 | 0.5000 | 0.8727 | BROKE |
| MF07 | malformed | 200 | ai | 0.9064 | 0.5000 | 0.8048 | HELD |
| MF08 | malformed | 413 | — | — | — | — | HELD |
| RQ01 | malformed | 400 | — | — | — | — | HELD |
| RQ02 | malformed | 400 | — | — | — | — | HELD |
| RQ03 | malformed | 400 | — | — | — | — | HELD |
| RQ04 | malformed | 400 | — | — | — | — | HELD |
| RQ05 | malformed | 400 | — | — | — | — | HELD |
| RQ06 | malformed | 400 | — | — | — | — | HELD |
| RQ07 | malformed | 400 | — | — | — | — | HELD |
| RQ08 | malformed | 400 | — | — | — | — | HELD |
| RQ09 | malformed | 400 | — | — | — | — | HELD |
| RQ10 | malformed | 400 | — | — | — | — | HELD |
| RQ11 | malformed | 400 | — | — | — | — | HELD |
| RQ12 | malformed | 400 | — | — | — | — | HELD |
| FL01_01 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_02 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_03 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_04 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_05 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_06 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_07 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_08 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_09 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_10 | flood_same_creator | 200 | human | 0.0287 | 0.5000 | 0.1465 | HELD |
| FL01_11 | flood_same_creator | 429 | — | — | — | — | HELD |
| FL01_12 | flood_same_creator | 429 | — | — | — | — | HELD |

### Criterion trials after the change

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False accusations | At most 1 of 20 | 0/20 flagged | 0/20 flagged | 0/20 flagged | MET |
| 2. AI-human mean gap | At least +0.20 on matched sets of 10 | -0.0188 | -0.0188 | -0.0188 | MISSED |
| 3. Label coverage | 3 of 3 live labels and a complete, exclusive score grid | 2/3 labels, 1001/1001 grid | 2/3 labels, 1001/1001 grid | 2/3 labels, 1001/1001 grid | MISSED |
| 4. Appeal logging | 10 of 10 valid appeals and one unknown-ID 404 | 10/10, unknown 404 | 10/10, unknown 404 | 10/10, unknown 404 | MET |
| 5. Invalid submissions | All expected JSON errors, no detector calls or decisions | 7/7, 0 decisions | 7/7, 0 decisions | 7/7, 0 decisions | MET |

The [full after run](results/run_2026-11-08_2131_after.md) used the same fixed texts and cases. The [earlier after pilot](results/run_2026-11-08_2122_after.md) is preserved. Below is JSON from trial 1 of the full run.

**1. False accusations**

```json
{
  "http_status": 200,
  "json": {
    "confidence": 0.6427,
    "content_id": "356661bf-b71a-41ee-b40a-63817acd85c9",
    "guess": "unsure",
    "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
    "model_score": 0.6943,
    "status": "decided",
    "style_score": 0.4879
  }
}
```

**2. AI-human mean gap**

```json
{
  "means": {
    "human": 0.44547,
    "ai": 0.42665
  },
  "gap": -0.018820000000000003,
  "ai_example": {
    "http_status": 200,
    "json": {
      "confidence": 0.6694,
      "content_id": "7ea1d5a7-0354-4b01-ac3c-f206403dd8c1",
      "guess": "unsure",
      "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
      "model_score": 0.7169,
      "status": "decided",
      "style_score": 0.5268
    }
  }
}
```

**3. Label coverage**

```json
{
  "responses": [
    {
      "http_status": 200,
      "json": {
        "confidence": 0.7272,
        "content_id": "3ea08614-fb52-495b-9580-f8250774b640",
        "guess": "unsure",
        "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
        "model_score": 0.792,
        "status": "decided",
        "style_score": 0.5328
      }
    }
  ],
  "grid_points": 1001,
  "grid_matched": 1001,
  "boundaries": {
    "0.45": [
      "human",
      "This writing looks like it was written by a person. This check cannot prove who wrote it."
    ],
    "0.8": [
      "ai",
      "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review."
    ]
  }
}
```

**4. Appeal logging**

```json
{
  "cases": [
    {
      "content_id": "cb0f1267-fdcf-484a-b58e-9bc05d35f4b1",
      "reasoning": "  I wrote this and can show my earlier draft 1.  ",
      "response": {
        "http_status": 200,
        "json": {
          "content_id": "cb0f1267-fdcf-484a-b58e-9bc05d35f4b1",
          "message": "Your appeal has been recorded and the submission is under review.",
          "status": "under_review"
        }
      },
      "audit": [
        {
          "combined_score": 0.7272,
          "content_id": "cb0f1267-fdcf-484a-b58e-9bc05d35f4b1",
          "creator_id": "eval_6cc746661c_1_appeals_1",
          "guess": "unsure",
          "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
          "model_score": 0.792,
          "status": "decided",
          "style_score": 0.5328,
          "timestamp": "2026-11-09T05:30:46+00:00"
        },
        {
          "content_id": "cb0f1267-fdcf-484a-b58e-9bc05d35f4b1",
          "creator_id": "eval_6cc746661c_1_appeals_1",
          "event": "appeal",
          "reasoning": "  I wrote this and can show my earlier draft 1.  ",
          "status": "under_review",
          "timestamp": "2026-11-09T05:30:48+00:00"
        }
      ]
    }
  ],
  "unknown": {
    "http_status": 404,
    "json": {
      "error": "not_found",
      "message": "No submission has that content_id."
    }
  }
}
```

**5. Invalid submissions**

```json
[
  {
    "case": "malformed JSON",
    "expected": 400,
    "http_status": 400,
    "json": {
      "error": "invalid_input",
      "message": "Send a JSON object."
    }
  },
  {
    "case": "oversized text",
    "expected": 413,
    "http_status": 413,
    "json": {
      "error": "text_too_large",
      "message": "text must be at most 10000 characters."
    }
  }
]
```

## What's Still Broken

| Remaining result | What I'd work on next |
|---|---|
| EV01 and EV04 | GPT-2 gives unusual spellings and vocabulary a lot of influence. I'd try a normalized copy for the model signal and compare both scores on fresh typo and rare-word pairs, including human controls. |
| EV02, EV03, EV06, and EV07 | Sentence breaks, quotations, and punctuation change the style score. I'd test paragraph-level summaries with explicit quotation handling so one unusual section has less influence. |
| EV05 and EV09 | Heavy editing and mixed authorship pull whole-text scores down. I'd test section-level scoring and use those scores to indicate where a review might help. |
| EV08 | I'd send very short text to unsure because there is too little context to make a useful high-confidence call. |
| PI01 and PI02 | Both got the human guess they asked for. The output was still computed from their text. I'd compare each against the same essay with the instruction removed to measure how much that added text shifts the scores. |
| MF03–MF06 | The route accepted control characters, punctuation-only text, one long word, and emoji-only text. I'd validate whether there is enough meaningful writing before scoring, with Unicode-aware rules so that legitimate writing in another script can still be submitted. |
| Criterion 3 | The label mapping still passed every boundary and grid check, but the only AI-labeled calibration text moved to unsure. I'd collect more varied unedited AI samples and compare coverage at candidate cutoffs alongside the human false-positive rate. |
| Criterion 2 | Raising the label cutoff had little effect on the score gap. I'd test both signals on writing from more authors and more AI generators, then check which signal adds useful separation before changing the weights. |

I stopped after one measured change so I could see what moving the cutoff did on its own. In production, I'd lean toward fewer false accusations and let more borderline AI writing go to review. Reviewers would have more cases to look at, and some AI-assisted submissions might get through, but writers would face fewer accusations based on a score alone.

## How I Used AI

I worked with ChatGPT to help me really think of the ways I could go about the acceptance criteria and getting the endpoint to run with one signal

I used ChatGPT to help me set up rate limiting and audit logging, run the attack tests, and compare the results before and after the cutoff change. I also used it to check whether the samples I picked from my own writing met the assignment criteria.

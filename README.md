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
    keep combined between 0.26 and 0.79
```

The model counts more because the style signal is simpler and easier to change. If the two signals strongly disagree, I keep the result inside the unsure range. Weights and thresholds are in `config.py`.

For example, model score 0.95 and style score 0.20 first produce 0.7625, which stays unsure. Model score 0.10 and style score 0.90 first produce 0.30, which also stays unsure. These are arithmetic examples, not observed GPT-2 results. An actual text where the two signals disagree has not been verified in this environment.

The API field `confidence` is the combined **AI-likelihood score**, following the starter's direction: 0 means more human-like and 1 means more AI-like. A human label therefore has a low value in this field. It is not a calibrated probability or the probability that the selected label is correct.

### What was verified

`python verify.py` passed all 16 backend checks. They cover input validation, all three labels through the route with controlled signals, 1,001 score points and threshold boundaries, signal disagreement, audit entries, missing models, and ten valid appeals. The tests use a temporary audit log and a mocked detector. They do not measure detection accuracy.

The full GPT-2 run could not be completed here because package/model downloads were blocked. Real-text score separation, real-text coverage of all three labels, the four calibration samples, and the human false-positive rate are still unverified. I am not counting controlled test scores as model results. `calibrate.py` can run source-labeled samples after the model is installed:

```powershell
.\.venv\Scripts\python.exe calibrate.py calibration_inputs.json
```

That input file must contain at least four objects with `name`, `source`, and `text`: known AI, known human, formal human, and lightly edited AI. Use actual human writing for the human samples. The script saves both signals and the combined score to `results/calibration.json` and reports whether all three labels appeared. I have not invented human-written examples or claimed these calibration runs happened.

The five targets in [criteria.md](criteria.md) are an **AI-assisted draft for me to review**. They were committed before implementation and scoring runs. The assignment asks me to choose my own targets, so that review is still required. I have not claimed the draft meets that authorship requirement or that all five targets passed.

## Label Variants

| Label | Score range | Exact text |
|---|---|---|
| High-confidence human | 0 ≤ score ≤ 0.25 | This writing looks like it was written by a person. This check cannot prove who wrote it. |
| Unsure | 0.25 < score < 0.80 | We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree. |
| High-confidence AI | 0.80 ≤ score ≤ 1 | This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review. |

I worded the unsure label this way because I do not want uncertainty to sound like an accusation. I think it should tell the writer what the system actually knows and give them a next step. None of the labels proves who wrote the text.

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

To replace this clearly marked demo with real model evidence, run `python sample_run.py` after installing dependencies and downloading GPT-2. The committed demo audit rows are explicitly tagged `controlled_test_double` so they cannot be confused with real-model results.

## How I Used AI

### Moment 1

**What I asked for:** I gave the project instructions to ChatGPT, shared my fork, and asked it to work through the milestones in my language and tone.

**What came back:** It drafted the flow, endpoint contracts, acceptance targets, style features, scoring rule, and backend implementation.

**What changed:** The repository now has both signals connected, a wide unsure range, input checks, audit logging, and an appeal path. I have not independently rewritten the five targets yet. AI helped write them, which I am disclosing because the assignment specifically asks for my own criteria.

### Moment 2

**What I asked for:** My request to finish the milestones also included checking that the service worked and preparing the required write-up.

**What came back:** ChatGPT added backend checks and ran them with controlled detector scores because it could not install the full model here. It also captured a submission and appeal demo.

**What changed:** The README and audit evidence identify the demo instead of presenting it as a real detector run. There is a separate command to capture actual GPT-2 results on my machine. I still need to review the criteria and inspect real model outputs before calling the project fully verified.

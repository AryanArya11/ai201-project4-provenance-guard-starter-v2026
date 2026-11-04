**Controlled demo, not a GPT-2 run.** The model score was fixed at 0.62; the style score, routes, labels, and audit writes ran normally. These responses were captured with Flask's test client. The equivalent curl requests are below. The sample paragraph is AI-written; this run checks behavior, not detection accuracy.


### A submission

```bash
curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text": "I spent most of the afternoon trying to figure out why my program was stuck. Then I noticed the counter was inside the wrong loop. That was it. I moved it, ran the program again, and finally got the result I expected.", "creator_id": "sample-writer"}'
```

```json
{
  "confidence": 0.5927,
  "content_id": "1cf8c7ed-5beb-4c90-b00e-cc70776ff19a",
  "guess": "unsure",
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "model_score": 0.62,
  "status": "decided",
  "style_score": 0.5108
}
```

### An appeal

```bash
curl -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{"content_id": "1cf8c7ed-5beb-4c90-b00e-cc70776ff19a", "reasoning": "I wrote this myself and can share my earlier drafts."}'
```

```json
{
  "content_id": "1cf8c7ed-5beb-4c90-b00e-cc70776ff19a",
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
      "combined_score": 0.5927,
      "content_id": "1cf8c7ed-5beb-4c90-b00e-cc70776ff19a",
      "creator_id": "sample-writer",
      "evidence_mode": "controlled_test_double",
      "guess": "unsure",
      "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
      "model_score": 0.62,
      "status": "decided",
      "style_score": 0.5108,
      "timestamp": "2026-11-04T06:49:00+00:00"
    },
    {
      "content_id": "1cf8c7ed-5beb-4c90-b00e-cc70776ff19a",
      "creator_id": "sample-writer",
      "event": "appeal",
      "evidence_mode": "controlled_test_double",
      "reasoning": "I wrote this myself and can share my earlier drafts.",
      "status": "under_review",
      "timestamp": "2026-11-04T06:49:00+00:00"
    }
  ]
}
```

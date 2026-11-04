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

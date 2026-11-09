# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 21:22
- Reviewed results: **41 held, 15 broke**

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `359f49af-aadc-4e4f-88b3-743fcbddac70` | human | 0.250 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `e8f6009b-ab60-44ae-9b61-181d61902a4e` | unsure | 0.499 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `70a1e9be-af5a-4512-8c69-69384e18843b` | unsure | 0.604 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `fadb25f8-57d6-4d10-a995-48116034e030` | unsure | 0.586 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `d36cdac9-488d-4365-a24c-344aeda7fbba` | human | 0.333 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `86285187-07d1-443b-908c-8c24e85a484d` | unsure | 0.460 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `3320264a-4b19-4821-afbd-98896c7d7972` | unsure | 0.565 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `85fc4b26-ded1-4248-b22c-38b98349885d` | human | 0.309 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `07ea65d1-fb16-490a-877a-c3ec5e5b12b5` | unsure | 0.628 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `880e4ca5-63cf-445e-8b44-d51b397ee0e0` | ai | 0.863 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `d3a8cd98-0479-4de2-b2ab-551f95d63a27` | unsure | 0.574 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `855d3a4c-fc9b-491a-8051-a68e7c687797` | unsure | 0.687 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `ab2530d6-e962-4fa5-b57f-d6420d11d19a` | unsure | 0.722 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `5ec08049-c644-4433-ba01-50f4b1b1021b` | unsure | 0.739 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `3fcfd72b-389d-4854-9de5-a4d3aedc9158` | unsure | 0.752 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `797c5ed6-d68f-4f5e-ae69-16dd5571e9f3` | unsure | 0.767 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `5c45ea7a-ac52-45c3-b66e-00b2c256e34f` | unsure | 0.789 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `e03d861b-8669-47aa-a428-b4f66214813b` | human | 0.367 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `76c45dca-60e4-4e32-bedb-7d040789830a` | human | 0.416 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `8f4a72cc-c579-43c3-ac43-3c03bf40e69a` | human | 0.243 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `4f35d395-4e1c-4e9c-ba1b-f5fcbf9fb97d` | unsure | 0.557 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `cf832429-a980-4b6b-81fc-086a144f4eb1` | unsure | 0.485 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `bf3f03e7-e4db-412d-9f8a-eea6344fa6be` | unsure | 0.563 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `7845eed1-cec4-4ebe-a578-e48fe3f86ea1` | unsure | 0.526 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `28f8b0aa-e0fd-434e-a66e-28a6625a9aff` | human | 0.125 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `3651f018-b95c-45bc-9b0d-6916f369a191` | human | 0.133 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `c100a47d-91b0-412e-9768-00bfac628e19` | ai | 0.873 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `7e8ad476-2575-4ae5-aaf9-fa9d89856167` | ai | 0.873 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `0e432f2a-15c9-4c30-9ff2-8d2855f605f7` | ai | 0.805 | HELD |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `66293c66-4ef4-4f69-856d-beaad306eb30` | human | 0.146 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0f72f7f7-be81-48eb-86b7-1559cf80c995` | human | 0.146 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `35561ea5-9278-42a7-81f3-10de5eddaab0` | human | 0.146 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a866e21a-db6d-489f-8eb0-1494ee92a353` | human | 0.146 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `823d3cad-b34d-40aa-9569-76ffab29c444` | human | 0.146 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7399434f-9f5f-4d7d-86bf-e38fd54f7e9c` | human | 0.146 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6ebd3ed7-c44c-4f25-b047-02c9a5cb4401` | human | 0.146 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e9e463f0-68cf-40da-a7c5-7e741fe6444a` | human | 0.146 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b91be219-e96e-46e4-86db-4271716a978d` | human | 0.146 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fc1d1f41-84c0-4272-bb51-4768f3d30338` | human | 0.146 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Held | Broke |
|---|---|---|---|
| evasion | 10 | 1 | 9 |
| false_positive | 8 | 8 | 0 |
| flood_same_creator | 12 | 12 | 0 |
| malformed | 20 | 16 | 4 |
| prompt_injection | 6 | 4 | 2 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "359f49af-aadc-4e4f-88b3-743fcbddac70",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.25,
  "model_score": 0.1635,
  "style_score": 0.5093,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "e8f6009b-ab60-44ae-9b61-181d61902a4e",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4988,
  "model_score": 0.5943,
  "style_score": 0.2121,
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "70a1e9be-af5a-4512-8c69-69384e18843b",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.6041,
  "model_score": 0.6662,
  "style_score": 0.4177,
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "fadb25f8-57d6-4d10-a995-48116034e030",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5862,
  "model_score": 0.6114,
  "style_score": 0.5106,
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "d36cdac9-488d-4365-a24c-344aeda7fbba",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3327,
  "model_score": 0.3212,
  "style_score": 0.3674,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "86285187-07d1-443b-908c-8c24e85a484d",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.46,
  "model_score": 0.5727,
  "style_score": 0.0625,
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "3320264a-4b19-4821-afbd-98896c7d7972",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5647,
  "model_score": 0.5862,
  "style_score": 0.5,
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "85fc4b26-ded1-4248-b22c-38b98349885d",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3089,
  "model_score": 0.2452,
  "style_score": 0.5,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "07ea65d1-fb16-490a-877a-c3ec5e5b12b5",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.6276,
  "model_score": 0.7042,
  "style_score": 0.3976,
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "880e4ca5-63cf-445e-8b44-d51b397ee0e0",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8625,
  "model_score": 0.9792,
  "style_score": 0.5124,
  "label": "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review.",
  "error": null,
  "verdict": "HELD"
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "d3a8cd98-0479-4de2-b2ab-551f95d63a27",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5741,
  "model_score": 0.6175,
  "style_score": 0.444,
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "error": null,
  "verdict": "HELD"
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "855d3a4c-fc9b-491a-8051-a68e7c687797",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6868,
  "model_score": 0.7387,
  "style_score": 0.531,
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "error": null,
  "verdict": "HELD"
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "ab2530d6-e962-4fa5-b57f-d6420d11d19a",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.7221,
  "model_score": 0.8051,
  "style_score": 0.473,
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "error": null,
  "verdict": "HELD"
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "5ec08049-c644-4433-ba01-50f4b1b1021b",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.7392,
  "model_score": 0.8329,
  "style_score": 0.4583,
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "error": null,
  "verdict": "HELD"
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "3fcfd72b-389d-4854-9de5-a4d3aedc9158",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.752,
  "model_score": 0.8005,
  "style_score": 0.6063,
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "error": null,
  "verdict": "HELD"
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "797c5ed6-d68f-4f5e-ae69-16dd5571e9f3",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.7671,
  "model_score": 0.8814,
  "style_score": 0.4241,
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "error": null,
  "verdict": "HELD"
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "5c45ea7a-ac52-45c3-b66e-00b2c256e34f",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.7889,
  "model_score": 0.8816,
  "style_score": 0.5106,
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "error": null,
  "verdict": "HELD"
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "e03d861b-8669-47aa-a428-b4f66214813b",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.3667,
  "model_score": 0.3223,
  "style_score": 0.5,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "76c45dca-60e4-4e32-bedb-7d040789830a",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.4158,
  "model_score": 0.4625,
  "style_score": 0.2757,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "8f4a72cc-c579-43c3-ac43-3c03bf40e69a",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2427,
  "model_score": 0.2044,
  "style_score": 0.3578,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "4f35d395-4e1c-4e9c-ba1b-f5fcbf9fb97d",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5568,
  "model_score": 0.5943,
  "style_score": 0.4443,
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "error": null,
  "verdict": "HELD"
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "cf832429-a980-4b6b-81fc-086a144f4eb1",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4852,
  "model_score": 0.4998,
  "style_score": 0.4415,
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "error": null,
  "verdict": "HELD"
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "bf3f03e7-e4db-412d-9f8a-eea6344fa6be",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5634,
  "model_score": 0.6401,
  "style_score": 0.3333,
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "error": null,
  "verdict": "HELD"
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "7845eed1-cec4-4ebe-a578-e48fe3f86ea1",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.526,
  "model_score": 0.5583,
  "style_score": 0.429,
  "label": "We are unsure whether AI was involved in this writing. This is not an accusation. You can ask for a review if you disagree.",
  "error": null,
  "verdict": "HELD"
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "28f8b0aa-e0fd-434e-a66e-28a6625a9aff",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.125,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "3651f018-b95c-45bc-9b0d-6916f369a191",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.1334,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "c100a47d-91b0-412e-9768-00bfac628e19",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8732,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review.",
  "error": null,
  "verdict": "BROKE"
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "7e8ad476-2575-4ae5-aaf9-fa9d89856167",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.8727,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review.",
  "error": null,
  "verdict": "BROKE"
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "0e432f2a-15c9-4c30-9ff2-8d2855f605f7",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.8048,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review.",
  "error": null,
  "verdict": "HELD"
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "66293c66-4ef4-4f69-856d-beaad306eb30",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1465,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "0f72f7f7-be81-48eb-86b7-1559cf80c995",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1465,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "35561ea5-9278-42a7-81f3-10de5eddaab0",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1465,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "a866e21a-db6d-489f-8eb0-1494ee92a353",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1465,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "823d3cad-b34d-40aa-9569-76ffab29c444",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1465,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "7399434f-9f5f-4d7d-86bf-e38fd54f7e9c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1465,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "6ebd3ed7-c44c-4f25-b047-02c9a5cb4401",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1465,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "e9e463f0-68cf-40da-a7c5-7e741fe6444a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1465,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "b91be219-e96e-46e4-86db-4271716a978d",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1465,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "fc1d1f41-84c0-4272-bb51-4768f3d30338",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1465,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing looks like it was written by a person. This check cannot prove who wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

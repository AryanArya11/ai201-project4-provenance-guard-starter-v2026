# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 21:20
- Reviewed results: **36 held, 20 broke**

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `b90e7d47-15eb-4547-b79f-69604ccca354` | human | 0.250 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `2a9ce1e7-3a39-4c18-974f-a1340173a8a4` | unsure | 0.499 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `0426ab20-4ec6-4d59-9e6b-a8288189f949` | unsure | 0.604 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `6a047593-b103-4aa1-862c-855d171e8bec` | unsure | 0.586 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `0aa91d66-272e-4e1f-aeab-9790b886dbe1` | human | 0.333 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `be08decd-520b-4a35-a3cd-a72ac777711a` | unsure | 0.460 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `2efed568-dfcf-424e-90d2-2972e033abbf` | unsure | 0.565 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `10c1230d-f613-4f7b-9d58-b4679308a34e` | human | 0.309 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `5bc5b72a-67bb-4172-9352-fce83aba8922` | unsure | 0.628 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `edefe030-78df-445c-968a-76a3752b6c86` | ai | 0.863 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `006fbccf-4806-4f82-9f6f-dcdf8b08e4d1` | unsure | 0.574 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `496abb24-0235-4418-a0f9-9b9925168aa8` | unsure | 0.687 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `bb75b70e-6b69-40a7-993e-cf21b9a7f113` | ai | 0.722 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `3d6ce94c-54be-480d-bc31-7d3dcc910c64` | ai | 0.739 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `fe346d85-4b24-4bc4-8209-b0365b3d1beb` | ai | 0.752 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `d44e6206-1a7e-4aee-ad93-b73a443bab07` | ai | 0.767 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `dda1722a-5533-4532-9e2b-2b546fde571a` | ai | 0.789 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `2aac6260-c244-441b-a340-2bf9a00662da` | human | 0.367 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `01663731-9309-4630-83a5-cd7df280f0a2` | human | 0.416 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `b170fc30-e918-420c-9581-618eba5e2f13` | human | 0.243 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `449fec1b-d20b-42cb-9016-7b44053dabf6` | unsure | 0.557 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `9476fe92-4eb2-4945-a095-ce8375677fd3` | unsure | 0.485 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `40081c8b-5f39-4979-87bc-978c34a038c6` | unsure | 0.563 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `e4bab25b-6fd3-45f0-a249-15959739b313` | unsure | 0.526 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `ac5cd4e7-a9df-4b32-9a37-f56852adf244` | human | 0.125 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `e906c969-6696-440d-aa2b-18355ba7f4bf` | human | 0.133 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `bd9fa34c-7ba1-4a05-9a19-fe429091a2f2` | ai | 0.873 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `e265a7f8-be6a-40b0-a8d3-6128b956a79d` | ai | 0.873 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `0488c6c5-8d64-42cd-913a-64db094bbca8` | ai | 0.805 | HELD |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `46924975-6567-4e00-ac1b-ba36ea841025` | human | 0.146 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `398640f8-7c20-46c2-bf87-c141e4bde198` | human | 0.146 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3e28d4da-0bfb-458f-b359-c2b87b90fe64` | human | 0.146 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `730aa673-6244-461d-9f8d-2765f8d828fe` | human | 0.146 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9ee0dd0b-7914-4bc2-9c5f-80208d30ad27` | human | 0.146 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `488078bb-07d7-41eb-b4d1-f3abcd839501` | human | 0.146 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `695475f7-0c4f-4fbf-9a42-0a3d52814c57` | human | 0.146 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b2d99dbd-31e2-495c-a5ef-ad65b2b9f49a` | human | 0.146 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4e5f09ed-2330-49d3-b32c-ed4004828065` | human | 0.146 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9a765311-0010-4e6a-a119-d530428d3a80` | human | 0.146 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Held | Broke |
|---|---|---|---|
| evasion | 10 | 1 | 9 |
| false_positive | 8 | 3 | 5 |
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
  "content_id": "b90e7d47-15eb-4547-b79f-69604ccca354",
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
  "content_id": "2a9ce1e7-3a39-4c18-974f-a1340173a8a4",
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
  "content_id": "0426ab20-4ec6-4d59-9e6b-a8288189f949",
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
  "content_id": "6a047593-b103-4aa1-862c-855d171e8bec",
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
  "content_id": "0aa91d66-272e-4e1f-aeab-9790b886dbe1",
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
  "content_id": "be08decd-520b-4a35-a3cd-a72ac777711a",
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
  "content_id": "2efed568-dfcf-424e-90d2-2972e033abbf",
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
  "content_id": "10c1230d-f613-4f7b-9d58-b4679308a34e",
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
  "content_id": "5bc5b72a-67bb-4172-9352-fce83aba8922",
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
  "content_id": "edefe030-78df-445c-968a-76a3752b6c86",
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
  "content_id": "006fbccf-4806-4f82-9f6f-dcdf8b08e4d1",
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
  "content_id": "496abb24-0235-4418-a0f9-9b9925168aa8",
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
  "content_id": "bb75b70e-6b69-40a7-993e-cf21b9a7f113",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7221,
  "model_score": 0.8051,
  "style_score": 0.473,
  "label": "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "3d6ce94c-54be-480d-bc31-7d3dcc910c64",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7392,
  "model_score": 0.8329,
  "style_score": 0.4583,
  "label": "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "fe346d85-4b24-4bc4-8209-b0365b3d1beb",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.752,
  "model_score": 0.8005,
  "style_score": 0.6063,
  "label": "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "d44e6206-1a7e-4aee-ad93-b73a443bab07",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.7671,
  "model_score": 0.8814,
  "style_score": 0.4241,
  "label": "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "dda1722a-5533-4532-9e2b-2b546fde571a",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7889,
  "model_score": 0.8816,
  "style_score": 0.5106,
  "label": "This writing shows strong signs of AI involvement, but this check can be wrong. If you wrote it yourself, you can ask for a review.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "2aac6260-c244-441b-a340-2bf9a00662da",
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
  "content_id": "01663731-9309-4630-83a5-cd7df280f0a2",
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
  "content_id": "b170fc30-e918-420c-9581-618eba5e2f13",
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
  "content_id": "449fec1b-d20b-42cb-9016-7b44053dabf6",
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
  "content_id": "9476fe92-4eb2-4945-a095-ce8375677fd3",
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
  "content_id": "40081c8b-5f39-4979-87bc-978c34a038c6",
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
  "content_id": "e4bab25b-6fd3-45f0-a249-15959739b313",
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
  "content_id": "ac5cd4e7-a9df-4b32-9a37-f56852adf244",
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
  "content_id": "e906c969-6696-440d-aa2b-18355ba7f4bf",
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
  "content_id": "bd9fa34c-7ba1-4a05-9a19-fe429091a2f2",
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
  "content_id": "e265a7f8-be6a-40b0-a8d3-6128b956a79d",
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
  "content_id": "0488c6c5-8d64-42cd-913a-64db094bbca8",
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
  "content_id": "46924975-6567-4e00-ac1b-ba36ea841025",
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
  "content_id": "398640f8-7c20-46c2-bf87-c141e4bde198",
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
  "content_id": "3e28d4da-0bfb-458f-b359-c2b87b90fe64",
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
  "content_id": "730aa673-6244-461d-9f8d-2765f8d828fe",
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
  "content_id": "9ee0dd0b-7914-4bc2-9c5f-80208d30ad27",
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
  "content_id": "488078bb-07d7-41eb-b4d1-f3abcd839501",
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
  "content_id": "695475f7-0c4f-4fbf-9a42-0a3d52814c57",
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
  "content_id": "b2d99dbd-31e2-495c-a5ef-ad65b2b9f49a",
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
  "content_id": "4e5f09ed-2330-49d3-b32c-ed4004828065",
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
  "content_id": "9a765311-0010-4e6a-a119-d530428d3a80",
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

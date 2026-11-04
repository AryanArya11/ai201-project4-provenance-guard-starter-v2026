### Actual four-text calibration

I ran all four samples through `POST /submit` using real local GPT-2 and the style signal. I supplied the two human paragraphs from my own writing. ChatGPT generated the AI sample and the edited AI sample. The full inputs and responses are in `results/calibration.json`, and the decisions are in `logs/audit.jsonl`.

| Sample | Model | Style | Combined | Label |
|---|---:|---:|---:|---|
| Unedited AI | 0.7920 | 0.5328 | 0.7272 | unsure |
| Plain human | 0.6943 | 0.4879 | 0.6427 | unsure |
| Formal human | 0.4125 | 0.4880 | 0.4314 | unsure |
| Lightly edited AI | 0.6974 | 0.4829 | 0.6438 | unsure |

The largest signal difference was on Unedited AI: model 0.7920, style 0.5328. The combined score was 0.7272, with the unsure label. None of these four inputs crossed the 0.50 strong-disagreement cutoff.

These four texts did not produce every label. Missing: ai, human. Real-text label coverage has not been demonstrated yet.

This is a small calibration run, so I am not calling it an accuracy evaluation. The larger fixed-set false-positive and score-gap targets still need the Unit 8 evaluation.

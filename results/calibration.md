### Actual four-text calibration and threshold revision

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

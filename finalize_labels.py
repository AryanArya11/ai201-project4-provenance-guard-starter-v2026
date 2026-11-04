"""Apply and document a calibration-based threshold revision, then rerun real texts.
Save beside app.py. Run with the project's Python 3.13 environment.
The original calibration and acceptance targets are preserved. Nothing is pushed.
"""
import json
import re
import shutil
from pathlib import Path


def main(root=None):
    root = Path(root) if root else Path(__file__).resolve().parent
    inputs_path = root / 'calibration_inputs.json'
    if not inputs_path.exists():
        raise SystemExit('Run this from the project folder after finish_unit7.py.')
    samples = json.loads(inputs_path.read_text(encoding='utf-8-sig'))
    if len(samples) != 4:
        raise SystemExit('Expected the four saved calibration samples. Nothing changed.')
    results = root / 'results'
    for extension in ['json', 'md']:
        original = results / f'calibration.{extension}'
        backup = results / f'calibration_before_thresholds.{extension}'
        if original.exists() and not backup.exists():
            shutil.copyfile(original, backup)
    config_path = root / 'config.py'
    config_text = config_path.read_text(encoding='utf-8')
    for name, value in [('HUMAN_THRESHOLD', '0.45'), ('AI_THRESHOLD', '0.70')]:
        config_text, count = re.subn(rf'^{name}\s*=\s*[0-9.]+\s*$', f'{name} = {value}', config_text, flags=re.MULTILINE)
        if count != 1:
            raise SystemExit(f'Could not locate one {name} setting. Nothing saved.')
    config_path.write_text(config_text, encoding='utf-8')
    # Import after saving the new settings so this process uses the revision.
    import config
    import scoring
    from app import app
    if (config.HUMAN_THRESHOLD, config.AI_THRESHOLD) != (0.45, 0.70):
        raise SystemExit('Settings did not reload. Run the script again in a fresh Python process.')
    rows = []
    client = app.test_client()
    for i, sample in enumerate(samples, 1):
        print(f"Scoring {i}/4 with real GPT-2: {sample['name']}...", flush=True)
        response = client.post('/submit', json={'text': sample['text'], 'creator_id': f'unit7-revised-calibration-{i}'})
        if response.status_code != 200:
            raise SystemExit(f'HTTP {response.status_code}: {response.get_json()}. Original evidence is preserved; rerun after resolving the error.')
        rows.append({**sample, 'http_status': response.status_code, **response.get_json(),
                     'thresholds': {'human_max': 0.45, 'ai_min': 0.70}})
    table = ['| Sample | Model | Style | Combined | Label |', '|---|---:|---:|---:|---|']
    for row in rows:
        table.append(f"| {row['name']} | {row['model_score']:.4f} | {row['style_score']:.4f} | {row['confidence']:.4f} | {row['guess']} |")
    observed = {row['guess'] for row in rows}
    missing = {'ai', 'human', 'unsure'} - observed
    coverage = ('All three labels appeared on actual text submissions after this revision.' if not missing else
                'Real-text label coverage is still incomplete. Missing: ' + ', '.join(sorted(missing)) + '.')
    report = '''### Actual four-text calibration and threshold revision

I first ran the four texts with human scores at or below 0.25 and AI scores at or above 0.80. All four received unsure. The original results are preserved in `results/calibration_before_thresholds.json` and `.md`; the original decisions also remain in the audit log.

The combined scores were 0.7272 for unedited AI, 0.6427 for my casual paragraph, 0.4314 for my formal paragraph, and 0.6438 for edited AI. The style scores were close together, from 0.4829 to 0.5328, so the model signal was doing most of the separating. I think the style signal is still weak on this small set, and I do not want to hide that.

After inspecting these calibration results, I changed `HUMAN_THRESHOLD` to 0.45 and `AI_THRESHOLD` to 0.70 in `config.py`. Scores at or below 0.45 receive human, scores at or above 0.70 receive AI, and scores in between receive unsure. The weights stayed at 0.75 for the model and 0.25 for style. Strong disagreements still stay unsure; the clamp is now 0.46 through 0.69 because it follows the configured boundaries.

This is a calibration-based change, not an independent accuracy result. I chose these thresholds after seeing these four texts and reran the same texts. The labels describe heuristic score bands, not proven probabilities. The narrower unsure range may produce more false accusations on unseen human writing. My original acceptance targets have not changed; the larger Unit 8 evaluation will test that tradeoff.

I supplied the two human paragraphs from my writing. ChatGPT generated the AI paragraph and the edited AI paragraph. The rerun used actual `POST /submit` requests through Flask's test client with local GPT-2, and each decision was logged.

''' + '\n'.join(table) + '\n\n' + coverage + '\n\n'
    split = max(rows, key=lambda row: abs(row['model_score'] - row['style_score']))
    report += (f"The largest signal difference in the rerun was on {split['name']}: model "
               f"{split['model_score']:.4f}, style {split['style_score']:.4f}, combined "
               f"{split['confidence']:.4f}, and label {split['guess']}. "
               'The disagreement cutoff remains a difference greater than 0.50.\n')
    (results / 'calibration.json').write_text(json.dumps(rows, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    (results / 'calibration.md').write_text(report, encoding='utf-8')
    readme_path = root / 'README.md'
    readme = readme_path.read_text(encoding='utf-8')
    heading = '### Actual four-text calibration'
    start = readme.find(heading)
    end = readme.find('## Label Variants', start)
    if start == -1 or end == -1:
        raise SystemExit('Real results saved. README layout differs; paste results/calibration.md under Signals and Scoring manually.')
    readme = readme[:start] + report + '\n' + readme[end:]
    readme = readme.replace('keep combined between 0.26 and 0.79', 'keep combined between 0.46 and 0.69')
    example_start = readme.find('For example, model score 0.95')
    example_end = readme.find('The API field `confidence`', example_start)
    if example_start != -1 and example_end != -1:
        readme = (readme[:example_start] +
                  'For example, model score 0.95 and style score 0.20 first produce 0.7625. Because the signals differ by more than 0.50, the revised rule limits that result to 0.69, which is unsure. Model score 0.10 and style score 0.90 first produce 0.30 and are limited to 0.46, also unsure. These are arithmetic examples; actual text results appear below.\n\n' + readme[example_end:])
    label_start = readme.index('## Label Variants')
    sample_start = readme.index('## Sample Run', label_start)
    label_table = ['| Label | Score range | Exact text |', '|---|---|---|']
    for name, limits, score in [('High-confidence human', '0 <= score <= 0.45', 0.0),
                               ('Unsure', '0.45 < score < 0.70', 0.5),
                               ('High-confidence AI', '0.70 <= score <= 1', 1.0)]:
        label_table.append(f'| {name} | {limits} | {scoring.score_to_label(score)[1]} |')
    label_section = ('## Label Variants\n\n' + '\n'.join(label_table) + '\n\n'
                     'I kept the unsure wording because I do not want uncertainty to sound like an accusation. '
                     'The high-confidence names refer to the configured score bands. The scores are not calibrated probabilities, and none of these labels proves authorship.\n\n')
    readme = readme[:label_start] + label_section + readme[sample_start:]
    readme_path.write_text(readme, encoding='utf-8')
    plan = root / 'SCORING_PLAN.md'
    note = ('\n\n## Unit 7 revision after real-text calibration\n\n'
            'The original thresholds above were 0.25 and 0.80. After all four calibration texts received unsure, '
            'I changed the thresholds to 0.45 and 0.70 and reran the same texts. The disagreement clamp follows '
            'the thresholds and is now 0.46 to 0.69. Weights and acceptance targets are unchanged. '
            'This uses the calibration set to select thresholds; it is not a held-out evaluation. '
            'Original results are preserved in results/calibration_before_thresholds.json.\n')
    if plan.exists() and '## Unit 7 revision after real-text calibration' not in plan.read_text(encoding='utf-8'):
        plan.write_text(plan.read_text(encoding='utf-8') + note, encoding='utf-8')
    # Make boundary checks follow the configured thresholds instead of the old values.
    checks = root / 'verify.py'
    if checks.exists():
        text = checks.read_text(encoding='utf-8')
        text = text.replace('scoring.score_to_label(0.25)[0]', 'scoring.score_to_label(config.HUMAN_THRESHOLD)[0]')
        text = text.replace('scoring.score_to_label(0.80)[0]', 'scoring.score_to_label(config.AI_THRESHOLD)[0]')
        checks.write_text(text, encoding='utf-8')
    print('\n' + '\n'.join(table))
    print('\n' + coverage)
    print('Original calibration preserved. README, scoring plan, config, and boundary checks updated.')
    if missing:
        print('Paste the table into ChatGPT; do not claim all labels were demonstrated.')
    else:
        print('Run verify.py next, then commit and push the revision and evidence.')


if __name__ == '__main__':
    main()

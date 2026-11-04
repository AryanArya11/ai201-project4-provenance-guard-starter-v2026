"""Run real signals on source-labeled writing: python calibrate.py inputs.json.

Input is a list of objects with name, source, and text. Include known AI,
known human, formal human, and lightly edited AI samples. Do not call AI-written
examples human. Results are diagnostic and do not change acceptance targets.
"""
import json
import sys
from pathlib import Path

import detector
import scoring
import stylometry


def main():
    if len(sys.argv)!=2:
        raise SystemExit('Usage: python calibrate.py inputs.json')
    samples=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    if not isinstance(samples,list) or len(samples)<4:
        raise SystemExit('Provide at least four source-labeled samples.')
    rows=[]
    for sample in samples:
        if not all(isinstance(sample.get(key),str) and sample[key].strip() for key in ['name','source','text']):
            raise SystemExit('Every sample needs nonempty name, source, and text strings.')
        model=detector.model_signal(sample['text'])
        style=stylometry.style_signal(sample['text'])
        combined=scoring.combine_signals(model,style)
        rows.append({**sample,'model_score':model,'style_score':style,
                     'combined_score':combined,'guess':scoring.score_to_label(combined)[0]})
    root=Path(__file__).parent
    (root/'results').mkdir(exist_ok=True)
    (root/'results/calibration.json').write_text(json.dumps(rows,indent=2)+'\n')
    print('| Sample | Source | Model | Style | Combined | Guess |')
    print('|---|---|---:|---:|---:|---|')
    for row in rows:
        print(f"| {row['name']} | {row['source']} | {row['model_score']:.4f} | {row['style_score']:.4f} | {row['combined_score']:.4f} | {row['guess']} |")
    guesses={row['guess'] for row in rows}
    print('Labels observed:',', '.join(sorted(guesses)))
    print('All three real-text labels observed:',guesses=={'ai','human','unsure'})


if __name__=='__main__':
    main()

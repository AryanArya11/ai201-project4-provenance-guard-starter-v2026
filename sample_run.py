"""Capture a submission, an appeal, and their log entries as readable text.

python sample_run.py          # real GPT-2; download it with python detector.py first
python sample_run.py --demo   # explicitly tagged, controlled detector score

The demo checks the backend only. It is not evidence of detector accuracy.
A successful real run also replaces the Sample Run section in README.md.
"""
import argparse
import json
import shlex
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

import audit
import detector
from app import app

TEXT = ('I spent most of the afternoon trying to figure out why my program was stuck. '
        'Then I noticed the counter was inside the wrong loop. That was it. '
        'I moved it, ran the program again, and finally got the result I expected.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demo',action='store_true')
    args=parser.parse_args()
    mode='controlled_test_double' if args.demo else 'real_gpt2'
    original=audit.log_decision
    original_appeal=audit.log_appeal
    # Demo provenance is written into every evidence row, not only the README.
    def decision(**kwargs):
        return original(**kwargs,evidence_mode=mode)
    def appeal(**kwargs):
        if args.demo:
            return audit._append({'timestamp':audit._now(),**kwargs,
                                  'event':'appeal','status':'under_review','evidence_mode':mode})
        return original_appeal(**kwargs)
    with ExitStack() as stack:
        stack.enter_context(patch.object(audit,'log_decision',side_effect=decision))
        stack.enter_context(patch.object(audit,'log_appeal',side_effect=appeal))
        if args.demo:
            stack.enter_context(patch.object(detector,'model_signal',return_value=0.62))
        client=app.test_client()
        body={'text':TEXT,'creator_id':'sample-writer'}
        submission=client.post('/submit',json=body)
        if submission.status_code!=200:
            raise SystemExit(f'Submission failed ({submission.status_code}): {submission.json}. No sample evidence was written.')
        content_id=submission.json['content_id']
        appeal_body={'content_id':content_id,'reasoning':'I wrote this myself and can share my earlier drafts.'}
        response=client.post('/appeal',json=appeal_body)
        if response.status_code!=200:
            raise SystemExit(f'Appeal failed: {response.json}')
        log_response=client.get('/log?limit=2')
    evidence={'mode':mode,'note':'The sample text was AI-written; no accuracy claim is made about its authorship.',
              'submit_request':body,'submit_status':submission.status_code,'submit_response':submission.json,
              'appeal_request':appeal_body,'appeal_status':response.status_code,'appeal_response':response.json,
              'log_response':log_response.json}
    root=Path(__file__).parent
    (root/'results').mkdir(exist_ok=True)
    name='sample_run_demo' if args.demo else 'sample_run'
    (root/'results'/f'{name}.json').write_text(json.dumps(evidence,indent=2)+'\n')
    intro=('**Controlled demo, not a GPT-2 run.** The model score was fixed at 0.62; the style score, routes, labels, and audit writes ran normally. '
           if args.demo else '**Actual local GPT-2 run.** Both signals ran normally. ')
    intro+='These responses were captured with Flask\'s test client. The equivalent curl requests are below. The sample paragraph is AI-written; this run checks behavior, not detection accuracy.\n\n'
    sections=[intro]
    for heading,route,request_body,result in [('A submission','submit',body,submission.json),('An appeal','appeal',appeal_body,response.json)]:
        payload=json.dumps(request_body)
        sections.append(f'### {heading}\n\n```bash\ncurl -X POST http://127.0.0.1:5000/{route} -H "Content-Type: application/json" -d {shlex.quote(payload)}\n```\n\n```json\n{json.dumps(result,indent=2)}\n```\n')
    sections.append('### What the log shows afterwards\n\n```bash\ncurl "http://127.0.0.1:5000/log?limit=2"\n```\n\n```json\n'+json.dumps(log_response.json,indent=2)+'\n```\n')
    snippet='\n'.join(sections)
    (root/'results'/f'{name}.md').write_text(snippet)
    if not args.demo:
        readme=root/'README.md'
        text=readme.read_text()
        start='<!-- SAMPLE_RUN_START -->'
        end='<!-- SAMPLE_RUN_END -->'
        if start in text and end in text:
            before,rest=text.split(start,1)
            _,after=rest.split(end,1)
            readme.write_text(before+start+'\n'+snippet+end+after)
    print(f'Saved results/{name}.json and results/{name}.md ({mode}).')
    print('Status:',response.json['status'])
    print('A demo does not verify real-model label coverage or accuracy.')


if __name__=='__main__':
    main()

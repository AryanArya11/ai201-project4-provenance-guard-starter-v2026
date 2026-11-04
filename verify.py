"""Backend checks with a controlled detector; this does not measure GPT-2 accuracy.

Run: python verify.py
All logs go in a temporary directory, so these checks preserve your evidence.
"""
import math
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import audit
import config
import detector
import scoring
import stylometry
from app import app


class BackendChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        for name, value in [('LOG_DIR', root), ('AUDIT_LOG', root / 'audit.jsonl')]:
            patcher = patch.object(config, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.client = app.test_client()
        self.body = {'text': 'I wrote this after class. It took a while to get right.',
                     'creator_id': 'writer-1'}

    def submit(self, score=0.6):
        with patch.object(detector, 'model_signal', return_value=score):
            return self.client.post('/submit', json=self.body)

    def test_ping_control(self):
        self.assertTrue(self.client.post('/ping', json={'message':'hello'}).json['ok'])

    def test_response_and_audit_match(self):
        response = self.submit()
        self.assertEqual(response.status_code, 200)
        data = response.json
        entry = audit.entries_for(data['content_id'])[0]
        for key in ['content_id', 'guess', 'model_score', 'style_score', 'label', 'status']:
            self.assertEqual(data[key], entry[key])
        self.assertEqual(data['confidence'], entry['combined_score'])
        self.assertEqual(self.client.get('/log').json['count'], 1)

    def test_each_label_through_submit(self):
        # Controlled signals prove route wiring and reachability, not text accuracy.
        for model, style, expected in [(0.05,0.10,'human'), (0.5,0.5,'unsure'), (0.98,0.95,'ai')]:
            with patch.object(detector,'model_signal',return_value=model), patch.object(stylometry,'style_signal',return_value=style):
                response=self.client.post('/submit',json=self.body)
            self.assertEqual(response.json['guess'], expected)

    def test_label_boundaries_and_complete_range(self):
        self.assertEqual(scoring.score_to_label(config.HUMAN_THRESHOLD)[0], 'human')
        self.assertEqual(scoring.score_to_label(config.AI_THRESHOLD)[0], 'ai')
        self.assertEqual(scoring.score_to_label(0.51)[0], 'unsure')
        self.assertEqual(scoring.score_to_label(0.95)[0], 'ai')
        for i in range(1001):
            self.assertIn(scoring.score_to_label(i/1000)[0], {'human','unsure','ai'})

    def test_disagreement_stays_unsure(self):
        for a,b in [(1,0), (0,1), (0.99,0.4), (0.1,0.9)]:
            self.assertEqual(scoring.score_to_label(scoring.combine_signals(a,b))[0], 'unsure')

    def test_invalid_signal_values(self):
        for value in [math.nan, math.inf, -0.1, 1.1]:
            with self.assertRaises(ValueError):
                scoring.combine_signals(value,0.5)

    def test_invalid_submit_bodies(self):
        bodies=[None, [], 'hello', 3, {}, {'text':None,'creator_id':'x'},
                {'text':[],'creator_id':'x'}, {'text':'   ','creator_id':'x'},
                {'text':'hello'}, {'text':'hello','creator_id':False},
                {'text':'hello','creator_id':'   '}, {'text':'hello','creator_id':'x'*201}]
        with patch.object(detector,'model_signal') as signal:
            for body in bodies:
                response=self.client.post('/submit',json=body)
                self.assertEqual(response.status_code,400,(body,response.json))
                self.assertEqual(response.json['error'],'invalid_input')
            signal.assert_not_called()
        self.assertEqual(audit.read_entries(),[])

    def test_malformed_json(self):
        for route in ['/submit','/appeal']:
            response=self.client.post(route,data='{broken',content_type='application/json')
            self.assertEqual(response.status_code,400)
            self.assertTrue(response.is_json)

    def test_oversized_text_and_request(self):
        with patch.object(detector,'model_signal') as signal:
            response=self.client.post('/submit',json={'text':'x'*10001,'creator_id':'x'})
            self.assertEqual(response.status_code,413)
            response=self.client.post('/submit',data='x'*100001,content_type='application/json')
            self.assertEqual(response.status_code,413)
            self.assertTrue(response.is_json)
            signal.assert_not_called()
        self.assertEqual(audit.read_entries(),[])

    def test_ten_appeals_preserve_decisions(self):
        for i in range(10):
            data=self.submit().json
            original=audit.entries_for(data['content_id'])[0].copy()
            reason=f'  I wrote this myself, and I have draft {i}.  '
            with patch.object(detector,'model_signal') as signal:
                response=self.client.post('/appeal',json={'content_id':data['content_id'],'reasoning':reason})
                signal.assert_not_called()
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.json['status'],'under_review')
            entries=audit.entries_for(data['content_id'])
            self.assertEqual(entries[0],original)
            self.assertEqual(entries[-1]['reasoning'],reason)
            self.assertEqual(entries[-1]['status'],'under_review')
        self.assertEqual(len(audit.read_entries()),20)

    def test_appeal_survives_new_client(self):
        data=self.submit().json
        self.client.post('/appeal',json={'content_id':data['content_id'],'reasoning':'My own writing.'})
        with app.test_client() as other:
            entries=other.get('/log').json['entries']
        self.assertEqual(entries[-1]['status'],'under_review')

    def test_unknown_appeal(self):
        response=self.client.post('/appeal',json={'content_id':'missing','reasoning':'I disagree.'})
        self.assertEqual(response.status_code,404)
        self.assertEqual(audit.read_entries(),[])

    def test_invalid_appeals(self):
        for body in [[], {}, {'content_id':None,'reasoning':'x'},
                     {'content_id':'x','reasoning':[]}, {'content_id':'x','reasoning':' '},
                     {'content_id':'x','reasoning':'x'*5001}]:
            self.assertEqual(self.client.post('/appeal',json=body).status_code,400)

    def test_short_input_error(self):
        with patch.object(detector,'model_signal',side_effect=ValueError('short')):
            self.assertEqual(self.client.post('/submit',json=self.body).status_code,400)
        self.assertEqual(audit.read_entries(),[])

    def test_detector_unavailable(self):
        with patch.object(detector,'model_signal',side_effect=detector.DetectorUnavailable('offline')):
            with self.assertLogs(app.logger,level='ERROR'):
                response=self.client.post('/submit',json=self.body)
        self.assertEqual(response.status_code,503)
        self.assertEqual(audit.read_entries(),[])

    def test_style_features(self):
        self.assertEqual(stylometry.type_token_ratio('cat cat dog'),2/3)
        self.assertEqual(stylometry.punctuation_density('Hi!'),1/3)
        self.assertEqual(stylometry.sentence_length_spread('One two. Three four.'),0)
        self.assertEqual(stylometry.style_signal('Hi.'),0.5)
        varied='One. '+('Different words make a longer sentence with more detail. '*4)
        regular='The system produces good results for every single user. '*5
        self.assertNotEqual(stylometry.style_signal(varied),stylometry.style_signal(regular))
        for text in ['', '你好。', varied, regular, '!'*100]:
            self.assertTrue(0<=stylometry.style_signal(text)<=1)


if __name__=='__main__':
    unittest.main(verbosity=2)

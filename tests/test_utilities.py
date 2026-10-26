import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
ROOT = Path(__file__).resolve().parents[1]
def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
site = module('build_candidate_site')
tracker = module('failure_tracker')
class SiteTests(unittest.TestCase):
    def setUp(self): self.d = json.loads((ROOT / 'scripts/sample_candidate.json').read_text())
    def test_fixture(self): self.assertIn('6 / 8', site.render(self.d))
    def test_unavailable_hides_data(self):
        self.d['sections']['brighthire']['items']=[{'label':'Secret','value':'HIDDEN-MARKER'}]
        self.assertNotIn('HIDDEN-MARKER',site.render(self.d))
    def test_escaping(self):
        self.d['candidate']='<script>alert(1)</script>'
        page=site.render(self.d); self.assertNotIn('<script>',page); self.assertIn('&lt;script&gt;',page)
    def test_numeric_and_null_values(self):
        self.d['sections']['gem']['items']=[{'label':2,'value':None},{'label':None,'value':42}]
        self.assertIn('42',site.render(self.d))
    def test_missing_sources(self):
        self.d['sections']={}; self.assertEqual(site.render(self.d).count(': unavailable'),4)
    def test_not_live(self): self.assertNotIn(': live',site.render(self.d))
    def test_invalid_coverage(self):
        for covered,total in [(-1,8),(9,8),(1,0),(True,8),('1',8)]:
            with self.subTest(covered=covered,total=total):
                d=copy.deepcopy(self.d); d['evidence_coverage'].update(topics_covered=covered,topics_total=total)
                with self.assertRaises(ValueError): site.render(d)
    def test_missing_timestamp(self):
        del self.d['sections']['gem']['fetched_at']
        with self.assertRaises(ValueError): site.render(self.d)
    def test_export(self):
        self.d['sections']['gem']['status']='export'; self.assertIn('export, not live',site.render(self.d))
    def test_cli_invalid_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'bad.json'; p.write_text('{}')
            r=subprocess.run([sys.executable,str(ROOT/'scripts/build_candidate_site.py'),str(p),str(Path(tmp)/'out')],capture_output=True,text=True)
            self.assertEqual(r.returncode,2); self.assertFalse((Path(tmp)/'out/index.html').exists())
class TrackerTests(unittest.TestCase):
    def test_no_log_not_connected(self): self.assertIn('unverified',tracker.states([],time.time())['gem']['state'])
    def test_three_failures(self):
        now=time.time(); rows=[{'ts':now-1,'system':'gem'}]*3
        self.assertEqual(tracker.states(rows,now)['gem']['state'],'STOP')
    def test_older_than_day(self):
        now=time.time(); self.assertEqual(tracker.states([{'ts':now-86401,'system':'gem'}],now)['gem']['failures_24h_since_reset'],0)
    def test_reset_keeps_history(self):
        now=time.time(); rows=[{'ts':now-10,'system':'gem'}]*3+[{'ts':now-1,'system':'gem','event':'reset'}]
        state=tracker.states(rows,now)['gem']; self.assertEqual(state['all_time'],3); self.assertEqual(state['failures_24h_since_reset'],0)
    def test_corrupt_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'x'; p.write_text('not json\n')
            with self.assertRaises(ValueError): tracker.load(p)
    def test_relative_path_and_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            env=dict(os.environ,TE_FAILURE_LOG='local.jsonl')
            def run(*args):
                return subprocess.run([sys.executable,str(ROOT/'scripts/failure_tracker.py'),*args],cwd=tmp,env=env,capture_output=True,text=True)
            for _ in range(3): self.assertEqual(run('log','--system','gem','--tool','read','--kind','timeout').returncode,0)
            self.assertEqual(json.loads(run('status','--json').stdout)['gem']['state'],'STOP')
            self.assertEqual(run('recent','-n','2').returncode,0)
            self.assertEqual(run('clear','--system','gem','--reason','Test fix verified').returncode,0)
            self.assertEqual(len((Path(tmp)/'local.jsonl').read_text().splitlines()),4)
    def test_invalid_cli_category(self):
        r=subprocess.run([sys.executable,str(ROOT/'scripts/failure_tracker.py'),'log','--system','bad','--tool','x','--kind','timeout'],capture_output=True)
        self.assertNotEqual(r.returncode,0)
if __name__=='__main__': unittest.main()

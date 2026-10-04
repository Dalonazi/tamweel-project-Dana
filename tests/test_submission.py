"""Boundary tests for final submission integrity and actionable failures."""
from pathlib import Path
import json
import sys
import tempfile
import unittest
import zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from submission_contract import build_manifest,check_manifest,extract_project,inventory,json_read,safe_name
from validate_submission import validate


class SubmissionTests(unittest.TestCase):
    def test_unsafe_paths(self):
        for name in ('../x','/x','a/../b','a\\b','C:x','a//b','.',''):
            with self.subTest(name=name),self.assertRaises(ValueError):safe_name(name)

    def test_archive_traversal_and_case_duplicates(self):
        for names in (['../outside.txt'],['A.txt','a.txt']):
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/'sample.zip'
                with zipfile.ZipFile(p,'w') as z:
                    for n in names:z.writestr(n,'x')
                with self.assertRaises(ValueError):extract_project(p,Path(d)/'project')

    def test_archive_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'sample.zip';entry=zipfile.ZipInfo('link');entry.create_system=3;entry.external_attr=0o120777<<16
            with zipfile.ZipFile(p,'w') as z:z.writestr(entry,'outside')
            with self.assertRaises(ValueError):extract_project(p,Path(d)/'project')

    def test_private_filename_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'challenge_labels.csv').write_text('x',encoding='utf-8')
            with self.assertRaises(ValueError):inventory(d)

    def test_manifest_tamper_and_added_file(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);(r/'artifacts').mkdir()
            (r/'artifacts/day5_run.json').write_text(json.dumps({'config':{'seed':211},'lab_revision':'abc'}))
            (r/'artifacts/environment.json').write_text('{}')
            (r/'README.md').write_text('project')
            build_manifest(r,bundle=True);self.assertTrue(check_manifest(r))
            (r/'README.md').write_text('modified')
            with self.assertRaises(ValueError):check_manifest(r)
            build_manifest(r);(r/'added.md').write_text('new')
            with self.assertRaises(ValueError):check_manifest(r)

    def test_strict_json(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.json'
            for bad in ('{"x":NaN}','{"x":Infinity}','{"x":1,"x":2}'):
                p.write_text(bad)
                with self.assertRaises(ValueError):json_read(p)

    def test_empty_project_never_ready_and_no_grade(self):
        with tempfile.TemporaryDirectory() as d:
            r=validate(d)
            self.assertFalse(r['ready_for_submission']);self.assertIsNone(r['automatic_grade'])
            self.assertTrue(any(x['check']=='fresh_execution' and x['status']=='FAIL' for x in r['checks']))
            self.assertTrue(all(x['file'] and x['how_to_fix'] for x in r['checks'] if x['status']=='FAIL'))

    def test_template_health_does_not_claim_final_readiness(self):
        result=validate(ROOT,template=True)
        self.assertEqual(result['status'],'STARTER_TEMPLATE_HEALTHY')
        self.assertFalse(result['ready_for_submission'])


if __name__=='__main__':unittest.main()

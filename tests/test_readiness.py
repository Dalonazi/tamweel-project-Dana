"""Run with python -m unittest discover -s tests -v from the project root."""
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import URLError

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from data_checks import load_course_data, validate_frame, verify_files
from generate_synthetic_data import generate_public
from setup_colab import fetch_verified


class DataContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frames,cls.contract,cls.summary=load_course_data(ROOT)

    def test_released_shapes_and_roles(self):
        self.assertEqual(self.frames['train'].shape,(10000,26))
        self.assertEqual(self.frames['challenge'].shape,(2500,25))
        self.assertEqual(self.frames['dirty'].shape,(10000,28))
        self.assertEqual(len(self.contract['features']),22)
        self.assertNotIn('default_within_90d',self.frames['challenge'])
        self.assertGreater(self.frames['train']['customer_id'].duplicated().sum(),0)

    def test_duplicate_application_rejected(self):
        frame=self.frames['train'].copy()
        frame.loc[1,'application_id']=frame.loc[0,'application_id']
        with self.assertRaisesRegex(ValueError,'unique'):
            validate_frame(frame,self.contract,'train')

    def test_target_in_challenge_rejected(self):
        frame=self.frames['challenge'].assign(default_within_90d=0)
        with self.assertRaisesRegex(ValueError,'column'):
            validate_frame(frame,self.contract,'challenge')

    def test_missing_predictor_rejected(self):
        frame=self.frames['train'].drop(columns=['income_sar'])
        with self.assertRaisesRegex(ValueError,'column'):
            validate_frame(frame,self.contract,'train')

    def test_nonfinite_and_range_rejected(self):
        for value in [float('inf'),-500]:
            frame=self.frames['train'].copy()
            frame.loc[0,'income_sar']=value
            with self.assertRaisesRegex(ValueError,'range'):
                validate_frame(frame,self.contract,'train')

    def test_missing_target_rejected(self):
        frame=self.frames['train'].copy()
        frame['default_within_90d']=frame['default_within_90d'].astype(float)
        frame.loc[0,'default_within_90d']=float('nan')
        with self.assertRaisesRegex(ValueError,'complete and binary'):
            validate_frame(frame,self.contract,'train')

    def test_training_rebuild_is_identical(self):
        with tempfile.TemporaryDirectory() as folder:
            directory=Path(folder)
            generate_public(directory)
            for name in ['tamweel_train.csv','tamweel_dirty.csv']:
                self.assertEqual((ROOT/'data'/name).read_bytes(),(directory/name).read_bytes())
            self.assertEqual(sorted(p.name for p in directory.iterdir()),['tamweel_dirty.csv','tamweel_train.csv'])

    def test_hash_change_and_path_escape_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/'sample.csv').write_bytes(b'changed')
            manifest={'files':{'sample.csv':{'sha256':hashlib.sha256(b'original').hexdigest()}}}
            with self.assertRaisesRegex(ValueError,'Checksum mismatch'):
                verify_files(root,manifest)
            with self.assertRaisesRegex(ValueError,'Unsafe'):
                verify_files(root,{'files':{'../outside':{'sha256':'0'*64}}})


class DownloadTests(unittest.TestCase):
    def test_valid_local_copy_needs_no_network(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'data.csv'
            path.write_bytes(b'verified')
            def unavailable(*a,**kw): raise URLError('offline')
            self.assertEqual(fetch_verified('https://example.test/data',path,hashlib.sha256(b'verified').hexdigest(),opener=unavailable),'verified local copy')

    def test_transient_error_retried(self):
        calls=[]
        def intermittent(*a,**kw):
            calls.append(1)
            if len(calls)==1: raise URLError('temporary')
            return io.BytesIO(b'valid')
        with tempfile.TemporaryDirectory() as folder, patch('setup_colab.time.sleep'):
            path=Path(folder)/'data.csv'
            fetch_verified('https://example.test/data',path,hashlib.sha256(b'valid').hexdigest(),opener=intermittent)
            self.assertEqual(len(calls),2)
            self.assertEqual(path.read_bytes(),b'valid')

    def test_corruption_never_accepted(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'data.csv'
            with self.assertRaisesRegex(ValueError,'Checksum mismatch'):
                fetch_verified('https://example.test/data',path,hashlib.sha256(b'valid').hexdigest(),opener=lambda *a,**kw:io.BytesIO(b'corrupt'))
            self.assertFalse(path.exists())

    def test_offline_without_copy_has_actionable_error(self):
        def unavailable(*a,**kw): raise URLError('offline')
        with tempfile.TemporaryDirectory() as folder, patch('setup_colab.time.sleep'):
            with self.assertRaisesRegex(RuntimeError,'Retry the setup cell'):
                fetch_verified('https://example.test/data',Path(folder)/'data.csv','0'*64,opener=unavailable)


if __name__=='__main__':
    unittest.main()

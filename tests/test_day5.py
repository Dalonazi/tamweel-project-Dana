"""Behavioral checks for nested stacking, model replay and submission integrity."""
from pathlib import Path
import json,sys,tempfile,unittest,zipfile
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from day5_final import *
from day5_delivery import *


class Day5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract=json.loads((ROOT/'data/data_contract.json').read_text(encoding='utf-8'))
        cls.train=pd.read_csv(ROOT/'data/tamweel_train.csv')
        cls.challenge=pd.read_csv(ROOT/'data/tamweel_challenge.csv')
        cls.pool,cls.cal,cls.roles=split_final_roles(cls.train)
        cls.oof,cls.scores,cls.audit=nested_comparison(cls.pool,cls.contract)
        cls.summary,cls.gate=worth_it(cls.scores)
        cls.candidate,cls.mapping,cls.calpred,cls.final_audit=fit_final(cls.pool,cls.cal,cls.contract,cls.gate['chosen'])

    def test_every_nested_training_excludes_outer_customers(self):
        lookup=self.train.set_index('application_id')
        for outer in self.audit['folds']:
            valid=lookup.loc[outer['validation_ids']]
            earlier=lookup.loc[outer['training_ids']]
            self.assertFalse(set(valid.customer_id)&set(earlier.customer_id))
            self.assertTrue((pd.to_datetime(earlier.application_date)+pd.Timedelta(days=90)<outer['validation_start']).all())
            self.assertTrue(set(outer['meta_training_ids'])<=set(outer['training_ids']))
            seen=set()
            for inner in outer['inner_folds']:
                fit=lookup.loc[inner['training_ids']]; check=lookup.loc[inner['validation_ids']]
                self.assertFalse(set(fit.customer_id)&set(check.customer_id))
                self.assertFalse(set(fit.customer_id)&set(valid.customer_id))
                self.assertTrue((pd.to_datetime(fit.application_date)+pd.Timedelta(days=90)<inner['validation_start']).all())
                self.assertFalse(seen&set(inner['validation_ids']));seen.update(inner['validation_ids'])
            self.assertEqual(seen,set(outer['meta_training_ids']))

    def test_final_calibration_customers_and_maturity(self):
        self.assertFalse(set(self.pool.customer_id)&set(self.cal.customer_id))
        self.assertFalse(set(self.oof.application_id)&set(self.cal.application_id))
        self.assertTrue((pd.to_datetime(self.pool.application_date)+pd.Timedelta(days=90)<CAL_START).all())
        self.assertTrue((pd.to_datetime(self.cal.application_date)+pd.Timedelta(days=90)<DEPLOY_DATE).all())
        self.assertFalse((self.pool.application_date>='2024-04-02').any())

    def test_role_allocation_does_not_use_label_values(self):
        changed=self.train.copy();changed[TARGET]=1-changed[TARGET]
        _,_,roles=split_final_roles(changed)
        pd.testing.assert_frame_equal(roles,self.roles)

    def test_final_fit_rejects_late_or_overlapping_calibration(self):
        with self.assertRaises(ValueError):fit_final(self.pool,self.cal.assign(application_date='2024-12-31'),self.contract,'Logistic')
        with self.assertRaises(ValueError):fit_final(self.pool,self.cal.assign(customer_id=self.pool.customer_id.iloc[0]),self.contract,'Logistic')

    def test_oof_corruption_rejected(self):
        for column,value in [('fold',99),(TARGET,7),('LightGBM',np.nan),('customer_id','BAD')]:
            data=self.oof.copy();data.loc[0,column]=value
            with self.assertRaises(ValueError): validate_comparison(data,self.pool)
        with self.assertRaises(ValueError): validate_comparison(self.oof.iloc[:-1],self.pool)

    def test_ensemble_gate_can_keep_or_ship_without_forcing_winner(self):
        rows=[{'fold':f,'candidate':n,'average_precision':.3+.01*f,'brier':.07,'ece':.03}
            for f in (1,2,3) for n in BASE+ENSEMBLES]
        equal=pd.DataFrame(rows)
        self.assertEqual(worth_it(equal)[1]['decision'],'KEEP SINGLE')
        better=equal.copy();better.loc[better.candidate.eq('Equal'),'average_precision']+=.08
        self.assertEqual(worth_it(better)[1]['chosen'],'Equal')
        better.loc[better.candidate.eq('Equal'),'brier']+=.02
        self.assertEqual(worth_it(better)[1]['decision'],'KEEP SINGLE')

    def test_gate_refuses_incomplete_folds(self):
        with self.assertRaises(ValueError): worth_it(self.scores.iloc[:-1])

    def test_budget_expires_before_any_partial_result(self):
        with self.assertRaises(EnsembleBudgetExpired): nested_comparison(self.pool,self.contract,FinalConfig(seconds=0))

    def test_all_six_native_exports_reproduce_predictions(self):
        X=self.challenge.iloc[:43];features=[f['name'] for f in self.contract['features']]
        original=self.candidate.chosen
        try:
            for chosen in BASE+ENSEMBLES:
                self.candidate.chosen=chosen
                with tempfile.TemporaryDirectory() as folder:
                    export_model(self.candidate,self.mapping,self.contract,folder)
                    actual=predict_final(X,folder)
                    expected=map_probability(self.candidate.predict_proba(X[features])[:,1],self.mapping)
                    np.testing.assert_allclose(actual.probability,expected,rtol=0,atol=1e-12)
        finally:self.candidate.chosen=original

    def test_predictions_are_order_and_chunk_invariant(self):
        with tempfile.TemporaryDirectory() as folder:
            export_model(self.candidate,self.mapping,self.contract,folder)
            sample=self.challenge.iloc[:65]
            full=predict_final(sample,folder).set_index('application_id')
            chunks=pd.concat([predict_final(sample.iloc[indices],folder) for indices in np.array_split(np.arange(len(sample)),3)]).set_index('application_id')
            shuffled=predict_final(sample.iloc[::-1],folder).set_index('application_id').loc[full.index]
            np.testing.assert_allclose(chunks.probability,full.probability,rtol=0,atol=1e-12)
            np.testing.assert_allclose(shuffled.probability,full.probability,rtol=0,atol=1e-12)

    def test_inference_rejects_leaks_missing_columns_and_invalid_values(self):
        with tempfile.TemporaryDirectory() as folder:
            export_model(self.candidate,self.mapping,self.contract,folder)
            sample=self.challenge.iloc[:2].copy()
            for bad in [sample.assign(default_within_90d=0),sample.drop(columns='age'),sample.assign(income_sar=np.inf),sample.assign(application_id='same')]:
                with self.assertRaises(ValueError): predict_final(bad,folder)
            self.assertEqual(len(predict_final(sample.iloc[:0],folder)),0)

    def test_model_checksum_and_manifest_paths(self):
        with tempfile.TemporaryDirectory() as folder:
            export_model(self.candidate,self.mapping,self.contract,folder)
            path=Path(folder)/'model.json';path.write_bytes(path.read_bytes()+b' ')
            with self.assertRaises(ValueError): load_model(folder)
            write_json(Path(folder)/'model_manifest.json',{'../private.json':'0'*64})
            with self.assertRaises(ValueError): load_model(folder)

    def test_batch_capacity_keeps_score_ties_together(self):
        p=pd.DataFrame({'application_id':[str(i) for i in range(10)],'probability':[.9,.8,.8,.5,.4,.3,.2,.1,.1,.1]})
        result,audit=apply_batch_policy(p,.2,CostPolicy(max_flag_fraction=.2))
        self.assertEqual(result.decision.tolist(),[1,0,0,0,0,0,0,0,0,0])
        self.assertEqual(audit['flagged'],1)
        self.assertEqual(apply_batch_policy(p.iloc[:1],.2)[1]['flagged'],0)
        self.assertEqual(apply_batch_policy(p,1.0000000000000002)[1]['flagged'],0)

    def test_batch_order_invariant_and_no_id_tie_breaking(self):
        p=pd.DataFrame({'application_id':[str(i) for i in range(100)],'probability':np.repeat([.9,.8,.7,.1],25)})
        result,_=apply_batch_policy(p,.5)
        changed,_=apply_batch_policy(p.sample(frac=1,random_state=7),.5)
        pd.testing.assert_frame_equal(result.sort_values('application_id').reset_index(drop=True),changed.sort_values('application_id').reset_index(drop=True))
        self.assertEqual(result.decision.sum(),0)

    def test_submission_rejects_wrong_ids_or_manually_changed_decisions(self):
        p=pd.DataFrame({'application_id':['a','b'],'probability':[.9,.1]})
        submitted,_=apply_batch_policy(p,.5)
        validate_submission(submitted,p,.5)
        with self.assertRaises(ValueError):validate_submission(submitted.assign(application_id=['x','b']),p,.5)
        with self.assertRaises(ValueError):validate_submission(submitted.assign(decision=[1,0]),p,.5)

    def test_recovery_is_labeled_and_disabled_for_assessment(self):
        csv=ROOT/'data/tamweel_oof_matrix.csv';meta=ROOT/'data/day5_oof_example.json'
        with self.assertRaises(ValueError):load_example(csv,meta,self.pool,assessment_mode=True)
        with self.assertRaises(ValueError):load_example(csv,meta,self.pool,FinalConfig(trees=160))
        example,_,_=load_example(csv,meta,self.pool)
        self.assertEqual(set(example.source),{'EDUCATIONAL_EXAMPLE'})
        self.assertEqual(reflection_check({k:'answer' for k in RESPONSES},'EDUCATIONAL_EXAMPLE')['status'],'EXAMPLE_ONLY_NOT_SUBMITTABLE')

    def test_bundle_detects_tampering_and_unsafe_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'data.csv').write_text('x\n1\n')
            _,archive=create_bundle(root,['data.csv'],{'source':'LIVE'})
            self.assertEqual(verify_bundle(archive)['files'],1)
            corrupt=root/'corrupt.zip'
            with zipfile.ZipFile(archive) as original,zipfile.ZipFile(corrupt,'w') as z:
                for name in original.namelist(): z.writestr(name,b'changed' if name=='data.csv' else original.read(name))
            with self.assertRaises(ValueError):verify_bundle(corrupt)
            unsafe=root/'unsafe.zip'
            with zipfile.ZipFile(unsafe,'w') as z:z.writestr('../outside.txt','escape')
            with self.assertRaises(ValueError):import_daily_evidence(unsafe,root/'evidence')
            with self.assertRaises(ValueError):create_bundle(root,['../data.csv'],{})

    def test_empty_learner_work_never_becomes_ready(self):
        self.assertEqual(reflection_check({})['status'],'LEARNER_WORK_REQUIRED')
        with tempfile.TemporaryDirectory() as folder:
            self.assertTrue(all(r['status']=='MISSING' for r in evidence_status(folder)))


if __name__=='__main__': unittest.main()

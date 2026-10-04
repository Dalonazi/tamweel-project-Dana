"""Regression tests for leakage, maturity, grouped splits and bounded tuning."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from day2_validation import (BASE_PARAMS, OUTER_WINDOWS, TUNING_WINDOWS, BudgetExpired, ValidationConfig,
    deduplicate_applications, evaluate_outer, feature_frame, fit_honest_model, leakage_audit,
    make_inner_stop, make_time_group_split, negative_controls, reflection_check, reserve_tuning_pool,
    safe_predict, summarize_folds, tune_on_reserved_pool)


class ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract=json.loads((ROOT/'data/data_contract.json').read_text(encoding='utf-8'))
        cls.dirty=pd.read_csv(ROOT/'data/tamweel_dirty.csv')
        cls.dictionary=pd.read_csv(ROOT/'data/feature_dictionary.csv')
        cls.frame,_=deduplicate_applications(pd.read_csv(ROOT/'data/tamweel_train.csv'))
        cls.names=[f['name'] for f in cls.contract['features']]
        cls.folds=make_time_group_split(cls.frame)
        cls.pool=reserve_tuning_pool(cls.frame,cls.folds)
        cls.config=ValidationConfig(max_trees=60,patience=10,trials=2)

    def test_dictionary_audit_and_unknown_fail_closed(self):
        audit=leakage_audit(self.dirty.assign(mystery_afterward=1),self.dictionary)
        self.assertEqual(set(audit.loc[audit.action=='DROP_POST_OUTCOME','feature']),{'days_past_due_60','collection_calls'})
        self.assertEqual(audit.loc[audit.feature=='mystery_afterward','action'].item(),'BLOCK_UNKNOWN')
        self.assertEqual(sum(audit.action=='KEEP'),22)
        with self.assertRaisesRegex(ValueError,'approved'):
            feature_frame(self.dirty[self.names+['collection_calls']],self.contract)

    def test_duplicate_events_removed_and_conflicts_rejected(self):
        duplicate=self.frame.iloc[[0]].copy()
        duplicate.application_id='DUPLICATE-EVENT'
        frame=pd.concat([self.frame,self.frame.iloc[[1]],duplicate],ignore_index=True)
        clean,report=deduplicate_applications(frame)
        self.assertEqual(len(clean),10000)
        self.assertEqual(report['duplicate_rows_removed'],2)
        conflict=self.frame.iloc[[0]].copy();conflict['income_sar']+=1
        with self.assertRaisesRegex(ValueError,'Conflicting'):
            deduplicate_applications(pd.concat([self.frame,conflict],ignore_index=True))

    def test_outer_and_inner_time_group_maturity(self):
        for fold in self.folds:
            t,v=self.frame.loc[fold['train']],self.frame.loc[fold['valid']]
            start=pd.Timestamp(fold['audit']['validation_start'])
            self.assertFalse(set(t.customer_id)&set(v.customer_id))
            self.assertLess((pd.to_datetime(t.application_date)+pd.Timedelta(days=90)).max(),start)
            fi,si,cut=make_inner_stop(t)
            self.assertFalse(set(t.loc[fi].customer_id)&set(t.loc[si].customer_id))
            self.assertLess((pd.to_datetime(t.loc[fi].application_date)+pd.Timedelta(days=90)).max(),pd.Timestamp(cut))
            self.assertTrue(set(fi).isdisjoint(si))

    def test_label_available_exactly_at_cutoff_is_excluded(self):
        extra=self.frame.iloc[[0,1]].copy()
        extra.application_id=['BOUNDARY-90','BOUNDARY-91']
        extra.customer_id=['UNSEEN-90','UNSEEN-91']
        start=pd.Timestamp(OUTER_WINDOWS[0][0])
        extra.application_date=[str((start-pd.Timedelta(days=n)).date()) for n in [90,91]]
        frame=pd.concat([self.frame,extra],ignore_index=True)
        folds=make_time_group_split(frame)
        ids=set(frame.loc[folds[0]['train'],'application_id'])
        self.assertNotIn('BOUNDARY-90',ids);self.assertIn('BOUNDARY-91',ids)

    def test_small_single_class_and_overlapping_folds_rejected(self):
        with self.assertRaisesRegex(ValueError,'few'):
            make_time_group_split(self.frame.head(40))
        with self.assertRaisesRegex(ValueError,'class'):
            make_time_group_split(self.frame.assign(default_within_90d=0))
        with self.assertRaisesRegex(ValueError,'nonoverlapping'):
            make_time_group_split(self.frame,[OUTER_WINDOWS[0],OUTER_WINDOWS[0]])
        with self.assertRaisesRegex(ValueError,'Deduplicate'):
            make_time_group_split(pd.concat([self.frame,self.frame.iloc[[0]]]))

    def test_search_has_no_outer_customer_or_unmatured_label(self):
        valid=np.concatenate([f['valid'] for f in self.folds])
        self.assertFalse(set(self.pool.customer_id)&set(self.frame.loc[valid].customer_id))
        self.assertLess((pd.to_datetime(self.pool.application_date)+pd.Timedelta(days=90)).max(),pd.Timestamp('2023-07-01'))
        for fold in make_time_group_split(self.pool,TUNING_WINDOWS):
            train,valid=self.pool.loc[fold['train']],self.pool.loc[fold['valid']]
            self.assertFalse(set(train.customer_id)&set(valid.customer_id))

    def test_outer_values_cannot_change_medians_or_stopping(self):
        fold=self.folds[0]
        model,a=fit_honest_model(self.frame.loc[fold['train']],self.contract,BASE_PARAMS,self.config)
        changed=self.frame.copy()
        changed.loc[fold['valid'],self.names]=999999
        changed.loc[fold['valid'],'default_within_90d']=1-changed.loc[fold['valid'],'default_within_90d']
        other,b=fit_honest_model(changed.loc[fold['train']],self.contract,BASE_PARAMS,self.config)
        self.assertEqual(a['selected_trees'],b['selected_trees'])
        for key in ['inner_imputer_medians','refit_imputer_medians']:
            np.testing.assert_array_equal(a[key],b[key])
        x=self.frame.loc[fold['valid'],self.names]
        np.testing.assert_allclose(safe_predict(model,x,self.contract),safe_predict(other,x,self.contract),rtol=0,atol=1e-12)
        with self.assertRaisesRegex(ValueError,'approved'):
            safe_predict(model,x.assign(collection_calls=1),self.contract)
        fi,_,_=make_inner_stop(self.frame.loc[fold['train']])
        np.testing.assert_allclose(a['inner_imputer_medians'],self.frame.loc[fi,self.names].median())

    def test_oof_ids_coverage_provenance_and_metrics(self):
        report,pred,provenance=evaluate_outer(self.frame,self.contract,self.folds,BASE_PARAMS,self.config,'test')
        self.assertEqual(len(pred),5039)
        self.assertFalse(pred.application_id.duplicated().any())
        self.assertTrue(pred.probability.between(0,1).all())
        for row,source in zip(report.itertuples(),provenance):
            rows=pred[pred.fold==row.fold]
            self.assertAlmostEqual(row.average_precision,average_precision_score(rows.default_within_90d,rows.probability))
            self.assertAlmostEqual(row.roc_auc,roc_auc_score(rows.default_within_90d,rows.probability))
            self.assertFalse(set(source['training_application_ids'])&set(source['validation_application_ids']))
        summary=summarize_folds(report).iloc[0]
        self.assertAlmostEqual(summary.ap_sd,report.average_precision.std(ddof=1))

    def test_tuning_limits_and_reproducibility(self):
        a,ha=tune_on_reserved_pool(self.pool,self.contract,self.config)
        b,hb=tune_on_reserved_pool(self.pool,self.contract,self.config)
        self.assertEqual(a['attempted_trials'],2)
        self.assertEqual(a['best_params'],b['best_params'])
        self.assertEqual(a['completed_trials'],2)
        np.testing.assert_allclose(ha.mean_ap,hb.mean_ap,rtol=0,atol=1e-12)
        with self.assertRaises(ValueError): ValidationConfig(trials=9)

    def test_timeout_before_first_trial_never_invents_parameters(self):
        result,history=tune_on_reserved_pool(self.pool,self.contract,ValidationConfig(timeout_seconds=0))
        self.assertEqual(result['status'],'NO_COMPLETED_TRIAL')
        self.assertIsNone(result['best_params'])
        self.assertTrue(history.empty)
        with self.assertRaises(BudgetExpired):
            fit_honest_model(self.pool,self.contract,BASE_PARAMS,self.config,deadline=0)

    def test_negative_control_is_labelled_and_not_for_oof_decisions(self):
        report=negative_controls(self.frame,self.dirty,self.contract,self.config)
        self.assertEqual(len(report),6)
        self.assertTrue((report.prediction_source=='NEGATIVE_CONTROL_NOT_FOR_DECISIONS').all())
        self.assertEqual(set(report.scheme),{'leaky_random_control','clean_random_control'})

    def test_reflection_does_not_award_grades(self):
        self.assertEqual(reflection_check({})['status'],'LEARNER_WORK_REQUIRED')
        result=reflection_check({k:'Written answer' for k in ['leak_example','split_reason','observed_gap','imputer_reason','limitations']})
        self.assertEqual(result['status'],'READY_FOR_REVIEW');self.assertIsNone(result['automatic_grade'])


if __name__=='__main__': unittest.main()

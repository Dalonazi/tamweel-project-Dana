"""Decision rules, OOF provenance and training-only imbalance transformations."""
from pathlib import Path
import json, sys, tempfile, unittest
from dataclasses import replace

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from day2_validation import deduplicate_applications, make_time_group_split, safe_predict
from day3_decision import (STRATEGIES, TARGET, NO_FLAGS_THRESHOLD, DecisionConfig, CostPolicy,
    capacity_limit, region_labels, positive_weight, oversample_positions, fit_strategy,
    generate_oof, validate_oof, threshold_sweep, select_threshold, flag_at,
    period_audit, region_audit, reflection_check, load_example, TrainingBudgetExpired)


def sample(y, p, folds=None):
    n = len(y)
    return pd.DataFrame({"application_id": [f"S{i}" for i in range(n)], TARGET: y,
        "probability": p, "fold": folds if folds is not None else [1]*n,
        "source": "LIVE", "split_role": "OOF", "strategy": "weighted", "region": "central"})


class DecisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads((ROOT / "data/data_contract.json").read_text(encoding="utf-8"))
        cls.frame, _ = deduplicate_applications(pd.read_csv(ROOT / "data/tamweel_train.csv"))
        cls.folds = make_time_group_split(cls.frame)
        cls.oof, cls.report, cls.provenance = generate_oof(cls.frame, cls.contract)

    def test_exact_sweep_matches_brute_force_confusion_and_capacity(self):
        pred = sample([0,1,0,1,1,0,0,0], [.9,.8,.8,.5,.3,.3,0,1], [1,1,1,1,2,2,2,2])
        policy = CostPolicy(10,1,.5)
        sweep = threshold_sweep(pred,policy)
        self.assertIn(.5,sweep.threshold.values)
        for row in sweep.itertuples():
            flagged = np.asarray(pred.probability) >= row.threshold
            tn,fp,fn,tp = confusion_matrix(pred[TARGET],flagged,labels=[0,1]).ravel()
            self.assertEqual((row.tn,row.fp,row.fn,row.tp),(tn,fp,fn,tp))
            self.assertEqual(row.loss_units,10*fn+fp)
            expected = all(flagged[pred.fold.eq(f)].sum() <= 2 for f in [1,2])
            self.assertEqual(row.capacity_feasible,expected)
        best = select_threshold(sweep)
        self.assertEqual(best['loss_units'],sweep.loc[sweep.capacity_feasible,'loss_units'].min())

    def test_capacity_checks_each_period_not_only_pooled_volume(self):
        pred=sample([1,0,0,0,1,0,0,0],[.9,.8,.7,.6,.2,.1,.05,.01],[1,1,1,1,2,2,2,2])
        sweep=threshold_sweep(pred,CostPolicy(max_flag_fraction=.5))
        row=sweep[sweep.threshold.eq(.5)].iloc[0]
        self.assertEqual(row.flag_fraction,.5)
        self.assertFalse(row.capacity_feasible)
        best=select_threshold(sweep)
        self.assertTrue(period_audit(pred,best['threshold'],CostPolicy(max_flag_fraction=.5)).within_capacity.all())

    def test_ties_preserved_no_flags_and_exact_round_trip(self):
        pred=sample([1,0,0,0],[1,1,.4,.4])
        chosen=select_threshold(threshold_sweep(pred,CostPolicy(max_flag_fraction=.25)))
        self.assertEqual(chosen['flagged'],0)
        self.assertEqual(chosen['threshold'],NO_FLAGS_THRESHOLD)
        decoded=json.loads(json.dumps(chosen))
        self.assertFalse(flag_at(pred.probability,decoded['threshold']).any())
        self.assertEqual(capacity_limit(25,.12),3)
        self.assertEqual(capacity_limit(1632,.12),195)
        zero=select_threshold(threshold_sweep(pred,CostPolicy(max_flag_fraction=0)))
        self.assertEqual(zero['flagged'],0)

    def test_tie_break_prefers_fewer_flags_then_higher_threshold(self):
        pred=sample([0,1],[.3,.7])
        best=select_threshold(threshold_sweep(pred,CostPolicy(0,0,1)),False)
        self.assertEqual(best['flagged'],0)
        self.assertEqual(best['threshold'],NO_FLAGS_THRESHOLD)

    def test_feasible_loss_need_not_beat_infeasible_default(self):
        pred=sample([1,1,0,0],[.9,.8,.1,.05])
        sweep=threshold_sweep(pred,CostPolicy(max_flag_fraction=0))
        default=sweep[sweep.threshold.eq(.5)].iloc[0]
        self.assertFalse(default.capacity_feasible)
        self.assertGreater(select_threshold(sweep)['loss_units'],default.loss_units)

    def test_invalid_inputs_and_zero_denominators_are_explicit(self):
        for args in [(-1,1,.12),(10,1,1.1),(np.nan,1,.12)]:
            with self.assertRaises(ValueError): CostPolicy(*args)
        pred=sample([0,0],[.2,.8])
        sweep=threshold_sweep(pred)
        self.assertTrue(sweep.recall.isna().all())
        self.assertTrue(pd.isna(sweep.iloc[-1].precision))
        for changed in [pred.iloc[:0],pred.assign(probability=np.nan),pred.assign(probability=1.2),
                        pred.assign(split_role='HOLDOUT'),pd.concat([pred,pred.iloc[[0]]])]:
            with self.assertRaises(ValueError): threshold_sweep(changed)
        with self.assertRaises(ValueError): flag_at([.1],float('inf'))

    def test_weights_and_sampling_use_only_training_distribution(self):
        train=self.frame.loc[self.folds[0]['train']]
        p=positive_weight(train[TARGET])
        self.assertAlmostEqual(p,(len(train)-train[TARGET].sum())/train[TARGET].sum())
        positions=oversample_positions(train[TARGET])
        np.testing.assert_array_equal(positions,oversample_positions(train[TARGET]))
        resampled=train.iloc[positions]
        self.assertEqual(resampled[TARGET].mean(),.5)
        self.assertTrue(set(resampled.application_id)<=set(train.application_id))
        self.assertFalse(set(resampled.customer_id)&set(self.frame.loc[self.folds[0]['valid']].customer_id))
        for source in self.provenance['models']:
            if source['strategy']=='weighted':
                self.assertEqual(source['scale_pos_weight'],source['negative_positive_ratio'])
            if source['strategy']=='oversampled':
                self.assertEqual(source['fitted_positive_rate'],.5)
                self.assertTrue(set(source['resampled_application_ids'])<=set(source['training_application_ids']))
        with self.assertRaises(ValueError): positive_weight([1,1])

    def test_imputer_is_fit_before_resampling_and_validation_changes_cannot_affect_fit(self):
        fold=self.folds[0];train=self.frame.loc[fold['train']]
        names=[f['name'] for f in self.contract['features']]
        model,a=fit_strategy(train,self.contract,'oversampled')
        np.testing.assert_allclose(a['imputer_medians'],train[names].median())
        changed=self.frame.copy()
        changed.loc[fold['valid'],names]=999999
        changed.loc[fold['valid'],TARGET]=1-changed.loc[fold['valid'],TARGET]
        other,b=fit_strategy(changed.loc[fold['train']],self.contract,'oversampled')
        self.assertEqual(a['resampled_application_ids'],b['resampled_application_ids'])
        X=self.frame.loc[fold['valid'],names]
        np.testing.assert_allclose(safe_predict(model,X,self.contract),safe_predict(other,X,self.contract),rtol=0,atol=1e-12)

    def test_oof_complete_and_same_rows_across_strategies(self):
        coverage=validate_oof(self.oof,self.frame,self.folds)
        self.assertEqual(coverage['eligible_rows'],5039)
        self.assertEqual(coverage['warmup_without_oof'],4961)
        self.assertEqual(len(self.report),9)
        for source in self.provenance['models']:
            train=self.frame.set_index('application_id').loc[source['training_application_ids']]
            valid=self.frame.set_index('application_id').loc[source['validation_application_ids']]
            self.assertFalse(set(train.customer_id)&set(valid.customer_id))
            boundary=pd.Timestamp(self.folds[source['fold']-1]['audit']['validation_start'])
            self.assertTrue((pd.to_datetime(train.application_date)+pd.Timedelta(days=90)<boundary).all())
        changed=self.oof.copy();changed.loc[0,'fold']=3
        with self.assertRaises(ValueError): validate_oof(changed,self.frame,self.folds)
        with self.assertRaises(ValueError): validate_oof(self.oof.iloc[1:],self.frame,self.folds)

    def test_region_denominator_gap_and_missing_group(self):
        pred=sample([0,0,1,0,1],[.9,.1,.8,.8,.2]).assign(region=['central','central','central','western','western'])
        table,info=region_audit(pred,.5)
        central=table[table.region=='central'].iloc[0]
        self.assertEqual(central.false_positive_rate,.5)
        self.assertEqual(info['fpr_gap_percentage_points'],50)
        self.assertTrue(table.loc[table.region=='eastern','false_positive_rate'].isna().all())
        broken=self.frame.copy();broken.loc[0,['region_central','region_western']]=1
        with self.assertRaises(ValueError): region_labels(broken)

    def test_budget_does_not_return_partial_oof_and_example_blocked_in_assessment(self):
        with self.assertRaises(TrainingBudgetExpired): generate_oof(self.frame,self.contract,DecisionConfig(timeout_seconds=0))
        with self.assertRaises(ValueError): DecisionConfig(trees=1000)
        with self.assertRaisesRegex(ValueError,'assessment'):
            load_example(Path('unused.csv'),Path('unused.json'),self.frame,self.folds,assessment_mode=True)

    def test_cost_sensitivity_and_reflection_never_award_grades(self):
        pred=self.oof[self.oof.strategy=='weighted']
        for fn in [8,10,12]:
            policy=CostPolicy(fn,1,.12)
            rule=select_threshold(threshold_sweep(pred,policy))
            self.assertTrue(period_audit(pred,rule['threshold'],policy).within_capacity.all())
        empty=reflection_check({})
        self.assertEqual(empty['status'],'LEARNER_WORK_REQUIRED')
        filled={key:'My evidence' for key in empty['missing']}
        self.assertEqual(reflection_check(filled)['status'],'READY_FOR_REVIEW')
        self.assertEqual(reflection_check(filled,'EDUCATIONAL_EXAMPLE')['status'],'EXAMPLE_ONLY_NOT_SUBMITTABLE')
        self.assertIsNone(reflection_check(filled)['automatic_grade'])


if __name__=='__main__': unittest.main()

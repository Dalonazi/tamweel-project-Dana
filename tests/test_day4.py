"""Checks for role separation, calibration, explanation units and queue limits."""
from pathlib import Path
import sys, json, tempfile, unittest
from dataclasses import replace
import numpy as np
import pandas as pd
from scipy.special import expit

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from day4_trust import *
from day2_validation import deduplicate_applications


class TrustChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frame,_=deduplicate_applications(pd.read_csv(ROOT/'data/tamweel_train.csv'))
        cls.contract=json.loads((ROOT/'data/data_contract.json').read_text(encoding='utf-8'))
        cls.parts,cls.assignment=split_roles(cls.frame)
        cls.model,cls.cal,cls.pred,cls.info=fit_and_calibrate(cls.parts,cls.contract)

    def test_roles_are_group_disjoint_and_mature(self):
        assert_roles(self.parts)
        self.assertEqual([len(self.parts[r]) for r in ROLES],[2516,584,589,1733])
        self.assertEqual(len(self.assignment),10000)
        bad=dict(self.parts);bad['calibration']=self.parts['fit']
        with self.assertRaises(ValueError):assert_roles(bad)
        bad={k:v.copy() for k,v in self.parts.items()}
        bad['fit'].loc[bad['fit'].index[0],'application_date']='2023-04-02'
        with self.assertRaises(ValueError):assert_roles(bad)

    def test_evaluation_labels_cannot_affect_fit_calibration_or_threshold(self):
        changed={k:v.copy() for k,v in self.parts.items()}
        changed['evaluation'][TARGET]=1-changed['evaluation'][TARGET]
        m,c,p,info=fit_and_calibrate(changed,self.contract)
        self.assertEqual(model_fingerprint(m),model_fingerprint(self.model))
        self.assertEqual(info['calibration_mapping'],self.info['calibration_mapping'])
        self.assertEqual(choose_policy_threshold(p[p.role=='policy'])[0],choose_policy_threshold(self.pred[self.pred.role=='policy'])[0])
        np.testing.assert_array_equal(p.calibrated_probability,self.pred.calibrated_probability)

    def test_imputer_and_weight_use_fit_only(self):
        names=self.info['feature_names'];fit=self.parts['fit']
        np.testing.assert_allclose(self.info['imputer_medians'],fit[names].median().to_numpy())
        self.assertAlmostEqual(self.info['scale_pos_weight'],(fit[TARGET]==0).sum()/fit[TARGET].sum())

    def test_calibration_mapping_preserves_observed_ranking(self):
        mapping=self.info['calibration_mapping']
        self.assertLess(mapping['a'],0)
        np.testing.assert_allclose(map_probability(self.pred.raw_probability,mapping),self.pred.calibrated_probability,atol=1e-14,rtol=0)
        ev=self.pred[self.pred.role=='evaluation']
        self.assertEqual(roc_auc_score(ev[TARGET],ev.raw_probability),roc_auc_score(ev[TARGET],ev.calibrated_probability))
        with self.assertRaises(ValueError):transport_threshold(.5,{**mapping,'strictly_increasing':False})

    def test_fixed_bins_include_endpoints_and_empty_bins(self):
        table=reliability_table([0,1,1],[0.,.5,1.],10)
        self.assertEqual(table['count'].sum(),3)
        self.assertEqual(table.iloc[-1]['count'],1)
        self.assertTrue(np.isnan(table.iloc[1].observed_rate))
        self.assertAlmostEqual(probability_metrics([0,1,1],[0.,.5,1.])['ece'],1/6)
        self.assertAlmostEqual(probability_metrics([0,1,1],[0.,.5,1.])['brier'],1/12)
        self.assertIsNone(probability_metrics([0,0],[.1,.2])['roc_auc'])
        with self.assertRaises(ValueError):reliability_table([0,1],[.2,np.nan])

    def test_policy_role_guard_and_exact_optimum(self):
        with self.assertRaises(ValueError):choose_policy_threshold(self.pred[self.pred.role=='evaluation'])
        rows=self.pred[self.pred.role=='policy'];chosen,sweep=choose_policy_threshold(rows)
        self.assertEqual(chosen['loss_units'],sweep.loc[sweep.feasible,'loss_units'].min())
        flags=rows.raw_probability>=chosen['threshold']
        self.assertEqual(flags.sum(),chosen['flagged'])
        self.assertLessEqual(flags.sum(),len(rows)*12//100)

    def test_ties_and_no_flags_are_feasible(self):
        rows=pd.DataFrame({'application_id':['a','b'],'role':['policy']*2,TARGET:[0,1],'raw_probability':[1.,1.]})
        chosen,_=choose_policy_threshold(rows,CostPolicy(max_flag_fraction=0))
        self.assertGreater(chosen['threshold'],1)
        self.assertEqual(chosen['flagged'],0)
        self.assertGreater(transport_threshold(chosen['threshold'],self.info['calibration_mapping']),1)

    def test_threshold_transport_does_not_retune_evaluation_capacity(self):
        chosen,_=choose_policy_threshold(self.pred[self.pred.role=='policy'])
        mapped=transport_threshold(chosen['threshold'],self.info['calibration_mapping'])
        flags,audit,band=review_audit(self.pred[self.pred.role=='evaluation'],chosen['threshold'],mapped)
        self.assertTrue(np.array_equal(flags.risk_flag,flags.raw_probability>=chosen['threshold']))
        self.assertTrue((audit.candidate_review>=audit.risk_flags).all())
        self.assertFalse(audit.candidate_within_capacity.all())
        self.assertEqual(band['half_width'],.02)

    def test_permutation_joint_region_and_signed_drops(self):
        result=permutation_report(self.model,self.parts['evaluation'],self.contract,TrustConfig(permutation_repeats=2))
        region=result[result.feature_group=='region_indicators_joint'].iloc[0]
        self.assertEqual(len(region['columns'].split('|')),3)
        np.testing.assert_allclose(result.mean_ap_drop,result[['drop_1','drop_2']].mean(axis=1))

    def test_shap_adds_in_raw_log_odds(self):
        result,meta=explain_sample(self.model,self.parts['evaluation'],self.contract,TrustConfig(shap_rows=20))
        np.testing.assert_allclose(result['base_values']+result['values'].sum(axis=1),result['raw_margin'],atol=1e-8)
        self.assertEqual(result['values'].shape,(20,22))
        self.assertIn('log-odds',meta['units'])
        self.assertGreater(np.max(np.abs(result['base_values']+result['values'].sum(axis=1)-expit(result['raw_margin']))),.1)

    def test_budget_example_identity_and_assessment_guard(self):
        with self.assertRaises(ShapBudgetExpired):explain_sample(self.model,self.parts['evaluation'],self.contract,TrustConfig(shap_seconds=0))
        npz=ROOT/'data/day4_shap_example.npz';meta=ROOT/'data/day4_shap_example.json'
        result,info=load_shap_example(npz,meta,self.model,self.parts['evaluation'],self.contract)
        self.assertEqual(info['source'],'EDUCATIONAL_EXAMPLE')
        with self.assertRaises(ValueError):load_shap_example(npz,meta,self.model,self.parts['evaluation'],self.contract,True)
        with tempfile.TemporaryDirectory() as directory:
            broken=Path(directory)/'wrong.json';payload=json.loads(meta.read_text());payload['model_sha256']='0'*64
            broken.write_text(json.dumps(payload))
            with self.assertRaises(ValueError):load_shap_example(npz,broken,self.model,self.parts['evaluation'],self.contract)

    def test_reason_codes_are_positive_ordered_and_noncausal(self):
        reasons=reason_codes(np.array([.2,-3.,.4]),['a','b','c'],[1,2,3],{'a':'A','b':'B','c':'C'})
        self.assertEqual(list(reasons.feature),['c','a'])
        self.assertTrue(all('لا يثبت' in reason for reason in reasons.reason_ar))
        self.assertEqual(len(reason_codes(np.array([-.1]),['a'],[1],{'a':'A'})),0)

    def test_cluster_bootstrap_keeps_customer_rows_together(self):
        tiny=pd.DataFrame({'role':['evaluation']*6,'customer_id':['a','a','b','b','c','c'],TARGET:[0,1,0,1,0,1],
            'raw_probability':[.1,.8,.2,.7,.3,.6],'calibrated_probability':[.05,.9,.1,.8,.2,.7]})
        table,summary=cluster_bootstrap(tiny,TrustConfig(bootstrap_repeats=20))
        self.assertTrue((table.rows==6).all())
        self.assertEqual(summary['valid'],20)
        self.assertEqual(summary['customers'],3)
        self.assertAlmostEqual(summary['brier_change']['lower'],table.brier_change.quantile(.025))
        again,_=cluster_bootstrap(tiny,TrustConfig(bootstrap_repeats=20))
        pd.testing.assert_frame_equal(table,again)

    def test_reflection_and_config_guards(self):
        self.assertEqual(reflection_check({},'LIVE')['status'],'LEARNER_WORK_REQUIRED')
        filled={key:'شرح' for key in ('global_local','output_units','reason_limits','calibration_evidence','stability','review_capacity')}
        self.assertEqual(reflection_check(filled,'LIVE')['status'],'READY_FOR_REVIEW')
        self.assertEqual(reflection_check(filled,'EDUCATIONAL_EXAMPLE')['status'],'EXAMPLE_ONLY_NOT_SUBMITTABLE')
        with self.assertRaises(ValueError):TrustConfig(shap_rows=10000)


if __name__=='__main__':unittest.main()

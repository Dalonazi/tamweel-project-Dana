"""Scientific isolation and reproducibility checks for the Day 1 lab."""
import json
from pathlib import Path
import sys
import unittest
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from day1_lab import (LabConfig, MODEL_NAMES, compare_models, fit_model,
                      learner_checkpoint, make_splits, select_tree_count)


class Day1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frame = pd.read_csv(ROOT / "data/tamweel_train.csv")
        cls.contract = json.loads((ROOT / "data/data_contract.json").read_text(encoding="utf-8"))
        cls.X, cls.y, cls.splits = make_splits(cls.frame, cls.contract)
        cls.config = LabConfig(max_trees=80, patience=10)
        cls.selections, cls.models, cls.timings = {}, {}, {}
        s = cls.splits
        for name in MODEL_NAMES:
            if name != MODEL_NAMES[0]:
                cls.selections[name] = select_tree_count(name, cls.X.loc[s["inner_fit"]],
                    cls.y.loc[s["inner_fit"]], cls.X.loc[s["inner_stop"]],
                    cls.y.loc[s["inner_stop"]], cls.config)
            cls.models[name], cls.timings[name] = fit_model(name, cls.X.loc[s["development"]],
                cls.y.loc[s["development"]], cls.config, cls.selections.get(name))
        cls.table, cls.probs = compare_models(cls.models, cls.timings, cls.selections,
            cls.X.loc[s["comparison"]], cls.y.loc[s["comparison"]])

    def test_split_isolation_and_reproducibility(self):
        s = self.splits
        self.assertEqual([len(s[k]) for k in s], [8000, 2000, 6000, 2000])
        self.assertFalse(set(s["development"]) & set(s["comparison"]))
        self.assertFalse(set(s["inner_fit"]) & set(s["inner_stop"]))
        self.assertEqual(set(s["inner_fit"]) | set(s["inner_stop"]), set(s["development"]))
        _, _, again = make_splits(self.frame, self.contract)
        for key in s:
            np.testing.assert_array_equal(s[key], again[key])
            self.assertLess(abs(self.y.loc[s[key]].mean() - self.y.mean()), 0.002)

    def test_metadata_and_future_information_excluded(self):
        frame = self.frame.assign(collections_after_application=999)
        X, _, _ = make_splits(frame, self.contract)
        self.assertEqual(list(X), [f["name"] for f in self.contract["features"]])
        self.assertEqual(len(X.columns), 22)
        self.assertFalse(set(self.contract["metadata"]) & set(X.columns))

    def test_outer_perturbation_does_not_change_training(self):
        altered = self.X.copy()
        altered.loc[self.splits["comparison"], :] = 999999
        s = self.splits
        for name in MODEL_NAMES[1:]:
            selection = select_tree_count(name, altered.loc[s["inner_fit"]], self.y.loc[s["inner_fit"]],
                altered.loc[s["inner_stop"]], self.y.loc[s["inner_stop"]], self.config)
            original = self.selections[name]
            self.assertEqual(selection["selected_trees"], original["selected_trees"])
            np.testing.assert_array_equal(selection["inner_imputer_medians"], original["inner_imputer_medians"])
            np.testing.assert_array_equal(selection["curves"]["stop"], original["curves"]["stop"])
        for name in MODEL_NAMES:
            model, _ = fit_model(name, altered.loc[s["development"]], self.y.loc[s["development"]],
                                  self.config, self.selections.get(name))
            np.testing.assert_allclose(model.predict_proba(self.X.loc[s["comparison"]])[:, 1],
                                       self.probs[name], rtol=0, atol=1e-12)

    def test_medians_learn_only_their_training_rows(self):
        for name, selection in self.selections.items():
            np.testing.assert_allclose(selection["inner_imputer_medians"],
                                       self.X.loc[self.splits["inner_fit"]].median().to_numpy())
        for model in self.models.values():
            np.testing.assert_allclose(model.named_steps["imputer"].statistics_,
                                       self.X.loc[self.splits["development"]].median().to_numpy())

    def test_metrics_reconcile_and_probabilities_valid(self):
        y = self.y.loc[self.splits["comparison"]]
        self.assertEqual(self.table.model.tolist(), list(MODEL_NAMES))
        self.assertTrue(np.isfinite(self.probs).all().all())
        self.assertTrue(self.probs.ge(0).all().all() and self.probs.le(1).all().all())
        for row in self.table.itertuples():
            self.assertAlmostEqual(row.roc_auc, roc_auc_score(y, self.probs[row.model]))
            self.assertAlmostEqual(row.average_precision, average_precision_score(y, self.probs[row.model]))
            self.assertGreater(row.train_seconds, 0)
            self.assertAlmostEqual(row.train_seconds, row.selection_seconds + row.refit_seconds)

    def test_selected_trees_used_in_refit(self):
        for name, selected in self.selections.items():
            self.assertGreaterEqual(selected["selected_trees"], 1)
            self.assertLessEqual(selected["selected_trees"], self.config.max_trees)
            self.assertEqual(self.models[name].named_steps["model"].n_estimators, selected["selected_trees"])
        self.assertIsNone(self.models["XGBoost"].named_steps["model"].early_stopping_rounds)

    def test_overlap_and_single_class_rejected(self):
        with self.assertRaisesRegex(ValueError, "separate"):
            select_tree_count("XGBoost", self.X.head(20), self.y.head(20), self.X.head(20), self.y.head(20), self.config)
        with self.assertRaisesRegex(ValueError, "Both binary"):
            make_splits(self.frame.assign(default_within_90d=0), self.contract)

    def test_missing_learner_work_never_receives_completion_or_grade(self):
        empty = learner_checkpoint(None, {}, "", ["", ""])
        self.assertEqual(empty["status"], "LEARNER_WORK_REQUIRED")
        self.assertIsNone(empty["automatic_grade"])
        complete = learner_checkpoint(MODEL_NAMES[0], {k: "Written response" for k in
            ["evidence", "limitation", "next_test"]}, "Problem", ["Answer 1", "Answer 2"])
        self.assertEqual(complete["status"], "READY_FOR_REVIEW")
        self.assertIsNone(complete["automatic_grade"])


if __name__ == "__main__":
    unittest.main()

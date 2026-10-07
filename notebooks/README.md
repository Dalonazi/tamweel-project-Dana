#Credit Risk Modelling and Decision Support
Project Overview
This project develops and validates an end-to-end credit risk modelling and decision-support workflow for predicting whether an applicant will default within 90 days.
The objective extends beyond building a model with strong predictive performance. The project evaluates whether the modelling process is methodologically sound, whether predicted probabilities are reliable, whether individual predictions can be explained, and whether model outputs can be translated into an operational decision under realistic review-capacity constraints.
The project therefore separates three related but distinct questions:
Can the model identify higher-risk applications?
Can the model's scores be interpreted and translated into reliable risk probabilities?
How should those predictions be converted into an operational review decision?
The final workflow combines model development, forward validation, cost-sensitive decision-making, explainability, probability calibration, capacity management and model-governance considerations.
Intended use: The project is a synthetic credit-risk modelling exercise designed to demonstrate a controlled model-development and validation workflow. Model outputs support prioritisation and review rather than autonomous credit approval or rejection.
Business Problem
Credit default is an imbalanced classification problem: only a relatively small proportion of applicants experience the target event.
In the initial dataset, the default rate was approximately 7.9%. This means that conventional accuracy can provide a misleading view of model quality. A model can achieve high accuracy simply by predicting the majority class while failing to identify applicants who later default.
The modelling objective was therefore defined as:
Predict whether an applicant will default within 90 days using information available at the application decision point.
This decision-time definition is important because information generated after the application cannot legitimately be used to predict a decision that would have been made earlier.
The project consequently evaluates model performance using metrics such as ROC-AUC and Average Precision, while later stages explicitly consider the different consequences of false positives and false negatives.
Project Workflow
The project was developed progressively across five modelling stages:
Stage Objective Main Question
Day 1 Baseline modelling Which candidate model provides the strongest initial evidence?
Day 2 Honest validation Does performance remain credible after controlling leakage and temporal structure?
Day 3 Cost-sensitive decisions What threshold balances model errors and operational capacity?
Day 4 Explainability & calibration Why does the model make its predictions, and are its probabilities reliable?
Day 5 Final model selection Does additional ensemble complexity provide enough value to justify deployment?
Each stage produces evidence that is used by the following stage rather than treating model development as a single train/test exercise.
1. Baseline Model Development
The first stage established an initial benchmark across three candidate classification models:
Logistic Regression
XGBoost
LightGBM
The initial dataset contained:
10,000 applications
22 predictors
approximately 7.9% positive/default cases
The initial teaching comparison produced:
Model ROC-AUC Average Precision Training Time
Logistic Regression 0.8213 0.3258 0.0486 s
XGBoost 0.8124 0.3338 0.3099 s
LightGBM 0.8138 0.3248 0.2125 s
Day 1 model comparison
Initial Interpretation
No candidate dominated every metric.
Logistic Regression achieved the strongest ROC-AUC and was substantially faster to train, while XGBoost achieved the highest Average Precision.
Because defaults represented only around 7.9% of observations, Average Precision provided useful additional evidence about performance on the minority class. XGBoost was therefore carried forward provisionally based on its stronger AP.
However, the difference was not interpreted as proof that XGBoost was universally superior.
The Day 1 split diagnostic also identified 1,226 customers shared between development and comparison samples, meaning that the initial comparison was not yet customer-independent.
This limitation motivated the more rigorous validation framework introduced in Day 2.
2. Leakage Control and Honest Validation
Strong model performance is only useful when the validation process represents the information that would genuinely have been available at prediction time.
The second stage therefore focused on:
leakage detection;
chronological validation;
customer separation;
target maturity;
training-only preprocessing;
bounded hyperparameter tuning; and
out-of-fold prediction generation.
Leakage Audit
Variables that would only become available after application were excluded from the predictive feature set.
Examples identified during the audit included:
days_past_due_60
collection_calls
These variables contain information generated after the lending decision. Including them would allow the model to indirectly observe information about the future outcome.
The effect of leakage was clearly visible in the validation results.
Validation Protocol ROC-AUC Average Precision
Leaky random control 0.9999 0.9988
Clean random control 0.8010 0.3110
Honest fixed protocol 0.7976 0.3153
Honest reserved-search protocol 0.7855 0.3133
The AP difference between the deliberately leaky and clean random controls was:
0.6879
The near-perfect leaky result therefore represents a warning rather than a successful model. It demonstrates how post-outcome information can create unrealistically strong apparent performance.
Forward Validation
The honest validation design used three forward periods while keeping customers separated between training and validation.
Fold Training Requests Validation Requests Shared Customers
1 3,223 1,632 0
2 4,460 1,674 0
3 5,731 1,733 0
The design ensures that later applications are evaluated using models developed from earlier information and prevents the same customer from appearing on both sides of an individual fold.
A 90-day target maturity rule was also applied so that the model was trained only on outcomes that would have been observable by the relevant validation date.
The reserved tuning cohort contained 1,935 applications and 176 positive cases. Hyperparameter search was deliberately bounded rather than repeatedly optimising against the outer validation periods.
Analytical Takeaway
The most important result from Day 2 is not that one validation protocol produced a slightly higher score than another.
It is that validation design materially changes how much confidence can be placed in the reported performance.
Random validation may appear reasonable numerically while still failing to represent how the model would encounter future customers. Forward, customer-separated validation provides a more defensible estimate of temporal generalisation.
3. Cost-Sensitive Decision Policy
A predictive score does not by itself determine what action should be taken.
Day 3 therefore moved from:
Which applicant has higher predicted risk?
to:
Which applications should actually be flagged for review?
This requires considering the consequences of classification errors.
The project used the teaching loss function:
\text{Loss} = 10 \times FN + FP
where a false negative is assigned greater cost than a false positive.
This reflects the principle that failing to identify a future default can have a different consequence from unnecessarily flagging a non-defaulting application.
Why Accuracy Is Insufficient
The imbalance problem is visible from a simple benchmark.
A rule that flags no applications at all achieves approximately:
92.38% accuracy
but:
0% recall
It therefore identifies none of the positive cases.
This demonstrates why model evaluation and threshold selection cannot be based on accuracy alone.
Threshold Selection
Threshold selection was performed using out-of-fold development predictions so that each observation was scored by a model that had not been fitted on that observation.
The selected operational threshold was approximately:
0.6583
At this threshold:
526 of 5,039 requests were flagged;
flag rate = 10.44%;
recall = approximately 0.4089;
observed teaching loss = 2,639 units.
The selected policy remained within the 12% review-capacity constraint.
The threshold also remained selected when the false-negative cost was varied from 8 to 12, although total loss changed accordingly.
Analytical Takeaway
The classification threshold is therefore not simply the library default of 0.50.
It is part of the business decision policy.
Lower thresholds generally identify more positive cases but create more review work and false positives. Higher thresholds reduce workload but increase the risk of missing positive cases.
The final operating point balances:
risk detection + error cost + review capacity
rather than optimising a single statistical metric.
Regional Diagnostic
The same threshold was applied across regional groups.
Observed false-positive rates were approximately:
Region False-Positive Rate
Central 8.09%
Western 8.29%
Eastern 7.72%
Other 7.64%
The maximum observed gap was approximately 0.65 percentage points.
These results are treated as a descriptive diagnostic, not as proof that the model is fair or unfair. Group-level differences require continued monitoring and contextual investigation.
4. Model Explainability
Day 4 examined both global and local model behaviour.
Two complementary approaches were used:
Permutation importance to measure how much predictive performance depends on individual features;
SHAP to examine how features contribute to model scores.
SHAP summary
Global Explanation
The global SHAP analysis identified the strongest average contributors to the model score.
Among the leading features were:
bureau_score
dti
loan_amount_sar
bureau_score had a mean absolute SHAP magnitude of approximately 0.904 log-odds, followed by dti at approximately 0.544 and loan_amount_sar at approximately 0.349.
This indicates that the fitted model relied strongly on information associated with credit history, indebtedness and requested financing amount.
Local Explanation
Global importance does not explain every individual application.
For an individual request, SHAP was used to decompose the model's raw score into feature-level contributions.
A feature with a positive SHAP value pushes the model toward a higher predicted risk score, while a negative contribution pushes it toward a lower score.
Importantly:
SHAP values are expressed in raw log-odds, not probability percentage points.
The explanations describe how the model generated a prediction. They do not establish that a feature causes default.
Correlated features can also share predictive information, so individual importance values should not be interpreted in isolation.
5. Probability Calibration
Ranking applications correctly and estimating reliable probabilities are different modelling objectives.
A model can successfully rank higher-risk applicants above lower-risk applicants while still systematically overestimating or underestimating the absolute probability of default.
Probability calibration was therefore evaluated separately.
Reliability curve
On the Day 4 evaluation sample of 1,733 requests with 139 positive outcomes, discrimination remained unchanged after sigmoid calibration:
ROC-AUC ≈ 0.771
Average Precision ≈ 0.259
However, probability-quality measures improved substantially:
Metric Raw Calibrated
Brier Score 0.113 0.067
ECE 0.147 0.022
The important distinction is that calibration did not improve the ordering of applications.
Instead, it improved the correspondence between predicted probabilities and observed event frequencies.
This separates two questions:
Discrimination:
 Who is riskier?
from:
Calibration:
 How trustworthy is the reported probability?
6. Stability Analysis
The observed calibration improvement was further examined using a paired customer-cluster bootstrap.
Stability analysis
The procedure used 200 bootstrap replicates while keeping requests from the same customer together.
The observed change in Brier score was approximately:
−0.046
with a 95% percentile interval of approximately:
−0.054 to −0.037
Because the interval remained below zero, the measured calibration improvement was consistent across these evaluation-data resamples.
However, this interval has a deliberately limited interpretation.
It measures sampling variation while keeping the fitted model and calibration procedure fixed. It does not capture:
uncertainty from retraining;
future population changes;
macroeconomic changes;
changes in application behaviour; or
long-term model drift.
It should therefore not be interpreted as a guarantee of future production performance.
7. Final Model Selection
The final stage reconsidered whether combining several models produced enough incremental value to justify the additional complexity.
The candidate approaches included:
Logistic Regression;
XGBoost;
LightGBM;
equal-weight averaging;
weighted averaging; and
stacking.
The comparison used nested forward out-of-fold evidence rather than selecting the final approach from a single random holdout.
Final model comparison
The ensemble candidates were assessed against a predefined worth-it gate. An ensemble was only considered preferable if its performance improvement was large enough to justify the additional modelling and governance complexity.
The ensemble alternatives did not pass this gate.
The final decision was therefore:
KEEP SINGLE MODEL — LOGISTIC REGRESSION
This result is important because model complexity is not itself a measure of model quality.
The candidate models also exhibited high residual correlation, indicating that they tended to make many of the same errors. Combining highly similar model signals therefore offered limited incremental information.
The simpler Logistic Regression solution was retained because the available forward-validation evidence did not justify the additional complexity of an ensemble.
8. Final Decision Policy and Capacity
The final workflow separates predictive modelling from operational decision-making.
For the final 2,500-request batch:
approximately 330 requests exceeded the transported threshold;
operational review capacity was 12% of the batch;
therefore, a maximum of 300 requests could be reviewed.
The capacity policy retained the 300 highest-priority requests.
This is an important operational distinction.
The model does not independently decide that every above-threshold application must receive the same action. Instead:
copy


Application
     ↓
Risk model
     ↓
Predicted risk
     ↓
Decision threshold
     ↓
Capacity policy
     ↓
Prioritised review

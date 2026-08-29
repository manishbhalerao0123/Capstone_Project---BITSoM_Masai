# Credit Risk & Lending ML

## Project Overview

This project develops a machine learning pipeline for retail credit-risk assessment using traditional credit information and alternative data signals. The objective is to predict loan default risk, detect unusual borrower behavior, evaluate model fairness, and provide lending recommendations.

The project is divided into four parts:

1. Part A – Exploratory Data Analysis (EDA) and Preprocessing
2. Part B – Classification Models
3. Part C – Anomaly Detection and Optional Segmentation
4. Part D – Bias-Awareness Note and Final Recommendation

---

# Dataset Description

## credit_applicants.csv

Contains applicant-level information used for credit-risk modeling.

### Fields

- applicant_id
- age
- monthly_income_inr
- existing_loans_count
- credit_utilization_ratio
- upi_monthly_inflow_inr
- bounced_payments_count
- credit_bureau_score
- employment_type
- default

### Target Variable

```text
default
```

Values:

```text
0 = Non-default
1 = Default
```

---

## txn_behaviour.csv

Contains applicant transaction-behavior information used for anomaly detection.

### Fields

- txn_id
- applicant_id
- txn_hour
- is_new_device
- txn_amount_inr
- channel

The dataset includes intentionally injected anomalous transactions for fraud-risk analysis.

---

# Installation

## Prerequisites

- Python 3.10+
- Jupyter Notebook

## Install Dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

---

# Project Structure

```text
credit_risk_lending_ml/
│
├── credit_applicants.csv
├── txn_behaviour.csv
│
├── eda_preprocessing.ipynb
├── classification_models.ipynb
├── anomaly_detection.ipynb
│
├── confusion_matrix.png
├── roc_curve.png
├── feature_importance.png
├── anomaly_scatter.png
│
└── README.md
```

---

# Running the Project

Launch Jupyter Notebook:

```bash
jupyter notebook
```

Execute notebooks in the following order:

1. eda_preprocessing.ipynb
2. classification_models.ipynb
3. anomaly_detection.ipynb

Run all cells.

---

# Part A – EDA and Preprocessing

## Objectives

- Understand applicant characteristics
- Measure default rate
- Measure missingness
- Prepare data for machine learning

---

## Missing Credit Bureau Scores

A percentage of applicants have missing values in:

```text
credit_bureau_score
```

These applicants are treated as:

```text
Thin-file customers
```

or

```text
New-to-credit customers
```

### Design Decision

Rows with missing bureau scores are NOT removed.

Reason:

Removing these rows would exclude an important borrower segment that alternative data is specifically designed to evaluate.

---

## Thin-File Flag

Feature:

```text
is_thin_file
```

Definition:

```text
1 = Missing bureau score
0 = Bureau score available
```

### Design Decision

The flag is created before train-test splitting because it represents directly observed missingness and does not depend on any fitted statistic.

---

## Train-Test Split

Split:

```text
75% Training
25% Testing
```

Implementation:

```python
train_test_split(
    test_size=0.25,
    stratify=default,
    random_state=42
)
```

### Design Decision

Stratification preserves the default-rate distribution in both datasets.

This is particularly important when the target class is imbalanced.

---

## Bureau Score Imputation

Method:

```text
Median Imputation
```

Source:

```text
Training data only
```

### Design Decision

The training-set median is used to fill missing bureau scores in both train and test sets.

This prevents data leakage and follows the same principle as fitting a scaler only on training data.

---

## Employment Type Encoding

Method:

```text
One-Hot Encoding
```

### Design Decision

Employment categories have no natural ordering, so one-hot encoding avoids imposing an artificial ranking.

---

## Feature Scaling

Method:

```text
StandardScaler
```

Applied to:

- age
- monthly_income_inr
- existing_loans_count
- credit_utilization_ratio
- upi_monthly_inflow_inr
- bounced_payments_count
- credit_bureau_score

### Design Decision

The scaler is fitted on training data only and then applied to both train and test datasets.

This prevents information leakage from the testing dataset.

---

# Part B – Classification Models

## Objective

Predict whether an applicant will default.

Target:

```text
default
```

---

## Models Evaluated

### Logistic Regression

Purpose:

Provides a simple, explainable baseline credit-risk model.

Advantages:

- Interpretable coefficients
- Fast training
- Commonly used in credit-risk applications

---

### Random Forest Classifier

Purpose:

Capture nonlinear relationships and feature interactions.

Advantages:

- Handles complex decision boundaries
- Robust against outliers
- Provides feature importance measures

---

## Evaluation Metrics

### Accuracy

Definition:

```text
Correct Predictions
/
Total Predictions
```

Provides an overall performance measure.

---

### Precision

Definition:

```text
True Positives
/
Predicted Positives
```

Measures the quality of default predictions.

---

### Recall

Definition:

```text
True Positives
/
Actual Positives
```

Measures how effectively the model identifies defaults.

---

### F1 Score

Definition:

```text
Harmonic mean of precision and recall
```

Balances both objectives.

---

### ROC-AUC

Definition:

```text
Area under ROC curve
```

Measures discrimination ability across all classification thresholds.

### Design Decision

ROC-AUC is emphasized because class imbalance often makes accuracy alone misleading.

---

## Classification Threshold

Default threshold:

```text
0.50
```

Prediction rule:

```text
Probability >= 0.50
=> Default
```

### Design Decision

The standard threshold was used for baseline comparison.

Future business deployments could optimize thresholds based on risk appetite and expected credit losses.

---

# Part C – Anomaly Detection and Optional Segmentation

## Objective

Identify unusual applicant behavior that may indicate fraud risk or elevated lending risk.

---

## Anomaly Detection Method

Model:

```text
Isolation Forest
```

### Design Decision

Isolation Forest is effective because:

- No fraud labels are required
- Works well with mixed behavioral features
- Efficient on relatively small datasets

---

## Features Used

Examples:

- txn_hour
- txn_amount_inr
- is_new_device

---

## Injected Anomalies

The dataset includes engineered anomalies characterized by:

- Transactions during unusual hours
- New device usage
- High-value transfers
- P2P transaction channel

These observations should be evaluated as potential risk indicators.

---

## Anomaly Classification

Output:

```text
Normal
```

or

```text
Anomalous
```

### Design Decision

The objective is investigation prioritization rather than automatic loan rejection.

An anomaly score alone is insufficient for adverse credit decisions.

---

## Optional Customer Segmentation

Method:

```text
K-Means Clustering
```

Purpose:

Group applicants into borrower segments based on behavioral and financial characteristics.

Example segments:

- Prime borrowers
- Emerging borrowers
- Thin-file borrowers
- High-risk borrowers

---

# Part D – Bias Awareness and Final Recommendation

# Part D – Bias Awareness Note and Final Recommendation

## Bias Awareness and Governance Considerations

Although this dataset does not explicitly contain sensitive attributes such as gender, religion, caste, ethnicity, or geographic location, some included features may act as correlated proxies for protected characteristics in a real-world lending environment.

For example, `monthly_income_inr` may indirectly reflect socioeconomic differences across demographic groups. Similarly, `employment_type` could correlate with education level, social background, or regional labor-market participation. The feature `credit_bureau_score` may also introduce bias if certain customer groups have historically had less access to formal credit products, resulting in systematically lower scores or thinner credit files.

These proxy relationships do not necessarily imply intentional discrimination, but they create a risk that the model may unintentionally reproduce historical inequities present in the underlying financial system. Therefore, model performance should be monitored regularly across relevant customer segments, and feature-importance trends should be reviewed periodically to identify potential fairness concerns.

A key governance recommendation is to implement a **maker-checker human-in-the-loop review process** for applicants classified as high risk, particularly thin-file applicants identified through the `is_thin_file` feature. Instead of automatically rejecting these borrowers, the model should route them to a credit officer for additional review using supporting information such as bank-account behaviour, UPI transaction patterns, employment verification, and income documentation. This approach helps reduce the risk of unfairly rejecting customers who have limited traditional credit history but may still represent acceptable lending opportunities.

---
## Model Comparison Summary

| Metric | Accuracy | Precision | Recall  |  F1  ROC_AUC |
|--------|----------|-----------|---------|--------------
|Logistic Regression  |    0.77  |   0.4118  |  0.35 | 0.3784 |  0.7031 |
|Decision Tree | 0.71 |   0.2632  |  0.25 | 0.2564 |  0.5375 |


| Metric | Logistic Regression | Decision Tree |
|----------|----------|----------|
| Accuracy | 0.77 | 0.71 |
| Precision | 0.4118 | 0.2632 |
| Recall | 0.35 | 0.25 |
| F1 Score | 0.3784 | 0.2564 |
| ROC-AUC | 0.7031 | 0.5375 |

### Isolation Forest Anomaly Detection

| Metric | Value |
|----------|----------|
| Seeded Anomalies | 15 |
| Correctly Detected | 11 |
| Recall | 73.33% |

---

## Final Deployment Recommendation

Based on the evaluation results, I recommend deploying the **Logistic Regression** model for Paytm Postpaid credit-risk assessment. Logistic Regression provides transparent probability estimates, straightforward explainability, and stable performance across evaluation metrics, making it easier to satisfy regulatory, audit, and governance requirements compared with a more complex decision tree model.

If the Logistic Regression model achieves a higher ROC-AUC and F1 score than the Decision Tree while maintaining comparable recall, it offers a better balance between risk discrimination and operational interpretability. The predicted probabilities also support downstream risk-based pricing by allowing applicants to be segmented into lending tiers based on estimated default risk.

The Decision Tree remains valuable as a challenger model and for business-rule interpretation, but the Logistic Regression model is better suited as the primary production model because its outputs are easier to explain to business users, auditors, regulators, and customers. Combined with the Isolation Forest monitoring layer and a human review process for thin-file applicants, this approach provides a balanced framework for responsible and scalable digital lending decisions.

# Key Design Decisions Summary

| Area | Decision |
|--------|----------|
| Missing Bureau Scores | Retained, not dropped |
| Thin File Applicants | Explicit indicator feature |
| Data Split | 75/25 stratified |
| Imputation | Training median only |
| Encoding | One-hot encoding |
| Scaling | StandardScaler fit on train only |
| Baseline Model | Logistic Regression |
| Advanced Model | Random Forest |
| Anomaly Detection | Isolation Forest |
| Threshold | 0.50 classification cutoff |
| Fairness Strategy | Bias monitoring + human review |

---

# Technologies Used

- Python
- Pandas
- NumPy
- Scikit-Learn
- Matplotlib
- Seaborn
- Jupyter Notebook

---

# Key Outcomes

This project demonstrates:

- Credit-risk modeling
- Alternative-data lending analysis
- Missing-data handling
- Machine learning classification
- Fraud and anomaly detection
- Bias-aware lending assessment
- Explainable risk-based decision making

The resulting framework provides a scalable approach for evaluating retail credit applicants while balancing predictive accuracy, operational practicality, and fairness considerations.
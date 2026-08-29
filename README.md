# Paytm FinTech Analytics & AI Platform

## Project Overview

This repository contains three independent but complementary FinTech projects covering:

1. Payments & Fraud Analytics
2. Credit Risk & Lending Machine Learning
3. AI-Augmented Advisory & Blockchain Risk Analysis

Together, these projects demonstrate practical applications of:

- SQL analytics
- Fraud detection
- Payment reconciliation
- Dashboarding
- Credit-risk modeling
- Machine learning
- Anomaly detection
- Portfolio analytics
- CAPM and DCF valuation
- Agent-based AI workflows
- Blockchain and crypto risk assessment

---

# Repository Structure

```text
project_root/
│
├── payments_fraud_analytics/
│   ├── README.md
│   ├── merchants.csv
│   ├── users.csv
│   ├── ledger.csv
│   ├── gateway_export.csv
│   ├── reconcile.ipynb
│   ├── dashboard.ipynb
│   └── ...
│
├── credit_risk_lending_ml/
│   ├── README.md
│   ├── credit_applicants.csv
│   ├── txn_behaviour.csv
│   ├── eda_preprocessing.ipynb
│   ├── classification_models.ipynb
│   ├── anomaly_detection.ipynb
│   └── ...
│
├── ai_advisory_blockchain/
│   ├── README.md
│   ├── advisory_agent.py
│   ├── extract_disclosure.py
│   ├── debate.py
│   ├── dcf_calculator.py
│   └── ...
│
├── requirements.txt
└── README.md
```

---

# Environment Setup

This submission uses a **single consolidated `requirements.txt`** for all three project parts.

## Python Version

```text
Python 3.10+
```

---

## Install Dependencies

Create a virtual environment (recommended):

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Example requirements.txt

```text
pandas
numpy
matplotlib
seaborn
scikit-learn
openpyxl
jupyter
```

No paid libraries are required.

---

# Part 1 – Payments & Fraud Analytics

Location:

```text
/payments_fraud_analytics
```

## Objective

Analyze payment transactions, identify fraud patterns, reconcile gateway and ledger records, and develop business dashboards.

---

## How to Run

### SQL Analytics

Load the database and execute:

```sql
.read fraud_queries.sql
```

### Reconciliation

```bash
jupyter notebook reconcile.ipynb
```

Run all notebook cells.

### Dashboard

```bash
jupyter notebook dashboard.ipynb
```

Run all notebook cells.

Generated artifacts include:

```text
headline_scorecards.png
trend_layer.png
gmv_payment_method.png
gmv_category.png
merchant_detail_table.png
```

---

## Key Design Decisions

### Fraud Detection

Burner Account Rule:

```text
0 <= account_age_days < 30
```

restricted to:

```text
status = 'chargeback'
```

Velocity Attack Rule:

```text
3 or more transactions
within a 10-minute window
```

---

### Reconciliation

Set operations were used to detect:

- Missing in Gateway
- Missing in Ledger

Merge-based comparison was used to identify:

- Amount mismatches
- Status mismatches

---

### Dashboard Design

A four-layer dashboard structure was chosen:

1. Headline KPIs
2. Trend Analysis
3. Breakdown Analysis
4. Detailed Merchant View

This layout mirrors common executive reporting frameworks.

---

# Part 2 – Credit Risk & Lending ML

Location:

```text
/credit_risk_lending_ml
```

## Objective

Build an end-to-end credit-risk assessment workflow including:

- Data preprocessing
- Classification modeling
- Risk-based pricing
- Anomaly detection
- Fair-lending considerations

---

## How to Run

Open Jupyter:

```bash
jupyter notebook
```

Execute notebooks sequentially:

```text
eda_preprocessing.ipynb
classification_models.ipynb
anomaly_detection.ipynb
```

Run all cells.

Generated outputs include:

```text
confusion_matrix.png
roc_curve.png
feature_importance.png
anomaly_scatter.png
```

---

## Key Design Decisions

### Missing Bureau Scores

Applicants with missing bureau scores are retained.

A feature:

```text
is_thin_file
```

is created to identify new-to-credit applicants.

Rows were not dropped because alternative data is specifically intended to evaluate this segment.

---

### Data Leakage Prevention

Imputation, scaling, and model fitting use:

```text
Training data only
```

for all learned statistics.

---

### Classification Models

Two models were evaluated:

```text
Logistic Regression
Decision Tree Classifier
```

Both were trained using the exact same train/test split.

---

### Risk-Based Pricing

Applicants were segmented into four risk tiers using:

```text
Predicted default probability quartiles
```

Lower-risk tiers receive lower illustrative lending rates.

Observed default rates were analyzed to verify monotonic risk ordering.

---

### Anomaly Detection

Isolation Forest was selected because:

- It does not require labeled fraud data.
- It performs well on numerical behavioural features.
- It aligns with the injected anomaly-generation process.

Contamination rate:

```text
15 / 265 ≈ 5.66%
```

was used to match the seeded anomaly proportion.

---

# Part 3 – AI-Augmented FinTech Advisory & Blockchain Risk

Location:

```text
/ai_advisory_blockchain
```

## Objective

Demonstrate AI-assisted financial-advisory workflows using:

- Portfolio allocation
- CAPM
- Portfolio risk estimation
- Structured disclosure extraction
- Multi-agent debate
- DCF valuation
- Blockchain risk analysis

---

## How to Run

### Portfolio Advisory Agent

```bash
python advisory_agent.py
```

---

### Disclosure Extraction

```bash
python extract_disclosure.py
```

---

### Multi-Agent Debate

```bash
python debate.py
```

---

### DCF Valuation

```bash
python dcf_calculator.py
```

---

### Blockchain Risk Analysis

Read:

```text
blockchain_risk_note.md
```

No code execution is required.

---

## MOCK_LLM Configuration

The project supports:

```text
MOCK_LLM
```

environment control.

All submitted outputs were generated using:

```text
MOCK_LLM=1
```

This is the required grading baseline.

No external API calls, paid AI services, vector databases, retrieval systems, or network dependencies were used.

To set:

### Windows

```bash
set MOCK_LLM=1
```

### Linux / Mac

```bash
export MOCK_LLM=1
```

---

## Key Design Decisions

### Portfolio Advisory Agent

Agent architecture follows:

```text
Think → Act → Observe
```

Allocation rules are deterministic and defined by investor risk category.

Escalation rule:

```text
Portfolio Volatility > 20%
```

results in:

```text
ESCALATED_TO_HUMAN_ADVISOR
```

---

### Structured Disclosure Extraction

Mock mode uses deterministic:

- keyword matching
- rule-based classification
- JSON output generation

No LLM was required.

---

### Multi-Agent Debate

Three agents were implemented:

```text
Bull Agent
Bear Agent
Synthesizer Agent
```

The synthesizer produces a balanced recommendation rather than a buy/sell directive.

---

### DCF Valuation

Enterprise value is estimated using:

```text
FCFF
WACC
Terminal Value
Sensitivity Analysis
```

A secondary EV/EBITDA valuation is used as a reasonableness check.

---

### Blockchain Risk Analysis

The analysis focuses on:

- Stablecoin design risk
- DAO governance risk
- Crypto allocation policy
- T.A.N.G. fraud framework

A maximum retail crypto allocation recommendation of:

```text
5%
```

is proposed, subject to investor suitability and risk tolerance.

---

# Summary

This repository demonstrates an end-to-end FinTech analytics workflow spanning:

### Payments

- Fraud detection
- Reconciliation
- Dashboarding

### Lending

- Credit scoring
- Risk-based pricing
- Anomaly detection

### Advisory

- Portfolio construction
- Agent-based AI systems
- Valuation
- Blockchain risk assessment

The projects collectively emphasize explainability, reproducibility, data-governance principles, and practical financial-services decision making using modern analytics and machine-learning techniques.

## Submitted By - 
Manish Sadashiv Bhalerao (bitsom_ftai_2601147)  
manishbhalerao0123@gmail.com  
8956503432
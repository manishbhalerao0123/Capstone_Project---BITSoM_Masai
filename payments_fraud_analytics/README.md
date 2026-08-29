# Payments & Fraud Analytics

## Project Overview

This project simulates the analytics workflow of a digital payments platform. The objective is to analyze merchant and transaction data, detect fraud patterns, reconcile payment records between internal and external systems, and build a management dashboard for operational monitoring.

The project is divided into four components:

1. Part A – Excel/Sheets Merchant Workbook
2. Part B – SQL Fraud Pattern Detection
3. Part C – Python Payment Reconciliation
4. Part D – Four-Layer Analytics Dashboard

---

# Dataset Description

## merchants

Contains merchant master information.

Fields:

- merchant_id
- merchant_name
- category
- region

## users

Contains customer information.

Fields:

- user_id
- signup_date

## ledger

Core transaction table.

Fields:

- transaction_id
- user_id
- merchant_id
- transaction_time
- amount_inr
- payment_method
- status
- risk_score

## gateway_export

External payment gateway transaction export used for reconciliation.

---

# Installation

## Prerequisites

- Python 3.10 or later
- Jupyter Notebook
- SQLite

## Install Required Packages

```bash
pip install pandas numpy matplotlib seaborn openpyxl jupyter
```

---

# Project Structure

```text
payments_fraud_analytics/
│
├── merchants.csv
├── users.csv
├── ledger.csv
├── gateway_export.csv
│
├── merchant_workbook.xlsx
├── fraud_queries.sql
├── reconcile.ipynb
├── dashboard.ipynb
│
├── headline_scorecards.png
├── trend_layer.png
├── gmv_payment_method.png
├── gmv_category.png
├── merchant_detail_table.png
│
└── README.md
```

---

# How to Run

## Part A – Merchant Workbook

Open:

```text
merchant_workbook.xlsx
```

Review:

- Merchant performance summary
- Revenue analysis
- Pivot tables
- Conditional formatting

No code execution is required.

---

## Part B – SQL Fraud Pattern Detection

Create a SQLite database and execute queries:

```bash
sqlite3 payments.db
```

Run:

```sql
.read fraud_queries.sql
```

The SQL script contains all fraud detection and analytical queries.

---

## Part C – Payment Reconciliation

Launch Jupyter Notebook:

```bash
jupyter notebook
```

Open:

```text
reconcile.ipynb
```

Run all cells.

The notebook generates:

- Missing in Gateway transactions
- Missing in Ledger transactions
- Amount mismatches
- Status mismatches

---

## Part D – Analytics Dashboard

Open:

```text
dashboard.ipynb
```

Run all cells.

Generated outputs:

```text
headline_scorecards.png
trend_layer.png
gmv_payment_method.png
gmv_category.png
merchant_detail_table.png
```

---

# Part A – Excel/Sheets Merchant Workbook

## Design Decisions

### Pivot Tables

Pivot tables were used to summarize:

- Merchant transaction volume
- Transaction counts
- Revenue contribution
- Chargeback activity

This enables business users to perform analysis without writing SQL queries.

### Conditional Formatting

Conditional formatting was used to visually identify:

- High-performing merchants
- High-risk merchants
- Revenue concentration

This improves usability and management reporting.

---

# Part B – SQL Fraud Pattern Detection

## Fraud Rules Implemented

### Chargeback Impact

Definition:

```text
status = 'chargeback'
```

Metrics calculated:

- Number of chargeback transactions
- Unique users affected
- Total chargeback amount

### Burner Account Detection

Rule:

```text
0 <= (transaction_time - signup_date).days < 30
```

Restricted to:

```text
status = 'chargeback'
```

Design Rationale:

Fraudsters often create accounts shortly before conducting fraudulent transactions. Recently created accounts with chargebacks are therefore considered higher risk.

### Velocity Attack Detection

Rule:

```text
3 or more transactions within a 10-minute window
```

Implementation:

Transactions were grouped using a 10-minute time bucket.

Design Rationale:

Rapid transaction bursts frequently indicate:

- Card testing
- Automated fraud scripts
- Account takeover attempts
- Payment abuse

### Join Strategy

#### INNER JOIN

Used for merchant-level transaction analysis because only matching merchant records are relevant.

#### LEFT JOIN

Used for user analysis to ensure users with zero transactions are also included in reports.

---

# Part C – Payment Reconciliation

## Objective

Verify consistency between:

```text
ledger.csv
```

and

```text
gateway_export.csv
```

## Reconciliation Logic

### Missing in Gateway

Transactions existing in the ledger but not present in the gateway export.

Implementation:

```python
ledger_ids - gateway_ids
```

### Missing in Ledger

Transactions existing in the gateway export but not present in the ledger.

Implementation:

```python
gateway_ids - ledger_ids
```

### Amount Mismatch

Transactions where:

```python
amount_inr_ledger != amount_inr_gateway
```

A difference column is calculated for investigation.

### Status Mismatch

Transactions where:

```python
status_ledger != status_gateway
```

## Expected Error Injection Rates

The generated dataset contains approximately:

- 5% missing in gateway
- 3% missing in ledger
- 2% amount mismatches
- 2% status mismatches

Observed results should be consistent with these proportions.

---

# Part D – Four-Layer Analytics Dashboard

The dashboard follows a standard business-intelligence layout.

---

## Layer 1 – Headline Metrics

### Total GMV

Definition:

```text
SUM(amount_inr)
```

Purpose:

Measures total transaction value processed by the platform.

### Success Rate

Definition:

```text
Successful Transactions
/
Total Transactions
```

Purpose:

Measures platform transaction efficiency.

### Reconciliation Match Rate

Definition:

```text
Transactions present in both systems
with matching amount and status
/
Total ledger transactions
```

Design Decision:

Transactions missing in either file, amount mismatches, and status mismatches are all considered unmatched.

### Chargeback Ratio

Definition:

```text
Chargeback Transaction Count
/
Total Transaction Count
```

Design Decision:

The metric is count-based rather than amount-based, as specified in the project requirements.

---

## Layer 2 – Trends Analysis

### Chart Type

Line Chart

### Metrics

- Daily GMV
- Daily Chargeback Count

### Reason for Selection

Line charts effectively display trends over time and make spikes, seasonality, and anomalies easy to identify.

---

## Layer 3 – Breakdown Analysis

### GMV by Payment Method

Chart Type:

Bar Chart

Reason:

Bar charts provide the clearest comparison across payment channels.

### GMV by Merchant Category

Chart Type:

Bar Chart

Reason:

Allows straightforward comparison of revenue contribution across business segments.

---

## Layer 4 – Merchant Detail Layer

### Chart Type

Rendered Table Image

Reason:

Project requirements specifically require a saved image rather than an interactive table.

### Merchant Risk Classification

Rule:

```text
Chargeback Ratio > 1%
```

Flag Assigned:

```text
HIGH RISK
```

Definition:

```text
Merchant Chargeback Ratio
=
Merchant Chargeback Count
/
Merchant Transaction Count
```

Design Decision:

The 1% threshold was adopted directly from the assignment specification.

---

# Dashboard Outputs

The following files are generated:

```text
headline_scorecards.png
trend_layer.png
gmv_payment_method.png
gmv_category.png
merchant_detail_table.png
```

Each visualization includes a written business interpretation explaining:

- Key observations
- Potential risks
- Revenue trends
- Merchant performance implications

---

# Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SQLite
- Microsoft Excel / Google Sheets
- Jupyter Notebook

---

# Key Outcomes

This project demonstrates:

- Payment analytics
- Fraud detection using SQL
- Transaction reconciliation
- Operational risk analysis
- Dashboard design
- Business KPI monitoring

The combined solution provides an end-to-end framework for monitoring payment operations, investigating suspicious activity, and tracking platform performance.
# AI-Augmented FinTech Advisory & Blockchain Risk

## Project Overview

This project demonstrates how AI-assisted financial advisory workflows can be implemented using agentic patterns, structured information extraction, portfolio theory, valuation techniques, and blockchain risk assessment.

The project consists of five components:

1. Part A – Portfolio Advisory Agent
2. Part B – Structured Disclosure Extraction
3. Part C – Multi-Agent Investment Debate
4. Part D – DCF Valuation Calculator
5. Part E – Blockchain and Crypto Risk Analysis

A key design requirement of this project is support for a deterministic offline mode controlled through the environment variable:

```text
MOCK_LLM
```

The recorded submission was executed entirely using:

```text
MOCK_LLM=1
```

which is the required grading baseline.

No external LLM API, API key, paid service, embedding model, vector database, retrieval pipeline, or internet-based model was used in the submitted results.

---

# Project Structure

```text
ai_advisory_blockchain/
│
├── stock_universe.py
├── investor_profiles.py
├── disclosure_snippets.py
│
├── advisory_agent.py
├── extract_disclosure.py
├── debate.py
├── dcf_calculator.py
│
├── blockchain_risk_note.md
│
├── advisory_output.txt
├── disclosure_output.txt
├── debate_output.txt
├── dcf_output.txt
│
└── README.md
```

---

# Installation

## Prerequisites

- Python 3.10+
- No API key required
- No external LLM required

## Install Dependencies

```bash
pip install pandas numpy
```

---

# Configuration

## Default Graded Configuration

The project is designed to operate fully offline.

Set:

```bash
export MOCK_LLM=1
```

or leave the variable unset.

All recorded outputs in this submission were generated using:

```text
MOCK_LLM=1
```

---

## Optional Extension (Not Used in Submitted Results)

The framework allows:

```bash
export MOCK_LLM=0
```

to connect to a free-tier LLM service such as Groq.

This optional path was not required for grading.

If implemented, users should document:

- LLM provider used
- Free-tier limitations
- API rate limits
- Model selected

Since the submitted project used only deterministic mock logic, no free-tier API usage occurred.

---

# Running the Project

## Portfolio Advisory Agent

```bash
python advisory_agent.py
```

Output:

- Portfolio allocation
- CAPM expected return
- Portfolio volatility
- Human escalation status
- Recommendation narrative

---

## Disclosure Extraction

```bash
python extract_disclosure.py
```

Output:

```json
{
  "risk_flags": [],
  "hedging_detected": false,
  "sentiment": "neutral"
}
```

for each disclosure snippet.

---

## Multi-Agent Debate

```bash
python debate.py
```

Output:

- Bull argument
- Bear argument
- Synthesized recommendation

---

## DCF Valuation

```bash
python dcf_calculator.py
```

Output:

- FCFF forecast
- Terminal value
- Enterprise value
- Sensitivity table
- EV/EBITDA comparison

---

# MOCK_LLM Mode Used for Recorded Results

## Submitted Configuration

```text
MOCK_LLM=1
```

### Reason

The project specification explicitly states that the deterministic mock implementation is the grading baseline.

All outputs included in this submission were therefore generated using:

```text
MOCK_LLM=1
```

This ensures:

- Reproducible results
- No network dependency
- No API charges
- No rate limits
- Fully deterministic evaluation

---

# Part A – Portfolio Advisory Agent

## Objective

Recommend portfolios for investors using a Think → Act → Observe workflow.

---

## Agent Architecture

### Think Stage

Reads investor profile and selects portfolio allocation.

Mandatory allocation mapping:

### Conservative

```text
PAYBOND
PAYGOLD
PAYRETAIL
```

Equal weight:

```text
33.33% each
```

### Moderate

```text
PAYRETAIL
PAYINFRA
PAYGOLD
```

Equal weight:

```text
33.33% each
```

### Aggressive

```text
PAYTECH
PAYFIN
PAYINFRA
```

Equal weight:

```text
33.33% each
```

### Design Decision

The allocation rules are prescribed by the assignment and are intentionally deterministic.

No optimization engine or portfolio search algorithm was used.

---

### Act Stage

Tool function:

```python
get_stock_data(ticker)
```

retrieves:

- beta
- analyst_expected_return
- std_dev

from the local stock universe.

### Design Decision

The tool simulates an external API call but operates entirely on local data.

---

### Observe Stage

Expected return calculated using CAPM:

```text
E(R) = Rf + β(Rm − Rf)
```

Important design choice:

```text
ONLY beta is used
```

The provided:

```text
analyst_expected_return
```

is not used in CAPM calculations.

---

## Portfolio Risk Calculation

Variance formula:

```text
Var(Rp)
=
Σ(w²σ²)
+
2Σ(wiwjCovij)
```

Covariance:

```text
Covij = ρ × σi × σj
```

Assumption:

```text
ρ = 0.30
```

for every pair of assets.

### Design Decision

The assignment explicitly specifies a constant pairwise correlation of 0.30.

---

## Human Escalation Rule

Threshold:

```text
Portfolio Std Dev > 20%
```

Outcome:

```text
ESCALATED_TO_HUMAN_ADVISOR
```

otherwise:

```text
APPROVED
```

### Expected Results

| Investor Type | Volatility | Escalation |
|--------------|------------|------------|
| Conservative | ~8.44% | No |
| Moderate | ~12.57% | No |
| Aggressive | ~20.58% | Yes |

---

# Part B – Structured Disclosure Extraction

## Objective

Extract structured investment signals from disclosure text.

---

## MOCK_LLM Implementation

Keyword and rule-based extraction.

No LLM calls are made.

---

## Risk Flag Rules

Triggers:

```text
litigation
regulatory
customer concentration
```

### Design Decision

Direct keyword matching provides deterministic and explainable outputs.

---

## Hedging Detection Rules

Triggers:

```text
assuming
cautiously
visibility
```

### Design Decision

These terms indicate uncertainty and forward-looking caution.

---

## Sentiment Classification

### Confident

Keywords:

```text
confident
approved
```

### Cautious

Presence of hedging language.

### Neutral

Default classification.

### Classification Hierarchy

```text
Confident
→ Cautious
→ Neutral
```

This precedence prevents ambiguous classifications.

---

# Part C – Multi-Agent Debate Demo

## Objective

Simulate multiple investment viewpoints.

Agents:

1. Bull Agent
2. Bear Agent
3. Synthesizer Agent

---

## Bull Agent

Emphasizes:

- Analyst expected return
- Growth opportunities
- Market upside

---

## Bear Agent

Emphasizes:

- Standard deviation
- Risk exposure
- Volatility

---

## Synthesizer Agent

Produces a balanced summary.

### Design Decision

The synthesizer does not issue a buy/sell instruction.

This mirrors advisory best practices where risk and reward are jointly evaluated.

---

## MOCK_LLM Implementation

Arguments are generated using deterministic templates.

No external model is called.

---

# Part D – DCF Valuation Calculator

## Objective

Estimate enterprise value for a hypothetical Paytm business line.

---

## FCFF Methodology

Formula:

```text
FCFF =
EBIT(1 − Tax Rate)
+ D&A
− Capital Expenditure
− Change in Net Working Capital
```

---

## Assumptions

### Operating Inputs

```text
EBIT                     = ₹120 Crore
Tax Rate                 = 25%
D&A                      = ₹15 Crore
CapEx                    = ₹20 Crore
Δ Net Working Capital    = ₹5 Crore
```

Result:

```text
FCFF = ₹80 Crore
```

---

## Cost of Equity

CAPM:

```text
Re = Rf + β(Rm − Rf)
```

Selected beta:

```text
PAYINFRA β = 1.10
```

Result:

```text
Re = 13.6%
```

---

## Capital Structure Assumptions

```text
70% Equity
30% Debt
```

After-tax cost of debt:

```text
6.75%
```

Resulting WACC:

```text
11.55%
```

---

## Growth Assumptions

5-Year Growth:

```text
10%
```

Terminal Growth:

```text
4%
```

### Design Decision

Terminal growth is intentionally well below WACC.

This ensures:

```text
WACC > Terminal Growth
```

in every sensitivity scenario.

---

## Sensitivity Analysis

Grid:

```text
WACC ±1%
Terminal Growth ±1%
```

Result:

```text
3 × 3 matrix
```

### Validation Check

Worst-case scenario:

```text
WACC − Terminal Growth ≥ 1%
```

Requirement satisfied.

---

## EV/EBITDA Cross-Check

Assumptions:

```text
EBITDA = ₹150 Crore
EV/EBITDA Multiple = 8x
```

Purpose:

Provide a secondary valuation estimate.

### Design Decision

Comparing DCF and multiple-based valuation provides reasonableness validation.

---

# Part E – Blockchain/Crypto Risk Analysis

## Objective

Assess blockchain and cryptocurrency risks for a hypothetical Paytm Crypto Insights offering.

---

## Stablecoin Analysis

Examined:

### Fiat-Collateralized Stablecoins

Characteristics:

- Reserve-backed
- More transparent structure
- Lower de-pegging risk

### Algorithmic Stablecoins

Characteristics:

- Depend on tokenomics
- Sensitive to confidence shocks
- Historically more fragile

### Design Decision

Stablecoin type must be clearly disclosed to retail users.

---

## DAO Governance Analysis

Key Risks:

- Token concentration
- Low voter participation
- Governance capture
- Treasury misuse

Recommendation:

Governance indicators should be surfaced alongside investment information.

---

## Crypto Allocation Recommendation

Maximum allocation recommended:

```text
5% of portfolio
```

### Rationale

Considers:

- Lack of intrinsic cash flow
- CAPM limitations
- High volatility
- Heavy-tailed returns
- Survivorship bias
- Transaction costs

Conservative investors may appropriately receive:

```text
0% allocation
```

recommendations.

---

## T.A.N.G. Fraud Framework

Analyzed:

### Authority-Based Scams

Examples:

- Fake bank representatives
- Fake customer support
- Fake regulators

Defense:

```text
Real-time behavioral monitoring
+
Step-up authentication
```

---

### Greed-Based Investment Scams

Examples:

- Guaranteed-return schemes
- Fake crypto opportunities
- High-return promises

Defense:

```text
Real-time warning systems
+
High-risk transaction monitoring
```

---

# Technologies Used

- Python
- CAPM
- Portfolio Variance Analysis
- DCF Valuation
- Rule-Based NLP
- Agentic Think-Act-Observe Design

---

# Key Outcomes

This project demonstrates:

- Agent-based financial advisory workflows
- Structured disclosure analysis
- Multi-agent financial reasoning
- DCF valuation techniques
- Human-in-the-loop governance controls
- Blockchain and crypto risk assessment

All required outputs were generated using the fully deterministic offline configuration:

```text
MOCK_LLM=1
```

which is the official grading baseline specified for the project.
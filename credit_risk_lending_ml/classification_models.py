# %% [markdown]
# ## Part B.1 – Train Logistic Regression and Decision Tree

# %% [markdown]
# Import Models and Metrics

# %%
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve
)

import pandas as pd
import matplotlib.pyplot as plt

# %% [markdown]
# Load Dataset

# %%
df = pd.read_csv("credit_applicants.csv")

print(df.shape)
df.head()

# %% [markdown]
# Clean Data

# %%
from sklearn.model_selection import train_test_split

# X = df.drop(columns=['default','applicant_id'], axis=1)
X = df.drop(columns=['default','applicant_id','employment_type']).fillna(0)
# X=df.fillna(0)

y = df["default"]

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.25,
        stratify=y,
        random_state=42
    )
)


# %% [markdown]
# Train Logistic Regression

# %%

lr_model = LogisticRegression(
    random_state=42,
    max_iter=1000
)

lr_model.fit(X_train, y_train)

# %% [markdown]
# Train Decision Tree

# %%
dt_model = DecisionTreeClassifier(
    random_state=42
)

dt_model.fit(X_train, y_train)

# %% [markdown]
# # Part B.2 – Generate Predictions

# %% [markdown]
# Logistic Regression

# %%
lr_pred = lr_model.predict(X_test)

lr_prob = lr_model.predict_proba(
    X_test
)[:,1]

# %% [markdown]
# Decision Tree

# %%
dt_pred = dt_model.predict(X_test)

dt_prob = dt_model.predict_proba(
    X_test
)[:,1]

# %% [markdown]
# # Part B.3 – Confusion Matrices

# %% [markdown]
# Logistic Regression

# %%
lr_cm = confusion_matrix(
    y_test,
    lr_pred
)

print("Logistic Regression")
print(lr_cm)

# %% [markdown]
# Decision Tree

# %%
dt_cm = confusion_matrix(
    y_test,
    dt_pred
)

print("Decision Tree")
print(dt_cm)

# %% [markdown]
# # Part B.4 – Calculate Evaluation Metrics

# %%
def evaluate_model(
        y_true,
        predictions,
        probabilities):

    return {
        "Accuracy":
            accuracy_score(
                y_true,
                predictions
            ),

        "Precision":
            precision_score(
                y_true,
                predictions
            ),

        "Recall":
            recall_score(
                y_true,
                predictions
            ),

        "F1":
            f1_score(
                y_true,
                predictions
            ),

        "ROC_AUC":
            roc_auc_score(
                y_true,
                probabilities
            )
    }

# %% [markdown]
# Evaluate Both Models

# %%
lr_metrics = evaluate_model(
    y_test,
    lr_pred,
    lr_prob
)

dt_metrics = evaluate_model(
    y_test,
    dt_pred,
    dt_prob
)

# %% [markdown]
# # Part B.5 – Comparison Table

# %%
comparison = pd.DataFrame(
    [lr_metrics,
     dt_metrics],
    index=[
        "Logistic Regression",
        "Decision Tree"
    ]
)

comparison = comparison.round(4)

print(comparison)

# %% [markdown]
# # Part B.6 – ROC Curve Comparison

# %%
lr_fpr, lr_tpr, _ = roc_curve(
    y_test,
    lr_prob
)

dt_fpr, dt_tpr, _ = roc_curve(
    y_test,
    dt_prob
)

# %% [markdown]
# Plot ROC Curves

# %%
plt.figure(figsize=(8,6))

plt.plot(
    lr_fpr,
    lr_tpr,
    label=f"Logistic Regression (AUC={roc_auc_score(y_test,lr_prob):.3f})"
)

plt.plot(
    dt_fpr,
    dt_tpr,
    label=f"Decision Tree (AUC={roc_auc_score(y_test,dt_prob):.3f})"
)

plt.plot([0,1],[0,1],'k--')

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title(
    "ROC Curve Comparison"
)

plt.legend()

plt.savefig(
    "roc_curve_comparison.png"
)

plt.show()

# %% [markdown]
# 1. confusion_matrix.png

# %%
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(10,4))

ConfusionMatrixDisplay.from_predictions(
    y_test,
    lr_pred,
    ax=axes[0],
    cmap="Blues"
)
axes[0].set_title("Logistic Regression")

ConfusionMatrixDisplay.from_predictions(
    y_test,
    dt_pred,
    ax=axes[1],
    cmap="Greens"
)
axes[1].set_title("Decision Tree")

plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.show()


# %% [markdown]
# 2. roc_curve.png

# %%
from sklearn.metrics import roc_curve, roc_auc_score

lr_fpr, lr_tpr, _ = roc_curve(y_test, lr_prob)
dt_fpr, dt_tpr, _ = roc_curve(y_test, dt_prob)

plt.figure(figsize=(8,6))

plt.plot(
    lr_fpr,
    lr_tpr,
    label=f"Logistic Regression (AUC={roc_auc_score(y_test, lr_prob):.3f})"
)

plt.plot(
    dt_fpr,
    dt_tpr,
    label=f"Decision Tree (AUC={roc_auc_score(y_test, dt_prob):.3f})"
)

plt.plot([0,1],[0,1],'k--')

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve Comparison")
plt.legend()

plt.savefig("roc_curve.png")
plt.show()

# %% [markdown]
# 3. feature_importance.png

# %%
import pandas as pd

feature_importance = pd.DataFrame({
    "feature": X_train.columns,
    "importance": dt_model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    "importance",
    ascending=False
).head(10)

plt.figure(figsize=(8,5))

plt.barh(
    feature_importance["feature"],
    feature_importance["importance"]
)

plt.xlabel("Importance")
plt.title("Top 10 Feature Importances")
plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig("feature_importance.png")
plt.show()

# %% [markdown]
# 4. anomaly_scatter.png

# %%
import pandas as pd
from sklearn.ensemble import IsolationForest

# 1. Ensure behaviour is a Pandas DataFrame
# behaviour = pd.DataFrame(behaviour)
behaviour=df

# anomaly_features = [
#     "txn_hour",
#     "txn_amount_inr",
#     "is_new_device"
# ]

anomaly_features = [
    "age",
    "monthly_income_inr",
    "existing_loans_count",
    "credit_utilization_ratio",
    "upi_monthly_inflow_inr",
    "bounced_payments_count",
    "credit_bureau_score"    
]

iso = IsolationForest(
    contamination=0.05,
    random_state=42
)

# This will now work without errors
behaviour["anomaly"] = iso.fit_predict(
    behaviour[anomaly_features]
)

behaviour["anomaly_label"] = behaviour[
    "anomaly"
].map({
    1: "Normal",
    -1: "Anomaly"
})


# %% [markdown]
# Scatter Plot

# %%
import seaborn as sns

plt.figure(figsize=(8,6))

sns.scatterplot(
    data=behaviour,
    x="monthly_income_inr",
    y="credit_bureau_score",
    hue="anomaly_label",
    palette={
        "Normal":"blue",
        "Anomaly":"red"
    }
)

plt.title("Transaction Behaviour Anomaly Detection")
plt.xlabel("Transaction Hour")
plt.ylabel("Transaction Amount (INR)")

plt.savefig("anomaly_scatter.png")

plt.show()

# %% [markdown]
# # Part B.7 – Risk-Based Pricing Table

# %% [markdown]
# Create Probabilities for Entire Dataset

# %%
all_probs = lr_model.predict_proba(
    X_test
)[:,1]

risk_df = X_test.copy()

risk_df["actual_default"] = y_test.values

risk_df["pd"] = all_probs

# %% [markdown]
# Create 4 Risk Tiers (Quartiles)

# %%
risk_df["risk_tier"] = pd.qcut(
    risk_df["pd"],
    q=4,
    labels=[
        "Tier 1 - Lowest Risk",
        "Tier 2 - Low Risk",
        "Tier 3 - Moderate Risk",
        "Tier 4 - Highest Risk"
    ]
)

# %% [markdown]
# Assign Interest Rates

# %%
rate_map = {

    "Tier 1 - Lowest Risk":
        "10% - 12%",

    "Tier 2 - Low Risk":
        "12% - 15%",

    "Tier 3 - Moderate Risk":
        "15% - 18%",

    "Tier 4 - Highest Risk":
        "18% - 24%"
}

risk_df["interest_rate"] = (
    risk_df["risk_tier"]
    .map(rate_map)
)

# %% [markdown]
# # Part B.8 – Calculate Actual Default Rates

# %%
risk_pricing = (
    risk_df
    .groupby(
        ["risk_tier",
         "interest_rate"]
    )
    .agg(
        applicants=(
            "actual_default",
            "count"
        ),

        observed_default_rate=(
            "actual_default",
            "mean"
        )
    )
    .reset_index()
)

risk_pricing[
    "observed_default_rate"
] = (
    risk_pricing[
        "observed_default_rate"
    ]
    * 100
).round(2)

print(risk_pricing)

# %% [markdown]
# Monotonicity Check

# %%
print(
    risk_pricing[
        [
          "risk_tier",
          "observed_default_rate"
        ]
    ]
)



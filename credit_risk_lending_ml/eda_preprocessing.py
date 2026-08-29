# %% [markdown]
# 1: Load Data and Explore Missingness

# %% [markdown]
# Step 1.1 Import Libraries

# %%
import pandas as pd
import numpy as np

# %% [markdown]
# Step 1.2 Load the Dataset

# %%
df = pd.read_csv("credit_applicants.csv")

print(df.shape)
df.head()

# %% [markdown]
# Step 1.3 Calculate Default Rate

# %%
default_rate = df["default"].mean() * 100

print(f"Default Rate: {default_rate:.2f}%")

# %% [markdown]
# Step 1.4 Calculate Missing Bureau Score Percentage

# %%
missing_pct = (
    df["credit_bureau_score"]
    .isna()
    .mean()
    * 100
)

print(
    f"Missing Bureau Score Percentage: {missing_pct:.2f}%"
)

# %% [markdown]
# Step 1.5 Create Thin-File Indicator

# %%
df["is_thin_file"] = (
    df["credit_bureau_score"]
    .isna()
    .astype(int)
)

df[
    ["credit_bureau_score",
     "is_thin_file"]
].head()

# %% [markdown]
# Task 2: Train-Test Split

# %% [markdown]
# Step 2.1 Separate Features and Target

# %%
X = df.drop("default", axis=1)

y = df["default"]

# %% [markdown]
# Step 2.2 Perform Stratified Split

# %%
from sklearn.model_selection import train_test_split

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
# Verify Stratification

# %%
print("Overall Default Rate:")
print(y.mean())

print("\nTraining Default Rate:")
print(y_train.mean())

print("\nTesting Default Rate:")
print(y_test.mean())

# %% [markdown]
# Task 2.3 Median Imputation (Training Data Only)

# %% [markdown]
# Calculate Median from Training Split

# %%
bureau_median = (
    X_train["credit_bureau_score"]
    .median()
)

print(
    f"Training Median Bureau Score: {bureau_median}"
)


# %% [markdown]
# Fill Missing Values

# %%
# Training:
X_train["credit_bureau_score"] = (
    X_train["credit_bureau_score"]
    .fillna(bureau_median)
)

# Testing:
X_test["credit_bureau_score"] = (
    X_test["credit_bureau_score"]
    .fillna(bureau_median)
)

# %% [markdown]
# Task 2.4 Encode Employment Type

# %% [markdown]
# One-Hot Encoding

# %%
X_train = pd.get_dummies(
    X_train,
    columns=["employment_type"],
    drop_first=True
)

X_test = pd.get_dummies(
    X_test,
    columns=["employment_type"],
    drop_first=True
)

# %% [markdown]
# Align Columns

# %%
X_train, X_test = X_train.align(
    X_test,
    join="left",
    axis=1,
    fill_value=0
)

# %% [markdown]
# Task 2.5 Scale Numeric Features

# %%
numeric_cols = [
    "age",
    "monthly_income_inr",
    "existing_loans_count",
    "credit_utilization_ratio",
    "upi_monthly_inflow_inr",
    "bounced_payments_count",
    "credit_bureau_score"
]

# %% [markdown]
# Fit StandardScaler on Training Data Only

# %%
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train[numeric_cols] = scaler.fit_transform(
    X_train[numeric_cols]
)

X_test[numeric_cols] = scaler.transform(
    X_test[numeric_cols]
)

# %% [markdown]
# Final Verification

# %%
print(X_train.shape)
print(X_test.shape)

X_train.head()



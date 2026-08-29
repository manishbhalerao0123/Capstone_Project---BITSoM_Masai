# %% [markdown]
# Step 1: Import Required Libraries

# %%
import pandas as pd

# %% [markdown]
# Step 2: Load the Files

# %%
ledger_df = pd.read_csv("ledger.csv")
gateway_df = pd.read_csv("gateway_export.csv")

print(ledger_df.shape)
print(gateway_df.shape)

ledger_df.head()
gateway_df.head()

# %% [markdown]
# Step 3: Create the Reconciliation Function

# %%
def reconcile_payments(ledger_df, gateway_df):
    """
    Reconcile ledger records with gateway export.

    Returns:
        missing_in_gateway
        missing_in_ledger
        amount_mismatches
        status_mismatches
    """

    # --------------------------------------------------
    # 1. Identify missing transaction IDs
    # --------------------------------------------------

    ledger_ids = set(ledger_df["transaction_id"])
    gateway_ids = set(gateway_df["transaction_id"])

    missing_in_gateway_ids = ledger_ids - gateway_ids
    missing_in_ledger_ids = gateway_ids - ledger_ids

    missing_in_gateway = ledger_df[ledger_df["transaction_id"].isin(missing_in_gateway_ids)].copy()

    missing_in_ledger = gateway_df[gateway_df["transaction_id"].isin(missing_in_ledger_ids)].copy()

    # --------------------------------------------------
    # 2. Compare common transactions
    # --------------------------------------------------

    merged = pd.merge(ledger_df,gateway_df,on="transaction_id",suffixes=("_ledger", "_gateway"))

    # --------------------------------------------------
    # 3. Amount mismatches
    # --------------------------------------------------

    amount_mismatches = merged[
        merged["amount_inr_ledger"] != merged["amount_inr_gateway"]
    ].copy()

    amount_mismatches["amount_difference"] = (
        amount_mismatches["amount_inr_ledger"]
        - amount_mismatches["amount_inr_gateway"]
    )

    # --------------------------------------------------
    # 4. Status mismatches
    # --------------------------------------------------

    status_mismatches = merged[
        merged["status_ledger"] != merged["status_gateway"]
    ].copy()

    return (
        missing_in_gateway,
        missing_in_ledger,
        amount_mismatches,
        status_mismatches
    )

# %% [markdown]
# Step 4: Execute the Function

# %%
(
    missing_in_gateway,
    missing_in_ledger,
    amount_mismatches,
    status_mismatches
) = reconcile_payments(
    ledger_df,
    gateway_df
)

# %% [markdown]
# Step 5: Report Discrepancy Counts

# %%
print("Transactions Missing in Gateway:",
      len(missing_in_gateway))

print("Transactions Missing in Ledger:",
      len(missing_in_ledger))

print("Amount Mismatches:",
      len(amount_mismatches))

print("Status Mismatches:",
      len(status_mismatches))

# %% [markdown]
# Step 6: Display Sample Records

# %%
print("\nMissing In Gateway")
print(missing_in_gateway.head())

print("\nMissing In Ledger")
print(missing_in_ledger.head())

print("\nAmount Mismatches")
print(amount_mismatches.head())

print("\nStatus Mismatches")
print(status_mismatches.head())

# %% [markdown]
# Step 7: Calculate Percentages for Project Report

# %%
total_transactions = len(ledger_df)

print(
    "Missing in Gateway %:",
    round(len(missing_in_gateway) * 100 / total_transactions, 2)
)

print(
    "Missing in Ledger %:",
    round(len(missing_in_ledger) * 100 / total_transactions, 2)
)

print(
    "Amount Mismatch %:",
    round(len(amount_mismatches) * 100 / total_transactions, 2)
)

print(
    "Status Mismatch %:",
    round(len(status_mismatches) * 100 / total_transactions, 2)
)



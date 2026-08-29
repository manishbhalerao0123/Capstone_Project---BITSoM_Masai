# %% [markdown]
# ## Part C – Anomaly Detection

# %% [markdown]
# Step 1: Imports

# %%
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
# Step 2: Load Data

# %%
behaviour = pd.read_csv(
    "txn_behaviour.csv"
)

print(behaviour.shape)

behaviour.head()

# %% [markdown]
# Step 3: Select Behavioural Features

# %%
features = [
    "txn_hour",
    "is_new_device",
    "txn_amount_inr"
]

X = behaviour[features]

# %% [markdown]
# Step 4: Standardize Data

# %%
scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# %% [markdown]
# Step 5: Define Contamination Rate

# %%
contamination_rate = 15 / 265

print(contamination_rate)

# %% [markdown]
# Step 6: Train Isolation Forest

# %%
iso = IsolationForest(
    random_state=42,
    contamination=15/265
)

iso.fit(X_scaled)

# %% [markdown]
# Step 7: Predict Anomalies

# %%
behaviour["anomaly_flag"] = (
    iso.predict(X_scaled)
)

behaviour["prediction"] = (
    behaviour["anomaly_flag"]
    .map({
        1: "Normal",
       -1: "Anomaly"
    })
)

# %% [markdown]
# Step 8: Count Detected Anomalies

# %%
detected_anomalies = (
    behaviour["anomaly_flag"] == -1
).sum()

print(
    "Detected anomalies:",
    detected_anomalies
)

# %% [markdown]
# ## simple recall check against your own injected ground truth

# %%
seeded = behaviour[
    behaviour["txn_id"]
    .str.startswith("BTXNA")
]
len(seeded)

# %% [markdown]
# Count Correctly Flagged Seeded Anomalies

# %%
true_detected = seeded[
    seeded["anomaly_flag"] == -1
]

detected_count = len(
    true_detected
)

print(
    f"Seeded anomalies detected: "
    f"{detected_count}/15"
)

# %% [markdown]
# Recall Calculation

# %%
recall = (
    detected_count / 15
) * 100

print(
    f"Recall: {recall:.2f}%"
)

# %% [markdown]
# Step 9: Create Required Image

# %%
plt.figure(
    figsize=(8,6)
)

sns.scatterplot(
    data=behaviour,
    x="txn_hour",
    y="txn_amount_inr",
    hue="prediction",
    palette={
        "Normal":"blue",
        "Anomaly":"red"
    }
)

plt.title(
    "Isolation Forest Anomaly Detection"
)

plt.xlabel(
    "Transaction Hour"
)

plt.ylabel(
    "Transaction Amount (INR)"
)

plt.savefig(
    "anomaly_scatter.png",
    bbox_inches="tight"
)

plt.show()

# %% [markdown]
# ## Optional Part – K-Means Segmentation (Ungraded)

# %% [markdown]
# Step 1: Imports

# %%
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score

# %% [markdown]
# Step 2: Load Applicant Data

# %%
applicants = pd.read_csv(
    "credit_applicants.csv"
)

print(applicants.shape)

applicants.head()

# %% [markdown]
# Step 3: Create Thin-File Indicator

# %%
applicants["is_thin_file"] = (
    applicants["credit_bureau_score"]
    .isna()
    .astype(int)
)

# %% [markdown]
# Step 4: Impute Missing Bureau Scores

# %%
bureau_median = (
    applicants["credit_bureau_score"]
    .median()
)

applicants["credit_bureau_score"] = (
    applicants["credit_bureau_score"]
    .fillna(bureau_median)
)

# %% [markdown]
# Step 5: One-Hot Encode Employment Type

# %%
applicants_encoded = pd.get_dummies(
    applicants,
    columns=["employment_type"],
    drop_first=True
)

# %% [markdown]
# Step 6: Select Clustering Features

# %%
cluster_features = applicants_encoded.drop(
    columns=[
        "applicant_id",
        "default"
    ]
)

# %% [markdown]
# Step 7: Standardize Features

# %%
scaler = StandardScaler()

X_scaled = scaler.fit_transform(
    cluster_features
)

# %% [markdown]
# Step 8: Determine Optimal K

# %%
scores = []

k_values = range(2, 9)

for k in k_values:

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    cluster_labels = model.fit_predict(
        X_scaled
    )

    score = calinski_harabasz_score(
        X_scaled,
        cluster_labels
    )

    scores.append(score)

    print(
        f"K={k}: CH Score={score:.2f}"
    )

# %% [markdown]
# Step 9: Visualize K Selection

# %%
plt.figure(figsize=(8,5))

plt.plot(
    k_values,
    scores,
    marker="o"
)

plt.xlabel("Number of Clusters (K)")
plt.ylabel("Calinski-Harabasz Score")

plt.title(
    "Cluster Selection Using Calinski-Harabasz Index"
)

plt.grid(True)

plt.show()

# %% [markdown]
# Step 10: Choose Best K

# %%
best_k = k_values[
    np.argmax(scores)
]

print(
    f"Best K = {best_k}"
)

# %% [markdown]
# Step 11: Fit Final K-Means Model

# %%
kmeans = KMeans(
    n_clusters=best_k,
    random_state=42,
    n_init=10
)

applicants["cluster"] = (
    kmeans.fit_predict(X_scaled)
)

# %% [markdown]
# Step 12: Profile Clusters

# %%
cluster_summary = (
    applicants
    .groupby("cluster")
    .agg(
        applicants=("default","count"),
        avg_income=(
            "monthly_income_inr",
            "mean"
        ),
        avg_bureau_score=(
            "credit_bureau_score",
            "mean"
        ),
        avg_utilization=(
            "credit_utilization_ratio",
            "mean"
        ),
        default_rate=(
            "default",
            "mean"
        )
    )
)

# %% [markdown]
# Step 13: Identify High-Risk Clusters

# %%
highest_default_cluster = (
    cluster_summary[
        "default_rate"
    ].idxmax()
)

highest_default_rate = (
    cluster_summary.loc[
        highest_default_cluster,
        "default_rate"
    ]
)

print(
    f"Cluster {highest_default_cluster} "
    f"has the highest default rate "
    f"({highest_default_rate:.2f}%)"
)

# %% [markdown]
# Step 14: Visualize Cluster Default Rates

# %%
plt.figure(figsize=(8,5))

sns.barplot(
    x=cluster_summary.index,
    y=cluster_summary["default_rate"]
)

plt.xlabel("Cluster")
plt.ylabel("Default Rate (%)")

plt.title(
    "Default Rate by Cluster"
)

plt.show()

# %% [markdown]
# Step 15: 2-D Cluster Visualization

# %%
from sklearn.decomposition import PCA

pca = PCA(
    n_components=2,
    random_state=42
)

pca_data = pca.fit_transform(
    X_scaled
)

cluster_plot = pd.DataFrame({
    "PC1": pca_data[:,0],
    "PC2": pca_data[:,1],
    "cluster": applicants["cluster"]
})

plt.figure(figsize=(8,6))

sns.scatterplot(
    data=cluster_plot,
    x="PC1",
    y="PC2",
    hue="cluster",
    palette="tab10"
)

plt.title(
    "Applicant Segments (K-Means)"
)

plt.show()



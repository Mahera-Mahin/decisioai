import pandas as pd
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA = BASE_DIR / "data" / "raw"
PROCESSED_DATA = BASE_DIR / "data" / "processed"

PROCESSED_DATA.mkdir(exist_ok=True)

# -----------------------------
# Load subscriptions data
# -----------------------------
subs = pd.read_csv(RAW_DATA / "subscriptions.csv")

# Convert dates
subs["start_date"] = pd.to_datetime(subs["start_date"])
subs["end_date"] = pd.to_datetime(subs["end_date"], errors="coerce")

# Extract month (YYYY-MM)
subs["month"] = subs["start_date"].dt.to_period("M").astype(str)

# -----------------------------
# NEW MRR
# -----------------------------
new_mrr = (
    subs.groupby("month")["mrr_amount"]
    .sum()
    .reset_index(name="new_mrr")
)

# -----------------------------
# EXPANSION MRR
# -----------------------------
expansion_mrr = (
    subs[subs["upgrade_flag"] == True]
    .groupby("month")["mrr_amount"]
    .sum()
    .reset_index(name="expansion_mrr")
)

# -----------------------------
# CHURNED MRR
# -----------------------------
churned_mrr = (
    subs[subs["churn_flag"] == True]
    .groupby("month")["mrr_amount"]
    .sum()
    .reset_index(name="churned_mrr")
)

# -----------------------------
# ACTIVE USERS (end of month)
# -----------------------------
def active_users_for_month(df, month):
    month_end = pd.Period(month).to_timestamp("M")
    active = df[
        (df["start_date"] <= month_end) &
        ((df["end_date"].isna()) | (df["end_date"] > month_end))
    ]
    return active["account_id"].nunique()

months = sorted(subs["month"].unique())
active_users = []

for m in months:
    active_users.append({
        "month": m,
        "active_users": active_users_for_month(subs, m)
    })

active_users = pd.DataFrame(active_users)

# -----------------------------
# NEW CUSTOMERS
# -----------------------------
first_subscription = (
    subs.sort_values("start_date")
    .groupby("account_id")
    .first()
    .reset_index()
)

first_subscription["month"] = (
    first_subscription["start_date"]
    .dt.to_period("M")
    .astype(str)
)

new_customers = (
    first_subscription.groupby("month")
    .size()
    .reset_index(name="new_customers")
)

# -----------------------------
# CHURNED CUSTOMERS
# -----------------------------
churned_customers = (
    subs[subs["churn_flag"] == True]
    .groupby("month")["account_id"]
    .nunique()
    .reset_index(name="churned_customers")
)

# -----------------------------
# MERGE ALL
# -----------------------------
df = (
    new_mrr
    .merge(expansion_mrr, on="month", how="left")
    .merge(churned_mrr, on="month", how="left")
    .merge(active_users, on="month", how="left")
    .merge(new_customers, on="month", how="left")
    .merge(churned_customers, on="month", how="left")
)

df.fillna(0, inplace=True)
df = df.sort_values("month")

# -----------------------------
# STARTING & ENDING MRR
# -----------------------------
df["starting_mrr"] = df["new_mrr"].shift(1).fillna(0)
df["ending_mrr"] = (
    df["starting_mrr"]
    + df["new_mrr"]
    + df["expansion_mrr"]
    - df["churned_mrr"]
)

# -----------------------------
# MARKETING SPEND (TEMP)
# -----------------------------
df["marketing_spend"] = 3000

# -----------------------------
# FINAL EXPORT
# -----------------------------
final_cols = [
    "month",
    "starting_mrr",
    "new_mrr",
    "expansion_mrr",
    "churned_mrr",
    "ending_mrr",
    "active_users",
    "new_customers",
    "churned_customers",
    "marketing_spend"
]

output_path = PROCESSED_DATA / "saas_metrics.csv"
df[final_cols].to_csv(output_path, index=False)

print(f"✅ Monthly SaaS metrics generated at: {output_path}")

import pandas as pd
from pathlib import Path

print("KPI CALCULATOR STARTED")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "saas_metrics.csv"

df = pd.read_csv(DATA_PATH)
print("CSV LOADED SUCCESSFULLY")
print(df.head())


# -----------------------
# BASIC VALIDATIONS
# -----------------------

required_columns = [
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

missing = [col for col in required_columns if col not in df.columns]

if missing:
    raise ValueError(f"Missing columns: {missing}")

if (df[required_columns[1:]] < 0).any().any():
    raise ValueError("Negative values found in metrics")

print("✅ Data validation passed")


# -----------------------
# KPI CALCULATIONS
# -----------------------

df["net_mrr_growth"] = df["ending_mrr"] - df["starting_mrr"]

df["net_mrr_growth_pct"] = (
    df["net_mrr_growth"] / df["starting_mrr"]
).replace([float("inf"), -float("inf")], 0).fillna(0)

df["revenue_churn_pct"] = (
    df["churned_mrr"] / df["starting_mrr"]
).replace([float("inf"), -float("inf")], 0).fillna(0)

df["customer_churn_pct"] = (
    df["churned_customers"] / df["active_users"]
).replace([float("inf"), -float("inf")], 0).fillna(0)

df["arpu"] = (
    df["ending_mrr"] / df["active_users"]
).replace([float("inf"), -float("inf")], 0).fillna(0)

df["cac"] = (
    df["marketing_spend"] / df["new_customers"]
).replace([float("inf"), -float("inf")], 0).fillna(0)

print("✅ KPIs calculated")

OUTPUT_PATH = BASE_DIR / "data" / "processed" / "saas_kpis.csv"
df.to_csv(OUTPUT_PATH, index=False)

print(f"📊 KPI file saved at {OUTPUT_PATH}")

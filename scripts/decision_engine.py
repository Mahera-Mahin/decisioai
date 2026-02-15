import pandas as pd
from pathlib import Path

print("🧠 DECISION ENGINE STARTED")

BASE_DIR = Path(__file__).resolve().parent.parent
KPI_PATH = BASE_DIR / "data" / "processed" / "saas_kpis.csv"

df = pd.read_csv(KPI_PATH)
df = df.sort_values("month")

print("KPI DATA LOADED")
print(df.tail(1))
latest = df.iloc[-1]

print("📅 Analyzing month:", latest["month"])

decisions = []

if latest["revenue_churn_pct"] > 0.10:
    decisions.append({
        "decision_type": "RETENTION_PRIORITY",
        "confidence": "HIGH",
        "reason": "Revenue churn is above 10%",
    })

if latest["net_mrr_growth_pct"] < 0.05:
    decisions.append({
        "decision_type": "GROWTH_SLOWDOWN",
        "confidence": "MEDIUM",
        "reason": "Net MRR growth is below 5%",
    })

if (
    latest["revenue_churn_pct"] < 0.05
    and latest["net_mrr_growth_pct"] > 0.10
):
    decisions.append({
        "decision_type": "SCALE",
        "confidence": "HIGH",
        "reason": "Low churn and strong growth",
    })
else:
    decisions.append({
        "decision_type": "STABILIZE",
        "confidence": "MEDIUM",
        "reason": "Growth or retention not stable",
    })

print("\n📌 DECISIONS GENERATED:")
for d in decisions:
    print(d)

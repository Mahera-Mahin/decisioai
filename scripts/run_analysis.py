import pandas as pd
from pathlib import Path
import requests

print("🚀 DECISIOAI FULL BUSINESS ANALYSIS")

# -----------------------------
# LOAD KPI DATA
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
KPI_PATH = BASE_DIR / "data" / "processed" / "saas_kpis.csv"

df = pd.read_csv(KPI_PATH)
df = df.sort_values("month")

latest = df.iloc[-1]

print("\n📊 Latest Month:", latest["month"])

# -----------------------------
# DECISION ENGINE (Simple Rules)
# -----------------------------
decision = None

if latest["revenue_churn_pct"] > 0.10:
    decision = {
        "decision_type": "RETENTION_PRIORITY",
        "confidence": "HIGH",
        "reason": "Revenue churn is above 10%"
    }

elif latest["net_mrr_growth_pct"] < 0.05:
    decision = {
        "decision_type": "GROWTH_SLOWDOWN",
        "confidence": "MEDIUM",
        "reason": "Net MRR growth is below 5%"
    }

else:
    decision = {
        "decision_type": "STABLE_GROWTH",
        "confidence": "MEDIUM",
        "reason": "Business metrics are stable"
    }

print("\n🧠 Decision Detected:")
print(decision)

# -----------------------------
# BUILD AI PROMPT
# -----------------------------
prompt = f"""
You are a senior SaaS business advisor.

Rules:
- Do NOT calculate metrics
- Do NOT invent numbers
- Do NOT change the decision

Decision:
{decision}

KPIs:
Revenue churn %: {latest['revenue_churn_pct']:.2f}
Net MRR growth %: {latest['net_mrr_growth_pct']:.2f}
Customer churn %: {latest['customer_churn_pct']:.2f}

Explain this decision clearly to a SaaS founder.
"""

# -----------------------------
# CALL OLLAMA
# -----------------------------
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "tinyllama",
        "prompt": prompt,
        "stream": False
    }
)

if response.status_code == 200:
    result = response.json()
    print("\n🧠 AI BUSINESS ADVICE:\n")
    print(result["response"])
else:
    print("❌ Error:", response.status_code)
    print(response.text)

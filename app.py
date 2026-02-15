from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
from pathlib import Path
import io
from groq import Groq
import os

app = FastAPI(title="DecisioAI Backend")

BASE_DIR = Path(__file__).resolve().parent
KPI_PATH = BASE_DIR / "data" / "processed" / "saas_kpis.csv"

# 🔴 PUT YOUR REAL GROQ KEY HERE (FOR LOCAL TESTING ONLY)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ==========================================
# Utility Functions
# ==========================================

def get_latest_kpis():
    df = pd.read_csv(KPI_PATH)
    df = df.sort_values("month")
    return df.iloc[-1]


def decision_engine(latest):
    if latest["revenue_churn_pct"] > 0.10:
        return {
            "decision_type": "RETENTION_PRIORITY",
            "confidence": "HIGH",
            "reason": "Revenue churn is above 10%"
        }

    elif latest["net_mrr_growth_pct"] < 0.05:
        return {
            "decision_type": "GROWTH_SLOWDOWN",
            "confidence": "MEDIUM",
            "reason": "Net MRR growth is below 5%"
        }

    else:
        return {
            "decision_type": "STABLE_GROWTH",
            "confidence": "MEDIUM",
            "reason": "Business metrics are stable"
        }


def validate_uploaded_data(df):

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
        "marketing_spend",
        "net_mrr_growth_pct",
        "revenue_churn_pct",
        "customer_churn_pct"
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        return False, f"Missing required columns: {missing}"

    if df.isnull().any().any():
        return False, "File contains missing values."

    numeric_cols = [
        "starting_mrr",
        "new_mrr",
        "expansion_mrr",
        "churned_mrr",
        "ending_mrr"
    ]

    if (df[numeric_cols] < 0).any().any():
        return False, "Revenue values cannot be negative."

    return True, "Valid"


def call_groq(latest, decision):

    client = Groq(api_key=GROQ_API_KEY)

    system_message = """
You are a sharp SaaS startup advisor.
Be analytical, concise, and practical.
Only use provided KPIs.
Do not invent numbers.
"""

    user_message = f"""
Business Context:

Decision: {decision['decision_type']}
Reason: {decision['reason']}

KPIs:
Revenue churn: {latest['revenue_churn_pct']:.2f}
Net MRR growth: {latest['net_mrr_growth_pct']:.2f}
Customer churn: {latest['customer_churn_pct']:.2f}

Explain clearly what the founder should focus on.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


# ==========================================
# Request Model
# ==========================================

class AskRequest(BaseModel):
    question: str


# ==========================================
# Routes
# ==========================================

@app.get("/")
def home():
    return {"message": "Welcome to DecisioAI Backend 🚀"}


@app.get("/analyze")
def analyze_business():

    latest = get_latest_kpis()
    decision = decision_engine(latest)
    explanation = call_groq(latest, decision)

    return {
        "month": latest["month"],
        "decision": decision,
        "ai_explanation": explanation
    }


@app.post("/upload-and-analyze")
async def upload_and_analyze(file: UploadFile = File(...)):

    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))

    is_valid, message = validate_uploaded_data(df)

    if not is_valid:
        return {"error": message}

    df = df.sort_values("month")
    latest = df.iloc[-1]

    decision = decision_engine(latest)
    explanation = call_groq(latest, decision)

    return {
        "month": latest["month"],
        "decision": decision,
        "ai_explanation": explanation
    }


@app.post("/ask")
def ask_business(request: AskRequest):

    latest = get_latest_kpis()
    decision = decision_engine(latest)

    client = Groq(api_key=GROQ_API_KEY)

    system_message = """
You are an AI SaaS business copilot.
Be analytical and concise.
Only use provided KPIs.
Do not invent numbers.
"""

    user_message = f"""
Business Context:

Decision: {decision['decision_type']}
Reason: {decision['reason']}

KPIs:
Revenue churn: {latest['revenue_churn_pct']:.2f}
Net MRR growth: {latest['net_mrr_growth_pct']:.2f}
Customer churn: {latest['customer_churn_pct']:.2f}

Founder Question:
{request.question}

Answer clearly using the data.
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3
    )

    answer = response.choices[0].message.content

    return {
        "question": request.question,
        "decision_context": decision,
        "answer": answer
    }

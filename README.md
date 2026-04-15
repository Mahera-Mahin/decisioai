🚀 DecisioAI — AI Decision Intelligence for SaaS Metrics

DecisioAI is a cloud-deployed MVP that transforms SaaS KPI data into clear, actionable business decisions.

Most dashboards report metrics.
DecisioAI focuses on what to do next.

🧠 Problem

SaaS founders and operators track metrics like:

MRR
Churn
Growth

But struggle to answer:

What should I prioritize this month?
Why is growth slowing?
Where am I losing revenue?
💡 Solution

DecisioAI converts:

Raw KPI Data → Validated Metrics → Decisions → AI Explanations

It combines:

Deterministic business logic
AI reasoning (LLM)
Structured KPI validation
⚙️ Key Features
📊 KPI Analyzer
Processes SaaS metrics (MRR, churn, growth)
Ensures data consistency through validation
🧩 Decision Engine
Rule-based prioritization:
Retention vs Growth
Example:
High churn → Retention priority
Low growth → Growth concern
🤖 AI Insight Engine
Explains:
Why the decision matters
What to focus on
Risks if ignored
Uses LLM constrained by business context
❓ Ask the Business
Natural language queries:
“What should I focus on this month?”
“Where am I losing revenue?”
Context-aware responses using latest KPIs
📁 CSV Upload
Upload structured KPI dataset
Automatic validation of required columns
🏗️ Architecture
Frontend (Streamlit)
        ↓
FastAPI Backend (Render)
        ↓
Decision Engine (Rule-based)
        ↓
LLM Reasoning Layer (Groq)
🛠️ Tech Stack
Backend: FastAPI
Frontend: Streamlit
AI Layer: Groq LLM API
Data Processing: Pandas
Deployment: Render (Backend), Streamlit Cloud (Frontend)
📂 Project Structure
decisioai/
│
├── app.py                  # FastAPI backend
├── dashboard.py           # Streamlit frontend
├── scripts/               # Data processing scripts
├── data/
│   ├── raw/
│   └── processed/
│       └── saas_kpis.csv
├── requirements.txt
└── README.md
📊 Required CSV Format

The system expects the following columns:

month
starting_mrr
new_mrr
expansion_mrr
churned_mrr
ending_mrr
active_users
new_customers
churned_customers
marketing_spend
net_mrr_growth_pct
revenue_churn_pct
customer_churn_pct
▶️ Running Locally
1️⃣ Clone Repository
git clone https://github.com/your-username/decisioai.git
cd decisioai
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Set Environment Variable
export GROQ_API_KEY=your_api_key

(Windows PowerShell)

$env:GROQ_API_KEY="your_api_key"
4️⃣ Run Backend
uvicorn app:app --reload
5️⃣ Run Frontend
streamlit run dashboard.py
🌍 Live Demo

👉 https://decisioai.streamlit.app/

🎯 Example Output

Input:
Revenue churn = 18%

Output:
Retention should be prioritized. Growth will not compound until revenue leakage stabilizes.

🧠 Key Learnings
Designing decision systems using rule-based logic
Combining deterministic logic with LLM reasoning
SaaS KPI modeling (MRR, churn, growth tradeoffs)
Backend API design and deployment
Building AI systems that augment decision-making
⚠️ Limitations (MVP)
Requires structured KPI input
No automated data ingestion (manual CSV upload)
No historical trend modeling or forecasting
Single-tenant (no user accounts)
🚀 Future Improvements
Cohort analysis & retention breakdown
Automated data ingestion (Stripe, CRM, etc.)
Forecasting & predictive analytics
Multi-tenant SaaS architecture
Improved UX for data upload & validation
🤝 Feedback

This is an early-stage MVP exploring AI-driven decision systems.

If you’re working on SaaS, analytics, or AI — feedback is welcome.

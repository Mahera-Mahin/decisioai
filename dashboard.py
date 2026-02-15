import streamlit as st
import requests

BACKEND_URL = "https://decisioai.onrender.com"

st.set_page_config(page_title="DecisioAI", layout="wide")

st.title("DecisioAI — AI Decision Copilot")
st.markdown("Turn SaaS metrics into actionable business decisions.")
st.markdown("---")


# ==========================================
# KPI + Analysis Section
# ==========================================

st.header("📊 Upload SaaS KPI CSV")

uploaded_file = st.file_uploader("Upload saas_kpis.csv", type=["csv"])

if uploaded_file is not None:
    if st.button("Analyze Business"):

        with st.spinner("Analyzing business metrics..."):

            response = requests.post(
                f"{BACKEND_URL}/upload-and-analyze",
                files={"file": uploaded_file}
            )

            if response.status_code == 200:
                result = response.json()

                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("Analysis Complete")

                    decision = result["decision"]

                    # ==========================================
                    # KPI Metric Cards (Top Section)
                    # ==========================================
                    st.subheader("📈 Business Snapshot")

                    # These are extracted from AI explanation context
                    # If you want direct KPI values, we can modify backend to return them too

                    col1, col2, col3 = st.columns(3)

                    # These are approximations from decision logic
                    # You can enhance backend to return raw KPI numbers later
                    if decision["decision_type"] == "RETENTION_PRIORITY":
                        risk_level = "High"
                    else:
                        risk_level = "Moderate"

                    col1.metric("Primary Focus", decision["decision_type"])
                    col2.metric("Confidence", decision["confidence"])
                    col3.metric("Risk Level", risk_level)

                    st.markdown("---")

                    # ==========================================
                    # Decision Section
                    # ==========================================
                    st.subheader(" Decision Context")

                    st.info(f"Reason: {decision['reason']}")

                    st.markdown("---")

                    # ==========================================
                    # AI Explanation Styled Card
                    # ==========================================
                    st.subheader("🧠 AI Insight")

                    st.markdown(
                        f"""
                        <div style="
                            background-color:#111827;
                            padding:25px;
                            border-radius:12px;
                            color:white;
                            font-size:16px;
                            line-height:1.6;
                        ">
                        {result["ai_explanation"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:
                st.error("Backend error.")


st.markdown("---")


# ==========================================
# Ask the Business Section
# ==========================================

st.header("🤖 Ask the Business")

question = st.text_input("Ask a business question:")

if st.button("Ask AI"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):

            response = requests.post(
                f"{BACKEND_URL}/ask",
                json={"question": question}
            )

            if response.status_code == 200:
                result = response.json()

                decision = result["decision_context"]

                # Decision Summary Cards
                st.subheader(" Decision Context")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Primary Focus", decision["decision_type"])

                with col2:
                    st.metric("Confidence", decision["confidence"])

                st.info(f"Reason: {decision['reason']}")

                st.markdown("---")

                # AI Answer Card
                st.subheader("🧠 AI Answer")

                st.markdown(
                    f"""
                    <div style="
                        background-color:#111827;
                        padding:25px;
                        border-radius:12px;
                        color:white;
                        font-size:16px;
                        line-height:1.6;
                    ">
                    {result["answer"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:
                st.error("Backend error.")

# streamlit_app.py – Sync with working 11 agents

import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Multi-AI Agent Contract Intelligence API",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Multi-AI Agent Contract Intelligence API")
st.write("Upload your contract and let our 11 AI agents analyze it!")

API_URL = "http://127.0.0.1:8000"

def check_api():
    try:
        response = requests.get(f"{API_URL}/")
        return response.status_code == 200
    except:
        return False

def main():
    if not check_api():
        st.error("⚠️ API is not running! Please start the FastAPI server first.")
        st.code("python main.py")
        return

    st.success("✅ API is running!")

    st.subheader("📝 Enter Your Contract Text")
    contract_text = st.text_area(
        "Paste your contract here:",
        height=200,
        placeholder="Example: This agreement is between Party A and Party B for $10,000..."
    )

    if st.button("🔍 Analyze Contract", type="primary"):
        if contract_text.strip():
            analyze_contract(contract_text)
        else:
            st.warning("Please enter some contract text first!")

def analyze_contract(contract_text):
    with st.spinner("🤖 Our AI agents are analyzing your contract..."):
        try:
            response = requests.post(
                f"{API_URL}/analyze-contract",
                json={"contract_text": contract_text}
            )
            if response.status_code == 200:
                display_results(response.json())
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")

def display_results(results):
    st.subheader("📊 Analysis Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📖 Contract Reader")
        reader = results["contract_reader"]
        st.write("**Parties Found:**", *reader.get("parties", []))
        st.write("**Dates Found:**", *reader.get("dates", []))
        st.write("**Amounts Found:**", *reader.get("amounts", []))

    with col2:
        st.markdown("### ⚠️ Risk Checker")
        risk = results["risk_checker"]
        st.write("**Risk Level:**", risk["risk_level"])
        st.write("**Risky Phrases:**", *risk["risky_phrases"])
        st.write("**Warnings:**", *risk["warnings"])

    with col3:
        st.markdown("### 📋 Summary")
        summary = results["summary"]
        st.write("**Contract Length:**", summary["contract_length"], "words")
        st.write("**Summary:**", summary["summary"])
        st.write("**Recommendations:**", *summary["recommendations"])

    st.markdown("---")

    st.markdown("### 🌍 Jurisdiction Checker")
    jurisdiction = results["jurisdiction"]
    st.write("**Jurisdictions Detected:**", *jurisdiction["jurisdictions"])

    st.markdown("### 📌 Obligation Extractor")
    obligations = results["obligations"]
    st.write("**Obligations Found:**", *obligations["obligations"])

    st.markdown("### 📑 Clause Categorizer")
    clauses = results["clauses"]
    for category, clause_text in clauses["clauses"].items():
        st.write(f"**{category}:** {clause_text}")

    st.markdown("### 🤝 Negotiation Advisor")
    negotiation = results["negotiation_advice"]
    for tip in negotiation["negotiation_tips"]:
        st.write(f"- {tip}")

    st.markdown("### 📄 Missing Clause Detector")
    missing = results["missing_clauses"]
    for clause in missing["missing_clauses"]:
        st.write(f"- {clause}")

    st.markdown("### 🚩 Red Flag Detector")
    red_flags = results["red_flags"]
    for flag in red_flags["red_flags"]:
        st.write(f"- {flag}")

    st.markdown("### 🧮 Contract Scorer")
    score = results["contract_score"]
    st.write("**Score:**", score["contract_score"])
    st.write("**Rating:**", score["rating"])

    st.markdown("### ✍️ Amendment Recommender")
    amendments = results["amendments"]
    for rec in amendments["amendments"]:
        st.write(f"- {rec}")

st.sidebar.title("ℹ️ About")
st.sidebar.write("""
This app uses 11 AI agents:

📖 **Contract Reader** – Finds parties, dates, amounts  
⚠️ **Risk Checker** – Identifies risky terms  
📋 **Summary Agent** – Creates overall summary  
🌍 **Jurisdiction Checker** – Flags governing law  
📌 **Obligation Extractor** – Extracts payments & duties  
📑 **Clause Categorizer** – Labels key clause types  
🤝 **Negotiation Advisor** – Suggests what to push back on  
📄 **Missing Clause Detector** – Finds missing legal terms  
🚩 **Red Flag Detector** – Flags contract red flags  
🧮 **Contract Scorer** – Scores contract quality  
✍️ **Amendment Recommender** – Suggests improvement edits
""")

st.sidebar.write("---")
st.sidebar.write("**API Status:**")
if check_api():
    st.sidebar.success("✅ Connected")
else:
    st.sidebar.error("❌ Disconnected")

if __name__ == "__main__":
    main()

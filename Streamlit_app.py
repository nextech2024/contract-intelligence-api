# streamlit_app.py - Frontend UI

import streamlit as st
import requests
import json

# Page config
st.set_page_config(
    page_title="Multi- AI Agent Contract Intelligence API",
    page_icon="📄",
    layout="wide"
)

# Title
st.title("📄 Multi-AI gent Contract Intelligence API")
st.write("Upload your contract and let our 3 AI agents analyze it!")

# API URL
API_URL = "http://127.0.0.1:8000"

# Check if API is running
def check_api():
    try:
        response = requests.get(f"{API_URL}/")
        return response.status_code == 200
    except:
        return False

# Main app
def main():
    # Check API status
    if not check_api():
        st.error("⚠️ API is not running! Please start the FastAPI server first.")
        st.code("python main.py")
        return
    
    st.success("✅ API is running!")
    
    # Contract input
    st.subheader("📝 Enter Your Contract Text")
    contract_text = st.text_area(
        "Paste your contract here:",
        height=200,
        placeholder="Example: This agreement is between Party A and Party B for $10,000..."
    )
    
    # Analyze button
    if st.button("🔍 Analyze Contract", type="primary"):
        if contract_text.strip():
            analyze_contract(contract_text)
        else:
            st.warning("Please enter some contract text first!")

def analyze_contract(contract_text):
    """Send contract to API and display results"""
    
    with st.spinner("🤖 Our AI agents are analyzing your contract..."):
        try:
            # Send to API
            response = requests.post(
                f"{API_URL}/analyze-contract",
                json={"contract_text": contract_text}
            )
            
            if response.status_code == 200:
                results = response.json()
                display_results(results)
            else:
                st.error(f"Error: {response.status_code}")
                
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")

def display_results(results):
    """Display the analysis results"""
    
    st.subheader("📊 Analysis Results")
    
    # Create 3 columns for 3 agents
    col1, col2, col3 = st.columns(3)
    
    # Agent 1: Contract Reader
    with col1:
        st.markdown("### 📖 Contract Reader")
        reader = results["contract_reader"]
        
        st.write("**Parties Found:**")
        parties = reader.get("parties", ["No parties found"])
        for party in parties:
            st.write(f"• {party}")
        
        st.write("**Dates Found:**")
        dates = reader.get("dates", ["No dates found"])
        for date in dates:
            st.write(f"• {date}")
        
        st.write("**Amounts Found:**")
        amounts = reader.get("amounts", ["No amounts found"])
        for amount in amounts:
            st.write(f"• {amount}")
    
    # Agent 2: Risk Checker
    with col2:
        st.markdown("### ⚠️ Risk Checker")
        risk = results["risk_checker"]
        
        # Risk level with color
        risk_level = risk["risk_level"]
        if risk_level == "HIGH":
            st.error(f"🚨 Risk Level: {risk_level}")
        elif risk_level == "MEDIUM":
            st.warning(f"⚠️ Risk Level: {risk_level}")
        else:
            st.success(f"✅ Risk Level: {risk_level}")
        
        st.write("**Risky Phrases:**")
        for phrase in risk["risky_phrases"]:
            st.write(f"• {phrase}")
        
        st.write("**Warnings:**")
        for warning in risk["warnings"]:
            st.write(warning)
    
    # Agent 3: Summary
    with col3:
        st.markdown("### 📋 Summary")
        summary = results["summary"]
        
        st.write(f"**Contract Length:** {summary['contract_length']} words")
        
        st.write("**Summary:**")
        st.write(summary["summary"])
        
        st.write("**Recommendations:**")
        for rec in summary["recommendations"]:
            st.write(f"• {rec}")

# Sidebar with info
st.sidebar.title("ℹ️ About")
st.sidebar.write("""
This app uses 3 AI agents:

🤖 **Contract Reader**
- Finds parties, dates, amounts

🤖 **Risk Checker** 
- Identifies risky terms

🤖 **Summary Agent**
- Creates overall summary
""")

st.sidebar.write("---")
st.sidebar.write("**API Status:**")
if check_api():
    st.sidebar.success("✅ Connected")
else:
    st.sidebar.error("❌ Disconnected")

# Run the app
if __name__ == "__main__":
    main()
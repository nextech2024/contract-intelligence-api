# contract-intelligence-api
Multi-AI Agent API for contract reading, risk checking, and clause categorization


# 🧠 Nextech Multi-AI Agent Contract Intelligence API

This FastAPI-based application uses multiple AI agents to read, analyze, and summarize legal contracts.

## 🚀 Features


ℹ️ About
This app uses 11 AI agents:

📖 Contract Reader – Finds parties, dates, amounts
⚠️ Risk Checker – Identifies risky terms
📋 Summary Agent – Creates overall summary
🌍 Jurisdiction Checker – Flags governing law
📌 Obligation Extractor – Extracts payments & duties
📑 Clause Categorizer – Labels key clause types
🤝 Negotiation Advisor – Suggests what to push back on
📄 Missing Clause Detector – Finds missing legal terms
🚩 Red Flag Detector – Flags contract red flags
🧮 Contract Scorer – Scores contract quality
✍️ Amendment Recommender
## 🛠️ How to Run

### Local (for testing/demo)
```bash
uvicorn main:app --host 0.0.0.0 --port 8000

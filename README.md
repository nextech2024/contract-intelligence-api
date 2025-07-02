# contract-intelligence-api
Multi-AI Agent API for contract reading, risk checking, and clause categorization


# 🧠 Nextech Multi-AI Agent Contract Intelligence API

This FastAPI-based application uses multiple AI agents to read, analyze, and summarize legal contracts.

## 🚀 Features

- 📑 **ContractReaderAgent** – Extracts key data like parties, amounts, and terms.
- ⚠️ **RiskCheckerAgent** – Flags risky clauses or missing protections.
- 📌 **ClauseCategorizerAgent** – Organizes clauses by topic (e.g., IP, termination).
- 📍 **JurisdictionAgent** – Detects applicable laws and jurisdictions.
- 📋 **ObligationAgent** – Highlights payment obligations or compliance terms.
- 🧾 **SummaryAgent** – Provides a human-readable summary of the entire contract.

## 🛠️ How to Run

### Local (for testing/demo)
```bash
uvicorn main:app --host 0.0.0.0 --port 8000

# 🚀 Deployment Guide for Nextech Multi-AI Agent Contract API

This guide helps you deploy the Contract Intelligence API either locally (for testing) or on AWS (for production use).

---

## 📦 Local Deployment (FastAPI)

### Requirements
- Python 3.9+
- pip
- virtualenv

### Setup Instructions

```bash
# Clone the repo
git clone https://github.com/nextech2024/contract-intelligence-api.git
cd contract-intelligence-api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn main:app --host 0.0.0.0 --port 8000

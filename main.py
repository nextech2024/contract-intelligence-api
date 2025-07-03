# main.py - FastAPI Backend

from mangum import Mangum
from fastapi import FastAPI
from pydantic import BaseModel
from agents import (
    ContractReaderAgent,
    RiskCheckerAgent,
    SummaryAgent,
    JurisdictionAgent,
    ObligationAgent,
    ClauseCategorizerAgent,
    NegotiationAdvisorAgent,
    MissingClauseDetectorAgent,
    RedFlagAgent,
    ContractScoringAgent,
    AmendmentRecommenderAgent
)

# Create FastAPI app
app = FastAPI(title="Multi-AI Agent Contract Intelligence API!")

# for AWS Lambda
handler = Mangum(app)

# Create all 11 agents
reader_agent = ContractReaderAgent()
risk_agent = RiskCheckerAgent()
summary_agent = SummaryAgent()
jurisdiction_agent = JurisdictionAgent()
obligation_agent = ObligationAgent()
clause_agent = ClauseCategorizerAgent()
negotiation_agent = NegotiationAdvisorAgent()
missing_clause_agent = MissingClauseDetectorAgent()
red_flag_agent = RedFlagAgent()
score_agent = ContractScoringAgent()
amendment_agent = AmendmentRecommenderAgent()

# Data model for contract input
class ContractInput(BaseModel):
    contract_text: str

@app.get("/")
def home():
    """Welcome message"""
    return {"message": "Multi-AI Agent Contract Intelligence API! 🚀"}

@app.post("/analyze-contract")
def analyze_contract(contract: ContractInput):
    """Analyze contract with all 11 agents"""
    
    # Step 1: Contract Reader analyzes first
    reader_result = reader_agent.analyze(contract.contract_text)
    
    # Step 2: Risk Checker analyzes
    risk_result = risk_agent.analyze(contract.contract_text)
    
    # Step 3: Summary Agent combines everything
    summary_result = summary_agent.analyze(
        contract.contract_text, 
        reader_result, 
        risk_result
    )
    
    # Step 4: Jurisdiction Agent checks legal jurisdiction
    jurisdiction_result = jurisdiction_agent.analyze(contract.contract_text)

    # Step 5: Obligation Extractor
    obligation_result = obligation_agent.analyze(contract.contract_text)

    # Step 6: Clause Categorizer Agent identifies clause types
    clause_result = clause_agent.analyze(contract.contract_text)

    # Step 7: Negotiation Advice
    negotiation_result = negotiation_agent.analyze(contract.contract_text)

    # Step 8: Missing Clause Detector
    missing_result = missing_clause_agent.analyze(contract.contract_text)

    # Step 9: Red Flag Detection
    red_flag_result = red_flag_agent.analyze(contract.contract_text)

    # Step 10: Contract Scoring
    score_result = score_agent.analyze(contract.contract_text)

    # Step 11: Amendment Recommendations
    amendment_result = amendment_agent.analyze(contract.contract_text)

    # Return all results
    return {
        "status": "success",
        "contract_reader": reader_result,
        "risk_checker": risk_result,
        "summary": summary_result,
        "jurisdiction": jurisdiction_result,
        "obligations": obligation_result,
        "clauses": clause_result,
        "negotiation_advice": negotiation_result,
        "missing_clauses": missing_result,
        "red_flags": red_flag_result,
        "contract_score": score_result,
        "amendments": amendment_result
    }

@app.get("/agents")
def list_agents():
    """List all available agents"""
    return {
        "agents": [
            {"name": "Contract Reader", "job": "Extract basic info"},
            {"name": "Risk Checker", "job": "Find risky parts"},
            {"name": "Summary Agent", "job": "Create summary"},
            {"name": "Jurisdiction Checker", "job": "Identify governing law clauses"},
            {"name": "Obligation Extractor", "job": "List responsibilities"},
            {"name": "Clause Categorizer", "job": "Group clauses by type"},
            {"name": "Negotiation Advisor", "job": "Suggest what to negotiate"},
            {"name": "Missing Clause Detector", "job": "Find missing standard clauses"},
            {"name": "Red Flag Detector", "job": "Highlight hidden red flags"},
            {"name": "Contract Scorer", "job": "Score contract quality"},
            {"name": "Amendment Recommender", "job": "Suggest helpful revisions"}
        ]
    }

# Run this if file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

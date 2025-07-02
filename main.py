# main.py - FastAPI Backend

from mangum import Mangum
from fastapi import FastAPI
from pydantic import BaseModel
from agents import ContractReaderAgent, RiskCheckerAgent, SummaryAgent, JurisdictionAgent,  ObligationAgent, ClauseCategorizerAgent

# Create FastAPI app
app = FastAPI(title="Multi-AI Agent Contract Intelligence API!")

#define routes...

#for AWS Lambda 
handler = Mangum(app)

# Create our 3 agents
reader_agent = ContractReaderAgent()
risk_agent = RiskCheckerAgent()
summary_agent = SummaryAgent()
jurisdiction_agent = JurisdictionAgent()
obligation_agent = ObligationAgent()
clause_agent = ClauseCategorizerAgent()



# Data model for contract input
class ContractInput(BaseModel):
    contract_text: str

@app.get("/")
def home():
    """Welcome message"""
    return {"message": "Multi-AI Agent Contract Intelligence API! 🚀"}

@app.post("/analyze-contract")
def analyze_contract(contract: ContractInput):
    """Analyze contract with all 3 agents"""
    
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


    # Return all results
    return {
        "status": "success",
        "contract_reader": reader_result,
        "risk_checker": risk_result,
        "summary": summary_result,
        "jurisdiction": jurisdiction_result,
        "obligations": obligation_result,
        "clauses": clause_result
    }

@app.get("/agents")
def list_agents():
    """List all available agents"""
    return {
        "agents": [
            {"name": "Contract Reader", "job": "Extract basic info"},
            {"name": "Risk Checker", "job": "Find risky parts"},
            {"name": "Summary Agent", "job": "Create summary"}
        ]
    }

# Run this if file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

 
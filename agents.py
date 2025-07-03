# agents.py - Fixed version with better detection

# agents.py - AI Agents for Contract Intelligence

import re

class ContractReaderAgent:
    def __init__(self):
        self.name = "Contract Reader"

    def analyze(self, contract_text):
        party_a = None
        party_b = None

        # Try several patterns for Party A
        patterns_a = [
            r'between\s+(.*?)\s*\(?["“]?Party A["”]?\)?',
            r'Party A[:\-]?\s*(.*?)[\n,.;]',
            r'"(.*?)"\s*\(?Party A\)?',
        ]
        for pattern in patterns_a:
            match = re.search(pattern, contract_text, re.IGNORECASE)
            if match:
                party_a = match.group(1).strip()
                break

        # Try several patterns for Party B
        patterns_b = [
            r'and\s+(.*?)\s*\(?["“]?Party B["”]?\)?',
            r'Party B[:\-]?\s*(.*?)[\n,.;]',
            r'"(.*?)"\s*\(?Party B\)?',
        ]
        for pattern in patterns_b:
            match = re.search(pattern, contract_text, re.IGNORECASE)
            if match:
                party_b = match.group(1).strip()
                break

        if party_a and party_b:
            parties = [f"Party A: {party_a}", f"Party B: {party_b}"]
        else:
            parties = ["Could not identify named parties"]

        # Dates & Amounts stay the same
        dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', contract_text)
        amounts = re.findall(r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?', contract_text)

        return {
            "agent_name": self.name,
            "parties": parties,
            "dates": dates or ["No dates found"],
            "amounts": amounts or ["No amounts found"]
        }


class RiskCheckerAgent:
    def __init__(self):
        self.name = "Risk Checker"

    def analyze(self, contract_text):
        risky_phrases = re.findall(r'\b(indemnify|liability|termination without cause|non-compete|penalty)\b', contract_text, re.IGNORECASE)
        risk_level = "LOW"
        if len(risky_phrases) >= 5:
            risk_level = "HIGH"
        elif len(risky_phrases) >= 2:
            risk_level = "MEDIUM"
        return {
            "agent_name": self.name,
            "risk_level": risk_level,
            "risky_phrases": list(set(risky_phrases)),
            "warnings": ["Carefully review the terms related to: " + ', '.join(set(risky_phrases))] if risky_phrases else []
        }

class SummaryAgent:
    def __init__(self):
        self.name = "Summary Agent"

    def analyze(self, contract_text, reader_result, risk_result):
        words = contract_text.split()
        summary = ' '.join(words[:50]) + ('...' if len(words) > 50 else '')
        recommendations = []
        if risk_result["risk_level"] != "LOW":
            recommendations.append("Seek legal advice before signing.")
        if not reader_result["dates"]:
            recommendations.append("Ensure dates are clearly specified.")
        return {
            "agent_name": self.name,
            "contract_length": len(words),
            "summary": summary,
            "recommendations": recommendations or ["No recommendations."]
        }

class JurisdictionAgent: 
    def __init__(self):
        self.name = "Jurisdiction Checker"

    def analyze(self, contract_text):
        jurisdiction_phrases = re.findall(r'(governed by|jurisdiction of|under the laws of)\s+[^.,\n]+', contract_text, re.IGNORECASE)
        return {
            "agent_name": self.name,
            "jurisdictions": jurisdiction_phrases or ["No jurisdiction clause found"]
        }

class ObligationAgent:
    def __init__(self):
        self.name = "Obligation Extractor"

    def analyze(self, contract_text):
        obligation_phrases = []
        patterns = [
            r'\b(?:party [ab]|vendor|contractor|client|service provider|company)\b.*?\b(?:shall|must|agrees to|is responsible for)\b.*?[.;]',
            r'\b(?:shall|must|agrees to|is responsible for)\b.*?[.;]'
        ]
        for pattern in patterns:
            matches = re.findall(pattern, contract_text, flags=re.IGNORECASE)
            obligation_phrases.extend(matches)
        return {
            "agent_name": self.name,
            "obligations": obligation_phrases or ["No clear obligations found"]
        }

class ClauseCategorizerAgent:
    def __init__(self):
        self.name = "Clause Categorizer"

    def analyze(self, contract_text):
        clause_categories = {
            "Termination": r'\btermination\b.*?(?=\n|\.|$)',
            "Confidentiality": r'\bconfidentiality\b.*?(?=\n|\.|$)',
            "Indemnity": r'\bindemnity\b.*?(?=\n|\.|$)',
            "Payment Terms": r'\bpayment terms\b.*?(?=\n|\.|$)'
        }
        results = {}
        for clause, pattern in clause_categories.items():
            match = re.search(pattern, contract_text, re.IGNORECASE | re.DOTALL)
            results[clause] = match.group(0).strip() if match else "Not found"
        return {
            "agent_name": self.name,
            "clauses": results
        }

class NegotiationAdvisorAgent:
    def __init__(self):
        self.name = "Negotiation Advisor"

    def analyze(self, contract_text):
        suggestions = []
        if "termination without cause" in contract_text.lower():
            suggestions.append("Negotiate a mutual termination clause.")
        if "indemnify" in contract_text.lower():
            suggestions.append("Limit indemnification scope.")
        return {
            "agent_name": self.name,
            "negotiation_tips": suggestions or ["No major negotiation points found"]
        }

class MissingClauseDetectorAgent:
    def __init__(self):
        self.name = "Missing Clause Detector"

    def analyze(self, contract_text):
        must_have_clauses = ["termination", "confidentiality", "payment terms", "dispute resolution"]
        missing = [clause for clause in must_have_clauses if clause not in contract_text.lower()]
        return {
            "agent_name": self.name,
            "missing_clauses": missing or ["All standard clauses found"]
        }

class RedFlagAgent:
    def __init__(self):
        self.name = "Red Flag Detector"

    def analyze(self, contract_text):
        red_flags = []
        if "unilateral change" in contract_text.lower():
            red_flags.append("Contract allows one-sided changes")
        if "automatic renewal" in contract_text.lower():
            red_flags.append("Auto-renewal without clear notice period")
        return {
            "agent_name": self.name,
            "red_flags": red_flags or ["No major red flags"]
        }

class ContractScoringAgent:
    def __init__(self):
        self.name = "Contract Scorer"

    def analyze(self, contract_text):
        score = 100
        if "indemnify" in contract_text.lower():
            score -= 10
        if "termination without cause" in contract_text.lower():
            score -= 15
        if "unilateral change" in contract_text.lower():
            score -= 15
        return {
            "agent_name": self.name,
            "contract_score": max(score, 0),
            "rating": "Good" if score >= 80 else ("Fair" if score >= 60 else "Poor")
        }

class AmendmentRecommenderAgent:
    def __init__(self):
        self.name = "Amendment Recommender"

    def analyze(self, contract_text):
        recommendations = []
        if "penalty" in contract_text.lower():
            recommendations.append("Consider clarifying or softening penalty terms.")
        if "termination without cause" in contract_text.lower():
            recommendations.append("Suggest mutual termination clause.")
        return {
            "agent_name": self.name,
            "amendments": recommendations or ["No major amendments needed"]
        }

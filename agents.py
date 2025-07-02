# agents.py - Fixed version with better detection

import re

class ContractReaderAgent:
    """Reads contract and extracts basic info"""
    
    def __init__(self):
        self.name = "Contract Reader"
    
    def analyze(self, contract_text):
        """Extract basic info from contract"""
        result = {
            "agent_name": self.name,
            "parties": self.find_parties(contract_text),
            "dates": self.find_dates(contract_text),
            "amounts": self.find_amounts(contract_text)
        }
        return result
    
    def find_parties(self, text):
        """Find parties in contract"""
        parties = []
        text_lower = text.lower()
        
        # Look for common party terms
        if "party a" in text_lower:
            parties.append("Party A")
        if "party b" in text_lower:
            parties.append("Party B")
        if "client" in text_lower:
            parties.append("Client")
        if "vendor" in text_lower:
            parties.append("Vendor")
        if "service provider" in text_lower:
            parties.append("Service Provider")
        if "company" in text_lower:
            parties.append("Company")
        if "contractor" in text_lower:
            parties.append("Contractor")
            
        return parties if parties else ["Parties not clearly identified"]
    
    def find_dates(self, text):
        """Find dates in contract"""
        # Multiple date patterns
        patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',  # 01/15/2024
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2}',    # 01/15/24
            r'\w+ \d{1,2}, \d{4}',             # January 15, 2024
            r'\d{1,2} \w+ \d{4}'               # 15 January 2024
        ]
        
        dates = []
        for pattern in patterns:
            found = re.findall(pattern, text)
            dates.extend(found)
        
        return dates if dates else ["No specific dates found"]
    
    def find_amounts(self, text):
        """Find money amounts"""
        # Look for dollar amounts
        patterns = [
            r'\$[\d,]+\.?\d*',           # $5,000 or $5,000.00
            r'\$\d+',                   # $5000
            r'[\d,]+\s*dollars?',       # 5000 dollars
            r'[\d,]+\s*USD'             # 5000 USD
        ]
        
        amounts = []
        for pattern in patterns:
            found = re.findall(pattern, text, re.IGNORECASE)
            amounts.extend(found)
        
        return amounts if amounts else ["No monetary amounts found"]


class RiskCheckerAgent:
    """Finds risky parts in contract"""
    
    def __init__(self):
        self.name = "Risk Checker"
        self.risk_words = [
            "penalty", "terminate", "breach", "liability", "void", "forfeit",
            "damages", "default", "sue", "court", "legal action", "cancel"
        ]
    
    def analyze(self, contract_text):
        """Check for risks in contract"""
        result = {
            "agent_name": self.name,
            "risk_level": self.calculate_risk(contract_text),
            "risky_phrases": self.find_risky_phrases(contract_text),
            "warnings": self.generate_warnings(contract_text)
        }
        return result
    
    def calculate_risk(self, text):
        """Calculate overall risk level"""
        text_lower = text.lower()
        risk_count = 0
        
        for word in self.risk_words:
            if word in text_lower:
                risk_count += 1
        
        if risk_count >= 4:
            return "HIGH"
        elif risk_count >= 2:
            return "MEDIUM"
        elif risk_count >= 1:
            return "LOW"
        else:
            return "VERY LOW"
    
    def find_risky_phrases(self, text):
        """Find specific risky phrases"""
        found_phrases = []
        text_lower = text.lower()
        
        for word in self.risk_words:
            if word in text_lower:
                found_phrases.append(f"Contains '{word}'")
        
        return found_phrases if found_phrases else ["No major risk terms found"]
    
    def generate_warnings(self, text):
        """Generate specific warnings"""
        warnings = []
        text_lower = text.lower()
        
        if "terminate" in text_lower:
            warnings.append("⚠️ Termination clauses present")
        if "penalty" in text_lower:
            warnings.append("⚠️ Penalty clauses detected")
        if "liability" in text_lower or "liable" in text_lower:
            warnings.append("⚠️ Liability terms present")
        if "breach" in text_lower:
            warnings.append("⚠️ Breach consequences specified")
        if "damages" in text_lower:
            warnings.append("⚠️ Damage clauses found")
            
        return warnings if warnings else ["✅ No major warning flags"]


class SummaryAgent:
    """Creates simple summary of everything"""
    
    def __init__(self):
        self.name = "Summary Agent"
    
    def analyze(self, contract_text, reader_result, risk_result):
        """Create summary from all analysis"""
        result = {
            "agent_name": self.name,
            "contract_length": len(contract_text.split()),
            "summary": self.create_summary(contract_text, reader_result, risk_result),
            "recommendations": self.give_recommendations(risk_result)
        }
        return result
    
    def create_summary(self, contract_text, reader_result, risk_result):
        """Create detailed summary"""
        parties = reader_result.get("parties", [])
        amounts = reader_result.get("amounts", [])
        risk_level = risk_result.get("risk_level", "UNKNOWN")
        
        # Count key contract elements
        word_count = len(contract_text.split())
        
        summary = f"""
📋 CONTRACT ANALYSIS SUMMARY:

📊 Basic Info:
• Contract Length: {word_count} words
• Parties: {len(parties)} identified
• Financial Terms: {len(amounts)} amounts found
• Risk Assessment: {risk_level}

💡 Key Findings:
• This appears to be a {"complex" if word_count > 100 else "simple"} contract
• {"Multiple parties involved" if len(parties) > 2 else "Standard two-party agreement"}
• {"Financial terms present" if amounts else "No clear financial terms"}
        """
        return summary.strip()
    
    def give_recommendations(self, risk_result):
        """Give specific recommendations"""
        risk_level = risk_result.get("risk_level", "LOW")
        warnings = risk_result.get("warnings", [])
        
        recommendations = []
        
        if risk_level == "HIGH":
            recommendations.extend([
                "🚨 HIGH RISK: Legal review strongly recommended",
                "Consider professional contract review",
                "Pay special attention to penalty clauses"
            ])
        elif risk_level == "MEDIUM":
            recommendations.extend([
                "⚠️ MEDIUM RISK: Careful review needed",
                "Review all termination and penalty terms",
                "Consider negotiating risk terms"
            ])
        elif risk_level == "LOW":
            recommendations.extend([
                "✅ LOW RISK: Standard contract terms",
                "Basic review recommended",
                "Focus on key business terms"
            ])
        else:
            recommendations.extend([
                "✅ VERY LOW RISK: Minimal risk detected",
                "Standard review process sufficient"
            ])
        
        # Add specific recommendations based on warnings
        if len(warnings) > 1:
            recommendations.append("📋 Multiple risk areas identified - detailed review needed")
        
        return recommendations

class JurisdictionAgent:
    """Identifies the legal jurisdiction mentioned in the contract"""
    
    def __init__(self):
        self.name = "Jurisdiction Checker"
    
    def analyze(self, contract_text):
        """Scan for jurisdiction phrases"""
        import re
        jurisdiction_phrases = re.findall(r'(governed by|jurisdiction of|under the laws of)\s+[^.,\n]+', contract_text, re.IGNORECASE)
        return {
            "agent_name": self.name,
            "jurisdictions": jurisdiction_phrases if jurisdiction_phrases else ["No jurisdiction clause found"]
        }

class ObligationAgent:
    """Extracts responsibilities and obligations in the contract"""

    def __init__(self):
        self.name = "Obligation Extractor"

    def analyze(self, contract_text):
        import re
        obligation_phrases = []

        # Look for patterns like "shall", "must", "agrees to", etc.
        patterns = [
            r'\b(?:party [ab]|vendor|contractor|client|service provider|company)\b.*?\b(?:shall|must|agrees to|is responsible for)\b.*?[.;]',
            r'\b(?:shall|must|agrees to|is responsible for)\b.*?[.;]'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, contract_text, flags=re.IGNORECASE)
            obligation_phrases.extend(matches)

        return {
            "agent_name": self.name,
            "obligations": obligation_phrases if obligation_phrases else ["No clear obligations found"]
        }

class ClauseCategorizerAgent:
    """Categorizes key clauses in the contract"""

    def __init__(self):
        self.name = "Clause Categorizer"

    def analyze(self, contract_text):
        import re
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

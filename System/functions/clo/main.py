"""
CLO Agent - Chief Legal Officer (Digital Paralegal)
Handles compliance, contracts, risk assessment, and legal research.
CRITICAL: CLO operates as a digital paralegal, NOT an attorney.

Commands:
    clo.compliance  - Compliance checklist and assessment
    clo.contract    - Contract template generation
    clo.risk        - Legal risk assessment
    clo.research    - Legal research
    clo.jurisdiction - Jurisdiction analysis
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'packages'))
from factory_core.agent import BaseAgent


class CLOAgent(BaseAgent):
    """
    CLO Agent - Chief Legal Officer (Digital Paralegal).

    CRITICAL DISCLAIMER:
    The CLO operates as a digital paralegal, NOT an attorney.
    All outputs must include appropriate disclaimers.
    All legal matters require attorney review.
    """

    LEGAL_DISCLAIMER = """
---

⚠️ **LEGAL DISCLAIMER**

This document was prepared by an AI assistant operating in a paralegal capacity.
This is NOT legal advice. This document has NOT been reviewed by a licensed attorney.

Before taking any actions based on this assessment:
1. Consult with a licensed attorney in your jurisdiction
2. Verify all regulatory requirements are current
3. Obtain professional legal review for all contracts

The information provided is for planning purposes only and may not be complete,
accurate, or current.
"""

    def __init__(self, factory_id: Optional[str] = None):
        super().__init__("CLO", "Chief Legal Officer", factory_id)
        self.memory_path = self._get_memory_path()
        self.logs_path = self._get_logs_path()

    def _get_memory_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "CLO" / ".clo" / "memory"

    def _get_logs_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "CLO" / "logs"

    def _get_project_root(self) -> Path:
        return Path(__file__).parent.parent.parent.parent

    def _load_ceo_brief(self) -> Optional[str]:
        brief_path = self.memory_path / "ceo-brief.md"
        if brief_path.exists():
            with open(brief_path, 'r') as f:
                return f.read()
        return None

    def _load_business_plan(self) -> Optional[str]:
        readme_path = self._get_project_root() / "README.md"
        if readme_path.exists():
            with open(readme_path, 'r') as f:
                return f.read()
        return None

    def _log_session(self, log_type: str, data: Dict[str, Any]) -> bool:
        try:
            self.logs_path.mkdir(parents=True, exist_ok=True)
            date_str = datetime.utcnow().strftime("%Y-%m-%d")
            log_path = self.logs_path / f"{log_type}-{date_str}.md"

            with open(log_path, 'a') as f:
                f.write(f"\n\n---\n\n# {log_type.title()} Session\n\n")
                f.write(f"**Date**: {datetime.utcnow().isoformat()}Z\n\n")
                f.write(json.dumps(data, indent=2))
            return True
        except Exception as e:
            self.logger.error(f"Could not log session: {e}")
            return False

    def _detect_high_risk_domains(self, text: str) -> list:
        """Detect high-risk legal domains."""
        text_lower = text.lower() if text else ""
        domains = []

        if any(kw in text_lower for kw in ["children", "kids", "minors", "under 18"]):
            domains.append({"domain": "Minors", "regulations": ["COPPA", "CARU"], "attorney_required": True})
        if any(kw in text_lower for kw in ["health", "medical", "patient", "therapy"]):
            domains.append({"domain": "Healthcare", "regulations": ["HIPAA", "HITECH"], "attorney_required": True})
        if any(kw in text_lower for kw in ["education", "school", "student"]):
            domains.append({"domain": "Education", "regulations": ["FERPA"], "attorney_required": True})
        if any(kw in text_lower for kw in ["crypto", "securities", "investment", "trading"]):
            domains.append({"domain": "Financial/Crypto", "regulations": ["SEC", "FinCEN"], "attorney_required": True})
        if any(kw in text_lower for kw in ["eu", "europe", "european", "gdpr"]):
            domains.append({"domain": "EU Operations", "regulations": ["GDPR"], "attorney_required": True})

        return domains

    # =========================================================================
    # CLO.COMPLIANCE - Compliance checklist
    # =========================================================================

    def clo_compliance(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create compliance checklist and regulatory assessment.
        """
        business_plan = self._load_business_plan()
        ceo_brief = self._load_ceo_brief()

        high_risk = self._detect_high_risk_domains(business_plan or "")

        prompt = f"""As a digital paralegal, create a compliance assessment for this business.

## Business Plan
{business_plan[:2500] if business_plan else "No plan available"}

## CEO Brief
{ceo_brief[:1000] if ceo_brief else "No brief available"}

## High-Risk Domains Detected
{json.dumps(high_risk, indent=2) if high_risk else "None detected"}

Generate a compliance assessment in this format:

# Compliance Assessment - [BUSINESS_NAME]

**Generated**: {datetime.utcnow().isoformat()}Z
**Prepared By**: CLO Agent (Digital Paralegal)
**Status**: DRAFT - REQUIRES ATTORNEY REVIEW

> ⚠️ **LEGAL DISCLAIMER**
> This document was prepared by an AI assistant operating as a digital paralegal.
> This is NOT legal advice. Consult with a licensed attorney.

## Regulatory Domain Analysis

| Domain | Applicable? | Reason | Priority |
|--------|-------------|--------|----------|
| Corporate Formation | Yes | All businesses | High |
| Consumer Protection (FTC) | [Yes/No] | [Reason] | [Priority] |
| Data Privacy (CCPA/GDPR) | [Yes/No] | [Reason] | [Priority] |
| [Other domains...] | | | |

## Compliance Checklist

### Corporate Formation
| Requirement | Status | Attorney Review |
|-------------|--------|-----------------|
| Choose entity type | ⏳ | ✅ Required |
| Register with state | ⏳ | ✅ Required |
| Obtain EIN | ⏳ | - |

### Data Privacy
[Continue for each applicable domain]

## Risk Assessment

| Risk Area | Likelihood | Impact | Mitigation |
|-----------|------------|--------|------------|
| [Risk] | H/M/L | H/M/L | [Action] |

## Required Documents

| Document | Purpose | Attorney Review |
|----------|---------|-----------------|
| Terms of Service | User agreement | ✅ Required |
| Privacy Policy | Data disclosure | ✅ Required |

## Recommended Actions

### Immediate (Before Launch)
- [ ] [Action] - Attorney: Required

### Short-term (Within 30 Days)
- [ ] [Action]

{self.LEGAL_DISCLAIMER}
"""

        try:
            assessment = self._think(
                prompt=prompt,
                task_type="legal_review",
                temperature=0.3,
                max_tokens=3000
            )

            self.memory_path.mkdir(parents=True, exist_ok=True)
            compliance_path = self.memory_path / "compliance-checklist.md"
            with open(compliance_path, 'w') as f:
                f.write(assessment)

            self._log_session("compliance", {
                "high_risk_domains": [d["domain"] for d in high_risk],
                "generated": True
            })

            return {
                "message": "Compliance assessment created",
                "assessment": assessment,
                "high_risk_domains": high_risk,
                "saved_to": str(compliance_path),
                "attorney_review_required": len(high_risk) > 0 or True
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # CLO.CONTRACT - Contract templates
    # =========================================================================

    def clo_contract(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate contract template drafts.
        """
        contract_type = payload.get("type", "terms_of_service")
        business_plan = self._load_business_plan()

        prompt = f"""As a digital paralegal, draft a {contract_type} template.

Business Context:
{business_plan[:1500] if business_plan else "General business"}

Generate a {contract_type} draft that:
1. Uses plain language where possible
2. Includes standard clauses for this type
3. Marks areas needing attorney customization with [ATTORNEY REVIEW]
4. Includes appropriate disclaimers

Begin with a clear disclaimer that this is a draft requiring attorney review.
"""

        try:
            contract = self._think(
                prompt=prompt,
                task_type="legal_review",
                temperature=0.3,
                max_tokens=2500
            )

            # Add disclaimer
            contract = f"# {contract_type.replace('_', ' ').title()} - DRAFT\n\n" + \
                      f"> ⚠️ DRAFT - Requires attorney review before use\n\n" + \
                      contract + self.LEGAL_DISCLAIMER

            return {
                "message": f"{contract_type} draft generated",
                "contract": contract,
                "attorney_review_required": True,
                "note": "DO NOT USE without attorney review"
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # CLO.RISK - Legal risk assessment
    # =========================================================================

    def clo_risk(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Legal risk assessment.
        """
        business_plan = self._load_business_plan()
        high_risk = self._detect_high_risk_domains(business_plan or "")

        prompt = f"""As a digital paralegal, assess legal risks for this business.

Business Context:
{business_plan[:2000] if business_plan else "General business"}

High-Risk Domains:
{json.dumps(high_risk, indent=2)}

Create a risk assessment covering:
1. Regulatory risks
2. Contractual risks
3. IP risks
4. Employment risks
5. Data/privacy risks

For each risk, include likelihood, impact, and mitigation strategies.
Include disclaimer that this requires attorney review.
"""

        try:
            assessment = self._think(
                prompt=prompt,
                task_type="legal_review",
                temperature=0.3,
                max_tokens=2000
            )

            self.memory_path.mkdir(parents=True, exist_ok=True)
            risk_path = self.memory_path / "risk-assessment.md"
            with open(risk_path, 'w') as f:
                f.write(assessment + self.LEGAL_DISCLAIMER)

            return {
                "message": "Risk assessment created",
                "assessment": assessment,
                "high_risk_domains": high_risk,
                "saved_to": str(risk_path),
                "attorney_review_required": True
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # CLO.RESEARCH - Legal research
    # =========================================================================

    def clo_research(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Legal research assistance.
        """
        topic = payload.get("topic", "")

        if not topic:
            return {"error": "Research topic required"}

        prompt = f"""As a digital paralegal, provide preliminary research on: {topic}

Include:
1. Overview of the legal area
2. Key regulations or laws that may apply
3. General considerations
4. Suggestions for attorney consultation

This is for informational purposes only - not legal advice.
"""

        try:
            research = self._think(
                prompt=prompt,
                task_type="legal_review",
                temperature=0.4,
                max_tokens=1500
            )

            return {
                "message": "Research summary",
                "topic": topic,
                "research": research,
                "disclaimer": "This is informational only, not legal advice. Consult an attorney."
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # CLO.JURISDICTION - Jurisdiction analysis
    # =========================================================================

    def clo_jurisdiction(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Jurisdiction analysis for business operations.
        """
        business_plan = self._load_business_plan()

        return {
            "message": "Jurisdiction considerations",
            "primary_considerations": [
                "State of incorporation (affects corporate law)",
                "Location of operations (affects employment law)",
                "Customer locations (affects consumer protection, privacy)",
                "International operations (affects GDPR, etc.)"
            ],
            "common_choices": {
                "delaware": "Popular for C-Corps due to business-friendly laws",
                "wyoming": "Popular for LLCs due to privacy and low fees",
                "home_state": "Simplest for small businesses"
            },
            "note": "Consult with attorney and accountant for jurisdiction decisions",
            "attorney_review_required": True
        }


# Cloud Function Entry Point
def entry_point(request):
    request_json = request.get_json(silent=True)
    if not request_json:
        return {"error": "JSON body required"}, 400

    command = request_json.get("command")
    payload = request_json.get("payload", {})
    factory_id = request_json.get("factory_id")

    if not command:
        return {"error": "Command required"}, 400

    agent = CLOAgent(factory_id=factory_id)
    result = agent.run(command, payload)
    return result


if __name__ == "__main__":
    import sys
    agent = CLOAgent()

    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [payload_json]")
        print("Commands: clo.compliance, clo.contract, clo.risk, clo.research, clo.jurisdiction")
        sys.exit(1)

    command = sys.argv[1]
    payload = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    result = agent.run(command, payload)
    print(json.dumps(result, indent=2))

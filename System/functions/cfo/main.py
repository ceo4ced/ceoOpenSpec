"""
CFO Agent - Chief Financial Officer
Handles financial planning, budget management, token tracking, and analysis.

Commands:
    cfo.budget    - Create budget projections
    cfo.tokens    - Track token/API usage and costs
    cfo.payments  - Manage payments and invoicing
    cfo.forecast  - Generate financial forecasts
    cfo.compliance - Financial compliance checks
    cfo.analyze   - Financial performance analysis
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'packages'))
from factory_core.agent import BaseAgent


class CFOAgent(BaseAgent):
    """
    CFO Agent - Chief Financial Officer of the AI business.

    Responsibilities:
    - Financial projections and budgeting
    - Token/API cost tracking
    - Cash flow management
    - Financial analysis and reporting
    - Compliance with financial regulations
    """

    def __init__(self, factory_id: Optional[str] = None):
        super().__init__("CFO", "Chief Financial Officer", factory_id)
        self.memory_path = self._get_memory_path()
        self.logs_path = self._get_logs_path()

    def _get_memory_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "CFO" / ".cfo" / "memory"

    def _get_logs_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "CFO" / "logs"

    def _get_project_root(self) -> Path:
        return Path(__file__).parent.parent.parent.parent

    def _load_ceo_brief(self) -> Optional[str]:
        """Load the CEO brief for this position."""
        brief_path = self.memory_path / "ceo-brief.md"
        if brief_path.exists():
            with open(brief_path, 'r') as f:
                return f.read()
        return None

    def _load_business_plan(self) -> Optional[str]:
        """Load the business plan from root README."""
        readme_path = self._get_project_root() / "README.md"
        if readme_path.exists():
            with open(readme_path, 'r') as f:
                return f.read()
        return None

    def _log_session(self, log_type: str, data: Dict[str, Any]) -> bool:
        """Log a session to the logs directory."""
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

    # =========================================================================
    # CFO.BUDGET - Create budget projections
    # =========================================================================

    def cfo_budget(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create comprehensive budget projections.
        """
        business_plan = self._load_business_plan()
        ceo_brief = self._load_ceo_brief()

        if not business_plan:
            return {
                "error": "Business plan not found",
                "message": "CEO must create business plan first via /ceo.plan"
            }

        prompt = f"""Based on this business plan and CEO brief, create comprehensive financial projections.

## Business Plan
{business_plan[:3000]}

## CEO Brief
{ceo_brief[:1500] if ceo_brief else "No brief available"}

Generate a detailed budget in this format:

# Financial Projections - [BUSINESS_NAME]

**Generated**: {datetime.utcnow().isoformat()}Z
**Prepared By**: CFO Agent
**Status**: DRAFT - REQUIRES HUMAN REVIEW

> This financial projection is for planning purposes only and does not constitute financial, tax, or investment advice.

## Executive Summary
[Brief overview of financial outlook]

## Key Assumptions
| Assumption | Value | Source |
|------------|-------|--------|
| Market growth rate | X% | Industry data |
| Customer acquisition cost | $X | Estimate |
| Average revenue per user | $X | Business model |
| Churn rate | X% | Industry benchmark |

## Revenue Projections

### Year 1 Quarterly
| Quarter | Customers | Revenue | Notes |
|---------|-----------|---------|-------|
| Q1 | X | $X | Launch |
| Q2 | X | $X | Growth |
| Q3 | X | $X | Scale |
| Q4 | X | $X | Maturity |

## Cost Projections

### Fixed Costs (Monthly)
| Category | Amount | Notes |
|----------|--------|-------|
| Infrastructure | $X | Hosting, tools |
| Software/SaaS | $X | Services |
| AI/API Costs | $X | LLM tokens |

### Variable Costs
| Category | Per Unit | Notes |
|----------|----------|-------|
| Customer acquisition | $X | CAC |
| Operations | $X | Per transaction |

## Key Metrics Targets
| Metric | Target | Timeframe |
|--------|--------|-----------|
| MRR | $X | Month 12 |
| CAC | $X | Ongoing |
| LTV:CAC | X:1 | Target |
| Runway | X months | Current |

## CFO Recommendations
1. [Recommendation]
2. [Recommendation]

---
*Consult with a CPA or financial advisor before making decisions.*
"""

        try:
            budget = self._think(
                prompt=prompt,
                task_type="critical_decision",
                temperature=0.4,
                max_tokens=3000
            )

            # Save budget
            self.memory_path.mkdir(parents=True, exist_ok=True)
            version = datetime.utcnow().strftime("%Y%m%d")
            budget_path = self.memory_path / f"budget-v{version}.md"
            with open(budget_path, 'w') as f:
                f.write(budget)

            self._log_session("budget", {"version": version})

            return {
                "message": "Budget projections generated",
                "budget": budget,
                "saved_to": str(budget_path),
                "next_step": "Review projections and adjust assumptions as needed"
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # CFO.TOKENS - Track API/token usage
    # =========================================================================

    def cfo_tokens(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Track and report on token/API usage and costs.
        """
        action = payload.get("action", "report")
        period = payload.get("period", "today")

        # In production, this would query BigQuery for actual usage
        # For now, return a template report

        report = f"""# Token Usage Report

**Period**: {period}
**Generated**: {datetime.utcnow().isoformat()}Z

## Usage Summary

| Agent | Tokens Used | Cost ($) | % of Budget |
|-------|-------------|----------|-------------|
| CEO | 0 | $0.00 | 0% |
| CFO | 0 | $0.00 | 0% |
| CMO | 0 | $0.00 | 0% |
| COO | 0 | $0.00 | 0% |
| CIO | 0 | $0.00 | 0% |
| CLO | 0 | $0.00 | 0% |
| CPO | 0 | $0.00 | 0% |
| CTO | 0 | $0.00 | 0% |
| CXA | 0 | $0.00 | 0% |
| **Total** | **0** | **$0.00** | **0%** |

## Budget Status

- Daily Budget: $X
- Spent Today: $0.00
- Remaining: $X
- Status: 🟢 Under Budget

## Recommendations

1. Token usage is within normal parameters
2. No cost optimization needed at this time

---
*Note: Actual usage data requires BigQuery integration*
"""

        return {
            "message": "Token usage report generated",
            "report": report,
            "period": period
        }

    # =========================================================================
    # CFO.PAYMENTS - Manage payments
    # =========================================================================

    def cfo_payments(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Manage payments and invoicing.
        """
        action = payload.get("action", "status")

        if action == "status":
            return {
                "message": "Payment system status",
                "stripe_connected": False,
                "pending_invoices": 0,
                "pending_payouts": 0,
                "note": "Payment integration requires Stripe setup during onboarding"
            }

        return {"message": f"Payment action '{action}' not implemented"}

    # =========================================================================
    # CFO.FORECAST - Generate forecasts
    # =========================================================================

    def cfo_forecast(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate financial forecasts.
        """
        horizon = payload.get("horizon", "12_months")
        business_plan = self._load_business_plan()

        prompt = f"""Based on this business plan, create a {horizon} financial forecast.

{business_plan[:2500] if business_plan else "No business plan available"}

Generate a forecast including:
1. Revenue projections by month
2. Cost projections by category
3. Cash flow analysis
4. Key milestone targets
5. Risk scenarios (optimistic/pessimistic)

Format as a professional financial forecast document.
"""

        try:
            forecast = self._think(
                prompt=prompt,
                task_type="critical_decision",
                temperature=0.4,
                max_tokens=2500
            )

            self.memory_path.mkdir(parents=True, exist_ok=True)
            forecast_path = self.memory_path / "forecast.md"
            with open(forecast_path, 'w') as f:
                f.write(forecast)

            return {
                "message": f"{horizon} forecast generated",
                "forecast": forecast,
                "saved_to": str(forecast_path)
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # CFO.COMPLIANCE - Financial compliance
    # =========================================================================

    def cfo_compliance(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check financial compliance requirements.
        """
        return {
            "message": "Financial compliance check",
            "requirements": [
                {"item": "EIN Registration", "status": "pending", "priority": "high"},
                {"item": "Business Bank Account", "status": "pending", "priority": "high"},
                {"item": "Accounting System", "status": "pending", "priority": "medium"},
                {"item": "Tax Registration", "status": "pending", "priority": "high"},
            ],
            "note": "Consult with a CPA for complete compliance requirements"
        }

    # =========================================================================
    # CFO.ANALYZE - Financial analysis
    # =========================================================================

    def cfo_analyze(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform financial analysis.
        """
        period = payload.get("period", "current")

        # Load any existing financial data
        budget_files = list(self.memory_path.glob("budget-*.md")) if self.memory_path.exists() else []
        forecast_path = self.memory_path / "forecast.md" if self.memory_path.exists() else None

        budget_content = ""
        if budget_files:
            with open(sorted(budget_files)[-1], 'r') as f:
                budget_content = f.read()[:1500]

        prompt = f"""Perform a financial health analysis based on available data.

## Available Budget Data
{budget_content if budget_content else "No budget data available yet"}

Generate a financial analysis report including:
1. Overall Health Assessment (GREEN/YELLOW/RED)
2. Key Financial Metrics
3. Variance Analysis (if actuals available)
4. Recommendations
5. Escalation items (if any)

Format as a professional analysis document.
"""

        try:
            analysis = self._think(
                prompt=prompt,
                task_type="critical_decision",
                temperature=0.4,
                max_tokens=2000
            )

            self._log_session("analysis", {"period": period})

            return {
                "message": "Financial analysis complete",
                "analysis": analysis,
                "period": period
            }

        except Exception as e:
            return {"error": str(e)}


# Cloud Function Entry Point
def entry_point(request):
    """HTTP Cloud Function entry point."""
    request_json = request.get_json(silent=True)

    if not request_json:
        return {"error": "JSON body required"}, 400

    command = request_json.get("command")
    payload = request_json.get("payload", {})
    factory_id = request_json.get("factory_id")

    if not command:
        return {"error": "Command required"}, 400

    agent = CFOAgent(factory_id=factory_id)
    result = agent.run(command, payload)

    return result


if __name__ == "__main__":
    import sys
    agent = CFOAgent()

    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [payload_json]")
        print("Commands: cfo.budget, cfo.tokens, cfo.payments, cfo.forecast, cfo.compliance, cfo.analyze")
        sys.exit(1)

    command = sys.argv[1]
    payload = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    result = agent.run(command, payload)
    print(json.dumps(result, indent=2))

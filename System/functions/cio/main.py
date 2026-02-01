"""
CIO Agent - Chief Information Officer
Handles data governance, security, infrastructure, and privacy.

Commands:
    cio.security      - Security framework and policies
    cio.data          - Data governance
    cio.infrastructure - Infrastructure planning
    cio.privacy       - Privacy assessment
    cio.mcp           - MCP (Model Context Protocol) configuration
    cio.redundancy    - Backup and redundancy planning
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'packages'))
from factory_core.agent import BaseAgent


class CIOAgent(BaseAgent):
    """
    CIO Agent - Chief Information Officer of the AI business.

    Responsibilities:
    - Data governance and management
    - Security framework
    - Infrastructure planning
    - Privacy compliance
    - System architecture
    """

    def __init__(self, factory_id: Optional[str] = None):
        super().__init__("CIO", "Chief Information Officer", factory_id)
        self.memory_path = self._get_memory_path()
        self.logs_path = self._get_logs_path()

    def _get_memory_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "CIO" / ".cio" / "memory"

    def _get_logs_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "CIO" / "logs"

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

    # =========================================================================
    # CIO.SECURITY - Security framework
    # =========================================================================

    def cio_security(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create security framework and policies.
        """
        business_plan = self._load_business_plan()
        ceo_brief = self._load_ceo_brief()

        prompt = f"""Based on this business plan, create a security framework.

## Business Plan
{business_plan[:2500] if business_plan else "No plan available"}

## CEO Brief
{ceo_brief[:1000] if ceo_brief else "No brief available"}

Generate a security framework including:

# Security Framework - [BUSINESS_NAME]

**Generated**: {datetime.utcnow().isoformat()}Z
**Risk Level**: [Low/Medium/High]

> This framework requires review by security professionals.

## Asset Inventory
| Asset Type | Examples | Sensitivity | Owner |
|------------|----------|-------------|-------|
| Customer Data | PII, emails | HIGH | CIO |
| Business Data | Financials | HIGH | CFO |
| Credentials | API keys | CRITICAL | CIO |

## Access Control
| Requirement | Implementation | Status |
|-------------|----------------|--------|
| Unique accounts | No shared accounts | [ ] |
| MFA required | All systems | [ ] |
| Password policy | 12+ chars | [ ] |

## Data Protection
| Data State | Encryption | Standard |
|------------|------------|----------|
| At rest | Required | AES-256 |
| In transit | Required | TLS 1.3 |
| Backups | Required | AES-256 |

## Incident Response
| Severity | Response Time | Notify |
|----------|---------------|--------|
| Critical | Immediate | CEO + Human |
| High | 4 hours | CEO |
| Medium | 24 hours | Log |

## Compliance Mapping
- [ ] GDPR (if EU customers)
- [ ] CCPA (if CA customers)
- [ ] SOC 2 (if enterprise)
- [ ] HIPAA (if healthcare)

---
*Security frameworks require professional review.*
"""

        try:
            framework = self._think(
                prompt=prompt,
                task_type="critical_decision",
                temperature=0.4,
                max_tokens=2500
            )

            self.memory_path.mkdir(parents=True, exist_ok=True)
            security_path = self.memory_path / "security-framework.md"
            with open(security_path, 'w') as f:
                f.write(framework)

            self._log_session("security", {"generated": True})

            return {
                "message": "Security framework created",
                "framework": framework,
                "saved_to": str(security_path),
                "note": "Review with security professional before implementation"
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # CIO.DATA - Data governance
    # =========================================================================

    def cio_data(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create data governance framework.
        """
        business_plan = self._load_business_plan()

        prompt = f"""Create a data governance framework for this business.

{business_plan[:2000] if business_plan else "No plan available"}

Include:
1. Data classification policy
2. Data retention policies
3. Data access controls
4. Data quality requirements
5. Compliance considerations
"""

        try:
            governance = self._think(
                prompt=prompt,
                task_type="critical_decision",
                temperature=0.4,
                max_tokens=2000
            )

            self.memory_path.mkdir(parents=True, exist_ok=True)
            data_path = self.memory_path / "data-governance.md"
            with open(data_path, 'w') as f:
                f.write(governance)

            return {
                "message": "Data governance framework created",
                "governance": governance,
                "saved_to": str(data_path)
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # CIO.INFRASTRUCTURE - Infrastructure planning
    # =========================================================================

    def cio_infrastructure(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Infrastructure planning and architecture.
        """
        return {
            "message": "Infrastructure architecture",
            "stack": {
                "cloud": "Google Cloud Platform (GCP)",
                "compute": "Cloud Functions (serverless)",
                "database": "BigQuery (analytics), Firestore (operational)",
                "storage": "Cloud Storage",
                "secrets": "Secret Manager",
                "monitoring": "Cloud Monitoring + Logging"
            },
            "ai_providers": {
                "primary": "OpenRouter (multi-model access)",
                "fallback": "OpenAI direct",
                "image": "DALL-E 3"
            },
            "messaging": {
                "internal": "Pub/Sub",
                "external": "Telegram, Twilio"
            }
        }

    # =========================================================================
    # CIO.PRIVACY - Privacy assessment
    # =========================================================================

    def cio_privacy(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Privacy impact assessment.
        """
        business_plan = self._load_business_plan()

        # Check for high-risk domains
        high_risk = []
        if business_plan:
            bp_lower = business_plan.lower()
            if any(kw in bp_lower for kw in ["children", "kids", "minors"]):
                high_risk.append({"domain": "Minors", "regulation": "COPPA"})
            if any(kw in bp_lower for kw in ["health", "medical"]):
                high_risk.append({"domain": "Healthcare", "regulation": "HIPAA"})
            if any(kw in bp_lower for kw in ["eu", "europe", "european"]):
                high_risk.append({"domain": "EU", "regulation": "GDPR"})

        return {
            "message": "Privacy assessment",
            "data_collected": [
                {"type": "Email addresses", "purpose": "Account management", "retention": "Active + 1 year"},
                {"type": "Usage data", "purpose": "Analytics", "retention": "2 years"},
                {"type": "Payment info", "purpose": "Billing (via Stripe)", "retention": "Per Stripe policy"}
            ],
            "high_risk_domains": high_risk if high_risk else "None identified",
            "required_documents": [
                "Privacy Policy",
                "Terms of Service",
                "Cookie Policy (if applicable)"
            ],
            "note": "CLO should review privacy policy requirements"
        }

    # =========================================================================
    # CIO.MCP - MCP configuration
    # =========================================================================

    def cio_mcp(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Model Context Protocol configuration.
        """
        return {
            "message": "MCP (Model Context Protocol) configuration",
            "status": "Framework ready",
            "servers": [
                {"name": "filesystem", "purpose": "File access for agents"},
                {"name": "memory", "purpose": "Persistent agent memory"},
                {"name": "fetch", "purpose": "Web data access"}
            ],
            "note": "MCP enables agents to access external tools and data"
        }

    # =========================================================================
    # CIO.REDUNDANCY - Backup and redundancy
    # =========================================================================

    def cio_redundancy(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Backup and redundancy planning.
        """
        return {
            "message": "Backup and redundancy plan",
            "backups": {
                "database": {"frequency": "Daily", "retention": "30 days", "location": "GCS multi-region"},
                "files": {"frequency": "Daily", "retention": "30 days", "location": "GCS multi-region"},
                "config": {"frequency": "On change", "retention": "90 days", "location": "Git + GCS"}
            },
            "redundancy": {
                "compute": "Cloud Functions auto-scale across zones",
                "database": "BigQuery multi-region replication",
                "ai_providers": "OpenRouter primary + OpenAI fallback"
            },
            "disaster_recovery": {
                "rto": "4 hours",
                "rpo": "24 hours",
                "procedure": "Documented in CIO/.cio/memory/dr-plan.md"
            }
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

    agent = CIOAgent(factory_id=factory_id)
    result = agent.run(command, payload)
    return result


if __name__ == "__main__":
    import sys
    agent = CIOAgent()

    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [payload_json]")
        print("Commands: cio.security, cio.data, cio.infrastructure, cio.privacy, cio.mcp, cio.redundancy")
        sys.exit(1)

    command = sys.argv[1]
    payload = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    result = agent.run(command, payload)
    print(json.dumps(result, indent=2))

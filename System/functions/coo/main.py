"""
COO Agent - Chief Operating Officer
Handles operations, processes, workforce planning, quality, and logistics.

Commands:
    coo.process   - Design operational processes
    coo.workforce - Workforce planning
    coo.logistics - Logistics and supply chain
    coo.quality   - Quality management
    coo.callcenter - Call center operations (future)
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'packages'))
from factory_core.agent import BaseAgent


class COOAgent(BaseAgent):
    """
    COO Agent - Chief Operating Officer of the AI business.

    Responsibilities:
    - Operations design and optimization
    - Process documentation
    - Workforce planning and HR
    - Quality management
    - Vendor operations
    """

    def __init__(self, factory_id: Optional[str] = None):
        super().__init__("COO", "Chief Operating Officer", factory_id)
        self.memory_path = self._get_memory_path()
        self.logs_path = self._get_logs_path()

    def _get_memory_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "COO" / ".coo" / "memory"

    def _get_logs_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "COO" / "logs"

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
    # COO.PROCESS - Design operational processes
    # =========================================================================

    def coo_process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Design and document operational processes.
        """
        business_plan = self._load_business_plan()
        ceo_brief = self._load_ceo_brief()

        prompt = f"""Based on this business plan, design an operations framework.

## Business Plan
{business_plan[:2500] if business_plan else "No plan available"}

## CEO Brief
{ceo_brief[:1000] if ceo_brief else "No brief available"}

Generate an operations framework including:

# Operations Framework - [BUSINESS_NAME]

**Generated**: {datetime.utcnow().isoformat()}Z
**Status**: DRAFT

## Core Business Processes

### Process 1: Customer Onboarding
**Purpose**: Get customers from signup to first value
**Owner**: Operations

| Step | Action | Tools | Output |
|------|--------|-------|--------|
| 1 | [Action] | [Tool] | [Output] |

### Process 2: Service Delivery
**Purpose**: Deliver core value to customers

### Process 3: Customer Support
**Purpose**: Handle customer issues and questions

## Organizational Structure

### Phase 1 (Launch)
| Role | Type | Responsibilities |
|------|------|------------------|
| Founder | Human | Overall direction |
| C-Suite | AI Agents | Domain expertise |

## Vendor Operations
| Category | Vendor | Purpose | Monthly Cost |
|----------|--------|---------|--------------|
| Hosting | GCP | Infrastructure | $X |
| AI | OpenRouter | LLM APIs | $X |

## Quality Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Response time | < 24h | Ticket tracking |
| Customer satisfaction | > 4.5 | Surveys |

## Compliance Considerations
- Worker classification (consult CLO)
- Safety requirements
- Industry-specific regulations
"""

        try:
            framework = self._think(
                prompt=prompt,
                task_type="agent_reasoning",
                temperature=0.5,
                max_tokens=2500
            )

            self.memory_path.mkdir(parents=True, exist_ok=True)
            ops_path = self.memory_path / "operations-plan.md"
            with open(ops_path, 'w') as f:
                f.write(framework)

            self._log_session("process", {"generated": True})

            return {
                "message": "Operations framework created",
                "framework": framework,
                "saved_to": str(ops_path)
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # COO.WORKFORCE - Workforce planning
    # =========================================================================

    def coo_workforce(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create workforce plan.
        """
        business_plan = self._load_business_plan()

        prompt = f"""Based on this business plan, create a workforce plan.

{business_plan[:2000] if business_plan else "No plan available"}

Include:
1. Roles needed (human vs AI)
2. Hiring timeline
3. Worker classification considerations
4. Budget implications

Note: Worker classification requires legal review from CLO.
"""

        try:
            plan = self._think(
                prompt=prompt,
                task_type="agent_reasoning",
                temperature=0.5,
                max_tokens=1500
            )

            self.memory_path.mkdir(parents=True, exist_ok=True)
            workforce_path = self.memory_path / "workforce-plan.md"
            with open(workforce_path, 'w') as f:
                f.write(plan)

            return {
                "message": "Workforce plan created",
                "plan": plan,
                "saved_to": str(workforce_path),
                "note": "Worker classification requires CLO review"
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # COO.LOGISTICS - Logistics planning
    # =========================================================================

    def coo_logistics(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Logistics and supply chain planning.
        """
        return {
            "message": "Logistics planning",
            "note": "Most AI businesses are digital-first with minimal physical logistics",
            "digital_operations": {
                "hosting": "Cloud-based (GCP)",
                "content_delivery": "CDN for assets",
                "data_storage": "BigQuery for logs/analytics"
            }
        }

    # =========================================================================
    # COO.QUALITY - Quality management
    # =========================================================================

    def coo_quality(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Quality management framework.
        """
        return {
            "message": "Quality management framework",
            "kpis": [
                {"metric": "Customer Satisfaction", "target": "> 4.5/5", "measurement": "Surveys"},
                {"metric": "Response Time", "target": "< 24 hours", "measurement": "Ticket tracking"},
                {"metric": "First Contact Resolution", "target": "> 80%", "measurement": "Support metrics"},
                {"metric": "Service Uptime", "target": "> 99.5%", "measurement": "Monitoring"}
            ],
            "processes": [
                "Regular quality audits",
                "Customer feedback collection",
                "Continuous improvement cycles"
            ]
        }

    # =========================================================================
    # COO.CALLCENTER - Call center operations
    # =========================================================================

    def coo_callcenter(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call center operations (future capability).
        """
        return {
            "message": "Call center operations",
            "status": "Not yet implemented",
            "note": "CXA agent handles phone communications via Twilio integration"
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

    agent = COOAgent(factory_id=factory_id)
    result = agent.run(command, payload)
    return result


if __name__ == "__main__":
    import sys
    agent = COOAgent()

    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [payload_json]")
        print("Commands: coo.process, coo.workforce, coo.logistics, coo.quality, coo.callcenter")
        sys.exit(1)

    command = sys.argv[1]
    payload = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    result = agent.run(command, payload)
    print(json.dumps(result, indent=2))

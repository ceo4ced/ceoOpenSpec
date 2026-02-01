"""
CTO Agent - Chief Technology Officer
Handles technical implementation, architecture, and engineering.
GATED: CTO cannot begin until CMO validation passes + human approval.

Commands:
    cto.status    - Check gate status
    cto.plan      - Technical planning (uses SpecKit methodology)
    cto.implement - Implementation guidance
    cto.backups   - Backup management
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'packages'))
from factory_core.agent import BaseAgent


class CTOAgent(BaseAgent):
    """
    CTO Agent - Chief Technology Officer of the AI business.

    IMPORTANT: CTO is GATED - cannot begin work until:
    1. CMO validation passes (PROCEED decision)
    2. Human founder approves CTO activation

    Responsibilities:
    - Technical architecture
    - Implementation planning (SpecKit methodology)
    - Code review and quality
    - System reliability
    """

    def __init__(self, factory_id: Optional[str] = None):
        super().__init__("CTO", "Chief Technology Officer", factory_id)
        self.memory_path = self._get_memory_path()
        self.logs_path = self._get_logs_path()

    def _get_memory_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "CTO" / ".cto" / "memory"

    def _get_logs_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "CTO" / "logs"

    def _get_project_root(self) -> Path:
        return Path(__file__).parent.parent.parent.parent

    def _check_gate_status(self) -> Dict[str, Any]:
        """Check if CTO gate is open (CMO validated + human approved)."""
        cmo_memory = self._get_project_root() / "C-Suites" / "CMO" / ".cmo" / "memory"

        # Check for CMO validation results
        validation_files = list(cmo_memory.glob("validation-results-*.md")) if cmo_memory.exists() else []
        cmo_validated = False
        cmo_decision = "UNKNOWN"

        if validation_files:
            latest = sorted(validation_files)[-1]
            with open(latest, 'r') as f:
                content = f.read()
                if "PROCEED" in content:
                    cmo_validated = True
                    cmo_decision = "PROCEED"
                elif "ITERATE" in content:
                    cmo_decision = "ITERATE"
                elif "PIVOT" in content:
                    cmo_decision = "PIVOT"

        # Check for human approval
        approval_path = self.memory_path / "human-approval.md"
        human_approved = approval_path.exists()

        gate_open = cmo_validated and human_approved

        return {
            "gate_open": gate_open,
            "cmo_validated": cmo_validated,
            "cmo_decision": cmo_decision,
            "human_approved": human_approved,
            "can_proceed": gate_open
        }

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
    # CTO.STATUS - Check gate status
    # =========================================================================

    def cto_status(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check CTO gate status and readiness to proceed.
        """
        gate = self._check_gate_status()

        status_message = ""
        if gate["gate_open"]:
            status_message = "🟢 CTO ACTIVATED - Ready to begin technical implementation"
        elif gate["cmo_validated"] and not gate["human_approved"]:
            status_message = "🟡 CMO validation passed - Awaiting human approval"
        elif not gate["cmo_validated"]:
            status_message = f"🔒 GATED - CMO validation required (current: {gate['cmo_decision']})"

        return {
            "message": status_message,
            "gate_status": gate,
            "requirements": {
                "cmo_validation": {"required": True, "met": gate["cmo_validated"]},
                "human_approval": {"required": True, "met": gate["human_approved"]}
            },
            "next_step": "Run /cmo.validate then /cmo.approve" if not gate["gate_open"] else "Ready for /cto.plan"
        }

    # =========================================================================
    # CTO.PLAN - Technical planning
    # =========================================================================

    def cto_plan(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create technical implementation plan using SpecKit methodology.
        """
        gate = self._check_gate_status()

        if not gate["gate_open"]:
            return {
                "error": "CTO is GATED",
                "message": "Cannot begin technical planning until CMO validation passes and human approves",
                "gate_status": gate
            }

        business_plan = self._load_business_plan()
        ceo_brief = self._load_ceo_brief()

        # Load PRD if available
        cpo_memory = self._get_project_root() / "C-Suites" / "CPO" / ".cpo" / "memory"
        prd_content = ""
        if cpo_memory.exists():
            prd_files = list(cpo_memory.glob("PRD-*.md"))
            if prd_files:
                with open(sorted(prd_files)[-1], 'r') as f:
                    prd_content = f.read()[:1500]

        prompt = f"""Create a technical implementation plan using the SpecKit methodology.

## Business Plan
{business_plan[:2000] if business_plan else "No plan available"}

## CEO Brief
{ceo_brief[:1000] if ceo_brief else "No brief available"}

## PRD (if available)
{prd_content if prd_content else "No PRD available - create general plan"}

Generate a technical plan including:

# Technical Implementation Plan

**Generated**: {datetime.utcnow().isoformat()}Z
**Methodology**: SpecKit

## Architecture Overview

### System Components
| Component | Technology | Purpose |
|-----------|------------|---------|
| Frontend | [Tech] | User interface |
| Backend | [Tech] | API and business logic |
| Database | [Tech] | Data storage |
| AI/ML | [Tech] | Intelligence layer |

### Architecture Diagram
```
[User] → [Frontend] → [API] → [Services] → [Database]
                                   ↓
                              [AI/LLM APIs]
```

## Technology Stack
- **Frontend**: [Recommendation]
- **Backend**: [Recommendation]
- **Database**: [Recommendation]
- **Hosting**: GCP (Cloud Functions, BigQuery)
- **AI**: OpenRouter (primary), OpenAI (fallback)

## Implementation Phases

### Phase 1: Foundation
| Task | Priority | Effort |
|------|----------|--------|
| [Task] | P0 | [Est] |

### Phase 2: Core Features
| Task | Priority | Effort |
|------|----------|--------|
| [Task] | P0 | [Est] |

### Phase 3: Polish & Launch
| Task | Priority | Effort |
|------|----------|--------|
| [Task] | P1 | [Est] |

## Technical Risks
| Risk | Likelihood | Mitigation |
|------|------------|------------|
| [Risk] | H/M/L | [Mitigation] |

## Quality Requirements
- Test coverage: > 80%
- Response time: < 500ms
- Uptime: > 99.5%

## Dependencies
| Dependency | Status | Notes |
|------------|--------|-------|
| [Dep] | [Status] | [Notes] |
"""

        try:
            plan = self._think(
                prompt=prompt,
                task_type="code_generation",
                temperature=0.4,
                max_tokens=3000
            )

            self.memory_path.mkdir(parents=True, exist_ok=True)
            plan_path = self.memory_path / "technical-plan.md"
            with open(plan_path, 'w') as f:
                f.write(plan)

            self._log_session("plan", {"generated": True})

            return {
                "message": "Technical plan created",
                "plan": plan,
                "saved_to": str(plan_path),
                "next_step": "Begin implementation with /cto.implement"
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # CTO.IMPLEMENT - Implementation guidance
    # =========================================================================

    def cto_implement(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide implementation guidance for a specific component.
        """
        gate = self._check_gate_status()

        if not gate["gate_open"]:
            return {
                "error": "CTO is GATED",
                "gate_status": gate
            }

        component = payload.get("component", "")
        task = payload.get("task", "")

        if not component and not task:
            # Return general implementation status
            return {
                "message": "Implementation status",
                "gate_status": gate,
                "available_commands": [
                    "/cto.implement --component=frontend",
                    "/cto.implement --component=backend",
                    "/cto.implement --component=database",
                    "/cto.implement --task='specific task'"
                ]
            }

        prompt = f"""Provide implementation guidance for:
Component: {component if component else "General"}
Task: {task if task else "Overview"}

Include:
1. Recommended approach
2. Key files/components to create
3. Code patterns to follow
4. Testing requirements
5. Potential pitfalls
"""

        try:
            guidance = self._think(
                prompt=prompt,
                task_type="code_generation",
                temperature=0.4,
                max_tokens=1500
            )

            return {
                "message": "Implementation guidance",
                "component": component,
                "task": task,
                "guidance": guidance
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # CTO.BACKUPS - Backup management
    # =========================================================================

    def cto_backups(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Backup management and status.
        """
        action = payload.get("action", "status")

        if action == "status":
            return {
                "message": "Backup status",
                "status": {
                    "code": {"location": "Git (GitHub)", "frequency": "On commit", "status": "active"},
                    "config": {"location": "Git + Secret Manager", "frequency": "On change", "status": "active"},
                    "data": {"location": "GCS multi-region", "frequency": "Daily", "status": "configured"},
                    "logs": {"location": "BigQuery", "frequency": "Real-time", "status": "active"}
                },
                "note": "Data backups require production environment"
            }

        return {"message": f"Backup action '{action}' received"}


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

    agent = CTOAgent(factory_id=factory_id)
    result = agent.run(command, payload)
    return result


if __name__ == "__main__":
    import sys
    agent = CTOAgent()

    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [payload_json]")
        print("Commands: cto.status, cto.plan, cto.implement, cto.backups")
        sys.exit(1)

    command = sys.argv[1]
    payload = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    result = agent.run(command, payload)
    print(json.dumps(result, indent=2))

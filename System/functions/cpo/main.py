"""
CPO Agent - Chief Product Officer
Handles product strategy, roadmap, PRDs, metrics, and decisions.

Commands:
    cpo.prd       - Create Product Requirements Document
    cpo.roadmap   - Product roadmap planning
    cpo.metrics   - Product metrics and KPIs
    cpo.onepager  - Create feature one-pager
    cpo.decide    - Product decision framework
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'packages'))
from factory_core.agent import BaseAgent


class CPOAgent(BaseAgent):
    """
    CPO Agent - Chief Product Officer of the AI business.

    Responsibilities:
    - Product strategy and vision
    - Feature prioritization
    - PRD creation
    - Roadmap management
    - Product metrics
    """

    def __init__(self, factory_id: Optional[str] = None):
        super().__init__("CPO", "Chief Product Officer", factory_id)
        self.memory_path = self._get_memory_path()
        self.logs_path = self._get_logs_path()

    def _get_memory_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "CPO" / ".cpo" / "memory"

    def _get_logs_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "CPO" / "logs"

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
    # CPO.PRD - Product Requirements Document
    # =========================================================================

    def cpo_prd(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a Product Requirements Document.
        """
        feature_name = payload.get("feature", "Core Product")
        business_plan = self._load_business_plan()

        prompt = f"""Create a Product Requirements Document for: {feature_name}

Business Context:
{business_plan[:2000] if business_plan else "No plan available"}

Generate a PRD in this format:

# PRD: {feature_name}

| Field | Value |
|-------|-------|
| PRD ID | PRD-{datetime.utcnow().strftime("%Y%m%d")}-001 |
| Version | 1.0 |
| Author | CPO |
| Status | Draft |

## Problem Statement

### Current State
[How things work today]

### Problem
[What problem are we solving?]

### Users Affected
[Who experiences this problem?]

## Goals

### Primary Goal
[Main outcome we want]

### Non-Goals
[What we're NOT doing]

## Success Metrics

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| [Metric] | [X] | [Y] | [How measured] |

## User Stories

**As a** [user type]
**I want to** [action]
**So that** [outcome]

Acceptance Criteria:
- [ ] [Criterion]

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | [Requirement] | P0 |

## Non-Functional Requirements

| ID | Category | Requirement |
|----|----------|-------------|
| NFR-001 | Performance | [Requirement] |

## Technical Considerations
[Architecture notes for CTO]

## Dependencies & Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | H/M/L | H/M/L | [Plan] |

## Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Design | [X] | Mockups approved |
| Development | [X] | Feature complete |
| Testing | [X] | QA passed |

---
*PRDs are contracts between Product, Engineering, and Design.*
"""

        try:
            prd = self._think(
                prompt=prompt,
                task_type="critical_decision",
                temperature=0.5,
                max_tokens=3000
            )

            self.memory_path.mkdir(parents=True, exist_ok=True)
            prd_id = f"PRD-{datetime.utcnow().strftime('%Y%m%d')}-001"
            prd_path = self.memory_path / f"{prd_id}.md"
            with open(prd_path, 'w') as f:
                f.write(prd)

            self._log_session("prd", {"prd_id": prd_id, "feature": feature_name})

            return {
                "message": "PRD created",
                "prd_id": prd_id,
                "prd": prd,
                "saved_to": str(prd_path),
                "next_step": "Review with CTO for technical feasibility"
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # CPO.ROADMAP - Product roadmap
    # =========================================================================

    def cpo_roadmap(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create or update product roadmap.
        """
        business_plan = self._load_business_plan()
        horizon = payload.get("horizon", "6_months")

        prompt = f"""Create a {horizon} product roadmap based on this business plan.

{business_plan[:2000] if business_plan else "No plan available"}

Generate a roadmap including:

# Product Roadmap

**Generated**: {datetime.utcnow().isoformat()}Z
**Horizon**: {horizon}

## Vision
[Where we're heading]

## Now (This Month)
| Feature | Status | Owner |
|---------|--------|-------|
| [Feature] | In Progress | CTO |

## Next (Next Month)
| Feature | Priority | Dependencies |
|---------|----------|--------------|
| [Feature] | P0 | [Deps] |

## Later (This Quarter)
| Feature | Priority | Notes |
|---------|----------|-------|
| [Feature] | P1 | [Notes] |

## Themes
- Theme 1: [Description]
- Theme 2: [Description]

## Dependencies
| Dependency | Owner | Status |
|------------|-------|--------|
| [Dep] | [Owner] | [Status] |

## Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [Impact] | [Mitigation] |
"""

        try:
            roadmap = self._think(
                prompt=prompt,
                task_type="agent_reasoning",
                temperature=0.5,
                max_tokens=2000
            )

            self.memory_path.mkdir(parents=True, exist_ok=True)
            roadmap_path = self.memory_path / "roadmap.md"
            with open(roadmap_path, 'w') as f:
                f.write(roadmap)

            return {
                "message": "Roadmap created",
                "roadmap": roadmap,
                "saved_to": str(roadmap_path)
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # CPO.METRICS - Product metrics
    # =========================================================================

    def cpo_metrics(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Define and track product metrics.
        """
        business_plan = self._load_business_plan()

        prompt = f"""Define product metrics framework for this business.

{business_plan[:1500] if business_plan else "No plan available"}

Include:
1. North Star Metric
2. Key Product Metrics (acquisition, activation, retention, revenue, referral)
3. Measurement methods
4. Target values
"""

        try:
            metrics = self._think(
                prompt=prompt,
                task_type="agent_reasoning",
                temperature=0.5,
                max_tokens=1500
            )

            return {
                "message": "Metrics framework defined",
                "metrics": metrics
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # CPO.ONEPAGER - Feature one-pager
    # =========================================================================

    def cpo_onepager(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create feature one-pager.
        """
        feature = payload.get("feature", "")

        if not feature:
            return {"error": "Feature name required"}

        prompt = f"""Create a one-pager for this feature: {feature}

A one-pager should be concise and answer:
1. What is the problem?
2. Who has this problem?
3. What's the proposed solution?
4. How do we measure success?
5. What's the effort estimate?

Keep it to one page / ~500 words.
"""

        try:
            onepager = self._think(
                prompt=prompt,
                task_type="agent_reasoning",
                temperature=0.6,
                max_tokens=1000
            )

            return {
                "message": "One-pager created",
                "feature": feature,
                "onepager": onepager,
                "next_step": "If approved, create full PRD with /cpo.prd"
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # CPO.DECIDE - Decision framework
    # =========================================================================

    def cpo_decide(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Product decision framework.
        """
        decision = payload.get("decision", "")
        options = payload.get("options", [])

        if not decision:
            return {"error": "Decision question required"}

        prompt = f"""Help make this product decision: {decision}

Options provided: {json.dumps(options) if options else "None - suggest options"}

Provide:
1. Framing of the decision
2. Key considerations
3. Options with pros/cons
4. Recommended approach
5. What data would help decide
"""

        try:
            analysis = self._think(
                prompt=prompt,
                task_type="critical_decision",
                temperature=0.5,
                max_tokens=1500
            )

            return {
                "message": "Decision analysis",
                "decision": decision,
                "analysis": analysis
            }

        except Exception as e:
            return {"error": str(e)}


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

    agent = CPOAgent(factory_id=factory_id)
    result = agent.run(command, payload)
    return result


if __name__ == "__main__":
    import sys
    agent = CPOAgent()

    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [payload_json]")
        print("Commands: cpo.prd, cpo.roadmap, cpo.metrics, cpo.onepager, cpo.decide")
        sys.exit(1)

    command = sys.argv[1]
    payload = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    result = agent.run(command, payload)
    print(json.dumps(result, indent=2))

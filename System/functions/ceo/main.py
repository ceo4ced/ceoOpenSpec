"""
CEO Agent - Chief Executive Officer
The primary interface with the founder and orchestrator of all C-Suite agents.

Commands:
    ceo.vision    - Gather business vision from the founder
    ceo.plan      - Generate business plan from vision
    ceo.propagate - Distribute plan to C-Suite agents
    ceo.onboard   - Guide founder through service onboarding
    ceo.inquire   - Handle questions from other agents
    ceo.report    - Generate status reports
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add packages to path so we can import factory_core
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'packages'))

from factory_core.agent import BaseAgent


class CEOAgent(BaseAgent):
    """
    CEO Agent - Chief Executive Officer of the AI business.

    The CEO:
    - Gathers vision from the founder
    - Creates the business plan
    - Orchestrates other C-Suite agents
    - Serves as the hub for inter-agent communication
    - Reports status to the founder
    """

    # Vision gathering questions
    VISION_QUESTIONS = [
        {
            "category": "Problem",
            "question": "What problem are you trying to solve?",
            "why": "Understanding the core problem helps us validate market need and shape the solution.",
            "examples": [
                "Small businesses struggle to manage their social media presence efficiently",
                "Parents can't find trustworthy after-school tutoring that fits their schedule"
            ]
        },
        {
            "category": "Audience",
            "question": "Who experiences this problem most acutely?",
            "why": "Identifying our ideal customer helps focus our marketing and product development.",
            "examples": [
                "Solo entrepreneurs running service businesses",
                "Working parents with children ages 8-14"
            ]
        },
        {
            "category": "Solution",
            "question": "How does your solution address this problem?",
            "why": "A clear solution description helps us communicate value and build the right product.",
            "examples": [
                "AI-powered social media scheduler with content suggestions",
                "On-demand tutoring app matching students with verified tutors"
            ]
        },
        {
            "category": "Differentiation",
            "question": "What makes your approach unique?",
            "why": "Differentiation is crucial for standing out in competitive markets.",
            "examples": [
                "We use AI to suggest content based on industry trends",
                "All tutors are background-checked teachers with verified credentials"
            ]
        },
        {
            "category": "Business Model",
            "question": "How will this business make money?",
            "why": "A clear revenue model is essential for financial planning and sustainability.",
            "examples": [
                "Monthly subscription of $29/mo for small business tier",
                "15% commission on each tutoring session booked"
            ]
        },
        {
            "category": "Scale",
            "question": "How big do you want this to become?",
            "why": "Understanding ambition helps us plan appropriate resources and timelines.",
            "examples": [
                "Lifestyle business serving 1,000 customers",
                "Venture-scale aiming for $10M ARR in 3 years"
            ]
        },
        {
            "category": "Timeline",
            "question": "What's your target launch timeline?",
            "why": "Timeline affects our development priorities and resource allocation.",
            "examples": [
                "MVP in 30 days, full launch in 90 days",
                "6 months to closed beta, 1 year to public launch"
            ]
        },
        {
            "category": "Budget",
            "question": "What resources do you have available?",
            "why": "Budget constraints shape our technology choices and go-to-market strategy.",
            "examples": [
                "$5,000 initial investment, bootstrapped thereafter",
                "$50,000 seed from savings, seeking $500K angel round"
            ]
        }
    ]

    # High-risk domains that require special consideration
    HIGH_RISK_DOMAINS = {
        "minors": {
            "keywords": ["children", "kids", "minors", "under 18", "youth", "teens", "students"],
            "regulations": ["COPPA", "CARU", "UK AADC"],
            "warning": "Targeting minors requires strict compliance with child protection laws."
        },
        "education": {
            "keywords": ["education", "school", "learning", "tutoring", "academic"],
            "regulations": ["FERPA"],
            "warning": "Educational data has special protection requirements."
        },
        "healthcare": {
            "keywords": ["health", "medical", "patient", "clinical", "therapy", "mental health"],
            "regulations": ["HIPAA", "HITECH"],
            "warning": "Healthcare data requires strict privacy and security controls."
        },
        "finance": {
            "keywords": ["financial", "banking", "payments", "crypto", "investment", "trading"],
            "regulations": ["SEC", "FinCEN", "PCI-DSS"],
            "warning": "Financial services have significant regulatory requirements."
        },
        "eu_market": {
            "keywords": ["europe", "eu", "european", "gdpr"],
            "regulations": ["GDPR"],
            "warning": "EU operations require GDPR compliance."
        }
    }

    def __init__(self, factory_id: Optional[str] = None):
        super().__init__("CEO", "Chief Executive Officer", factory_id)
        self.memory_path = self._get_memory_path()
        self.logs_path = self._get_logs_path()

    def _get_memory_path(self) -> Path:
        """Get path to CEO memory directory."""
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "CEO" / ".ceo" / "memory"

    def _get_logs_path(self) -> Path:
        """Get path to CEO logs directory."""
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "CEO" / "logs"

    def _get_project_root(self) -> Path:
        """Get project root path."""
        return Path(__file__).parent.parent.parent.parent

    def _load_vision(self) -> Optional[Dict[str, Any]]:
        """Load existing vision from memory."""
        vision_path = self.memory_path / "vision.md"
        if vision_path.exists():
            try:
                with open(vision_path, 'r') as f:
                    content = f.read()
                    # Parse the markdown into structured data
                    return {"raw": content, "exists": True}
            except Exception as e:
                self.logger.warning(f"Could not load vision: {e}")
        return None

    def _save_vision(self, vision_data: Dict[str, Any]) -> bool:
        """Save vision to memory."""
        try:
            self.memory_path.mkdir(parents=True, exist_ok=True)
            vision_path = self.memory_path / "vision.md"
            with open(vision_path, 'w') as f:
                f.write(vision_data.get("markdown", ""))
            return True
        except Exception as e:
            self.logger.error(f"Could not save vision: {e}")
            return False

    def _detect_high_risk_domains(self, text: str) -> List[Dict[str, Any]]:
        """Detect high-risk domains in the given text."""
        text_lower = text.lower()
        flagged = []

        for domain_id, domain_info in self.HIGH_RISK_DOMAINS.items():
            for keyword in domain_info["keywords"]:
                if keyword in text_lower:
                    flagged.append({
                        "domain": domain_id,
                        "keyword": keyword,
                        "regulations": domain_info["regulations"],
                        "warning": domain_info["warning"]
                    })
                    break  # Only flag each domain once

        return flagged

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
    # CEO.VISION - Gather business vision from founder
    # =========================================================================

    def ceo_vision(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gather business vision from the founder through structured conversation.

        Args:
            payload: {
                "action": "start" | "respond" | "confirm" | "summary",
                "user_input": str (optional),
                "question_index": int (optional),
                "conversation_history": list (optional)
            }

        Returns:
            Response with next question or vision summary
        """
        action = payload.get("action", "start")
        user_input = payload.get("user_input", "")
        question_index = payload.get("question_index", 0)
        conversation_history = payload.get("conversation_history", [])
        responses = payload.get("responses", {})

        if action == "start":
            # Check if vision already exists
            existing_vision = self._load_vision()
            if existing_vision and existing_vision.get("exists"):
                return {
                    "message": "I found an existing vision document. Would you like to update it or start fresh?",
                    "existing_vision": existing_vision.get("raw", "")[:500] + "...",
                    "options": ["update", "start_fresh"],
                    "next_action": "choose_mode"
                }

            # Start fresh vision gathering
            q = self.VISION_QUESTIONS[0]
            return {
                "message": "Welcome! Let's capture your business vision. I'll ask you a series of questions to understand what you want to build.",
                "question": {
                    "index": 0,
                    "category": q["category"],
                    "question": q["question"],
                    "why": q["why"],
                    "examples": q["examples"]
                },
                "total_questions": len(self.VISION_QUESTIONS),
                "next_action": "respond"
            }

        elif action == "respond":
            # Process the user's response and move to next question
            if user_input:
                responses[self.VISION_QUESTIONS[question_index]["category"]] = user_input
                conversation_history.append({
                    "question": self.VISION_QUESTIONS[question_index]["question"],
                    "response": user_input
                })

            # Check for high-risk domains in response
            high_risk = self._detect_high_risk_domains(user_input)

            next_index = question_index + 1

            if next_index >= len(self.VISION_QUESTIONS):
                # All questions answered, generate summary
                return self._generate_vision_summary(responses, conversation_history, high_risk)

            # Ask next question
            q = self.VISION_QUESTIONS[next_index]
            result = {
                "message": "Got it. Let me ask you about the next aspect of your vision.",
                "question": {
                    "index": next_index,
                    "category": q["category"],
                    "question": q["question"],
                    "why": q["why"],
                    "examples": q["examples"]
                },
                "total_questions": len(self.VISION_QUESTIONS),
                "progress": f"{next_index}/{len(self.VISION_QUESTIONS)}",
                "responses": responses,
                "conversation_history": conversation_history,
                "next_action": "respond"
            }

            if high_risk:
                result["high_risk_warning"] = high_risk

            return result

        elif action == "summary":
            # Generate vision summary using LLM
            return self._generate_vision_summary(
                payload.get("responses", {}),
                payload.get("conversation_history", []),
                []
            )

        elif action == "confirm":
            # Founder confirmed the vision summary
            vision_markdown = payload.get("vision_markdown", "")

            if self._save_vision({"markdown": vision_markdown}):
                self._log_session("vision", {
                    "responses": responses,
                    "confirmed": True
                })

                return {
                    "message": "Your vision has been saved. Ready to create the business plan.",
                    "saved_to": str(self.memory_path / "vision.md"),
                    "next_step": "Run /ceo.plan to generate your business plan",
                    "next_action": "ceo.plan"
                }
            else:
                return {
                    "message": "There was an error saving your vision. Please try again.",
                    "error": True
                }

        return {"error": f"Unknown action: {action}"}

    def _generate_vision_summary(
        self,
        responses: Dict[str, str],
        history: List[Dict],
        high_risk: List[Dict]
    ) -> Dict[str, Any]:
        """Use LLM to generate a structured vision summary."""

        # Build prompt from responses
        responses_text = "\n".join([
            f"**{category}**: {response}"
            for category, response in responses.items()
        ])

        high_risk_text = ""
        if high_risk:
            high_risk_text = "\n\nHigh-Risk Domains Detected:\n" + "\n".join([
                f"- {r['domain']}: {r['warning']} (Regulations: {', '.join(r['regulations'])})"
                for r in high_risk
            ])

        prompt = f"""Based on the founder's responses to my vision questions, create a structured vision summary.

Founder's Responses:
{responses_text}
{high_risk_text}

Generate a professional vision summary in this exact markdown format:

## Vision Summary

### Problem Statement
[Synthesize from founder's response - 2-3 sentences]

### Target Audience
[Who we serve - be specific]

### Solution
[How we solve the problem]

### Unique Value Proposition
[What makes us different - one clear statement]

### Business Model
[How we make money - be specific about pricing if mentioned]

### Scale & Ambition
[Growth targets and vision for size]

### Timeline
[Key milestones mentioned]

### Resources
[Available budget/team]

### High-Risk Domains
[List any flagged domains and their implications, or "None identified"]

---

After each section, write naturally and professionally. Do not use placeholder text.
"""

        try:
            summary = self._think(
                prompt=prompt,
                task_type="critical_decision",
                temperature=0.5,
                max_tokens=2000
            )

            return {
                "message": "I've synthesized your vision into a structured summary. Please review and confirm.",
                "vision_summary": summary,
                "responses": responses,
                "high_risk_domains": high_risk,
                "next_action": "confirm",
                "instructions": "If this accurately captures your vision, confirm to save. Otherwise, let me know what needs to change."
            }
        except Exception as e:
            self.logger.error(f"Error generating vision summary: {e}")
            return {
                "error": str(e),
                "message": "There was an error generating the vision summary. Please try again."
            }

    # =========================================================================
    # CEO.PLAN - Generate business plan from vision
    # =========================================================================

    def ceo_plan(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a business plan from the gathered vision.

        Args:
            payload: {
                "action": "generate" | "update",
                "sections": list (optional, for partial updates)
            }

        Returns:
            Generated business plan or error
        """
        # Check for vision document
        vision = self._load_vision()
        if not vision or not vision.get("exists"):
            return {
                "error": "Vision document not found",
                "message": "Run /ceo.vision first to gather the business vision.",
                "next_action": "ceo.vision"
            }

        vision_content = vision.get("raw", "")

        # Load mission files if they exist
        mission_content = self._load_mission_files()

        prompt = f"""Based on the following vision document, generate a comprehensive business plan in Lean Canvas format.

## Vision Document
{vision_content}

## Existing Mission (if any)
{mission_content}

Generate the business plan in this exact markdown format. Fill in all sections with specific, actionable content based on the vision. Do NOT use placeholder text like [X] or TBD.

# [BUSINESS_NAME]

> [One-line tagline/value proposition]

## Executive Summary
[2-3 paragraph overview of the business]

## Problem
- [Problem 1]
- [Problem 2]
- [Problem 3]

### Existing Alternatives
[How people currently solve this problem]

## Solution
- [Solution element 1]
- [Solution element 2]
- [Solution element 3]

## Unique Value Proposition
[Single clear compelling message that states why you are different and worth buying]

## Target Customers

### Early Adopters
[Description of ideal first customers]

### Customer Segments
1. [Segment 1]
2. [Segment 2]

## Revenue Streams
- [Revenue stream 1]: [Description]
- [Revenue stream 2]: [Description]

## Cost Structure
- Fixed: [Fixed costs]
- Variable: [Variable costs]

## Key Metrics
| Metric | Target | Timeframe |
|--------|--------|-----------|
| [Metric 1] | [Target] | [When] |
| [Metric 2] | [Target] | [When] |
| [Metric 3] | [Target] | [When] |

## Unfair Advantage
[Something that cannot easily be bought or copied]

## Channels
- [Channel 1]: [How we reach customers]
- [Channel 2]: [How we reach customers]

## Regulatory Considerations
[High-risk domains and compliance requirements identified from vision]

## Timeline
| Milestone | Target Date | Owner |
|-----------|-------------|-------|
| [Milestone 1] | [Date] | [C-suite position] |
| [Milestone 2] | [Date] | [C-suite position] |
| [Milestone 3] | [Date] | [C-suite position] |

## C-Suite Status
| Position | Status | Last Updated |
|----------|--------|--------------|
| CEO | ✅ Active | {datetime.utcnow().strftime("%Y-%m-%d")} |
| CFO | ⏳ Pending | - |
| CMO | ⏳ Pending | - |
| COO | ⏳ Pending | - |
| CIO | ⏳ Pending | - |
| CLO | ⏳ Pending | - |
| CTO | 🔒 Gated | - |

## Next Steps
- [ ] CFO: Create financial projections
- [ ] CMO: Develop marketing strategy and validation plan
- [ ] COO: Design operations framework
- [ ] CIO: Plan data and security architecture
- [ ] CLO: Assess legal/compliance requirements
- [ ] [GATE] CMO validation complete
- [ ] [GATE] Human approval
- [ ] CTO: Begin product development

---

*Generated by CEO Agent | Last Updated: {datetime.utcnow().strftime("%Y-%m-%d")}*

Make sure every section has real content based on the vision, not placeholders.
"""

        try:
            business_plan = self._think(
                prompt=prompt,
                task_type="critical_decision",
                temperature=0.4,
                max_tokens=4000
            )

            # Save to root README.md
            root_readme = self._get_project_root() / "README.md"

            # Also save plan version to memory
            self.memory_path.mkdir(parents=True, exist_ok=True)
            plan_version_path = self.memory_path / "plan-version.md"
            with open(plan_version_path, 'w') as f:
                f.write(f"# Business Plan Version\n\n")
                f.write(f"**Generated**: {datetime.utcnow().isoformat()}Z\n")
                f.write(f"**Based on**: vision.md\n")

            # Log the generation
            self._log_session("plan-generation", {
                "vision_used": True,
                "timestamp": datetime.utcnow().isoformat()
            })

            return {
                "message": "Business plan generated successfully.",
                "business_plan": business_plan,
                "save_to": str(root_readme),
                "next_step": "Review the plan, then run /ceo.propagate to distribute to C-Suite",
                "next_action": "ceo.propagate",
                "instructions": "Please review the business plan. When ready, confirm to save to README.md and propagate to the C-Suite."
            }

        except Exception as e:
            self.logger.error(f"Error generating business plan: {e}")
            return {
                "error": str(e),
                "message": "There was an error generating the business plan."
            }

    def _load_mission_files(self) -> str:
        """Load existing mission files if they exist."""
        mission_dir = self._get_project_root() / ".mission"
        content = []

        mission_files = [
            "mission-statement.md",
            "values.md",
            "objective.md",
            "elevator-pitch.md"
        ]

        for filename in mission_files:
            filepath = mission_dir / filename
            if filepath.exists():
                try:
                    with open(filepath, 'r') as f:
                        file_content = f.read()
                        if file_content.strip() and "TEMPLATE" not in file_content.upper():
                            content.append(f"### {filename}\n{file_content[:500]}")
                except Exception:
                    pass

        return "\n\n".join(content) if content else "No mission files configured yet."

    # =========================================================================
    # CEO.PROPAGATE - Distribute plan to C-Suite agents
    # =========================================================================

    def ceo_propagate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Distribute the business plan to all C-Suite positions.

        Args:
            payload: {
                "positions": list (optional, defaults to all),
                "business_plan": str (optional, will load from README if not provided)
            }

        Returns:
            Propagation status and briefs generated
        """
        # Load business plan
        readme_path = self._get_project_root() / "README.md"
        if not readme_path.exists():
            return {
                "error": "Business plan not found",
                "message": "Run /ceo.plan first to generate the business plan.",
                "next_action": "ceo.plan"
            }

        with open(readme_path, 'r') as f:
            business_plan = f.read()

        # Positions to brief (CTO is info-only, gated)
        positions = {
            "CFO": {
                "focus": "Financial projections, budget, funding strategy",
                "extract": ["Revenue Streams", "Cost Structure", "Timeline", "Key Metrics"]
            },
            "CMO": {
                "focus": "Marketing strategy, validation plan, customer acquisition",
                "extract": ["Target Customers", "Channels", "Unique Value Proposition"],
                "note": "CRITICAL: CMO owns the validation gate. CTO cannot proceed until CMO validation is complete."
            },
            "COO": {
                "focus": "Operations plan, workforce needs, process design",
                "extract": ["Solution", "Timeline", "Cost Structure"]
            },
            "CIO": {
                "focus": "Data governance, security framework, privacy assessment",
                "extract": ["Regulatory Considerations", "Solution", "Target Customers"]
            },
            "CLO": {
                "focus": "Compliance checklist, contract templates, risk assessment",
                "extract": ["Regulatory Considerations", "Revenue Streams", "Target Customers"]
            },
            "CTO": {
                "focus": "Technical requirements (GATED - cannot start until validation)",
                "extract": ["Solution", "Timeline"],
                "status": "GATED",
                "note": "CTO is gated until: 1) CMO validation complete, 2) Human approval received"
            }
        }

        briefs_generated = {}

        for position, config in positions.items():
            brief = self._generate_position_brief(position, config, business_plan)
            briefs_generated[position] = brief

            # Save brief to position's memory
            self._save_position_brief(position, brief)

        # Create propagation record
        propagation_record = self._create_propagation_record(positions, briefs_generated)

        # Log propagation
        self._log_session("propagation", {
            "positions_briefed": list(positions.keys()),
            "timestamp": datetime.utcnow().isoformat()
        })

        return {
            "message": "Business plan propagated to all C-Suite positions.",
            "positions_briefed": list(positions.keys()),
            "briefs": {pos: brief[:500] + "..." for pos, brief in briefs_generated.items()},
            "propagation_record": propagation_record,
            "gate_status": {
                "cto_gated": True,
                "requires": ["CMO validation", "Human approval"]
            },
            "next_step": "C-Suite agents are now ready to work. Run /ceo.report to see status.",
            "next_action": "ceo.report"
        }

    def _generate_position_brief(
        self,
        position: str,
        config: Dict[str, Any],
        business_plan: str
    ) -> str:
        """Generate a brief for a specific position using LLM."""

        prompt = f"""Based on this business plan, generate a brief for the {position} position.

## Business Plan
{business_plan[:3000]}

Generate a brief in this format:

# CEO Brief to {position}

**Date**: {datetime.utcnow().isoformat()}Z
**From**: CEO Agent
**Re**: Domain Assignment

## Business Context
[Relevant excerpt from business plan for this position]

## Your Domain Focus
{config['focus']}

## Key Requirements
1. [Specific requirement for {position}]
2. [Specific requirement for {position}]
3. [Specific requirement for {position}]

## High-Risk Considerations
[Any regulatory or risk considerations relevant to {position}]

## Expected Deliverables
- [ ] [Primary deliverable]
- [ ] [Secondary deliverable]

## Timeline
[Expected completion based on business plan timeline]

{f"## Special Note{chr(10)}{config.get('note', '')}" if config.get('note') else ""}

## Questions?
Submit inquiries via /{position.lower()}.inquire → CEO

---

*Refer to your .ethics/ethics.md for behavioral guidelines.*
"""

        try:
            brief = self._think(
                prompt=prompt,
                task_type="agent_reasoning",
                temperature=0.5,
                max_tokens=1500
            )
            return brief
        except Exception as e:
            self.logger.error(f"Error generating brief for {position}: {e}")
            return f"# Brief for {position}\n\nError generating brief: {e}"

    def _save_position_brief(self, position: str, brief: str) -> bool:
        """Save a brief to the position's memory directory."""
        try:
            # Path: C-Suites/[POSITION]/.[pos]/memory/ceo-brief.md
            pos_lower = position.lower()
            memory_path = (
                self._get_project_root() / "C-Suites" / position /
                f".{pos_lower}" / "memory" / "ceo-brief.md"
            )
            memory_path.parent.mkdir(parents=True, exist_ok=True)

            with open(memory_path, 'w') as f:
                f.write(brief)

            return True
        except Exception as e:
            self.logger.error(f"Error saving brief for {position}: {e}")
            return False

    def _create_propagation_record(
        self,
        positions: Dict,
        briefs: Dict
    ) -> str:
        """Create a propagation record."""
        record = f"""# Business Plan Propagation

**Date**: {datetime.utcnow().isoformat()}Z

## Positions Briefed

| Position | Brief Sent | Status |
|----------|------------|--------|
"""
        for pos, config in positions.items():
            status = config.get("status", "Ready to work")
            if pos == "CMO":
                status = "Ready to work (GATE OWNER)"
            record += f"| {pos} | ✅ | {status} |\n"

        record += """
## Gate Requirements

Before CTO can begin:
- [ ] CMO validation complete
- [ ] Validation metrics met
- [ ] Human approval received

## Next Expected Outputs

- CFO: Financial projections
- CMO: Marketing strategy + validation plan
- COO: Operations framework
- CIO: Data governance plan
- CLO: Compliance assessment
"""

        # Save propagation record
        try:
            record_path = self.memory_path / f"propagation-{datetime.utcnow().strftime('%Y-%m-%d')}.md"
            self.memory_path.mkdir(parents=True, exist_ok=True)
            with open(record_path, 'w') as f:
                f.write(record)
        except Exception as e:
            self.logger.warning(f"Could not save propagation record: {e}")

        return record

    # =========================================================================
    # CEO.ONBOARD - Guide founder through service onboarding
    # =========================================================================

    def ceo_onboard(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Guide the founder through the service onboarding process.

        Args:
            payload: {
                "action": "start" | "status" | "verify" | "complete",
                "phase": int (optional),
                "service": str (optional, for verify action),
                "data": dict (optional, submitted credentials)
            }

        Returns:
            Current onboarding phase or verification result
        """
        action = payload.get("action", "start")
        phase = payload.get("phase", 1)

        if action == "start":
            return {
                "message": "Welcome to business onboarding! I'll guide you through setting up the required services.",
                "important": "⚠️ I CANNOT create accounts, agree to terms, or enter payment info. YOU must do these actions.",
                "phase": 1,
                "phase_name": "Business Identity",
                "fields": [
                    {"name": "business_name", "label": "Business Name", "required": True},
                    {"name": "domain", "label": "Business Domain", "placeholder": "example.com", "required": True},
                    {"name": "founder_name", "label": "Your Name (Chairman)", "required": True},
                    {"name": "founder_email", "label": "Your Email", "required": True},
                    {"name": "founder_phone", "label": "Your Phone", "required": False},
                    {"name": "telegram_id", "label": "Telegram User ID", "required": True}
                ],
                "next_action": "submit_phase_1"
            }

        elif action == "status":
            # Check onboarding status
            status = self._get_onboarding_status()
            return {
                "message": "Current onboarding status",
                "status": status,
                "next_phase": status.get("next_phase", 1)
            }

        elif action == "verify":
            service = payload.get("service", "")
            result = self._verify_service(service, payload.get("data", {}))
            return result

        elif action == "complete":
            return self._complete_onboarding(payload)

        # Handle phase submissions
        elif action.startswith("submit_phase_"):
            phase_num = int(action.split("_")[-1])
            return self._process_onboarding_phase(phase_num, payload.get("data", {}))

        return {"error": f"Unknown action: {action}"}

    def _get_onboarding_status(self) -> Dict[str, Any]:
        """Get current onboarding status."""
        status_path = self.memory_path / "onboarding-status.json"
        if status_path.exists():
            try:
                with open(status_path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass

        return {
            "phase_1_complete": False,
            "phase_2_complete": False,
            "phase_3_complete": False,
            "services_connected": [],
            "next_phase": 1
        }

    def _process_onboarding_phase(self, phase: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a completed onboarding phase."""
        status = self._get_onboarding_status()
        status[f"phase_{phase}_complete"] = True
        status["next_phase"] = phase + 1

        if phase == 1:
            status["business_info"] = data

        # Save status
        self._save_onboarding_status(status)

        # Return next phase info
        phases = {
            2: {
                "phase_name": "Essential Services",
                "services": [
                    {"name": "gcp", "label": "Google Cloud Platform", "required": True},
                    {"name": "openrouter", "label": "OpenRouter API", "required": True},
                    {"name": "stripe", "label": "Stripe Payments", "required": True}
                ]
            },
            3: {
                "phase_name": "Communication",
                "services": [
                    {"name": "gmail", "label": "Gmail/Google Workspace", "required": True},
                    {"name": "twilio", "label": "Twilio (Phone)", "required": False},
                    {"name": "telegram", "label": "Telegram Bot", "required": True}
                ]
            }
        }

        if phase + 1 in phases:
            return {
                "message": f"Phase {phase} complete! Moving to phase {phase + 1}.",
                "phase": phase + 1,
                **phases[phase + 1],
                "next_action": f"submit_phase_{phase + 1}"
            }
        else:
            return {
                "message": "All phases complete! Ready to verify connections.",
                "next_action": "verify_all"
            }

    def _save_onboarding_status(self, status: Dict[str, Any]) -> None:
        """Save onboarding status."""
        try:
            self.memory_path.mkdir(parents=True, exist_ok=True)
            status_path = self.memory_path / "onboarding-status.json"
            with open(status_path, 'w') as f:
                json.dump(status, f, indent=2)
        except Exception as e:
            self.logger.error(f"Could not save onboarding status: {e}")

    def _verify_service(self, service: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify a service connection (stub - actual verification would hit APIs)."""
        # In production, this would actually test the connection
        return {
            "service": service,
            "status": "verification_pending",
            "message": f"To verify {service}, please ensure you've completed setup and provided valid credentials.",
            "note": "Actual API verification would be performed in production."
        }

    def _complete_onboarding(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Complete the onboarding process."""
        status = self._get_onboarding_status()
        status["completed"] = True
        status["completed_at"] = datetime.utcnow().isoformat()
        self._save_onboarding_status(status)

        self._log_session("onboarding", {
            "completed": True,
            "business_info": status.get("business_info", {})
        })

        return {
            "message": "🎉 Onboarding complete!",
            "business": status.get("business_info", {}).get("business_name", "Your Business"),
            "next_steps": [
                "Complete your .mission files (mission-statement.md, values.md, etc.)",
                "Review ethics files for each C-Suite position",
                "Run /ceo.vision to capture your business vision",
                "Run /ceo.plan to generate the business plan"
            ],
            "status": status
        }

    # =========================================================================
    # CEO.INQUIRE - Handle questions from other C-Suite agents
    # =========================================================================

    def ceo_inquire(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle inquiries from other C-Suite agents.

        Args:
            payload: {
                "from": str (position asking),
                "type": "information" | "clarification" | "decision" | "escalation",
                "subject": str,
                "question": str,
                "context": str (optional),
                "urgency": "high" | "medium" | "low"
            }

        Returns:
            Response or escalation to founder
        """
        from_position = payload.get("from", "UNKNOWN")
        inquiry_type = payload.get("type", "information")
        subject = payload.get("subject", "General Inquiry")
        question = payload.get("question", "")
        context = payload.get("context", "")
        urgency = payload.get("urgency", "medium")

        if not question:
            return {"error": "Question is required"}

        # Load business context
        readme_path = self._get_project_root() / "README.md"
        vision = self._load_vision()

        business_context = ""
        if readme_path.exists():
            with open(readme_path, 'r') as f:
                business_context = f.read()[:2000]

        vision_context = vision.get("raw", "")[:1000] if vision else ""

        # Determine if we can answer or need to escalate
        escalation_triggers = [
            "budget" in question.lower() and "approval" in question.lower(),
            "legal" in question.lower(),
            "regulatory" in question.lower(),
            inquiry_type == "decision",
            inquiry_type == "escalation",
            urgency == "high" and inquiry_type != "information"
        ]

        if any(escalation_triggers):
            return self._escalate_to_founder(payload, business_context)

        # Try to answer using LLM
        prompt = f"""You are the CEO agent answering an inquiry from the {from_position}.

## Inquiry
From: {from_position}
Type: {inquiry_type}
Subject: {subject}
Question: {question}
Context: {context}

## Business Plan
{business_context}

## Vision
{vision_context}

Provide a helpful response. If the answer is in the business plan or vision, cite it.
If you cannot answer with confidence, say so and recommend escalating to the founder.

Format your response as:

## Response to {from_position}

**Subject**: {subject}
**Date**: {datetime.utcnow().isoformat()}Z

### Answer
[Your response]

### Source
[Where this information came from - Business Plan, Vision, or Inference]

### Confidence
[High/Medium/Low]

### Related Information
[Any additional context that might help]
"""

        try:
            response = self._think(
                prompt=prompt,
                task_type="agent_reasoning",
                temperature=0.4,
                max_tokens=1500
            )

            # Log the inquiry
            self._log_session("inquiry", {
                "from": from_position,
                "type": inquiry_type,
                "subject": subject,
                "resolved": "direct_answer"
            })

            return {
                "message": "Inquiry processed",
                "from": from_position,
                "response": response,
                "escalated": False
            }

        except Exception as e:
            self.logger.error(f"Error processing inquiry: {e}")
            return self._escalate_to_founder(payload, business_context, reason=str(e))

    def _escalate_to_founder(
        self,
        inquiry: Dict[str, Any],
        context: str,
        reason: str = ""
    ) -> Dict[str, Any]:
        """Escalate an inquiry to the founder."""

        escalation = f"""## Escalation to Founder

**From**: {inquiry.get('from', 'Unknown')}
**Subject**: {inquiry.get('subject', 'General')}
**Urgency**: {inquiry.get('urgency', 'medium').upper()}
**Type**: {inquiry.get('type', 'inquiry')}

### Question
{inquiry.get('question', 'No question provided')}

### Context
{inquiry.get('context', 'No additional context')}

### CEO Assessment
This inquiry requires founder input because:
{reason if reason else "The question involves a decision or commitment outside my authority."}

### Options (if applicable)
Please advise on how to proceed.

**Awaiting your input...**
"""

        # Log escalation
        self._log_session("escalation", {
            "from": inquiry.get("from"),
            "subject": inquiry.get("subject"),
            "reason": reason or "Requires founder decision"
        })

        return {
            "message": "Inquiry escalated to founder",
            "escalation": escalation,
            "escalated": True,
            "urgency": inquiry.get("urgency", "medium"),
            "awaiting": "founder_response"
        }

    # =========================================================================
    # CEO.REPORT - Generate status report for founder
    # =========================================================================

    def ceo_report(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a status report for the founder.

        Args:
            payload: {
                "format": "full" | "summary" | "blockers",
                "positions": list (optional, filter to specific positions)
            }

        Returns:
            Status report
        """
        report_format = payload.get("format", "full")

        # Gather status from each position
        positions_status = {}
        c_suite = ["CEO", "CFO", "CMO", "COO", "CIO", "CLO", "CTO", "CXA"]

        for pos in c_suite:
            positions_status[pos] = self._get_position_status(pos)

        # Check for blockers
        blockers = []
        for pos, status in positions_status.items():
            if status.get("blocked"):
                blockers.append({
                    "position": pos,
                    "reason": status.get("blocker_reason", "Unknown")
                })

        # Load business info
        readme_path = self._get_project_root() / "README.md"
        business_name = "Your Business"
        if readme_path.exists():
            with open(readme_path, 'r') as f:
                content = f.read()
                # Try to extract business name from first heading
                lines = content.split('\n')
                for line in lines:
                    if line.startswith('# '):
                        business_name = line[2:].strip()
                        break

        # Generate report
        report = f"""# Business Status Report

**Generated**: {datetime.utcnow().isoformat()}Z
**Business**: {business_name}

## Executive Summary
"""

        # Add executive summary based on status
        active_count = sum(1 for s in positions_status.values() if s.get("status") == "active")
        pending_count = sum(1 for s in positions_status.values() if s.get("status") == "pending")

        if active_count > 0:
            report += f"The business has {active_count} active C-Suite positions working. "
        if pending_count > 0:
            report += f"{pending_count} positions are pending activation. "
        if blockers:
            report += f"**{len(blockers)} blockers** require attention."

        report += "\n\n## C-Suite Dashboard\n\n"
        report += "| Position | Status | Progress | Last Activity | Blockers |\n"
        report += "|----------|--------|----------|---------------|----------|\n"

        status_icons = {
            "active": "🟢",
            "complete": "✅",
            "pending": "⏳",
            "blocked": "🔴",
            "waiting": "🟡",
            "gated": "🔒"
        }

        for pos in c_suite:
            status = positions_status[pos]
            icon = status_icons.get(status.get("status", "pending"), "⏳")
            progress = status.get("progress", "-")
            last_activity = status.get("last_activity", "-")
            blocker = status.get("blocker_reason", "None")
            report += f"| {pos} | {icon} {status.get('status', 'pending').title()} | {progress} | {last_activity} | {blocker} |\n"

        report += """
## Validation Gate Status

- [ ] CMO market validation complete
- [ ] Minimum interest threshold met
- [ ] Human approval received

**CTO Activation**: NOT READY

## Pending Decisions

"""
        if blockers:
            for b in blockers:
                report += f"- **{b['position']}**: {b['reason']}\n"
        else:
            report += "No pending decisions at this time.\n"

        report += """
## Next Steps

1. Continue C-Suite domain work
2. Monitor CMO validation progress
3. Prepare for human approval gate

---

*To get detailed status from any position, ask about that specific area.*
"""

        # Save report
        try:
            report_path = self.memory_path / "latest-report.md"
            self.memory_path.mkdir(parents=True, exist_ok=True)
            with open(report_path, 'w') as f:
                f.write(report)
        except Exception as e:
            self.logger.warning(f"Could not save report: {e}")

        # Log report generation
        self._log_session("report", {
            "format": report_format,
            "blockers": len(blockers)
        })

        return {
            "message": "Status report generated",
            "report": report,
            "positions": positions_status,
            "blockers": blockers,
            "saved_to": str(self.memory_path / "latest-report.md")
        }

    def _get_position_status(self, position: str) -> Dict[str, Any]:
        """Get status for a specific C-Suite position."""
        pos_lower = position.lower()

        # Check for brief (means position has been activated)
        brief_path = (
            self._get_project_root() / "C-Suites" / position /
            f".{pos_lower}" / "memory" / "ceo-brief.md"
        )

        # Check for recent logs
        logs_path = self._get_project_root() / "C-Suites" / position / "logs"

        status = {
            "position": position,
            "status": "pending",
            "progress": "-",
            "last_activity": "-",
            "blocker_reason": "Awaiting propagation"
        }

        if position == "CEO":
            # CEO is always active if we got here
            status.update({
                "status": "active",
                "progress": "Orchestrating",
                "last_activity": datetime.utcnow().strftime("%Y-%m-%d"),
                "blocker_reason": "None"
            })
        elif position == "CTO":
            status.update({
                "status": "gated",
                "progress": "-",
                "blocker_reason": "CMO validation + approval"
            })
        elif brief_path.exists():
            status.update({
                "status": "active",
                "progress": "Working",
                "blocker_reason": "None"
            })

        return status


# =============================================================================
# Cloud Function Entry Point
# =============================================================================

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

    agent = CEOAgent(factory_id=factory_id)
    result = agent.run(command, payload)

    return result


# =============================================================================
# CLI Entry Point (for testing)
# =============================================================================

if __name__ == "__main__":
    import sys

    agent = CEOAgent()

    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [payload_json]")
        print("Commands: ceo.vision, ceo.plan, ceo.propagate, ceo.onboard, ceo.inquire, ceo.report")
        sys.exit(1)

    command = sys.argv[1]
    payload = {}

    if len(sys.argv) > 2:
        try:
            payload = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            print(f"Invalid JSON payload: {sys.argv[2]}")
            sys.exit(1)

    result = agent.run(command, payload)
    print(json.dumps(result, indent=2))

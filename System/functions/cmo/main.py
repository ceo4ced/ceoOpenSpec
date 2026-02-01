"""
CMO Agent - Chief Marketing Officer
Handles marketing strategy, validation campaigns, brand management, and content.
CRITICAL: CMO owns the validation gate that controls CTO activation.

Commands:
    cmo.validate  - Record validation results (PROCEED/PIVOT/ITERATE)
    cmo.strategy  - Create marketing strategy
    cmo.campaign  - Manage marketing campaigns
    cmo.content   - Generate marketing content
    cmo.brand     - Brand guidelines and assets
    cmo.approve   - Request human approval for CTO activation
    cmo.logo      - Logo generation and brand identity assets
    cmo.tiktok    - TikTok content creation and analytics
    cmo.website   - Website specification and planning
    cmo.dashboard - Dashboard UI specifications and component designs
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'packages'))
from factory_core.agent import BaseAgent


class CMOAgent(BaseAgent):
    """
    CMO Agent - Chief Marketing Officer of the AI business.

    CRITICAL RESPONSIBILITY: Owns the validation gate.
    CTO cannot proceed until CMO validation is complete AND human approves.
    """

    def __init__(self, factory_id: Optional[str] = None):
        super().__init__("CMO", "Chief Marketing Officer", factory_id)
        self.memory_path = self._get_memory_path()
        self.logs_path = self._get_logs_path()

    def _get_memory_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "CMO" / ".cmo" / "memory"

    def _get_logs_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "CMO" / "logs"

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
    # CMO.VALIDATE - Record validation results (CRITICAL GATE)
    # =========================================================================

    def cmo_validate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Record validation campaign results and make gate decision.

        This is the CRITICAL gate that determines if CTO can proceed.
        Possible decisions: PROCEED, PIVOT, ITERATE
        """
        action = payload.get("action", "record")

        if action == "record":
            # Record campaign results
            results = payload.get("results", {})

            # Calculate gate decision based on thresholds
            signups = results.get("signups", 0)
            target_signups = results.get("target_signups", 100)
            cost_per_signup = results.get("cost_per_signup", 0)
            max_cost = results.get("max_cost_per_signup", 10)
            engagement_rate = results.get("engagement_rate", 0)
            min_engagement = results.get("min_engagement_rate", 2)

            # Determine decision
            criteria_met = 0
            criteria_total = 3

            if signups >= target_signups:
                criteria_met += 1
            if cost_per_signup <= max_cost or cost_per_signup == 0:
                criteria_met += 1
            if engagement_rate >= min_engagement:
                criteria_met += 1

            if criteria_met == criteria_total:
                decision = "PROCEED"
                decision_icon = "🟢"
            elif criteria_met >= criteria_total - 1:
                decision = "ITERATE"
                decision_icon = "🟡"
            else:
                decision = "PIVOT"
                decision_icon = "🔴"

            validation_result = {
                "decision": decision,
                "decision_icon": decision_icon,
                "criteria_met": f"{criteria_met}/{criteria_total}",
                "results": results,
                "timestamp": datetime.utcnow().isoformat()
            }

            # Save validation result
            self.memory_path.mkdir(parents=True, exist_ok=True)
            date_str = datetime.utcnow().strftime("%Y-%m-%d")
            result_path = self.memory_path / f"validation-results-{date_str}.md"

            with open(result_path, 'w') as f:
                f.write(f"# Validation Results\n\n")
                f.write(f"## GATE DECISION: {decision} {decision_icon}\n\n")
                f.write(f"**Date**: {datetime.utcnow().isoformat()}Z\n\n")
                f.write(f"### Criteria Assessment\n\n")
                f.write(f"- Signups: {signups}/{target_signups}\n")
                f.write(f"- Cost per signup: ${cost_per_signup} (max ${max_cost})\n")
                f.write(f"- Engagement rate: {engagement_rate}% (min {min_engagement}%)\n\n")

                if decision == "PROCEED":
                    f.write("### Next Steps\n")
                    f.write("1. Request human approval for CTO activation\n")
                    f.write("2. Share validated messaging with CTO\n")
                elif decision == "ITERATE":
                    f.write("### Iteration Needed\n")
                    f.write("Close to thresholds - recommend one more iteration\n")
                else:
                    f.write("### Pivot Required\n")
                    f.write("Significant miss on thresholds - recommend pivot discussion\n")

            self._log_session("validation", validation_result)

            response = {
                "message": f"Validation complete: {decision}",
                "gate_decision": decision,
                "criteria_met": f"{criteria_met}/{criteria_total}",
                "saved_to": str(result_path)
            }

            if decision == "PROCEED":
                response["next_step"] = "Run /cmo.approve to request human approval for CTO activation"
                response["next_action"] = "cmo.approve"
            elif decision == "ITERATE":
                response["next_step"] = "Plan iteration campaign with adjusted approach"
            else:
                response["next_step"] = "Discuss pivot options with founder"
                response["escalate"] = True

            return response

        elif action == "status":
            # Check current validation status
            result_files = list(self.memory_path.glob("validation-results-*.md")) if self.memory_path.exists() else []

            if result_files:
                latest = sorted(result_files)[-1]
                with open(latest, 'r') as f:
                    content = f.read()
                return {
                    "message": "Current validation status",
                    "latest_result": content[:1000],
                    "file": str(latest)
                }

            return {
                "message": "No validation results yet",
                "next_step": "Run validation campaign and record results"
            }

        return {"error": f"Unknown action: {action}"}

    # =========================================================================
    # CMO.APPROVE - Request human approval for CTO activation
    # =========================================================================

    def cmo_approve(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request human approval to activate CTO.
        """
        # Check that validation passed
        result_files = list(self.memory_path.glob("validation-results-*.md")) if self.memory_path.exists() else []

        if not result_files:
            return {
                "error": "No validation results found",
                "message": "Complete validation first with /cmo.validate"
            }

        latest = sorted(result_files)[-1]
        with open(latest, 'r') as f:
            content = f.read()

        if "PROCEED" not in content:
            return {
                "error": "Validation did not pass",
                "message": "Gate decision must be PROCEED before requesting approval"
            }

        approval_request = f"""# CTO Activation Approval Request

**Requested By**: CMO Agent
**Date**: {datetime.utcnow().isoformat()}Z

## Validation Summary

{content[:1500]}

## Approval Required

The CMO validation gate has been satisfied with a PROCEED decision.

Before CTO can begin product development, human founder approval is required.

### To Approve:
Reply with approval to activate the CTO agent.

### To Deny:
Provide feedback on concerns or additional validation needed.

---
*This is a critical gate in the CEO OpenSpec workflow.*
"""

        # Save approval request
        approval_path = self.memory_path / "approval-request.md"
        with open(approval_path, 'w') as f:
            f.write(approval_request)

        self._log_session("approval-request", {
            "validation_file": str(latest),
            "requested": datetime.utcnow().isoformat()
        })

        return {
            "message": "Approval request generated",
            "approval_request": approval_request,
            "status": "awaiting_human_approval",
            "note": "Human founder must approve before CTO activation"
        }

    # =========================================================================
    # CMO.STRATEGY - Create marketing strategy
    # =========================================================================

    def cmo_strategy(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create comprehensive marketing strategy.
        """
        business_plan = self._load_business_plan()
        ceo_brief = self._load_ceo_brief()

        prompt = f"""Based on this business plan, create a comprehensive marketing strategy.

## Business Plan
{business_plan[:2500] if business_plan else "No plan available"}

## CEO Brief
{ceo_brief[:1000] if ceo_brief else "No brief available"}

Generate a marketing strategy including:

# Marketing Strategy - [BUSINESS_NAME]

**Generated**: {datetime.utcnow().isoformat()}Z

## Target Audience
### Primary Persona
[Detailed description]

### Secondary Personas
[Other segments]

## Positioning
### Value Proposition
[Core message]

### Competitive Differentiation
[How we stand out]

## Channels
| Channel | Purpose | Priority | Budget % |
|---------|---------|----------|----------|
| [Channel] | [Purpose] | High/Med/Low | X% |

## Validation Plan
### Campaign Design
- Platform: TikTok (primary)
- Budget: $500 test
- Duration: 7 days
- Goal: 100 waitlist signups

### Success Criteria (GATE THRESHOLDS)
- Minimum signups: 100
- Max cost per signup: $5
- Min engagement rate: 3%

## Content Strategy
[Overview]

## Timeline
| Phase | Duration | Focus |
|-------|----------|-------|
| Validation | Week 1-2 | Test messaging |
| Launch | Week 3-4 | Full campaign |
"""

        try:
            strategy = self._think(
                prompt=prompt,
                task_type="content_generation",
                temperature=0.6,
                max_tokens=2500
            )

            self.memory_path.mkdir(parents=True, exist_ok=True)
            version = datetime.utcnow().strftime("%Y%m%d")
            strategy_path = self.memory_path / f"strategy-v{version}.md"
            with open(strategy_path, 'w') as f:
                f.write(strategy)

            return {
                "message": "Marketing strategy created",
                "strategy": strategy,
                "saved_to": str(strategy_path),
                "next_step": "Execute validation campaign, then record results with /cmo.validate"
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # CMO.CAMPAIGN - Manage campaigns
    # =========================================================================

    def cmo_campaign(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Manage marketing campaigns.
        """
        action = payload.get("action", "status")

        if action == "create":
            return self._create_campaign(payload)
        elif action == "status":
            return self._campaign_status()

        return {"message": f"Campaign action '{action}' received"}

    def _create_campaign(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new campaign."""
        platform = payload.get("platform", "tiktok")
        budget = payload.get("budget", 500)
        goal = payload.get("goal", "validation")

        campaign = {
            "id": f"campaign-{datetime.utcnow().strftime('%Y%m%d')}",
            "platform": platform,
            "budget": budget,
            "goal": goal,
            "status": "draft",
            "created": datetime.utcnow().isoformat()
        }

        return {
            "message": "Campaign created",
            "campaign": campaign,
            "note": "Human must execute campaign on platform"
        }

    def _campaign_status(self) -> Dict[str, Any]:
        """Get campaign status."""
        return {
            "message": "Campaign status",
            "active_campaigns": 0,
            "note": "No active campaigns"
        }

    # =========================================================================
    # CMO.CONTENT - Generate content
    # =========================================================================

    def cmo_content(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate marketing content.
        """
        content_type = payload.get("type", "social")
        topic = payload.get("topic", "")
        business_plan = self._load_business_plan()

        prompt = f"""Generate {content_type} marketing content for this business.

Topic: {topic if topic else "General business promotion"}

Business Context:
{business_plan[:1500] if business_plan else "No plan available"}

Generate engaging content appropriate for the platform. Keep it authentic and avoid overly salesy language.
"""

        try:
            content = self._think(
                prompt=prompt,
                task_type="content_generation",
                temperature=0.8,
                max_tokens=1000
            )

            return {
                "message": "Content generated",
                "content_type": content_type,
                "content": content
            }

        except Exception as e:
            return {"error": str(e)}

    # =========================================================================
    # CMO.BRAND - Brand guidelines
    # =========================================================================

    def cmo_brand(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Manage brand guidelines and assets.
        """
        action = payload.get("action", "guidelines")

        if action == "guidelines":
            business_plan = self._load_business_plan()

            prompt = f"""Based on this business plan, create brand guidelines.

{business_plan[:2000] if business_plan else "No plan available"}

Generate brand guidelines including:
1. Brand Voice (tone, personality)
2. Visual Identity recommendations
3. Messaging framework
4. Do's and Don'ts
"""

            try:
                guidelines = self._think(
                    prompt=prompt,
                    task_type="content_generation",
                    temperature=0.6,
                    max_tokens=1500
                )

                return {
                    "message": "Brand guidelines generated",
                    "guidelines": guidelines
                }

            except Exception as e:
                return {"error": str(e)}

        return {"message": f"Brand action '{action}' received"}

    # =========================================================================
    # CMO.LOGO - Logo generation and brand identity
    # =========================================================================

    def cmo_logo(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate logo concepts and manage brand identity assets.
        All logos require GREENLIGHT: BRAND from human before use.
        """
        action = payload.get("action", "generate")

        if action == "generate":
            return self._generate_logo_concepts(payload)
        elif action == "variations":
            return self._logo_variations(payload)
        elif action == "export":
            return self._logo_export(payload)
        elif action == "status":
            return self._logo_status()

        return {"error": f"Unknown action: {action}"}

    def _generate_logo_concepts(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Generate logo concepts using AI."""
        business_plan = self._load_business_plan()

        # Extract concept details
        concept = payload.get("concept", "")
        style = payload.get("style", ["modern", "minimalist"])
        colors = payload.get("colors", {
            "primary": "#4A90D9",
            "secondary": "#1A1A2E"
        })
        variations = payload.get("variations", 5)

        # Get business name from plan
        business_name = "Business"
        if business_plan:
            lines = business_plan.split('\n')
            for line in lines:
                if line.startswith('# '):
                    business_name = line[2:].strip()
                    break

        prompt = f"""Create {variations} logo concept descriptions for {business_name}.

Business Context:
{business_plan[:1500] if business_plan else "No plan available"}

Concept Direction: {concept if concept else "Modern, professional, memorable"}
Style Preferences: {', '.join(style) if isinstance(style, list) else style}
Color Palette: Primary {colors.get('primary', '#4A90D9')}, Secondary {colors.get('secondary', '#1A1A2E')}

For each concept, describe:
1. Concept name
2. Visual description (what it looks like)
3. Symbol/iconography used
4. Typography style
5. Pros and cons
6. Best use cases

Format as a presentation for human review, including a CMO recommendation at the end.
Remember: All logos require GREENLIGHT: BRAND from human before any use.
"""

        try:
            concepts = self._think(
                prompt=prompt,
                task_type="content_generation",
                temperature=0.7,
                max_tokens=2500
            )

            # Generate logo ID
            logo_id = f"LOGO-{datetime.utcnow().strftime('%Y%m%d')}-001"

            # Save concepts
            self.memory_path.mkdir(parents=True, exist_ok=True)
            concepts_path = self.memory_path / f"logo-concepts-{logo_id}.md"
            with open(concepts_path, 'w') as f:
                f.write(f"# Logo Concepts: {business_name}\n\n")
                f.write(f"**Logo ID**: {logo_id}\n")
                f.write(f"**Generated**: {datetime.utcnow().isoformat()}Z\n")
                f.write(f"**Status**: AWAITING GREENLIGHT: BRAND\n\n")
                f.write("---\n\n")
                f.write(concepts)

            self._log_session("logo", {
                "action": "generate",
                "logo_id": logo_id,
                "variations": variations
            })

            return {
                "message": "Logo concepts generated",
                "logo_id": logo_id,
                "concepts": concepts,
                "saved_to": str(concepts_path),
                "status": "awaiting_approval",
                "approval_required": "GREENLIGHT: BRAND from human",
                "next_step": "Review concepts and approve with: APPROVE CONCEPT [N]"
            }

        except Exception as e:
            return {"error": str(e)}

    def _logo_variations(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Generate variations of an approved logo."""
        logo_id = payload.get("logo_id")
        variation_types = payload.get("types", ["primary", "icon", "wordmark", "reversed"])

        return {
            "message": "Logo variation types",
            "logo_id": logo_id,
            "available_types": {
                "primary": "Main logo (icon + wordmark)",
                "icon": "Icon only, no text (favicon, app icon)",
                "wordmark": "Text only, no icon",
                "horizontal": "Wide layout",
                "vertical": "Stacked layout",
                "reversed": "For dark backgrounds",
                "monochrome": "Single color (print, embroidery)"
            },
            "note": "Actual variation generation requires approved logo and design tools"
        }

    def _logo_export(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Export approved logo in various formats."""
        logo_id = payload.get("logo_id")

        return {
            "message": "Logo export specifications",
            "logo_id": logo_id,
            "export_formats": {
                "svg": "Vector, scalable - web use",
                "png": "Transparent background - digital",
                "pdf": "CMYK color space - print",
                "eps": "Vector, editable - professional design",
                "ico": "Multi-size - favicon"
            },
            "standard_sizes": [
                "1200x630 (OG image)",
                "512x512 (App icon)",
                "180x180 (Apple touch)",
                "32x32 (Favicon)"
            ],
            "note": "Actual export requires approved logo and design tools"
        }

    def _logo_status(self) -> Dict[str, Any]:
        """Get logo generation status."""
        logo_files = list(self.memory_path.glob("logo-concepts-*.md")) if self.memory_path.exists() else []

        if logo_files:
            latest = sorted(logo_files)[-1]
            with open(latest, 'r') as f:
                content = f.read()[:500]
            return {
                "message": "Logo status",
                "latest_concepts": str(latest),
                "preview": content,
                "status": "AWAITING GREENLIGHT: BRAND" if "AWAITING" in content else "Unknown"
            }

        return {
            "message": "No logo concepts generated yet",
            "next_step": "Run /cmo.logo to generate concepts"
        }

    # =========================================================================
    # CMO.TIKTOK - TikTok content and analytics
    # =========================================================================

    def cmo_tiktok(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        TikTok content creation, trends, scheduling, and analytics.
        """
        action = payload.get("action", "create")

        if action == "create":
            return self._tiktok_create(payload)
        elif action == "trend":
            return self._tiktok_trend(payload)
        elif action == "schedule":
            return self._tiktok_schedule(payload)
        elif action == "analytics":
            return self._tiktok_analytics(payload)
        elif action == "optimize":
            return self._tiktok_optimize(payload)

        return {"error": f"Unknown action: {action}"}

    def _tiktok_create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create TikTok content."""
        concept = payload.get("concept", "")
        style = payload.get("style", ["trending", "educational"])
        cta = payload.get("cta", "Link in bio")
        business_plan = self._load_business_plan()

        prompt = f"""Create a TikTok video script optimized for virality.

Business Context:
{business_plan[:1000] if business_plan else "No plan available"}

Concept: {concept if concept else "Showcase the product/service value"}
Style: {', '.join(style) if isinstance(style, list) else style}
CTA: {cta}

Create a 30-second TikTok script following this structure:

HOOK (0-3s): Stop the scroll immediately
- Must grab attention in first second
- Use pattern interrupt, surprising statement, or direct address

BUILDUP (3-20s): Deliver value/entertainment
- Keep visual interest high
- Add pattern interrupt at 10s mark

PAYOFF (20-30s): Satisfy hook promise + CTA
- Deliver on what was promised
- Clear call to action

Include:
1. Visual directions (what to show)
2. Text overlay suggestions
3. Recommended sound/music type
4. Hashtag recommendations
5. Best posting time

All TikTok content requires human approval before publication.
"""

        try:
            script = self._think(
                prompt=prompt,
                task_type="content_generation",
                temperature=0.8,
                max_tokens=1500
            )

            post_id = f"TT-{datetime.utcnow().strftime('%Y%m%d')}-001"

            self._log_session("tiktok", {
                "action": "create",
                "post_id": post_id,
                "concept": concept
            })

            return {
                "message": "TikTok script created",
                "post_id": post_id,
                "script": script,
                "status": "draft",
                "approval_required": True,
                "note": "Human must approve before publication"
            }

        except Exception as e:
            return {"error": str(e)}

    def _tiktok_trend(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Research TikTok trends."""
        query = payload.get("query", "tech products")

        return {
            "message": f"TikTok trend research for: {query}",
            "trending_formats": [
                {"format": "POV", "description": "Point of view storytelling", "brand_fit": "High"},
                {"format": "GRWM", "description": "Get ready with me", "brand_fit": "Medium"},
                {"format": "Tutorial", "description": "How-to content", "brand_fit": "High"},
                {"format": "Behind the scenes", "description": "Company/product BTS", "brand_fit": "High"}
            ],
            "recommended_hashtags": [
                "#TechTok", "#ProductReview", "#SmallBusiness", "#Startup"
            ],
            "optimal_posting_times": {
                "monday": ["6am", "10am", "10pm"],
                "tuesday": ["9am", "12pm"],
                "wednesday": ["7am", "8am", "11pm"],
                "thursday": ["9am", "12pm", "7pm"],
                "friday": ["5am", "1pm", "3pm"],
                "saturday": ["11am", "7pm", "8pm"],
                "sunday": ["7am", "8am", "4pm"]
            },
            "note": "Times in EST. Adjust for target audience timezone."
        }

    def _tiktok_schedule(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule TikTok content."""
        post_id = payload.get("post_id")
        schedule_time = payload.get("time")

        return {
            "message": "TikTok scheduling",
            "post_id": post_id,
            "requested_time": schedule_time,
            "status": "pending_approval",
            "note": "TikTok API integration required for auto-scheduling"
        }

    def _tiktok_analytics(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Get TikTok analytics."""
        period = payload.get("period", "7d")

        return {
            "message": f"TikTok analytics ({period})",
            "metrics": {
                "followers": 0,
                "total_views": 0,
                "engagement_rate": "0%",
                "profile_views": 0
            },
            "top_performing_content": [],
            "audience_insights": {
                "peak_active_time": "7-9 PM EST",
                "top_age_group": "18-24",
                "gender_split": "Unknown"
            },
            "note": "TikTok API integration required for actual analytics"
        }

    def _tiktok_optimize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize TikTok content."""
        post_id = payload.get("post_id")

        return {
            "message": "TikTok optimization analysis",
            "post_id": post_id,
            "optimization_tips": [
                "Hook in first 1-3 seconds",
                "Add pattern interrupt at 10s",
                "Use trending sounds",
                "Add captions (85% watch without sound)",
                "End with clear CTA"
            ],
            "a_b_test_suggestions": [
                {"element": "Hook", "test": "Question vs Statement"},
                {"element": "CTA timing", "test": "15s vs 25s"},
                {"element": "Thumbnail", "test": "Face vs Text overlay"}
            ]
        }

    # =========================================================================
    # CMO.WEBSITE - Website specification
    # =========================================================================

    def cmo_website(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create website specifications and planning.
        """
        action = payload.get("action", "spec")

        if action == "spec":
            return self._website_spec(payload)
        elif action == "landing":
            return self._landing_page_spec(payload)
        elif action == "checklist":
            return self._website_checklist()

        return {"error": f"Unknown action: {action}"}

    def _website_spec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create full website specification."""
        site_type = payload.get("type", "marketing")
        business_plan = self._load_business_plan()

        prompt = f"""Create a website specification for a {site_type} website.

Business Context:
{business_plan[:2000] if business_plan else "No plan available"}

Generate a comprehensive website specification including:

# Website Specification

## Overview
- Purpose
- Target Audience
- Primary CTA
- Domain requirements

## Site Architecture
- Page structure (sitemap)
- User journey

## Page Specifications
For each page:
- Hero section content
- Key sections
- CTAs
- Visual requirements

## Technical Requirements
- Platform recommendation (Framer/Webflow/Next.js)
- Performance targets
- SEO requirements
- Mobile requirements

## Integrations
- Analytics
- Forms
- Email
- Payment (if needed)

## Legal Requirements
- Privacy Policy (CLO)
- Terms of Service (CLO)
- Cookie consent (if EU)
- Accessibility (WCAG 2.1 AA)

## Launch Checklist
- Pre-launch items
- Launch items
- Post-launch items

Website launches require GREENLIGHT from human.
"""

        try:
            spec = self._think(
                prompt=prompt,
                task_type="content_generation",
                temperature=0.5,
                max_tokens=3000
            )

            # Save spec
            self.memory_path.mkdir(parents=True, exist_ok=True)
            spec_path = self.memory_path / f"website-spec-{datetime.utcnow().strftime('%Y%m%d')}.md"
            with open(spec_path, 'w') as f:
                f.write(spec)

            self._log_session("website", {
                "action": "spec",
                "type": site_type
            })

            return {
                "message": "Website specification created",
                "spec": spec,
                "saved_to": str(spec_path),
                "next_steps": [
                    "Review spec with stakeholders",
                    "Get CLO review for legal pages",
                    "Get CIO review for technical requirements",
                    "Request GREENLIGHT from human"
                ]
            }

        except Exception as e:
            return {"error": str(e)}

    def _landing_page_spec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create landing page specification."""
        goal = payload.get("goal", "lead_capture")
        business_plan = self._load_business_plan()

        prompt = f"""Create a high-converting landing page specification.

Goal: {goal}
Business Context:
{business_plan[:1500] if business_plan else "No plan available"}

Create a landing page spec with:

## Hero Section
- Headline (max 10 words, clear value prop)
- Subheadline (1-2 sentences)
- CTA button text
- Visual (image/video description)

## Problem Statement
- Pain point we address
- Agitate the problem

## Solution
- How we solve it
- 3-5 key benefits

## Social Proof
- Testimonials
- Logos/trust badges
- Statistics

## Features (Brief)
- Top 3 features with icons

## CTA Section
- Repeat main CTA
- Reduce friction

## FAQ
- Top 3-5 questions

## Footer
- Legal links
- Contact info

Include conversion optimization tips for each section.
"""

        try:
            spec = self._think(
                prompt=prompt,
                task_type="content_generation",
                temperature=0.6,
                max_tokens=2000
            )

            return {
                "message": "Landing page specification created",
                "goal": goal,
                "spec": spec,
                "conversion_tips": [
                    "Keep above-fold focused on value prop + CTA",
                    "Use specific numbers in social proof",
                    "Reduce form fields to minimum",
                    "Add urgency without being pushy",
                    "Mobile-first design"
                ]
            }

        except Exception as e:
            return {"error": str(e)}

    def _website_checklist(self) -> Dict[str, Any]:
        """Get website launch checklist."""
        return {
            "message": "Website launch checklist",
            "pre_launch": [
                "All content reviewed and approved",
                "All links tested",
                "Forms tested (submissions work)",
                "Analytics installed (GA4)",
                "SEO meta tags set",
                "Performance tested (Core Web Vitals)",
                "Mobile tested (all breakpoints)",
                "Legal pages live (Privacy, Terms)",
                "SSL certificate configured",
                "Backup configured"
            ],
            "launch": [
                "DNS pointed to production",
                "SSL verified (https working)",
                "301 redirects configured (if migrating)",
                "Verify in Google Search Console",
                "Submit sitemap"
            ],
            "post_launch": [
                "Monitor analytics (first 48 hours)",
                "Check for 404 errors",
                "Test conversions",
                "Gather user feedback",
                "Monitor Core Web Vitals"
            ],
            "approval_required": "GREENLIGHT from human before launch"
        }

    # =========================================================================
    # CMO.DASHBOARD - Dashboard UI specifications
    # =========================================================================

    # Role to plan document mapping
    ROLE_PLAN_MAPPING = {
        "CEO": {"path": "C-Suites/CEO/README.md", "title": "Business Plan"},
        "CFO": {"path": "C-Suites/CFO/README.md", "title": "Financial Plan"},
        "CMO": {"path": "C-Suites/CMO/README.md", "title": "Marketing Plan"},
        "COO": {"path": "C-Suites/COO/README.md", "title": "Operations Plan"},
        "CIO": {"path": "C-Suites/CIO/README.md", "title": "Information Plan"},
        "CLO": {"path": "C-Suites/CLO/README.md", "title": "Legal Plan"},
        "CPO": {"path": "C-Suites/CPO/README.md", "title": "Product Plan"},
        "CTO": {"path": "C-Suites/CTO/README.md", "title": "Technical Plan"},
        "CXA": {"path": "C-Suites/CXA/README.md", "title": "Experience Plan"},
    }

    def cmo_dashboard(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate dashboard UI specifications for C-Suite dashboards.

        Actions:
            spec     - Generate full dashboard update specification
            plan     - Generate Plan Section component spec
            activity - Generate Function Activity component spec
            layout   - Generate layout rules and CSS
            export   - Export all specs to files
        """
        action = payload.get("action", "spec")

        if action == "spec":
            return self._dashboard_full_spec(payload)
        elif action == "plan":
            return self._dashboard_plan_section_spec(payload)
        elif action == "activity":
            return self._dashboard_activity_section_spec(payload)
        elif action == "layout":
            return self._dashboard_layout_spec(payload)
        elif action == "export":
            return self._dashboard_export_specs(payload)

        return {"error": f"Unknown action: {action}"}

    def _dashboard_full_spec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete dashboard update specification."""
        role = payload.get("role", "ALL")

        spec = f"""# C-Suite Dashboard Update Specification

**Generated**: {datetime.utcnow().isoformat()}Z
**Author**: CMO Agent
**Target**: {role if role != "ALL" else "All C-Suite Dashboards"}
**Status**: AWAITING APPROVAL

---

## Overview

This specification defines updates to the C-Suite dashboard to display:
1. **Plan Section** - Role's respective plan document with navigation
2. **Function Activity Section** - Real-time function execution tracking
3. **Agent Activity Console** - Always positioned at bottom

### Layout Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│ Header (Title, Refresh, Red Phone)                      │
├─────────────────────────────────────────────────────────┤
│ FLEXIBLE ZONE (scrollable)                              │
│  ├─ Plan Section (NEW)                                  │
│  └─ Function Activity Section (NEW)                     │
├─────────────────────────────────────────────────────────┤
│ FIXED ZONE (bottom, 200px)                              │
│  └─ Agent Activity Console (existing, repositioned)     │
└─────────────────────────────────────────────────────────┘
```

**Key Rule**: Activity Console ALWAYS stays at bottom. New sections insert above it.

---

## Component 1: Plan Section

### Purpose
Display the role's respective plan document with interactive navigation.

### Data Source
| Role | Plan Document | Title |
|------|---------------|-------|
"""
        # Add role mappings
        for role_name, info in self.ROLE_PLAN_MAPPING.items():
            spec += f"| {role_name} | `{info['path']}` | {info['title']} |\n"

        spec += f"""
### Visual Design

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 📋 [ROLE] Plan                                    [Expand ↗] [Edit ✎]      │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────┬───────────────────────────────────────┐   │
│  │ Table of Contents            │ Plan Content Preview                  │   │
│  │ ──────────────────────       │ ────────────────────────────          │   │
│  │ ○ 1. Section One             │ ## 1. Section One                     │   │
│  │ ○ 2. Section Two        ───▶ │ Content preview here...               │   │
│  │ ○ 3. Section Three           │                                       │   │
│  │                              │ Status: ████████░░ 80%                │   │
│  │ Last Updated: [DATE]         │                                       │   │
│  └──────────────────────────────┴───────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Properties

| Property | Value |
|----------|-------|
| Height | 280px collapsed, expandable |
| Layout | 2-column: TOC (30%) + Content (70%) |
| Background | `#111827` |
| Border | `1px solid #1e293b` |
| Border Radius | 8px |

### Interactions
- Click TOC item → Scroll content to section
- Expand button → Full-screen modal with complete plan
- Edit button → Link to plan editor (if permitted)

---

## Component 2: Function Activity Section

### Purpose
Display real-time function execution with newest entries at top.

### Visual Design

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚡ Function Activity                              [Filter ▼] [Clear]        │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ ● NEW ENTRIES APPEAR HERE (Sorted: Newest First)                      │  │
│  ├───────────────────────────────────────────────────────────────────────┤  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │ ▼ ceo.decide()                              just now  ● RUN    │  │  │
│  │  │   ├─ Input: {{ decision_type: "strategic" }}                    │  │  │
│  │  │   ├─ Processing: Evaluating options...                         │  │  │
│  │  │   └─ Status: ████████░░░░ 67%                                   │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │ ▶ ceo.plan()                                   2m ago  ✓ OK    │  │  │
│  │  │   Completed in 8.2s | Tokens: 1,247 | Cost: $0.024              │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Properties

| Property | Value |
|----------|-------|
| Height | 320px (scrollable) |
| Max Entries | 50 (oldest pruned) |
| Sort Order | Newest first (prepend) |
| Background | `#0f172a` |
| Border | `1px solid #1e293b` |

### Entry States

| State | Icon | Color | Badge |
|-------|------|-------|-------|
| Running | ● | `#10b981` | RUN |
| Success | ✓ | `#10b981` | OK |
| Error | ✕ | `#ef4444` | ERR |
| Pending | ○ | `#64748b` | WAIT |

---

## Component 3: Agent Activity Console (Repositioned)

### Changes from Current
- **Position**: Fixed at bottom (200px height, reduced from 400px)
- **Behavior**: New entries prepend (newest on top within console)
- **z-index**: Stays below flexible zone content

### CSS Updates

```css
.agent-activity-console {{
  position: sticky;
  bottom: 0;
  height: 200px;
  flex-shrink: 0;
  z-index: 10;
}}
```

---

## Layout CSS Specification

```css
/* Main content area */
.dashboard-content {{
  display: flex;
  flex-direction: column;
  height: calc(100vh - 64px); /* Account for header */
  overflow: hidden;
}}

/* Flexible zone - scrollable content */
.flexible-zone {{
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 16px;
}}

/* Fixed zone - always at bottom */
.fixed-zone {{
  flex-shrink: 0;
  height: 200px;
  border-top: 1px solid #1e293b;
}}

/* Plan Section */
.plan-section {{
  background: #111827;
  border: 1px solid #1e293b;
  border-radius: 8px;
  height: 280px;
  display: grid;
  grid-template-columns: 30% 70%;
}}

.plan-section.expanded {{
  position: fixed;
  inset: 0;
  height: 100vh;
  z-index: 100;
}}

/* Function Activity Section */
.function-activity {{
  background: #0f172a;
  border: 1px solid #1e293b;
  border-radius: 8px;
  height: 320px;
  overflow-y: auto;
}}

.function-entry {{
  border: 1px solid #1e293b;
  border-radius: 4px;
  margin: 8px;
  padding: 12px;
  background: #111827;
}}

.function-entry.running {{
  border-color: #10b981;
  animation: pulse 2s infinite;
}}

.function-entry.error {{
  border-color: #ef4444;
}}

@keyframes pulse {{
  0%, 100% {{ opacity: 1; }}
  50% {{ opacity: 0.7; }}
}}
```

---

## Data Structures

### FunctionActivity Interface

```typescript
interface FunctionActivity {{
  id: string;
  role: string;                    // CEO, CFO, etc.
  functionName: string;            // ceo.decide, cfo.budget
  status: 'running' | 'success' | 'error' | 'pending';
  timestamp: Date;
  input?: Record<string, any>;
  output?: Record<string, any>;
  error?: string;
  progress?: number;               // 0-100 if running
  estimatedRemaining?: number;     // Seconds
  duration?: number;               // Seconds if complete
  tokens?: number;
  cost?: number;                   // USD
}}
```

### PlanSection Interface

```typescript
interface PlanSection {{
  role: string;
  planPath: string;
  planTitle: string;
  content: string;                 // Markdown content
  lastUpdated: Date;
  sections: TableOfContentsItem[];
  completionStatus: {{
    complete: number;
    inReview: number;
    draft: number;
  }};
}}

interface TableOfContentsItem {{
  id: string;
  title: string;
  level: number;                   // 1, 2, 3 for h1, h2, h3
  anchor: string;
}}
```

---

## Implementation Notes

1. **Plan Content Loading**
   - Parse markdown from `C-Suites/[ROLE]/README.md`
   - Extract headings for TOC generation
   - Render with syntax highlighting for code blocks

2. **Function Activity Updates**
   - New entries prepend to list (newest first)
   - Auto-prune when exceeding 50 entries
   - WebSocket or polling for real-time updates

3. **Activity Console Repositioning**
   - Reduce height from 400px to 200px
   - Add sticky positioning at bottom
   - Maintain existing functionality

4. **Responsive Design**
   - Mobile: Stack sections vertically
   - Tablet: Reduce plan section height to 200px
   - Desktop: Full layout as specified

---

## Approval Required

This specification requires **GREENLIGHT: DASHBOARD** from human before implementation.

---

*Generated by CMO Agent | Dashboard Specification v1.0*
"""

        # Save spec
        self.memory_path.mkdir(parents=True, exist_ok=True)
        spec_path = self.memory_path / f"dashboard-spec-{datetime.utcnow().strftime('%Y%m%d')}.md"
        with open(spec_path, 'w') as f:
            f.write(spec)

        self._log_session("dashboard", {
            "action": "spec",
            "role": role
        })

        return {
            "message": "Dashboard specification generated",
            "spec": spec,
            "saved_to": str(spec_path),
            "components": ["Plan Section", "Function Activity Section", "Agent Activity Console"],
            "status": "awaiting_approval",
            "approval_required": "GREENLIGHT: DASHBOARD from human"
        }

    def _dashboard_plan_section_spec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Plan Section component specification."""
        role = payload.get("role", "CEO")

        plan_info = self.ROLE_PLAN_MAPPING.get(role.upper(), {
            "path": f"C-Suites/{role.upper()}/README.md",
            "title": f"{role.upper()} Plan"
        })

        spec = {
            "component": "PlanSection",
            "description": f"Displays the {plan_info['title']} for the {role.upper()} dashboard",
            "data_source": {
                "path": plan_info["path"],
                "title": plan_info["title"],
                "format": "markdown"
            },
            "layout": {
                "height": "280px",
                "height_expanded": "100vh",
                "grid": "30% TOC / 70% Content",
                "background": "#111827",
                "border": "1px solid #1e293b",
                "border_radius": "8px"
            },
            "header": {
                "icon": "📋",
                "title": f"{role.upper()} Plan",
                "actions": [
                    {"label": "Expand", "icon": "↗", "action": "toggleExpand"},
                    {"label": "Edit", "icon": "✎", "action": "openEditor"}
                ]
            },
            "toc_panel": {
                "width": "30%",
                "features": [
                    "Auto-generated from markdown headings",
                    "Click to scroll content",
                    "Highlight active section",
                    "Show last updated date",
                    "Show completion status"
                ]
            },
            "content_panel": {
                "width": "70%",
                "features": [
                    "Markdown rendering",
                    "Syntax highlighting for code",
                    "Table rendering",
                    "Scroll sync with TOC",
                    "Progress indicators"
                ]
            },
            "status_indicators": {
                "compliant": {"icon": "●", "color": "#10b981", "label": "Compliant"},
                "review": {"icon": "○", "color": "#f59e0b", "label": "In Review"},
                "draft": {"icon": "○", "color": "#64748b", "label": "Draft"},
                "overdue": {"icon": "●", "color": "#ef4444", "label": "Overdue"}
            }
        }

        return {
            "message": f"Plan Section spec for {role.upper()}",
            "spec": spec,
            "role": role.upper(),
            "plan_document": plan_info["path"]
        }

    def _dashboard_activity_section_spec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Function Activity Section component specification."""
        role = payload.get("role", "ALL")

        spec = {
            "component": "FunctionActivitySection",
            "description": "Real-time function execution tracking with newest entries at top",
            "layout": {
                "height": "320px",
                "overflow": "auto",
                "background": "#0f172a",
                "border": "1px solid #1e293b",
                "border_radius": "8px"
            },
            "header": {
                "icon": "⚡",
                "title": "Function Activity",
                "actions": [
                    {"label": "Filter", "icon": "▼", "action": "openFilter"},
                    {"label": "Clear", "icon": "×", "action": "clearActivity"}
                ]
            },
            "entry_states": {
                "running": {
                    "icon": "●",
                    "color": "#10b981",
                    "badge": "RUN",
                    "badge_bg": "#10b98120",
                    "animation": "pulse"
                },
                "success": {
                    "icon": "✓",
                    "color": "#10b981",
                    "badge": "OK",
                    "badge_bg": "#10b98120"
                },
                "error": {
                    "icon": "✕",
                    "color": "#ef4444",
                    "badge": "ERR",
                    "badge_bg": "#ef444420"
                },
                "pending": {
                    "icon": "○",
                    "color": "#64748b",
                    "badge": "WAIT",
                    "badge_bg": "#64748b20"
                }
            },
            "entry_structure": {
                "collapsed": {
                    "fields": ["functionName", "timestamp", "status", "summary"],
                    "summary_format": "Completed in {duration}s | Tokens: {tokens} | Cost: ${cost}"
                },
                "expanded": {
                    "fields": ["functionName", "timestamp", "status", "input", "output", "progress", "metrics"],
                    "show_progress_bar": True,
                    "show_estimated_time": True
                }
            },
            "behavior": {
                "sort_order": "newest_first",
                "insert_position": "prepend",
                "max_entries": 50,
                "prune_strategy": "remove_oldest",
                "auto_expand_running": True,
                "auto_collapse_complete": True
            },
            "filter_options": [
                {"label": "All", "value": "all"},
                {"label": "Running", "value": "running"},
                {"label": "Errors", "value": "error"},
                {"label": "This Role Only", "value": "role"}
            ],
            "data_interface": {
                "typescript": """interface FunctionActivity {
  id: string;
  role: string;
  functionName: string;
  status: 'running' | 'success' | 'error' | 'pending';
  timestamp: Date;
  input?: Record<string, any>;
  output?: Record<string, any>;
  error?: string;
  progress?: number;
  estimatedRemaining?: number;
  duration?: number;
  tokens?: number;
  cost?: number;
}"""
            }
        }

        return {
            "message": "Function Activity Section spec",
            "spec": spec,
            "role_filter": role
        }

    def _dashboard_layout_spec(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Generate layout rules and CSS specification."""

        css_spec = """/* ========================================
   C-Suite Dashboard Layout Specification
   Generated by CMO Agent
   ======================================== */

/* ===================
   Layout Structure
   =================== */

/* Main dashboard content area */
.dashboard-content {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 64px); /* Account for header */
  overflow: hidden;
  background: var(--bg-primary, #0a0e17);
}

/* Flexible zone - holds Plan and Function Activity sections */
.flexible-zone {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 16px;
  /* Ensure content doesn't overlap fixed zone */
  padding-bottom: 16px;
}

/* Fixed zone - Agent Activity Console always at bottom */
.fixed-zone {
  flex-shrink: 0;
  height: 200px;
  border-top: 1px solid var(--border-color, #1e293b);
  background: var(--bg-secondary, #111827);
}

/* ===================
   Plan Section
   =================== */

.plan-section {
  background: var(--bg-secondary, #111827);
  border: 1px solid var(--border-color, #1e293b);
  border-radius: 8px;
  min-height: 280px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.plan-section__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color, #1e293b);
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
}

.plan-section__title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: var(--text-primary, #f9fafb);
}

.plan-section__actions {
  display: flex;
  gap: 8px;
}

.plan-section__body {
  flex: 1;
  display: grid;
  grid-template-columns: 30% 70%;
  overflow: hidden;
}

.plan-section__toc {
  padding: 16px;
  border-right: 1px solid var(--border-color, #1e293b);
  overflow-y: auto;
}

.plan-section__content {
  padding: 16px;
  overflow-y: auto;
}

/* Expanded state */
.plan-section.expanded {
  position: fixed;
  inset: 0;
  height: 100vh;
  z-index: 100;
  border-radius: 0;
  margin: 0;
}

/* ===================
   Function Activity
   =================== */

.function-activity {
  background: var(--bg-tertiary, #0f172a);
  border: 1px solid var(--border-color, #1e293b);
  border-radius: 8px;
  min-height: 320px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.function-activity__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color, #1e293b);
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
}

.function-activity__body {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

/* Function Entry Card */
.function-entry {
  border: 1px solid var(--border-color, #1e293b);
  border-radius: 4px;
  margin-bottom: 8px;
  padding: 12px;
  background: var(--bg-secondary, #111827);
  transition: all 0.2s ease;
}

.function-entry:hover {
  border-color: var(--accent-blue, #3b82f6);
}

.function-entry.running {
  border-color: var(--status-success, #10b981);
  animation: pulse 2s infinite;
}

.function-entry.error {
  border-color: var(--status-error, #ef4444);
}

.function-entry__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.function-entry__name {
  font-family: 'SF Mono', Monaco, Consolas, monospace;
  font-weight: 500;
  color: var(--accent-blue, #3b82f6);
}

.function-entry__meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.875rem;
  color: var(--text-muted, #64748b);
}

.function-entry__status {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

.function-entry__status.running {
  background: #10b98120;
  color: #10b981;
}

.function-entry__status.success {
  background: #10b98120;
  color: #10b981;
}

.function-entry__status.error {
  background: #ef444420;
  color: #ef4444;
}

.function-entry__details {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border-color, #1e293b);
  font-family: 'SF Mono', Monaco, Consolas, monospace;
  font-size: 0.875rem;
}

.function-entry__progress {
  margin-top: 8px;
}

.function-entry__progress-bar {
  height: 4px;
  background: var(--bg-tertiary, #0f172a);
  border-radius: 2px;
  overflow: hidden;
}

.function-entry__progress-fill {
  height: 100%;
  background: var(--status-success, #10b981);
  transition: width 0.3s ease;
}

/* ===================
   Agent Activity Console (Updated)
   =================== */

.agent-activity-console {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #0a0e1a;
}

.agent-activity-console__header {
  padding: 8px 16px;
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border-bottom: 1px solid var(--border-color, #1e293b);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.agent-activity-console__body {
  flex: 1;
  overflow-y: auto;
  padding: 8px 16px;
  font-family: 'SF Mono', Monaco, Consolas, monospace;
  font-size: 0.875rem;
}

/* ===================
   Animations
   =================== */

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.function-entry.new {
  animation: slideIn 0.3s ease;
}

/* ===================
   Responsive
   =================== */

@media (max-width: 1024px) {
  .plan-section__body {
    grid-template-columns: 1fr;
  }

  .plan-section__toc {
    border-right: none;
    border-bottom: 1px solid var(--border-color, #1e293b);
    max-height: 150px;
  }
}

@media (max-width: 768px) {
  .flexible-zone {
    padding: 8px;
    gap: 8px;
  }

  .plan-section {
    min-height: 200px;
  }

  .function-activity {
    min-height: 250px;
  }

  .fixed-zone {
    height: 150px;
  }
}

/* ===================
   CSS Variables
   =================== */

:root {
  --bg-primary: #0a0e17;
  --bg-secondary: #111827;
  --bg-tertiary: #0f172a;
  --border-color: #1e293b;
  --text-primary: #f9fafb;
  --text-secondary: #9ca3af;
  --text-muted: #64748b;
  --accent-blue: #3b82f6;
  --accent-gold: #f59e0b;
  --status-success: #10b981;
  --status-error: #ef4444;
  --status-warning: #f59e0b;
}
"""

        layout_rules = {
            "hierarchy": [
                "1. Header (fixed top)",
                "2. Flexible Zone (scrollable middle)",
                "   - Plan Section",
                "   - Function Activity Section",
                "   - [Future sections insert here]",
                "3. Fixed Zone (sticky bottom)",
                "   - Agent Activity Console"
            ],
            "insertion_rule": "New sections ALWAYS insert above Activity Console",
            "z_index": {
                "header": 50,
                "flexible_content": 1,
                "activity_console": 10,
                "modals": 100,
                "expanded_plan": 100
            },
            "breakpoints": {
                "mobile": "max-width: 768px",
                "tablet": "max-width: 1024px",
                "desktop": "min-width: 1025px"
            }
        }

        return {
            "message": "Layout and CSS specification",
            "css": css_spec,
            "layout_rules": layout_rules,
            "variables": {
                "bg_primary": "#0a0e17",
                "bg_secondary": "#111827",
                "bg_tertiary": "#0f172a",
                "border_color": "#1e293b",
                "text_primary": "#f9fafb",
                "status_success": "#10b981",
                "status_error": "#ef4444"
            }
        }

    def _dashboard_export_specs(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Export all dashboard specifications to files."""
        export_path = self.memory_path / "dashboard-exports"
        export_path.mkdir(parents=True, exist_ok=True)

        exported_files = []
        timestamp = datetime.utcnow().strftime("%Y%m%d")

        # Export full spec
        full_spec = self._dashboard_full_spec({"role": "ALL"})
        full_spec_path = export_path / f"dashboard-full-spec-{timestamp}.md"
        with open(full_spec_path, 'w') as f:
            f.write(full_spec.get("spec", ""))
        exported_files.append(str(full_spec_path))

        # Export CSS
        layout_spec = self._dashboard_layout_spec({})
        css_path = export_path / f"dashboard-styles-{timestamp}.css"
        with open(css_path, 'w') as f:
            f.write(layout_spec.get("css", ""))
        exported_files.append(str(css_path))

        # Export component specs as JSON
        plan_spec = self._dashboard_plan_section_spec({"role": "CEO"})
        activity_spec = self._dashboard_activity_section_spec({"role": "ALL"})

        components_path = export_path / f"dashboard-components-{timestamp}.json"
        with open(components_path, 'w') as f:
            json.dump({
                "plan_section": plan_spec.get("spec"),
                "function_activity": activity_spec.get("spec"),
                "layout_rules": layout_spec.get("layout_rules")
            }, f, indent=2, default=str)
        exported_files.append(str(components_path))

        self._log_session("dashboard", {
            "action": "export",
            "files": exported_files
        })

        return {
            "message": "Dashboard specifications exported",
            "exported_files": exported_files,
            "export_directory": str(export_path),
            "next_step": "Review specs and request GREENLIGHT: DASHBOARD from human"
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

    agent = CMOAgent(factory_id=factory_id)
    result = agent.run(command, payload)
    return result


if __name__ == "__main__":
    import sys
    agent = CMOAgent()

    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [payload_json]")
        print("Commands: cmo.validate, cmo.strategy, cmo.campaign, cmo.content, cmo.brand, cmo.approve, cmo.logo, cmo.tiktok, cmo.website, cmo.dashboard")
        print("\nDashboard actions:")
        print("  cmo.dashboard '{\"action\": \"spec\"}'       - Full dashboard spec")
        print("  cmo.dashboard '{\"action\": \"plan\"}'       - Plan section spec")
        print("  cmo.dashboard '{\"action\": \"activity\"}'   - Function activity spec")
        print("  cmo.dashboard '{\"action\": \"layout\"}'     - CSS/layout spec")
        print("  cmo.dashboard '{\"action\": \"export\"}'     - Export all specs")
        sys.exit(1)

    command = sys.argv[1]
    payload = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    result = agent.run(command, payload)
    print(json.dumps(result, indent=2))

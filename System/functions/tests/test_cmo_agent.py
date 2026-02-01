"""
Unit tests for CMO Agent.
"""

import os
import sys
import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from conftest import load_agent_module

# Load CMO agent module
cmo_module = load_agent_module('cmo')
CMOAgent = cmo_module.CMOAgent


class TestCMOAgentInitialization:
    """Test CMO agent initialization."""

    def test_agent_initialization(self):
        """Test that CMO agent initializes correctly."""
        agent = CMOAgent()
        assert agent.agent_id == "CMO"
        assert agent.role == "Chief Marketing Officer"

    def test_agent_with_custom_factory_id(self):
        """Test agent initialization with custom factory ID."""
        agent = CMOAgent(factory_id="test-factory")
        assert agent.factory_id == "test-factory"


class TestCMOValidateCommand:
    """Test CMO validate command (CRITICAL GATE)."""

    def test_validate_proceed_decision(self, temp_project_root):
        """Test validation with PROCEED decision."""
        with patch.object(CMOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CMOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CMO" / ".cmo" / "memory"

            result = agent.cmo_validate({
                "action": "record",
                "results": {
                    "signups": 150,
                    "target_signups": 100,
                    "cost_per_signup": 4,
                    "max_cost_per_signup": 5,
                    "engagement_rate": 5,
                    "min_engagement_rate": 3
                }
            })

            assert result["gate_decision"] == "PROCEED"
            assert result["criteria_met"] == "3/3"

    def test_validate_pivot_decision(self, temp_project_root):
        """Test validation with PIVOT decision."""
        with patch.object(CMOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CMOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CMO" / ".cmo" / "memory"

            result = agent.cmo_validate({
                "action": "record",
                "results": {
                    "signups": 20,
                    "target_signups": 100,
                    "cost_per_signup": 25,
                    "max_cost_per_signup": 5,
                    "engagement_rate": 1,
                    "min_engagement_rate": 3
                }
            })

            assert result["gate_decision"] == "PIVOT"
            assert "escalate" in result

    def test_validate_iterate_decision(self, temp_project_root):
        """Test validation with ITERATE decision."""
        with patch.object(CMOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CMOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CMO" / ".cmo" / "memory"

            result = agent.cmo_validate({
                "action": "record",
                "results": {
                    "signups": 90,  # Close but not met
                    "target_signups": 100,
                    "cost_per_signup": 4,
                    "max_cost_per_signup": 5,
                    "engagement_rate": 4,
                    "min_engagement_rate": 3
                }
            })

            assert result["gate_decision"] == "ITERATE"

    def test_validate_status_no_results(self, temp_project_root):
        """Test validation status with no results."""
        with patch.object(CMOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CMOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CMO" / ".cmo" / "memory"

            result = agent.cmo_validate({"action": "status"})

            assert "No validation results" in result["message"]


class TestCMOApproveCommand:
    """Test CMO approve command."""

    def test_approve_requires_validation(self, temp_project_root):
        """Test that approve requires validation first."""
        with patch.object(CMOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CMOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CMO" / ".cmo" / "memory"

            result = agent.cmo_approve({})

            assert "error" in result
            assert "validation" in result["message"].lower()

    def test_approve_requires_proceed(self, temp_project_root):
        """Test that approve requires PROCEED decision."""
        with patch.object(CMOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CMOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CMO" / ".cmo" / "memory"

            # Create a PIVOT validation result
            agent.memory_path.mkdir(parents=True, exist_ok=True)
            result_file = agent.memory_path / "validation-results-2024-01-01.md"
            result_file.write_text("# Validation\n\n## GATE DECISION: PIVOT")

            result = agent.cmo_approve({})

            assert "error" in result
            assert "PROCEED" in result["message"]


class TestCMOStrategyCommand:
    """Test CMO strategy command."""

    @patch.object(CMOAgent, '_think')
    @patch.object(CMOAgent, '_load_business_plan')
    @patch.object(CMOAgent, '_load_ceo_brief')
    def test_strategy_generation(self, mock_brief, mock_plan, mock_think, temp_project_root):
        """Test marketing strategy generation."""
        mock_plan.return_value = "# Business Plan"
        mock_brief.return_value = "# CEO Brief"
        mock_think.return_value = "# Marketing Strategy\n\nContent..."

        with patch.object(CMOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CMOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CMO" / ".cmo" / "memory"

            result = agent.cmo_strategy({})

            assert "strategy" in result
            assert "saved_to" in result


class TestCMOCampaignCommand:
    """Test CMO campaign command."""

    def test_campaign_create(self):
        """Test campaign creation."""
        agent = CMOAgent()
        result = agent.cmo_campaign({
            "action": "create",
            "platform": "tiktok",
            "budget": 500
        })

        assert "campaign" in result
        assert result["campaign"]["platform"] == "tiktok"
        assert result["campaign"]["budget"] == 500

    def test_campaign_status(self):
        """Test campaign status check."""
        agent = CMOAgent()
        result = agent.cmo_campaign({"action": "status"})

        assert "active_campaigns" in result


class TestCMOContentCommand:
    """Test CMO content command."""

    @patch.object(CMOAgent, '_think')
    @patch.object(CMOAgent, '_load_business_plan')
    def test_content_generation(self, mock_plan, mock_think):
        """Test content generation."""
        mock_plan.return_value = "# Business Plan"
        mock_think.return_value = "Generated social media content..."

        agent = CMOAgent()
        result = agent.cmo_content({
            "type": "social",
            "topic": "product launch"
        })

        assert "content" in result
        assert result["content_type"] == "social"


class TestCMOBrandCommand:
    """Test CMO brand command."""

    @patch.object(CMOAgent, '_think')
    @patch.object(CMOAgent, '_load_business_plan')
    def test_brand_guidelines(self, mock_plan, mock_think):
        """Test brand guidelines generation."""
        mock_plan.return_value = "# Business Plan"
        mock_think.return_value = "# Brand Guidelines\n\nVoice: Professional..."

        agent = CMOAgent()
        result = agent.cmo_brand({"action": "guidelines"})

        assert "guidelines" in result


class TestCMOLogoCommand:
    """Test CMO logo command."""

    def test_logo_status_no_concepts(self, temp_project_root):
        """Test logo status with no concepts."""
        with patch.object(CMOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CMOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CMO" / ".cmo" / "memory"

            result = agent.cmo_logo({"action": "status"})

            assert "No logo concepts" in result["message"]

    @patch.object(CMOAgent, '_think')
    @patch.object(CMOAgent, '_load_business_plan')
    def test_logo_generate(self, mock_plan, mock_think, temp_project_root):
        """Test logo concept generation."""
        mock_plan.return_value = "# Test Business\n\nContent..."
        mock_think.return_value = "# Logo Concepts\n\n## Concept 1..."

        with patch.object(CMOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CMOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CMO" / ".cmo" / "memory"

            result = agent.cmo_logo({
                "action": "generate",
                "concept": "Modern tech",
                "variations": 3
            })

            assert "logo_id" in result
            assert "concepts" in result
            assert result["approval_required"] == "GREENLIGHT: BRAND from human"

    def test_logo_variations(self):
        """Test logo variation types."""
        agent = CMOAgent()
        result = agent.cmo_logo({
            "action": "variations",
            "logo_id": "LOGO-001"
        })

        assert "available_types" in result
        assert "primary" in result["available_types"]
        assert "icon" in result["available_types"]

    def test_logo_export(self):
        """Test logo export specifications."""
        agent = CMOAgent()
        result = agent.cmo_logo({
            "action": "export",
            "logo_id": "LOGO-001"
        })

        assert "export_formats" in result
        assert "svg" in result["export_formats"]


class TestCMOTiktokCommand:
    """Test CMO TikTok command."""

    @patch.object(CMOAgent, '_think')
    @patch.object(CMOAgent, '_load_business_plan')
    def test_tiktok_create(self, mock_plan, mock_think):
        """Test TikTok content creation."""
        mock_plan.return_value = "# Business Plan"
        mock_think.return_value = "# TikTok Script\n\nHOOK: ..."

        agent = CMOAgent()
        result = agent.cmo_tiktok({
            "action": "create",
            "concept": "Product demo"
        })

        assert "post_id" in result
        assert "script" in result
        assert result["approval_required"] == True

    def test_tiktok_trend(self):
        """Test TikTok trend research."""
        agent = CMOAgent()
        result = agent.cmo_tiktok({
            "action": "trend",
            "query": "AI products"
        })

        assert "trending_formats" in result
        assert "recommended_hashtags" in result
        assert "optimal_posting_times" in result

    def test_tiktok_schedule(self):
        """Test TikTok scheduling."""
        agent = CMOAgent()
        result = agent.cmo_tiktok({
            "action": "schedule",
            "post_id": "TT-001",
            "time": "2024-02-01T10:00:00Z"
        })

        assert result["status"] == "pending_approval"

    def test_tiktok_analytics(self):
        """Test TikTok analytics."""
        agent = CMOAgent()
        result = agent.cmo_tiktok({
            "action": "analytics",
            "period": "30d"
        })

        assert "metrics" in result
        assert "audience_insights" in result

    def test_tiktok_optimize(self):
        """Test TikTok optimization."""
        agent = CMOAgent()
        result = agent.cmo_tiktok({
            "action": "optimize",
            "post_id": "TT-001"
        })

        assert "optimization_tips" in result
        assert "a_b_test_suggestions" in result


class TestCMOWebsiteCommand:
    """Test CMO website command."""

    @patch.object(CMOAgent, '_think')
    @patch.object(CMOAgent, '_load_business_plan')
    def test_website_spec(self, mock_plan, mock_think, temp_project_root):
        """Test website specification generation."""
        mock_plan.return_value = "# Business Plan"
        mock_think.return_value = "# Website Specification\n\nContent..."

        with patch.object(CMOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CMOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CMO" / ".cmo" / "memory"

            result = agent.cmo_website({
                "action": "spec",
                "type": "marketing"
            })

            assert "spec" in result
            assert "next_steps" in result

    @patch.object(CMOAgent, '_think')
    @patch.object(CMOAgent, '_load_business_plan')
    def test_website_landing(self, mock_plan, mock_think):
        """Test landing page specification."""
        mock_plan.return_value = "# Business Plan"
        mock_think.return_value = "# Landing Page\n\nHero section..."

        agent = CMOAgent()
        result = agent.cmo_website({
            "action": "landing",
            "goal": "lead_capture"
        })

        assert "spec" in result
        assert "conversion_tips" in result

    def test_website_checklist(self):
        """Test website launch checklist."""
        agent = CMOAgent()
        result = agent.cmo_website({"action": "checklist"})

        assert "pre_launch" in result
        assert "launch" in result
        assert "post_launch" in result
        assert result["approval_required"] == "GREENLIGHT from human before launch"


class TestCMOCommandDispatch:
    """Test CMO command dispatch."""

    def test_run_dispatches_validate(self):
        """Test dispatch to validate command."""
        with patch.object(CMOAgent, 'cmo_validate') as mock_cmd:
            mock_cmd.return_value = {"test": "result"}

            agent = CMOAgent()
            result = agent.run("cmo.validate", {})

            mock_cmd.assert_called_once()

    def test_run_dispatches_logo(self):
        """Test dispatch to logo command."""
        with patch.object(CMOAgent, 'cmo_logo') as mock_cmd:
            mock_cmd.return_value = {"test": "result"}

            agent = CMOAgent()
            result = agent.run("cmo.logo", {})

            mock_cmd.assert_called_once()

    def test_run_dispatches_tiktok(self):
        """Test dispatch to tiktok command."""
        with patch.object(CMOAgent, 'cmo_tiktok') as mock_cmd:
            mock_cmd.return_value = {"test": "result"}

            agent = CMOAgent()
            result = agent.run("cmo.tiktok", {})

            mock_cmd.assert_called_once()

    def test_run_dispatches_website(self):
        """Test dispatch to website command."""
        with patch.object(CMOAgent, 'cmo_website') as mock_cmd:
            mock_cmd.return_value = {"test": "result"}

            agent = CMOAgent()
            result = agent.run("cmo.website", {})

            mock_cmd.assert_called_once()

    def test_run_dispatches_dashboard(self):
        """Test dispatch to dashboard command."""
        with patch.object(CMOAgent, 'cmo_dashboard') as mock_cmd:
            mock_cmd.return_value = {"test": "result"}

            agent = CMOAgent()
            result = agent.run("cmo.dashboard", {})

            mock_cmd.assert_called_once()


class TestCMODashboardCommand:
    """Test CMO dashboard specification command."""

    def test_dashboard_full_spec(self, temp_project_root):
        """Test full dashboard specification generation."""
        with patch.object(CMOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CMOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CMO" / ".cmo" / "memory"

            result = agent.cmo_dashboard({"action": "spec"})

            assert "spec" in result
            assert "Plan Section" in result["components"]
            assert "Function Activity Section" in result["components"]
            assert result["status"] == "awaiting_approval"
            assert "saved_to" in result

    def test_dashboard_full_spec_role_specific(self, temp_project_root):
        """Test dashboard spec for specific role."""
        with patch.object(CMOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CMOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CMO" / ".cmo" / "memory"

            result = agent.cmo_dashboard({"action": "spec", "role": "CFO"})

            assert "CFO" in result["spec"]

    def test_dashboard_plan_section_spec(self):
        """Test plan section component specification."""
        agent = CMOAgent()
        result = agent.cmo_dashboard({
            "action": "plan",
            "role": "CEO"
        })

        assert "spec" in result
        assert result["spec"]["component"] == "PlanSection"
        assert result["role"] == "CEO"
        assert "C-Suites/CEO/README.md" in result["plan_document"]

    def test_dashboard_plan_section_spec_all_roles(self):
        """Test plan section spec contains role mapping."""
        agent = CMOAgent()
        roles = ["CEO", "CFO", "CMO", "COO", "CIO", "CLO", "CPO", "CTO", "CXA"]

        for role in roles:
            result = agent.cmo_dashboard({
                "action": "plan",
                "role": role
            })
            assert result["role"] == role
            assert role in result["plan_document"]

    def test_dashboard_activity_section_spec(self):
        """Test function activity section specification."""
        agent = CMOAgent()
        result = agent.cmo_dashboard({"action": "activity"})

        assert "spec" in result
        assert result["spec"]["component"] == "FunctionActivitySection"
        assert "entry_states" in result["spec"]
        assert "running" in result["spec"]["entry_states"]
        assert "success" in result["spec"]["entry_states"]
        assert "error" in result["spec"]["entry_states"]

    def test_dashboard_activity_section_behavior(self):
        """Test activity section behavior specification."""
        agent = CMOAgent()
        result = agent.cmo_dashboard({"action": "activity"})

        behavior = result["spec"]["behavior"]
        assert behavior["sort_order"] == "newest_first"
        assert behavior["insert_position"] == "prepend"
        assert behavior["max_entries"] == 50

    def test_dashboard_layout_spec(self):
        """Test layout and CSS specification."""
        agent = CMOAgent()
        result = agent.cmo_dashboard({"action": "layout"})

        assert "css" in result
        assert "layout_rules" in result
        assert ".dashboard-content" in result["css"]
        assert ".flexible-zone" in result["css"]
        assert ".fixed-zone" in result["css"]
        assert ".plan-section" in result["css"]
        assert ".function-activity" in result["css"]

    def test_dashboard_layout_hierarchy(self):
        """Test layout hierarchy rules."""
        agent = CMOAgent()
        result = agent.cmo_dashboard({"action": "layout"})

        rules = result["layout_rules"]
        assert "hierarchy" in rules
        assert "insertion_rule" in rules
        assert "Activity Console" in rules["insertion_rule"]

    def test_dashboard_export_specs(self, temp_project_root):
        """Test exporting all dashboard specifications."""
        with patch.object(CMOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CMOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CMO" / ".cmo" / "memory"

            result = agent.cmo_dashboard({"action": "export"})

            assert "exported_files" in result
            assert len(result["exported_files"]) == 3  # full spec, css, components
            assert "export_directory" in result

    def test_dashboard_unknown_action(self):
        """Test unknown action returns error."""
        agent = CMOAgent()
        result = agent.cmo_dashboard({"action": "unknown"})

        assert "error" in result

    def test_role_plan_mapping_exists(self):
        """Test that role to plan mapping is defined."""
        agent = CMOAgent()
        mapping = agent.ROLE_PLAN_MAPPING

        expected_roles = ["CEO", "CFO", "CMO", "COO", "CIO", "CLO", "CPO", "CTO", "CXA"]
        for role in expected_roles:
            assert role in mapping
            assert "path" in mapping[role]
            assert "title" in mapping[role]

    def test_dashboard_spec_contains_wireframe(self, temp_project_root):
        """Test that full spec contains wireframe diagrams."""
        with patch.object(CMOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CMOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CMO" / ".cmo" / "memory"

            result = agent.cmo_dashboard({"action": "spec"})

            spec = result["spec"]
            assert "┌─" in spec  # Contains ASCII box drawing
            assert "FLEXIBLE ZONE" in spec
            assert "FIXED ZONE" in spec

    def test_dashboard_activity_states_have_icons(self):
        """Test that all activity states have icons and colors."""
        agent = CMOAgent()
        result = agent.cmo_dashboard({"action": "activity"})

        states = result["spec"]["entry_states"]
        for state_name, state_config in states.items():
            assert "icon" in state_config
            assert "color" in state_config
            assert "badge" in state_config

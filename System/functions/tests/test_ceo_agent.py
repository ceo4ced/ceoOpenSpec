"""
Unit tests for CEO Agent.
"""

import os
import sys
import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from conftest import load_agent_module

# Load CEO agent module
ceo_module = load_agent_module('ceo')
CEOAgent = ceo_module.CEOAgent


class TestCEOAgentInitialization:
    """Test CEO agent initialization."""

    def test_agent_initialization(self):
        """Test that CEO agent initializes correctly."""
        agent = CEOAgent()
        assert agent.agent_id == "CEO"
        assert agent.role == "Chief Executive Officer"
        assert agent.factory_id == "development"

    def test_agent_with_custom_factory_id(self):
        """Test agent initialization with custom factory ID."""
        agent = CEOAgent(factory_id="test-factory")
        assert agent.factory_id == "test-factory"

    def test_vision_questions_defined(self):
        """Test that vision questions are properly defined."""
        agent = CEOAgent()
        assert len(agent.VISION_QUESTIONS) == 8
        assert all("category" in q for q in agent.VISION_QUESTIONS)
        assert all("question" in q for q in agent.VISION_QUESTIONS)

    def test_high_risk_domains_defined(self):
        """Test that high-risk domains are defined."""
        agent = CEOAgent()
        assert "minors" in agent.HIGH_RISK_DOMAINS
        assert "healthcare" in agent.HIGH_RISK_DOMAINS
        assert "finance" in agent.HIGH_RISK_DOMAINS


class TestCEOVisionCommand:
    """Test CEO vision command."""

    def test_vision_start_action(self):
        """Test starting vision gathering."""
        with patch.object(CEOAgent, '_load_vision', return_value=None):
            agent = CEOAgent()
            result = agent.ceo_vision({"action": "start"})

            assert "question" in result
            assert result["question"]["index"] == 0
            assert result["question"]["category"] == "Problem"
            assert result["total_questions"] == 8
            assert result["next_action"] == "respond"

    def test_vision_start_with_existing_vision(self):
        """Test starting when vision exists."""
        existing = {"raw": "# Existing Vision\nContent here...", "exists": True}
        with patch.object(CEOAgent, '_load_vision', return_value=existing):
            agent = CEOAgent()
            result = agent.ceo_vision({"action": "start"})

            assert "existing_vision" in result
            assert "options" in result
            assert "update" in result["options"]

    def test_vision_respond_advances_question(self):
        """Test that responding advances to next question."""
        with patch.object(CEOAgent, '_load_vision', return_value=None):
            agent = CEOAgent()
            result = agent.ceo_vision({
                "action": "respond",
                "user_input": "We solve content creation problems",
                "question_index": 0,
                "responses": {},
                "conversation_history": []
            })

            assert result["question"]["index"] == 1
            assert "Problem" in result["responses"]

    def test_vision_detect_high_risk_minors(self):
        """Test high-risk detection for minors."""
        agent = CEOAgent()
        risks = agent._detect_high_risk_domains("We serve children and kids under 18")

        assert len(risks) > 0
        assert any(r["domain"] == "minors" for r in risks)
        assert any("COPPA" in r["regulations"] for r in risks)

    def test_vision_detect_high_risk_healthcare(self):
        """Test high-risk detection for healthcare."""
        agent = CEOAgent()
        risks = agent._detect_high_risk_domains("Our product handles patient medical records")

        assert len(risks) > 0
        assert any(r["domain"] == "healthcare" for r in risks)
        assert any("HIPAA" in r["regulations"] for r in risks)


class TestCEOPlanCommand:
    """Test CEO plan command."""

    def test_plan_requires_vision(self):
        """Test that plan requires vision document."""
        with patch.object(CEOAgent, '_load_vision', return_value=None):
            agent = CEOAgent()
            result = agent.ceo_plan({})

            assert "error" in result
            assert "vision" in result["message"].lower()

    @patch.object(CEOAgent, '_think')
    @patch.object(CEOAgent, '_load_vision')
    @patch.object(CEOAgent, '_load_mission_files')
    def test_plan_generation(self, mock_mission, mock_vision, mock_think):
        """Test business plan generation."""
        mock_vision.return_value = {"raw": "# Vision\nTest content", "exists": True}
        mock_mission.return_value = "Test mission"
        mock_think.return_value = "# Test Business Plan\n\nGenerated content..."

        agent = CEOAgent()
        result = agent.ceo_plan({})

        assert "business_plan" in result
        mock_think.assert_called_once()


class TestCEOPropagateCommand:
    """Test CEO propagate command."""

    def test_propagate_requires_plan(self, temp_project_root):
        """Test that propagate requires business plan."""
        with patch.object(CEOAgent, '_get_project_root', return_value=temp_project_root):
            # Remove README
            readme = temp_project_root / "README.md"
            if readme.exists():
                readme.unlink()

            agent = CEOAgent()
            result = agent.ceo_propagate({})

            assert "error" in result

    @patch.object(CEOAgent, '_think')
    @patch.object(CEOAgent, '_generate_position_brief')
    def test_propagate_briefs_all_positions(self, mock_brief, mock_think, temp_project_root):
        """Test that propagate creates briefs for all positions."""
        mock_brief.return_value = "# Test Brief\n\nContent..."

        with patch.object(CEOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CEOAgent()
            result = agent.ceo_propagate({})

            assert "positions_briefed" in result
            assert "CFO" in result["positions_briefed"]
            assert "CMO" in result["positions_briefed"]
            assert "CTO" in result["positions_briefed"]


class TestCEOOnboardCommand:
    """Test CEO onboard command."""

    def test_onboard_start(self):
        """Test onboarding start."""
        agent = CEOAgent()
        result = agent.ceo_onboard({"action": "start"})

        assert result["phase"] == 1
        assert "fields" in result
        assert any(f["name"] == "business_name" for f in result["fields"])

    def test_onboard_status(self, temp_project_root):
        """Test onboarding status check."""
        with patch.object(CEOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CEOAgent()
            # Update memory path to temp
            agent.memory_path = temp_project_root / "C-Suites" / "CEO" / ".ceo" / "memory"

            result = agent.ceo_onboard({"action": "status"})

            assert "status" in result
            assert "next_phase" in result["status"]


class TestCEOInquireCommand:
    """Test CEO inquire command."""

    def test_inquire_requires_question(self):
        """Test that inquire requires a question."""
        agent = CEOAgent()
        result = agent.ceo_inquire({"from": "CFO"})

        assert "error" in result

    def test_inquire_escalation_triggers(self):
        """Test that certain inquiries trigger escalation."""
        with patch.object(CEOAgent, '_load_vision', return_value=None):
            with patch.object(CEOAgent, '_escalate_to_founder') as mock_escalate:
                mock_escalate.return_value = {"escalated": True}

                agent = CEOAgent()
                result = agent.ceo_inquire({
                    "from": "CFO",
                    "type": "decision",
                    "subject": "Budget Approval",
                    "question": "Can we approve this budget increase?"
                })

                mock_escalate.assert_called_once()


class TestCEOReportCommand:
    """Test CEO report command."""

    def test_report_generation(self, temp_project_root):
        """Test status report generation."""
        with patch.object(CEOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CEOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CEO" / ".ceo" / "memory"

            result = agent.ceo_report({"format": "full"})

            assert "report" in result
            assert "positions" in result
            assert "CEO" in result["positions"]

    def test_report_shows_cto_gated(self, temp_project_root):
        """Test that report shows CTO as gated."""
        with patch.object(CEOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CEOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CEO" / ".ceo" / "memory"

            result = agent.ceo_report({})

            assert result["positions"]["CTO"]["status"] == "gated"


class TestCEOCommandDispatch:
    """Test CEO command dispatch."""

    def test_run_dispatches_to_correct_method(self):
        """Test that run() dispatches to correct command method."""
        with patch.object(CEOAgent, 'ceo_vision') as mock_vision:
            mock_vision.return_value = {"test": "result"}

            agent = CEOAgent()
            result = agent.run("ceo.vision", {"action": "start"})

            mock_vision.assert_called_once_with({"action": "start"})
            assert result["status"] == "success"

    def test_run_unknown_command(self):
        """Test handling of unknown commands."""
        agent = CEOAgent()
        result = agent.run("ceo.unknown", {})

        assert result["status"] == "error"
        assert "not implemented" in result["error"]

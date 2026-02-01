"""
Unit tests for CPO Agent.
"""

import os
import sys
import pytest
from unittest.mock import patch

from conftest import load_agent_module

# Load CPO agent module
cpo_module = load_agent_module('cpo')
CPOAgent = cpo_module.CPOAgent


class TestCPOAgentInitialization:
    """Test CPO agent initialization."""

    def test_agent_initialization(self):
        """Test that CPO agent initializes correctly."""
        agent = CPOAgent()
        assert agent.agent_id == "CPO"
        assert agent.role == "Chief Product Officer"


class TestCPOPrdCommand:
    """Test CPO PRD command."""

    @patch.object(CPOAgent, '_think')
    @patch.object(CPOAgent, '_load_business_plan')
    def test_prd_generation(self, mock_plan, mock_think, temp_project_root):
        """Test PRD generation."""
        mock_plan.return_value = "# Business Plan"
        mock_think.return_value = "# PRD: Core Product\n\nContent..."

        with patch.object(CPOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CPOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CPO" / ".cpo" / "memory"

            result = agent.cpo_prd({"feature": "Core Product"})

            assert "prd" in result
            assert "prd_id" in result
            assert "saved_to" in result


class TestCPORoadmapCommand:
    """Test CPO roadmap command."""

    @patch.object(CPOAgent, '_think')
    @patch.object(CPOAgent, '_load_business_plan')
    def test_roadmap_generation(self, mock_plan, mock_think, temp_project_root):
        """Test roadmap generation."""
        mock_plan.return_value = "# Business Plan"
        mock_think.return_value = "# Product Roadmap\n\nContent..."

        with patch.object(CPOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CPOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CPO" / ".cpo" / "memory"

            result = agent.cpo_roadmap({"horizon": "6_months"})

            assert "roadmap" in result


class TestCPOMetricsCommand:
    """Test CPO metrics command."""

    @patch.object(CPOAgent, '_think')
    @patch.object(CPOAgent, '_load_business_plan')
    def test_metrics_framework(self, mock_plan, mock_think):
        """Test metrics framework generation."""
        mock_plan.return_value = "# Business Plan"
        mock_think.return_value = "# Metrics Framework\n\nNorth Star: ..."

        agent = CPOAgent()
        result = agent.cpo_metrics({})

        assert "metrics" in result


class TestCPOOnepagerCommand:
    """Test CPO one-pager command."""

    def test_onepager_requires_feature(self):
        """Test one-pager requires feature name."""
        agent = CPOAgent()
        result = agent.cpo_onepager({})

        assert "error" in result

    @patch.object(CPOAgent, '_think')
    def test_onepager_generation(self, mock_think):
        """Test one-pager generation."""
        mock_think.return_value = "# Feature One-Pager\n\nProblem: ..."

        agent = CPOAgent()
        result = agent.cpo_onepager({"feature": "User Dashboard"})

        assert "onepager" in result
        assert result["feature"] == "User Dashboard"


class TestCPODecideCommand:
    """Test CPO decide command."""

    def test_decide_requires_decision(self):
        """Test decide requires decision question."""
        agent = CPOAgent()
        result = agent.cpo_decide({})

        assert "error" in result

    @patch.object(CPOAgent, '_think')
    def test_decide_analysis(self, mock_think):
        """Test decision analysis."""
        mock_think.return_value = "# Decision Analysis\n\nOptions: ..."

        agent = CPOAgent()
        result = agent.cpo_decide({
            "decision": "Should we build mobile or web first?",
            "options": ["Mobile", "Web", "Both"]
        })

        assert "analysis" in result
        assert result["decision"] == "Should we build mobile or web first?"


class TestCPOCommandDispatch:
    """Test CPO command dispatch."""

    def test_run_all_commands(self):
        """Test that all commands dispatch correctly."""
        agent = CPOAgent()
        commands = ["cpo.prd", "cpo.roadmap", "cpo.metrics", "cpo.onepager", "cpo.decide"]

        for cmd in commands:
            with patch.object(agent, cmd.replace(".", "_")) as mock_cmd:
                mock_cmd.return_value = {"test": "result"}
                result = agent.run(cmd, {})
                mock_cmd.assert_called_once()

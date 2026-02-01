"""
Unit tests for CFO Agent.
"""

import os
import sys
import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from conftest import load_agent_module

# Load CFO agent module
cfo_module = load_agent_module('cfo')
CFOAgent = cfo_module.CFOAgent


class TestCFOAgentInitialization:
    """Test CFO agent initialization."""

    def test_agent_initialization(self):
        """Test that CFO agent initializes correctly."""
        agent = CFOAgent()
        assert agent.agent_id == "CFO"
        assert agent.role == "Chief Financial Officer"

    def test_agent_with_custom_factory_id(self):
        """Test agent initialization with custom factory ID."""
        agent = CFOAgent(factory_id="test-factory")
        assert agent.factory_id == "test-factory"


class TestCFOBudgetCommand:
    """Test CFO budget command."""

    def test_budget_requires_business_plan(self):
        """Test that budget requires business plan."""
        with patch.object(CFOAgent, '_load_business_plan', return_value=None):
            agent = CFOAgent()
            result = agent.cfo_budget({})

            assert "error" in result

    @patch.object(CFOAgent, '_think')
    @patch.object(CFOAgent, '_load_business_plan')
    @patch.object(CFOAgent, '_load_ceo_brief')
    def test_budget_generation(self, mock_brief, mock_plan, mock_think, temp_project_root):
        """Test budget generation with valid plan."""
        mock_plan.return_value = "# Test Business Plan"
        mock_brief.return_value = "# CEO Brief"
        mock_think.return_value = "# Financial Projections\n\nTest budget content..."

        with patch.object(CFOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CFOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CFO" / ".cfo" / "memory"

            result = agent.cfo_budget({})

            assert "budget" in result
            assert "saved_to" in result
            mock_think.assert_called_once()


class TestCFOTokensCommand:
    """Test CFO tokens command."""

    def test_tokens_report(self):
        """Test token usage report generation."""
        agent = CFOAgent()
        result = agent.cfo_tokens({"action": "report", "period": "today"})

        assert "report" in result
        assert result["period"] == "today"

    def test_tokens_default_period(self):
        """Test tokens uses default period."""
        agent = CFOAgent()
        result = agent.cfo_tokens({})

        assert result["period"] == "today"


class TestCFOPaymentsCommand:
    """Test CFO payments command."""

    def test_payments_status(self):
        """Test payment status check."""
        agent = CFOAgent()
        result = agent.cfo_payments({"action": "status"})

        assert "stripe_connected" in result
        assert "pending_invoices" in result

    def test_payments_unknown_action(self):
        """Test unknown payment action."""
        agent = CFOAgent()
        result = agent.cfo_payments({"action": "unknown"})

        assert "unknown" in result["message"]


class TestCFOForecastCommand:
    """Test CFO forecast command."""

    @patch.object(CFOAgent, '_think')
    @patch.object(CFOAgent, '_load_business_plan')
    def test_forecast_generation(self, mock_plan, mock_think, temp_project_root):
        """Test forecast generation."""
        mock_plan.return_value = "# Business Plan"
        mock_think.return_value = "# 12-Month Forecast\n\nContent..."

        with patch.object(CFOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CFOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CFO" / ".cfo" / "memory"

            result = agent.cfo_forecast({"horizon": "12_months"})

            assert "forecast" in result

    def test_forecast_default_horizon(self):
        """Test forecast uses default horizon."""
        with patch.object(CFOAgent, '_think', return_value="Mock forecast"):
            with patch.object(CFOAgent, '_load_business_plan', return_value="Plan"):
                agent = CFOAgent()
                result = agent.cfo_forecast({})

                # Default horizon should be 12_months
                assert "12_months" in result.get("message", "")


class TestCFOComplianceCommand:
    """Test CFO compliance command."""

    def test_compliance_check(self):
        """Test financial compliance check."""
        agent = CFOAgent()
        result = agent.cfo_compliance({})

        assert "requirements" in result
        assert len(result["requirements"]) > 0
        assert any(r["item"] == "EIN Registration" for r in result["requirements"])


class TestCFOAnalyzeCommand:
    """Test CFO analyze command."""

    @patch.object(CFOAgent, '_think')
    def test_analyze_generation(self, mock_think, temp_project_root):
        """Test financial analysis generation."""
        mock_think.return_value = "# Financial Analysis\n\nHealth: GREEN"

        with patch.object(CFOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CFOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CFO" / ".cfo" / "memory"

            result = agent.cfo_analyze({"period": "current"})

            assert "analysis" in result
            assert result["period"] == "current"


class TestCFOCommandDispatch:
    """Test CFO command dispatch."""

    def test_run_dispatches_budget(self):
        """Test dispatch to budget command."""
        with patch.object(CFOAgent, 'cfo_budget') as mock_cmd:
            mock_cmd.return_value = {"test": "result"}

            agent = CFOAgent()
            result = agent.run("cfo.budget", {})

            mock_cmd.assert_called_once()

    def test_run_dispatches_tokens(self):
        """Test dispatch to tokens command."""
        with patch.object(CFOAgent, 'cfo_tokens') as mock_cmd:
            mock_cmd.return_value = {"test": "result"}

            agent = CFOAgent()
            result = agent.run("cfo.tokens", {})

            mock_cmd.assert_called_once()

    def test_run_unknown_command(self):
        """Test handling of unknown commands."""
        agent = CFOAgent()
        result = agent.run("cfo.unknown", {})

        assert result["status"] == "error"

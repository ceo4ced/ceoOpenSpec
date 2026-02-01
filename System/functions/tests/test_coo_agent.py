"""
Unit tests for COO Agent.
"""

import os
import sys
import pytest
from unittest.mock import patch

from conftest import load_agent_module

# Load COO agent module
coo_module = load_agent_module('coo')
COOAgent = coo_module.COOAgent


class TestCOOAgentInitialization:
    """Test COO agent initialization."""

    def test_agent_initialization(self):
        """Test that COO agent initializes correctly."""
        agent = COOAgent()
        assert agent.agent_id == "COO"
        assert agent.role == "Chief Operating Officer"


class TestCOOProcessCommand:
    """Test COO process command."""

    @patch.object(COOAgent, '_think')
    @patch.object(COOAgent, '_load_business_plan')
    @patch.object(COOAgent, '_load_ceo_brief')
    def test_process_generation(self, mock_brief, mock_plan, mock_think, temp_project_root):
        """Test operations framework generation."""
        mock_plan.return_value = "# Business Plan"
        mock_brief.return_value = "# CEO Brief"
        mock_think.return_value = "# Operations Framework\n\nContent..."

        with patch.object(COOAgent, '_get_project_root', return_value=temp_project_root):
            agent = COOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "COO" / ".coo" / "memory"

            result = agent.coo_process({})

            assert "framework" in result
            assert "saved_to" in result


class TestCOOWorkforceCommand:
    """Test COO workforce command."""

    @patch.object(COOAgent, '_think')
    @patch.object(COOAgent, '_load_business_plan')
    def test_workforce_planning(self, mock_plan, mock_think, temp_project_root):
        """Test workforce planning."""
        mock_plan.return_value = "# Business Plan"
        mock_think.return_value = "# Workforce Plan\n\nContent..."

        with patch.object(COOAgent, '_get_project_root', return_value=temp_project_root):
            agent = COOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "COO" / ".coo" / "memory"

            result = agent.coo_workforce({})

            assert "plan" in result
            assert "CLO review" in result["note"]


class TestCOOLogisticsCommand:
    """Test COO logistics command."""

    def test_logistics_info(self):
        """Test logistics information."""
        agent = COOAgent()
        result = agent.coo_logistics({})

        assert "digital_operations" in result


class TestCOOQualityCommand:
    """Test COO quality command."""

    def test_quality_framework(self):
        """Test quality management framework."""
        agent = COOAgent()
        result = agent.coo_quality({})

        assert "kpis" in result
        assert len(result["kpis"]) > 0
        assert "processes" in result


class TestCOOCallcenterCommand:
    """Test COO callcenter command."""

    def test_callcenter_status(self):
        """Test call center status."""
        agent = COOAgent()
        result = agent.coo_callcenter({})

        assert "status" in result
        assert "CXA" in result["note"]


class TestCOOCommandDispatch:
    """Test COO command dispatch."""

    def test_run_all_commands(self):
        """Test that all commands dispatch correctly."""
        agent = COOAgent()
        commands = ["coo.process", "coo.workforce", "coo.logistics", "coo.quality", "coo.callcenter"]

        for cmd in commands:
            with patch.object(agent, cmd.replace(".", "_")) as mock_cmd:
                mock_cmd.return_value = {"test": "result"}
                result = agent.run(cmd, {})
                mock_cmd.assert_called_once()

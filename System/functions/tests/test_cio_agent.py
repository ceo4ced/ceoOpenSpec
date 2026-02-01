"""
Unit tests for CIO Agent.
"""

import os
import sys
import pytest
from unittest.mock import patch

from conftest import load_agent_module

# Load CIO agent module
cio_module = load_agent_module('cio')
CIOAgent = cio_module.CIOAgent


class TestCIOAgentInitialization:
    """Test CIO agent initialization."""

    def test_agent_initialization(self):
        """Test that CIO agent initializes correctly."""
        agent = CIOAgent()
        assert agent.agent_id == "CIO"
        assert agent.role == "Chief Information Officer"


class TestCIOSecurityCommand:
    """Test CIO security command."""

    @patch.object(CIOAgent, '_think')
    @patch.object(CIOAgent, '_load_business_plan')
    @patch.object(CIOAgent, '_load_ceo_brief')
    def test_security_framework(self, mock_brief, mock_plan, mock_think, temp_project_root):
        """Test security framework generation."""
        mock_plan.return_value = "# Business Plan"
        mock_brief.return_value = "# CEO Brief"
        mock_think.return_value = "# Security Framework\n\nContent..."

        with patch.object(CIOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CIOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CIO" / ".cio" / "memory"

            result = agent.cio_security({})

            assert "framework" in result
            assert "saved_to" in result


class TestCIODataCommand:
    """Test CIO data governance command."""

    @patch.object(CIOAgent, '_think')
    @patch.object(CIOAgent, '_load_business_plan')
    def test_data_governance(self, mock_plan, mock_think, temp_project_root):
        """Test data governance generation."""
        mock_plan.return_value = "# Business Plan"
        mock_think.return_value = "# Data Governance\n\nContent..."

        with patch.object(CIOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CIOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CIO" / ".cio" / "memory"

            result = agent.cio_data({})

            assert "governance" in result


class TestCIOInfrastructureCommand:
    """Test CIO infrastructure command."""

    def test_infrastructure_info(self):
        """Test infrastructure information."""
        agent = CIOAgent()
        result = agent.cio_infrastructure({})

        assert "stack" in result
        assert "cloud" in result["stack"]
        assert "ai_providers" in result


class TestCIOPrivacyCommand:
    """Test CIO privacy command."""

    def test_privacy_assessment(self):
        """Test privacy assessment."""
        agent = CIOAgent()
        result = agent.cio_privacy({})

        assert "data_collected" in result
        assert "required_documents" in result

    @patch.object(CIOAgent, '_load_business_plan')
    def test_privacy_detects_high_risk(self, mock_plan):
        """Test privacy detects high-risk domains."""
        mock_plan.return_value = "# Business\n\nWe serve children in the EU with healthcare data"

        agent = CIOAgent()
        result = agent.cio_privacy({})

        assert "high_risk_domains" in result
        assert len(result["high_risk_domains"]) > 0


class TestCIOMcpCommand:
    """Test CIO MCP command."""

    def test_mcp_configuration(self):
        """Test MCP configuration info."""
        agent = CIOAgent()
        result = agent.cio_mcp({})

        assert "servers" in result
        assert len(result["servers"]) > 0


class TestCIORedundancyCommand:
    """Test CIO redundancy command."""

    def test_redundancy_plan(self):
        """Test backup and redundancy plan."""
        agent = CIOAgent()
        result = agent.cio_redundancy({})

        assert "backups" in result
        assert "redundancy" in result
        assert "disaster_recovery" in result


class TestCIOCommandDispatch:
    """Test CIO command dispatch."""

    def test_run_all_commands(self):
        """Test that all commands dispatch correctly."""
        agent = CIOAgent()
        commands = ["cio.security", "cio.data", "cio.infrastructure", "cio.privacy", "cio.mcp", "cio.redundancy"]

        for cmd in commands:
            with patch.object(agent, cmd.replace(".", "_")) as mock_cmd:
                mock_cmd.return_value = {"test": "result"}
                result = agent.run(cmd, {})
                mock_cmd.assert_called_once()

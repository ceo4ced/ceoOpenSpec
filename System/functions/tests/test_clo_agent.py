"""
Unit tests for CLO Agent (Digital Paralegal).
"""

import os
import sys
import pytest
from unittest.mock import patch

from conftest import load_agent_module

# Load CLO agent module
clo_module = load_agent_module('clo')
CLOAgent = clo_module.CLOAgent


class TestCLOAgentInitialization:
    """Test CLO agent initialization."""

    def test_agent_initialization(self):
        """Test that CLO agent initializes correctly."""
        agent = CLOAgent()
        assert agent.agent_id == "CLO"
        assert agent.role == "Chief Legal Officer"

    def test_legal_disclaimer_exists(self):
        """Test that legal disclaimer is defined."""
        agent = CLOAgent()
        assert hasattr(agent, 'LEGAL_DISCLAIMER')
        assert "NOT legal advice" in agent.LEGAL_DISCLAIMER


class TestCLOHighRiskDetection:
    """Test CLO high-risk domain detection."""

    def test_detect_minors(self):
        """Test detection of minors-related content."""
        agent = CLOAgent()
        risks = agent._detect_high_risk_domains("We serve children under 18")

        assert len(risks) > 0
        assert any(r["domain"] == "Minors" for r in risks)
        assert any("COPPA" in r["regulations"] for r in risks)

    def test_detect_healthcare(self):
        """Test detection of healthcare content."""
        agent = CLOAgent()
        risks = agent._detect_high_risk_domains("We handle patient medical records")

        assert any(r["domain"] == "Healthcare" for r in risks)
        assert any("HIPAA" in r["regulations"] for r in risks)

    def test_detect_crypto(self):
        """Test detection of crypto/securities content."""
        agent = CLOAgent()
        risks = agent._detect_high_risk_domains("We offer crypto trading and investment")

        assert any(r["domain"] == "Financial/Crypto" for r in risks)

    def test_no_risks_for_safe_content(self):
        """Test no risks for standard content."""
        agent = CLOAgent()
        risks = agent._detect_high_risk_domains("We sell software to businesses")

        assert len(risks) == 0


class TestCLOComplianceCommand:
    """Test CLO compliance command."""

    @patch.object(CLOAgent, '_think')
    @patch.object(CLOAgent, '_load_business_plan')
    @patch.object(CLOAgent, '_load_ceo_brief')
    def test_compliance_assessment(self, mock_brief, mock_plan, mock_think, temp_project_root):
        """Test compliance assessment generation."""
        mock_plan.return_value = "# Business Plan"
        mock_brief.return_value = "# CEO Brief"
        mock_think.return_value = "# Compliance Assessment\n\nContent..."

        with patch.object(CLOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CLOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CLO" / ".clo" / "memory"

            result = agent.clo_compliance({})

            assert "assessment" in result
            assert result["attorney_review_required"] == True


class TestCLOContractCommand:
    """Test CLO contract command."""

    @patch.object(CLOAgent, '_think')
    @patch.object(CLOAgent, '_load_business_plan')
    def test_contract_generation(self, mock_plan, mock_think):
        """Test contract template generation."""
        mock_plan.return_value = "# Business Plan"
        mock_think.return_value = "# Terms of Service\n\nContent..."

        agent = CLOAgent()
        result = agent.clo_contract({"type": "terms_of_service"})

        assert "contract" in result
        assert result["attorney_review_required"] == True
        assert "DRAFT" in result["contract"]


class TestCLORiskCommand:
    """Test CLO risk command."""

    @patch.object(CLOAgent, '_think')
    @patch.object(CLOAgent, '_load_business_plan')
    def test_risk_assessment(self, mock_plan, mock_think, temp_project_root):
        """Test legal risk assessment."""
        mock_plan.return_value = "# Business Plan"
        mock_think.return_value = "# Risk Assessment\n\nContent..."

        with patch.object(CLOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CLOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CLO" / ".clo" / "memory"

            result = agent.clo_risk({})

            assert "assessment" in result
            assert result["attorney_review_required"] == True


class TestCLOResearchCommand:
    """Test CLO research command."""

    def test_research_requires_topic(self):
        """Test that research requires a topic."""
        agent = CLOAgent()
        result = agent.clo_research({})

        assert "error" in result

    @patch.object(CLOAgent, '_think')
    def test_research_generation(self, mock_think):
        """Test legal research generation."""
        mock_think.return_value = "# Legal Research\n\nContent..."

        agent = CLOAgent()
        result = agent.clo_research({"topic": "GDPR compliance"})

        assert "research" in result
        assert result["topic"] == "GDPR compliance"
        assert "disclaimer" in result


class TestCLOJurisdictionCommand:
    """Test CLO jurisdiction command."""

    def test_jurisdiction_info(self):
        """Test jurisdiction information."""
        agent = CLOAgent()
        result = agent.clo_jurisdiction({})

        assert "primary_considerations" in result
        assert "common_choices" in result
        assert result["attorney_review_required"] == True


class TestCLOCommandDispatch:
    """Test CLO command dispatch."""

    def test_run_all_commands(self):
        """Test that all commands dispatch correctly."""
        agent = CLOAgent()
        commands = ["clo.compliance", "clo.contract", "clo.risk", "clo.research", "clo.jurisdiction"]

        for cmd in commands:
            with patch.object(agent, cmd.replace(".", "_")) as mock_cmd:
                mock_cmd.return_value = {"test": "result"}
                result = agent.run(cmd, {})
                mock_cmd.assert_called_once()

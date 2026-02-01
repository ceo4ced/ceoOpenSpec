"""
Unit tests for CTO Agent.
"""

import os
import sys
import pytest
from unittest.mock import patch

from conftest import load_agent_module

# Load CTO agent module
cto_module = load_agent_module('cto')
CTOAgent = cto_module.CTOAgent


class TestCTOAgentInitialization:
    """Test CTO agent initialization."""

    def test_agent_initialization(self):
        """Test that CTO agent initializes correctly."""
        agent = CTOAgent()
        assert agent.agent_id == "CTO"
        assert agent.role == "Chief Technology Officer"


class TestCTOGateStatus:
    """Test CTO gate status checking."""

    def test_gate_closed_by_default(self, temp_project_root):
        """Test that gate is closed by default."""
        with patch.object(CTOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CTOAgent()
            gate = agent._check_gate_status()

            assert gate["gate_open"] == False
            assert gate["cmo_validated"] == False
            assert gate["human_approved"] == False

    def test_gate_requires_both_conditions(self, temp_project_root):
        """Test that gate requires both CMO validation and human approval."""
        with patch.object(CTOAgent, '_get_project_root', return_value=temp_project_root):
            # Create CMO validation with PROCEED
            cmo_memory = temp_project_root / "C-Suites" / "CMO" / ".cmo" / "memory"
            cmo_memory.mkdir(parents=True, exist_ok=True)
            (cmo_memory / "validation-results-2024-01-01.md").write_text(
                "# Validation\n\n## GATE DECISION: PROCEED"
            )

            agent = CTOAgent()
            gate = agent._check_gate_status()

            # CMO validated but human not approved
            assert gate["cmo_validated"] == True
            assert gate["human_approved"] == False
            assert gate["gate_open"] == False

    def test_gate_opens_with_both_conditions(self, temp_project_root):
        """Test that gate opens when both conditions met."""
        with patch.object(CTOAgent, '_get_project_root', return_value=temp_project_root):
            # Create CMO validation with PROCEED
            cmo_memory = temp_project_root / "C-Suites" / "CMO" / ".cmo" / "memory"
            cmo_memory.mkdir(parents=True, exist_ok=True)
            (cmo_memory / "validation-results-2024-01-01.md").write_text(
                "# Validation\n\n## GATE DECISION: PROCEED"
            )

            # Create human approval
            cto_memory = temp_project_root / "C-Suites" / "CTO" / ".cto" / "memory"
            cto_memory.mkdir(parents=True, exist_ok=True)
            (cto_memory / "human-approval.md").write_text("Approved")

            agent = CTOAgent()
            agent.memory_path = cto_memory
            gate = agent._check_gate_status()

            assert gate["cmo_validated"] == True
            assert gate["human_approved"] == True
            assert gate["gate_open"] == True


class TestCTOStatusCommand:
    """Test CTO status command."""

    def test_status_shows_gated(self, temp_project_root):
        """Test status shows gated when gate closed."""
        with patch.object(CTOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CTOAgent()
            result = agent.cto_status({})

            assert "GATED" in result["message"]
            assert result["gate_status"]["gate_open"] == False


class TestCTOPlanCommand:
    """Test CTO plan command."""

    def test_plan_blocked_when_gated(self, temp_project_root):
        """Test that plan is blocked when gate is closed."""
        with patch.object(CTOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CTOAgent()
            result = agent.cto_plan({})

            assert "error" in result
            assert "GATED" in result["error"]

    @patch.object(CTOAgent, '_think')
    @patch.object(CTOAgent, '_check_gate_status')
    @patch.object(CTOAgent, '_load_business_plan')
    @patch.object(CTOAgent, '_load_ceo_brief')
    def test_plan_succeeds_when_gate_open(self, mock_brief, mock_plan, mock_gate, mock_think, temp_project_root):
        """Test plan succeeds when gate is open."""
        mock_gate.return_value = {"gate_open": True, "cmo_validated": True, "human_approved": True}
        mock_plan.return_value = "# Business Plan"
        mock_brief.return_value = "# CEO Brief"
        mock_think.return_value = "# Technical Plan\n\nContent..."

        with patch.object(CTOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CTOAgent()
            agent.memory_path = temp_project_root / "C-Suites" / "CTO" / ".cto" / "memory"

            result = agent.cto_plan({})

            assert "plan" in result
            assert "saved_to" in result


class TestCTOImplementCommand:
    """Test CTO implement command."""

    def test_implement_blocked_when_gated(self, temp_project_root):
        """Test that implement is blocked when gate is closed."""
        with patch.object(CTOAgent, '_get_project_root', return_value=temp_project_root):
            agent = CTOAgent()
            result = agent.cto_implement({})

            assert "error" in result

    @patch.object(CTOAgent, '_check_gate_status')
    def test_implement_status_when_gate_open(self, mock_gate):
        """Test implement returns status when gate is open."""
        mock_gate.return_value = {"gate_open": True, "cmo_validated": True, "human_approved": True}

        agent = CTOAgent()
        result = agent.cto_implement({})

        assert "available_commands" in result

    @patch.object(CTOAgent, '_think')
    @patch.object(CTOAgent, '_check_gate_status')
    def test_implement_with_component(self, mock_gate, mock_think):
        """Test implement with specific component."""
        mock_gate.return_value = {"gate_open": True, "cmo_validated": True, "human_approved": True}
        mock_think.return_value = "# Implementation Guide\n\nContent..."

        agent = CTOAgent()
        result = agent.cto_implement({"component": "frontend"})

        assert "guidance" in result
        assert result["component"] == "frontend"


class TestCTOBackupsCommand:
    """Test CTO backups command."""

    def test_backups_status(self):
        """Test backup status."""
        agent = CTOAgent()
        result = agent.cto_backups({"action": "status"})

        assert "status" in result
        assert "code" in result["status"]
        assert "data" in result["status"]


class TestCTOCommandDispatch:
    """Test CTO command dispatch."""

    def test_run_all_commands(self):
        """Test that all commands dispatch correctly."""
        agent = CTOAgent()
        commands = ["cto.status", "cto.plan", "cto.implement", "cto.backups"]

        for cmd in commands:
            with patch.object(agent, cmd.replace(".", "_")) as mock_cmd:
                mock_cmd.return_value = {"test": "result"}
                result = agent.run(cmd, {})
                mock_cmd.assert_called_once()

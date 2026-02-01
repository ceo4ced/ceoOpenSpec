"""
Unit tests for CXA Agent.
"""

import os
import sys
import pytest
from unittest.mock import patch

from conftest import load_agent_module

# Load CXA agent module
cxa_module = load_agent_module('cxa')
CXAAgent = cxa_module.CXAAgent


class TestCXAAgentInitialization:
    """Test CXA agent initialization."""

    def test_agent_initialization(self):
        """Test that CXA agent initializes correctly."""
        agent = CXAAgent()
        assert agent.agent_id == "CXA"
        assert agent.role == "Chief Experience Agent"

    def test_email_routing_rules_exist(self):
        """Test that email routing rules are defined."""
        agent = CXAAgent()
        assert hasattr(agent, 'EMAIL_ROUTING')
        assert len(agent.EMAIL_ROUTING) > 0


class TestCXAEmailRouting:
    """Test CXA email routing logic."""

    def test_route_legal_email(self):
        """Test routing of legal emails to CLO."""
        agent = CXAAgent()
        result = agent._route_email({
            "from": "attorney@law.com",
            "subject": "Legal Notice",
            "body": "This is a legal matter."
        })

        assert result["route_to"] == "CLO"

    def test_route_press_email(self):
        """Test routing of press emails to CMO."""
        agent = CXAAgent()
        result = agent._route_email({
            "from": "reporter@news.com",
            "subject": "Interview Request",
            "body": "We'd like to interview your CEO."
        })

        assert result["route_to"] == "CMO"
        assert result["priority"] == "high"

    def test_route_investor_email(self):
        """Test routing of investor emails to CFO."""
        agent = CXAAgent()
        result = agent._route_email({
            "from": "partner@vc.com",
            "subject": "Investment Opportunity",
            "body": "We'd like to discuss funding."
        })

        assert result["route_to"] == "CFO"

    def test_route_support_email(self):
        """Test routing of support emails to COO."""
        agent = CXAAgent()
        result = agent._route_email({
            "from": "customer@example.com",
            "subject": "Need Help",
            "body": "I have an issue with my account."
        })

        assert result["route_to"] == "COO"

    def test_route_unknown_email(self):
        """Test routing of unknown emails to HUMAN."""
        agent = CXAAgent()
        result = agent._route_email({
            "from": "random@example.com",
            "subject": "Hello",
            "body": "General inquiry."
        })

        assert result["route_to"] == "HUMAN"


class TestCXAEmailCommand:
    """Test CXA email command."""

    def test_email_check(self):
        """Test email check status."""
        agent = CXAAgent()
        result = agent.cxa_email({"action": "check"})

        assert "unread" in result
        assert "pending_routing" in result

    def test_email_route(self, temp_project_root):
        """Test email routing."""
        with patch.object(CXAAgent, '_get_project_root', return_value=temp_project_root):
            agent = CXAAgent()
            agent.logs_path = temp_project_root / "C-Suites" / "CXA" / "logs"

            result = agent.cxa_email({
                "action": "route",
                "email": {
                    "from": "press@tc.com",
                    "subject": "Interview",
                    "body": "Press inquiry"
                }
            })

            assert "routing" in result
            assert result["routing"]["route_to"] == "CMO"

    def test_email_route_requires_email(self):
        """Test that route requires email data."""
        agent = CXAAgent()
        result = agent.cxa_email({"action": "route"})

        assert "error" in result

    def test_email_respond(self, temp_project_root):
        """Test email response."""
        with patch.object(CXAAgent, '_get_project_root', return_value=temp_project_root):
            agent = CXAAgent()
            agent.logs_path = temp_project_root / "C-Suites" / "CXA" / "logs"

            result = agent.cxa_email({
                "action": "respond",
                "email_id": "EMAIL-001",
                "response": "Thank you for your inquiry."
            })

            assert "email_id" in result

    def test_email_search(self):
        """Test email search."""
        agent = CXAAgent()
        result = agent.cxa_email({
            "action": "search",
            "query": "invoice"
        })

        assert "results" in result


class TestCXAPhoneCommand:
    """Test CXA phone command."""

    def test_phone_status(self):
        """Test phone status."""
        agent = CXAAgent()
        result = agent.cxa_phone({"action": "status"})

        assert "configured" in result
        assert "calls_today" in result

    def test_phone_call(self, temp_project_root):
        """Test initiating a call."""
        with patch.object(CXAAgent, '_get_project_root', return_value=temp_project_root):
            agent = CXAAgent()
            agent.logs_path = temp_project_root / "C-Suites" / "CXA" / "logs"

            result = agent.cxa_phone({
                "action": "call",
                "to": "+1234567890"
            })

            assert result["status"] == "pending"

    def test_phone_call_requires_number(self):
        """Test that call requires phone number."""
        agent = CXAAgent()
        result = agent.cxa_phone({"action": "call"})

        assert "error" in result

    def test_phone_sms(self, temp_project_root):
        """Test sending SMS."""
        with patch.object(CXAAgent, '_get_project_root', return_value=temp_project_root):
            agent = CXAAgent()
            agent.logs_path = temp_project_root / "C-Suites" / "CXA" / "logs"

            result = agent.cxa_phone({
                "action": "sms",
                "to": "+1234567890",
                "message": "Hello!"
            })

            assert "queued" in result["message"]


class TestCXAScheduleCommand:
    """Test CXA schedule command."""

    def test_schedule_view(self):
        """Test viewing schedule."""
        agent = CXAAgent()
        result = agent.cxa_schedule({"action": "view"})

        assert "events" in result
        assert "availability" in result

    def test_schedule_book(self):
        """Test booking a meeting."""
        agent = CXAAgent()
        result = agent.cxa_schedule({
            "action": "book",
            "event": {"title": "Team Meeting", "time": "2024-02-01T10:00:00Z"}
        })

        assert result["status"] == "pending_confirmation"

    def test_schedule_availability(self):
        """Test checking availability."""
        agent = CXAAgent()
        result = agent.cxa_schedule({
            "action": "availability",
            "date_range": "next_week"
        })

        assert "slots" in result


class TestCXAContactsCommand:
    """Test CXA contacts command."""

    def test_contacts_list(self):
        """Test listing contacts."""
        agent = CXAAgent()
        result = agent.cxa_contacts({"action": "list"})

        assert "contacts" in result
        assert "total" in result

    def test_contacts_add(self, temp_project_root):
        """Test adding a contact."""
        with patch.object(CXAAgent, '_get_project_root', return_value=temp_project_root):
            agent = CXAAgent()
            agent.logs_path = temp_project_root / "C-Suites" / "CXA" / "logs"

            result = agent.cxa_contacts({
                "action": "add",
                "contact": {"name": "John Doe", "email": "john@example.com"}
            })

            assert "contact" in result

    def test_contacts_add_requires_email_or_phone(self):
        """Test that add requires email or phone."""
        agent = CXAAgent()
        result = agent.cxa_contacts({
            "action": "add",
            "contact": {"name": "John Doe"}
        })

        assert "error" in result

    def test_contacts_search(self):
        """Test searching contacts."""
        agent = CXAAgent()
        result = agent.cxa_contacts({
            "action": "search",
            "query": "john"
        })

        assert "results" in result


class TestCXACommandDispatch:
    """Test CXA command dispatch."""

    def test_run_all_commands(self):
        """Test that all commands dispatch correctly."""
        agent = CXAAgent()
        commands = ["cxa.email", "cxa.phone", "cxa.schedule", "cxa.contacts"]

        for cmd in commands:
            with patch.object(agent, cmd.replace(".", "_")) as mock_cmd:
                mock_cmd.return_value = {"test": "result"}
                result = agent.run(cmd, {})
                mock_cmd.assert_called_once()

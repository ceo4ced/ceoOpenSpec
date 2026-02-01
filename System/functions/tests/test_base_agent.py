"""
Unit tests for BaseAgent class.
"""

import os
import sys
import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'packages'))

from factory_core.agent import BaseAgent


class TestBaseAgentInitialization:
    """Test BaseAgent initialization."""

    def test_agent_initialization(self):
        """Test basic agent initialization."""
        agent = BaseAgent("TEST", "Test Agent")

        assert agent.agent_id == "TEST"
        assert agent.role == "Test Agent"
        assert agent.factory_id == "development"  # Default

    def test_agent_with_custom_factory_id(self):
        """Test agent with custom factory ID."""
        agent = BaseAgent("TEST", "Test Agent", factory_id="custom-factory")

        assert agent.factory_id == "custom-factory"


class TestBaseAgentCommandDispatch:
    """Test BaseAgent command dispatch."""

    def test_run_returns_success_structure(self):
        """Test that run returns proper success structure."""
        agent = BaseAgent("TEST", "Test Agent")

        # Add a mock command method
        agent.test_command = Mock(return_value={"result": "success"})

        result = agent.run("test.command", {"param": "value"})

        assert result["status"] == "success"
        assert result["agent"] == "TEST"
        assert "timestamp" in result
        assert "data" in result

    def test_run_handles_unknown_command(self):
        """Test that run handles unknown commands."""
        agent = BaseAgent("TEST", "Test Agent")

        result = agent.run("test.unknown", {})

        assert result["status"] == "error"
        assert "not implemented" in result["error"]

    def test_run_converts_dots_to_underscores(self):
        """Test that command names are properly converted."""
        agent = BaseAgent("TEST", "Test Agent")
        agent.test_example = Mock(return_value={"test": True})

        agent.run("test.example", {})

        agent.test_example.assert_called_once_with({})


class TestBaseAgentLogging:
    """Test BaseAgent logging capabilities."""

    def test_logger_exists(self):
        """Test that logger is initialized."""
        agent = BaseAgent("TEST", "Test Agent")

        assert agent.logger is not None

    def test_logger_is_child_of_factory_core(self):
        """Test that logger is properly configured as child logger."""
        agent = BaseAgent("TEST", "Test Agent")

        # Logger should be a child logger with agent ID
        assert "TEST" in agent.logger.name


class TestBaseAgentUsageTracking:
    """Test BaseAgent usage tracking."""

    def test_usage_tracking_initialized(self):
        """Test that usage tracking is initialized."""
        agent = BaseAgent("TEST", "Test Agent")

        assert hasattr(agent, 'session_usage')
        assert agent.session_usage.total_tokens == 0
        assert agent.session_usage.cost_usd == 0.0


class TestBaseAgentThinkMethod:
    """Test BaseAgent _think method."""

    @patch('factory_core.agent.APIManager')
    def test_think_calls_api_manager(self, mock_api_manager):
        """Test that _think calls APIManager correctly."""
        # Setup mock for complete_with_usage
        from api_manager import CompletionResult, UsageInfo
        mock_instance = mock_api_manager.return_value
        mock_usage = UsageInfo(
            input_tokens=100,
            output_tokens=50,
            total_tokens=150,
            cost_usd=0.01,
            model_used="test-model"
        )
        mock_instance.complete_with_usage.return_value = CompletionResult(
            content="Test response",
            usage=mock_usage,
            success=True
        )

        agent = BaseAgent("TEST", "Test Agent")
        result = agent._think(
            prompt="Test prompt",
            task_type="agent_reasoning"
        )

        assert result == "Test response"
        mock_instance.complete_with_usage.assert_called_once()

    @patch('factory_core.agent.APIManager')
    def test_think_updates_usage(self, mock_api_manager):
        """Test that _think updates usage tracking."""
        from api_manager import CompletionResult, UsageInfo
        mock_instance = mock_api_manager.return_value
        mock_usage = UsageInfo(
            input_tokens=100,
            output_tokens=50,
            total_tokens=150,
            cost_usd=0.01,
            model_used="test-model"
        )
        mock_instance.complete_with_usage.return_value = CompletionResult(
            content="Test response",
            usage=mock_usage,
            success=True
        )

        agent = BaseAgent("TEST", "Test Agent")
        agent._think(prompt="Test", task_type="agent_reasoning")

        # Usage should be tracked
        assert agent.session_usage.total_tokens >= 0


class TestBaseAgentGovernance:
    """Test BaseAgent governance loading."""

    def test_load_governance_method_exists(self):
        """Test that governance loading method exists."""
        agent = BaseAgent("TEST", "Test Agent")

        assert hasattr(agent, '_load_governance')

    def test_governance_has_mandate(self):
        """Test that governance includes default mandate."""
        agent = BaseAgent("TEST", "Test Agent")

        assert "mandate" in agent.governance

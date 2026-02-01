"""
Pytest configuration and fixtures for C-Suite agent tests.
"""

import os
import sys
import json
import pytest
import importlib.util
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Add lib to path FIRST (required for api_manager import)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))

# Add packages to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'packages'))


def load_agent_module(agent_name: str):
    """
    Load an agent module by name using importlib to avoid name conflicts.

    Args:
        agent_name: The agent directory name (e.g., 'ceo', 'cfo', 'cmo')

    Returns:
        The loaded module
    """
    functions_dir = Path(__file__).parent.parent
    module_path = functions_dir / agent_name / "main.py"

    spec = importlib.util.spec_from_file_location(f"{agent_name}_main", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"{agent_name}_main"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for _think method."""
    return "This is a mock LLM response for testing purposes."


@pytest.fixture
def mock_api_manager():
    """Mock APIManager to avoid actual API calls."""
    with patch('factory_core.agent.APIManager') as mock:
        instance = mock.return_value
        instance.chat.return_value = {
            "content": "Mock LLM response",
            "usage": {"prompt_tokens": 100, "completion_tokens": 50},
            "model": "test-model"
        }
        yield instance


@pytest.fixture
def temp_project_root(tmp_path):
    """Create a temporary project structure for testing."""
    # Create C-Suites directories
    c_suites = ["CEO", "CFO", "CMO", "COO", "CIO", "CLO", "CPO", "CTO", "CXA"]

    for suite in c_suites:
        suite_dir = tmp_path / "C-Suites" / suite
        suite_lower = suite.lower()

        # Create directories
        (suite_dir / f".{suite_lower}" / "memory").mkdir(parents=True)
        (suite_dir / f".{suite_lower}" / "commands").mkdir(parents=True)
        (suite_dir / ".ethics").mkdir(parents=True)
        (suite_dir / "logs").mkdir(parents=True)

        # Create ethics file
        ethics_file = suite_dir / ".ethics" / "ethics.md"
        ethics_file.write_text(f"# {suite} Ethics\n\nTest ethics content.")

    # Create .mission directory
    mission_dir = tmp_path / ".mission"
    mission_dir.mkdir(parents=True)

    # Create governance file
    governance_file = mission_dir / "agent-governance.md"
    governance_file.write_text("# Agent Governance\n\nTest governance content.")

    # Create README (business plan)
    readme = tmp_path / "README.md"
    readme.write_text("""# Test Business

> AI-powered testing solution

## Problem
Testing is hard.

## Solution
We make it easy.

## Revenue Streams
- Subscription: $29/mo
""")

    return tmp_path


@pytest.fixture
def sample_business_plan():
    """Sample business plan content."""
    return """# Nano Banana

> AI-powered content creation for small businesses

## Problem
Small businesses struggle to create engaging content consistently.

## Solution
AI-powered content generation that maintains brand voice.

## Target Customers
- Small business owners
- Solo entrepreneurs
- Marketing teams < 5 people

## Revenue Streams
- Basic: $29/mo
- Pro: $79/mo
- Enterprise: Custom

## Timeline
| Milestone | Date |
|-----------|------|
| MVP | Month 1 |
| Launch | Month 3 |
"""


@pytest.fixture
def sample_vision():
    """Sample vision document."""
    return {
        "Problem": "Small businesses can't afford marketing agencies",
        "Audience": "Solo entrepreneurs and small teams",
        "Solution": "AI-powered content creation tool",
        "Differentiation": "Maintains consistent brand voice",
        "Business Model": "SaaS subscription at $29/mo",
        "Scale": "10,000 customers in 2 years",
        "Timeline": "MVP in 30 days",
        "Budget": "$10,000 initial investment"
    }


@pytest.fixture
def sample_validation_results():
    """Sample validation campaign results."""
    return {
        "signups": 150,
        "target_signups": 100,
        "cost_per_signup": 4.50,
        "max_cost_per_signup": 5.00,
        "engagement_rate": 5.2,
        "min_engagement_rate": 3.0
    }


@pytest.fixture
def sample_email():
    """Sample incoming email for CXA routing."""
    return {
        "from": "press@techcrunch.com",
        "subject": "Interview Request - AI Startup Feature",
        "body": "We'd like to interview your founder about your AI product."
    }


class MockAgent:
    """Base mock agent for testing without LLM calls."""

    def __init__(self, agent_class, tmp_path):
        self.agent_class = agent_class
        self.tmp_path = tmp_path

    def create(self):
        """Create agent with mocked _think method."""
        with patch.object(self.agent_class, '_think', return_value="Mock LLM response"):
            with patch.object(self.agent_class, '_get_project_root', return_value=self.tmp_path):
                agent = self.agent_class(factory_id="test")
                return agent


@pytest.fixture
def mock_agent_factory(temp_project_root):
    """Factory for creating mock agents."""
    def _create_mock_agent(agent_class):
        return MockAgent(agent_class, temp_project_root).create()
    return _create_mock_agent

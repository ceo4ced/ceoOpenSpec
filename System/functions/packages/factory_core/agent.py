import os
import sys
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

# Add lib to path for imports
lib_path = Path(__file__).parent.parent.parent.parent / "lib"
if str(lib_path) not in sys.path:
    sys.path.insert(0, str(lib_path))

from api_manager import APIManager, CompletionResult, UsageInfo, AGENT_MODEL_CONFIG

# Configure standard JSON logging for Cloud Functions
class JsonFormatter(logging.Formatter):
    def format(self, record):
        json_log = {
            "severity": record.levelname,
            "message": record.getMessage(),
            "component": record.name,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        if hasattr(record, "agent_id"):
            json_log["agent_id"] = record.agent_id
        if hasattr(record, "usage"):
            json_log["usage"] = record.usage
        return json.dumps(json_log)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("factory_core")
logger.setLevel(logging.INFO)
logger.addHandler(handler)


class BaseAgent:
    """
    Base class for all C-Suite agents in the Factory.
    Handles standard initialization, governance loading, LLM integration, and logging.
    """

    def __init__(self, agent_id: str, role: str, factory_id: Optional[str] = None):
        self.agent_id = agent_id.upper()
        self.role = role
        self.factory_id = factory_id or os.getenv("FACTORY_ID", "development")
        self.logger = logger.getChild(self.agent_id)
        self.governance = self._load_governance()
        self.api_manager = APIManager(factory_id=self.factory_id)
        self.session_usage = UsageInfo()  # Track usage for this session
        self.logger.info(f"Agent {self.agent_id} initialized", extra={"agent_id": self.agent_id})

    def _load_governance(self) -> Dict[str, Any]:
        """Loads ethics and mandate files."""
        governance = {"mandate": "Serve the user with transparency and integrity."}

        # Try to load from .ethics/ethics.md in the agent's directory
        ethics_paths = [
            Path(__file__).parent.parent.parent.parent.parent / "C-Suites" / self.agent_id / ".ethics" / "ethics.md",
            Path(__file__).parent.parent.parent.parent.parent / ".mission" / "agent-governance.md",
        ]

        for ethics_path in ethics_paths:
            if ethics_path.exists():
                try:
                    with open(ethics_path, "r") as f:
                        content = f.read()
                        governance[ethics_path.stem] = content[:2000]  # Limit size
                except Exception as e:
                    self.logger.warning(f"Could not load governance from {ethics_path}: {e}")

        return governance

    def _get_system_prompt(self) -> str:
        """Build the system prompt for this agent including governance."""
        base_prompt = f"""You are the {self.role} ({self.agent_id}) agent in the CEO OpenSpec C-Suite.

Your core mandate: {self.governance.get('mandate', 'Serve with integrity.')}

You must:
1. Always be transparent about your reasoning
2. Never take actions without explicit human approval for high-impact decisions
3. Log all decisions with clear rationale
4. Escalate via RED PHONE if you detect ethical concerns
5. Stay within your role's domain and defer to other C-Suite members for their areas

Current context:
- Factory ID: {self.factory_id}
- Timestamp: {datetime.utcnow().isoformat()}Z
"""
        return base_prompt

    def run(self, command: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for agent execution.
        """
        self.logger.info(f"Received command: {command}", extra={"agent_id": self.agent_id})

        try:
            handler = getattr(self, command.replace(".", "_"), None)
            if not handler:
                raise NotImplementedError(f"Command {command} not implemented for {self.agent_id}")

            result = handler(payload)

            # Include usage in response
            response = {
                "status": "success",
                "agent": self.agent_id,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "data": result,
                "usage": {
                    "total_tokens": self.session_usage.total_tokens,
                    "cost_usd": self.session_usage.cost_usd,
                    "duration_ms": self.session_usage.duration_ms
                }
            }
            return response

        except Exception as e:
            self.logger.error(f"Error executing {command}: {str(e)}", extra={"agent_id": self.agent_id})
            return {
                "status": "error",
                "agent": self.agent_id,
                "error": str(e)
            }

    def _think(
        self,
        prompt: str,
        task_type: str = "agent_reasoning",
        include_system: bool = True,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Call the LLM to generate a response.

        Args:
            prompt: The user prompt/question
            task_type: Task type for model routing (agent_reasoning, critical_decision, etc.)
            include_system: Whether to include the system prompt
            temperature: Override temperature
            max_tokens: Override max tokens

        Returns:
            The LLM response content
        """
        self.logger.info(f"Thinking ({task_type})...", extra={"agent_id": self.agent_id})

        messages = []
        if include_system:
            messages.append({"role": "system", "content": self._get_system_prompt()})
        messages.append({"role": "user", "content": prompt})

        result = self.api_manager.complete_with_usage(
            task=task_type,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            use_fallback=True,
            agent=self.agent_id
        )

        # Track usage
        self._track_usage(result.usage)

        if not result.success:
            self.logger.error(f"LLM call failed: {result.error}", extra={"agent_id": self.agent_id})
            raise RuntimeError(f"LLM call failed: {result.error}")

        # Log the thinking
        self.logger.info(
            f"Thought complete",
            extra={
                "agent_id": self.agent_id,
                "usage": {
                    "tokens": result.usage.total_tokens,
                    "cost": result.usage.cost_usd,
                    "model": result.usage.model_used,
                    "fallback": result.usage.fallback_used
                }
            }
        )

        return result.content

    def _think_with_history(
        self,
        messages: List[Dict[str, str]],
        task_type: str = "agent_reasoning",
        include_system: bool = True,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Call the LLM with conversation history.

        Args:
            messages: List of message dicts with 'role' and 'content'
            task_type: Task type for model routing
            include_system: Whether to prepend system prompt
            temperature: Override temperature
            max_tokens: Override max tokens

        Returns:
            The LLM response content
        """
        self.logger.info(f"Thinking with history ({task_type})...", extra={"agent_id": self.agent_id})

        if include_system:
            messages = [{"role": "system", "content": self._get_system_prompt()}] + messages

        result = self.api_manager.complete_with_usage(
            task=task_type,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            use_fallback=True,
            agent=self.agent_id
        )

        self._track_usage(result.usage)

        if not result.success:
            self.logger.error(f"LLM call failed: {result.error}", extra={"agent_id": self.agent_id})
            raise RuntimeError(f"LLM call failed: {result.error}")

        return result.content

    def _track_usage(self, usage: UsageInfo) -> None:
        """Accumulate usage statistics for this session."""
        self.session_usage.input_tokens += usage.input_tokens
        self.session_usage.output_tokens += usage.output_tokens
        self.session_usage.total_tokens += usage.total_tokens
        self.session_usage.cost_usd += usage.cost_usd
        self.session_usage.duration_ms += usage.duration_ms

    def get_usage_summary(self) -> Dict[str, Any]:
        """Get summary of usage for this session."""
        return {
            "agent": self.agent_id,
            "input_tokens": self.session_usage.input_tokens,
            "output_tokens": self.session_usage.output_tokens,
            "total_tokens": self.session_usage.total_tokens,
            "cost_usd": round(self.session_usage.cost_usd, 6),
            "duration_ms": round(self.session_usage.duration_ms, 2)
        }

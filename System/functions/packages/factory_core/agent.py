import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

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
        return json.dumps(json_log)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("factory_core")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

class BaseAgent:
    """
    Base class for all C-Suite agents in the Factory.
    Handles standard initialization, governance loading, and logging.
    """
    
    def __init__(self, agent_id: str, role: str):
        self.agent_id = agent_id.upper()
        self.role = role
        self.logger = logger.getChild(self.agent_id)
        self.governance = self._load_governance()
        self.logger.info(f"Agent {self.agent_id} initialized", extra={"agent_id": self.agent_id})

    def _load_governance(self) -> Dict[str, Any]:
        """Loads ethics and mandate files."""
        # TODO: Load from actual markdown files or BigQuery
        return {"mandate": "Serve the user."}

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
            return {
                "status": "success",
                "agent": self.agent_id,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "data": result
            }
            
        except Exception as e:
            self.logger.error(f"Error executing {command}: {str(e)}", extra={"agent_id": self.agent_id})
            return {
                "status": "error",
                "agent": self.agent_id,
                "error": str(e)
            }

    def _think(self, prompt: str) -> str:
        """
        Internal method to call the LLM.
        In production, this would call Vertex AI or OpenRouter.
        """
        self.logger.info("Thinking...", extra={"agent_id": self.agent_id})
        # Mock response for now
        return "I have thought about this."

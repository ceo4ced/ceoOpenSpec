"""
Factory API Manager - Centralized LLM API client with per-factory isolation.

This module provides:
- OpenRouter as primary provider (with Gemini models)
- Automatic fallback logic
- Task-specific model routing
- Per-factory credential management

Usage:
    from lib.api_manager import APIManager
    
    # Development (uses .env.local)
    manager = APIManager()
    
    # Production (factory-specific)
    manager = APIManager(factory_id="factory_001")
    
    # Make requests
    response = manager.complete(
        task="backstory_generation",
        messages=[{"role": "user", "content": "Generate a backstory..."}]
    )
"""

import json
import os
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any


@dataclass
class ModelConfig:
    """Configuration for a specific model."""
    provider: str  # "openrouter" or "openai"
    model: str
    temperature: float = 0.7
    max_tokens: int = 1024
    
    
@dataclass
class TaskRouting:
    """Task-specific model routing with fallback."""
    primary: ModelConfig
    fallback: Optional[ModelConfig] = None
    

@dataclass
class FactoryConfig:
    """Complete configuration for a factory."""
    factory_id: str
    api_keys: Dict[str, str] = field(default_factory=dict)
    task_routing: Dict[str, TaskRouting] = field(default_factory=dict)
    
    
# Default task routing (uses free Gemini models via OpenRouter)
DEFAULT_TASK_ROUTING = {
    "backstory_generation": TaskRouting(
        primary=ModelConfig(
            provider="openrouter",
            model="google/gemini-2.0-flash-exp:free",
            temperature=0.8,
            max_tokens=512
        ),
        fallback=ModelConfig(
            provider="openrouter", 
            model="mistralai/mistral-7b-instruct:free",
            temperature=0.8,
            max_tokens=512
        )
    ),
    "image_generation": TaskRouting(
        primary=ModelConfig(
            provider="openrouter",
            model="google/gemini-2.0-flash-exp:free",
            temperature=0.7,
            max_tokens=1024
        ),
        fallback=ModelConfig(
            provider="openai",
            model="dall-e-3"
        )
    ),
    "agent_reasoning": TaskRouting(
        primary=ModelConfig(
            provider="openrouter",
            model="google/gemini-2.0-flash-exp:free",
            temperature=0.5,
            max_tokens=2048
        ),
        fallback=ModelConfig(
            provider="openrouter",
            model="mistralai/mistral-7b-instruct:free",
            temperature=0.5,
            max_tokens=2048
        )
    ),
    "quick_response": TaskRouting(
        primary=ModelConfig(
            provider="openrouter",
            model="google/gemini-2.0-flash-exp:free",
            temperature=0.3,
            max_tokens=256
        )
    ),
    "default": TaskRouting(
        primary=ModelConfig(
            provider="openrouter",
            model="google/gemini-2.0-flash-exp:free"
        )
    )
}


class APIManager:
    """
    Centralized API manager for LLM requests.
    
    Supports:
    - OpenRouter (primary) with Gemini models
    - OpenAI (fallback for DALL-E)
    - Per-factory credentials
    - Task-specific model routing
    """
    
    def __init__(
        self, 
        factory_id: Optional[str] = None,
        config_path: Optional[str] = None
    ):
        """
        Initialize API manager.
        
        Args:
            factory_id: Factory identifier for per-factory configs
            config_path: Path to factory config JSON file
        """
        self.factory_id = factory_id or "development"
        self.config = self._load_config(config_path)
        self._load_env()
        
    def _load_env(self) -> None:
        """Load environment variables from .env.local or .env."""
        try:
            from dotenv import load_dotenv
            # lib is in System/lib, so root is parent.parent.parent
            project_root = Path(__file__).parent.parent.parent
            
            # Try .env.local first, then .env
            for env_file in [".env.local", ".env"]:
                env_path = project_root / env_file
                if env_path.exists():
                    load_dotenv(env_path)
                    break
        except ImportError:
            pass  # dotenv not installed, use system env vars
            
    def _load_config(self, config_path: Optional[str] = None) -> FactoryConfig:
        """Load factory configuration."""
        if config_path and Path(config_path).exists():
            with open(config_path) as f:
                data = json.load(f)
            return self._parse_config(data)
            
        # Check for factory-specific config
        factories_dir = Path(__file__).parent.parent / "factories" / self.factory_id
        if factories_dir.exists():
            config_file = factories_dir / "config.json"
            if config_file.exists():
                with open(config_file) as f:
                    data = json.load(f)
                return self._parse_config(data)
                
        # Return default config
        return FactoryConfig(
            factory_id=self.factory_id,
            task_routing=DEFAULT_TASK_ROUTING
        )
        
    def _parse_config(self, data: Dict[str, Any]) -> FactoryConfig:
        """Parse config JSON into FactoryConfig."""
        task_routing = {}
        for task, routing in data.get("task_routing", {}).items():
            primary = ModelConfig(**routing["primary"])
            fallback = ModelConfig(**routing["fallback"]) if routing.get("fallback") else None
            task_routing[task] = TaskRouting(primary=primary, fallback=fallback)
            
        return FactoryConfig(
            factory_id=data.get("factory_id", self.factory_id),
            api_keys=data.get("api_keys", {}),
            task_routing=task_routing or DEFAULT_TASK_ROUTING
        )
        
    def _get_api_key(self, provider: str) -> str:
        """Get API key for a provider."""
        # Check factory config first
        if provider in self.config.api_keys:
            key = self.config.api_keys[provider]
            if key.startswith("secret://"):
                # TODO: Load from Secret Manager
                pass
            return key
            
        # Fall back to environment variables
        env_keys = {
            "openrouter": "OPENROUTER_API_KEY",
            "openai": "OPENAI_API_KEY"
        }
        env_var = env_keys.get(provider, f"{provider.upper()}_API_KEY")
        key = os.getenv(env_var, "")
        
        if not key:
            raise ValueError(f"API key not found for {provider}. Set {env_var} in .env.local")
            
        return key
        
    def _get_routing(self, task: str) -> TaskRouting:
        """Get routing configuration for a task."""
        return self.config.task_routing.get(task, DEFAULT_TASK_ROUTING.get(task, DEFAULT_TASK_ROUTING["default"]))
        
    def complete(
        self,
        task: str,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        use_fallback: bool = True
    ) -> str:
        """
        Make a chat completion request.
        
        Args:
            task: Task type for routing (e.g., "backstory_generation")
            messages: Chat messages
            temperature: Override default temperature
            max_tokens: Override default max tokens
            use_fallback: Whether to try fallback on failure
            
        Returns:
            Response content string
        """
        routing = self._get_routing(task)
        
        try:
            return self._make_request(
                routing.primary,
                messages,
                temperature,
                max_tokens
            )
        except Exception as e:
            if use_fallback and routing.fallback:
                print(f"Primary failed ({e}), trying fallback...")
                return self._make_request(
                    routing.fallback,
                    messages,
                    temperature,
                    max_tokens
                )
            raise
            
    def _make_request(
        self,
        config: ModelConfig,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Make request to specific provider."""
        if config.provider == "openrouter":
            return self._openrouter_request(config, messages, temperature, max_tokens)
        elif config.provider == "openai":
            return self._openai_request(config, messages, temperature, max_tokens)
        else:
            raise ValueError(f"Unknown provider: {config.provider}")
            
    def _openrouter_request(
        self,
        config: ModelConfig,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Make request to OpenRouter."""
        api_key = self._get_api_key("openrouter")
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.getenv("OPENROUTER_REFERER", "https://ceopenspec.ai"),
            "X-Title": os.getenv("OPENROUTER_TITLE", "ceoOpenSpec"),
            "X-Factory-ID": self.factory_id  # For billing attribution
        }
        
        payload = {
            "model": config.model,
            "messages": messages,
            "temperature": temperature or config.temperature,
            "max_tokens": max_tokens or config.max_tokens
        }
        
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers
        )
        
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
            
        if "choices" not in data or not data["choices"]:
            raise ValueError(f"Unexpected OpenRouter response: {data}")
            
        return data["choices"][0]["message"]["content"].strip()
        
    def _openai_request(
        self,
        config: ModelConfig,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Make request to OpenAI (for DALL-E fallback)."""
        api_key = self._get_api_key("openai")
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": config.model,
            "messages": messages,
            "temperature": temperature or config.temperature,
            "max_tokens": max_tokens or config.max_tokens
        }
        
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers
        )
        
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
            
        return data["choices"][0]["message"]["content"].strip()
        
    def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024"
    ) -> str:
        """
        Generate an image using Gemini (via OpenRouter) with DALL-E fallback.
        
        Note: For actual image generation, we use DALL-E as Gemini's image
        generation isn't available via OpenRouter. This method returns the
        image URL.
        """
        # Try OpenAI DALL-E (primary for image generation)
        api_key = self._get_api_key("openai")
        
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "size": size,
            "quality": "standard",
            "n": 1
        }
        
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers
        )
        
        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.loads(response.read().decode("utf-8"))
            
        return data["data"][0]["url"]


# Convenience function for quick usage
def get_manager(factory_id: Optional[str] = None) -> APIManager:
    """Get an API manager instance."""
    return APIManager(factory_id=factory_id)

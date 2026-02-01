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
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime


# =============================================================================
# Model Pricing (per 1M tokens in USD)
# =============================================================================
MODEL_PRICING = {
    # OpenRouter models (Anthropic)
    "anthropic/claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
    "anthropic/claude-3.5-sonnet-20241022": {"input": 3.00, "output": 15.00},
    "anthropic/claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
    # OpenRouter models (OpenAI)
    "openai/gpt-4o-2024-08-06": {"input": 2.50, "output": 10.00},
    "openai/gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "openai/gpt-4-turbo": {"input": 10.00, "output": 30.00},
    # OpenRouter models (Google)
    "google/gemini-2.0-flash-exp:free": {"input": 0.00, "output": 0.00},
    "google/gemini-2.0-flash": {"input": 0.10, "output": 0.40},
    "google/gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    # OpenRouter models (Mistral)
    "mistralai/mistral-7b-instruct:free": {"input": 0.00, "output": 0.00},
    # Direct OpenAI models
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "dall-e-3": {"input": 0.00, "output": 0.00, "per_image": 0.04},  # $0.04 per image (1024x1024)
}

# =============================================================================
# Agent Model Configuration (per C-Suite position)
# =============================================================================
AGENT_MODEL_CONFIG = {
    "CEO": {
        "default": "anthropic/claude-3.5-sonnet-20241022",
        "critical": "anthropic/claude-3-opus-20240229",
        "budget": "gpt-4o-mini",
    },
    "CFO": {
        "default": "anthropic/claude-3.5-sonnet-20241022",
        "analysis": "anthropic/claude-3.5-sonnet-20241022",
        "budget": "gpt-4o-mini",
    },
    "CMO": {
        "default": "anthropic/claude-3.5-sonnet-20241022",
        "content": "anthropic/claude-3.5-sonnet-20241022",
        "quick": "gpt-4o-mini",
        "budget": "gpt-4o-mini",
    },
    "COO": {
        "default": "gpt-4o-mini",
        "planning": "anthropic/claude-3.5-sonnet-20241022",
        "budget": "google/gemini-2.0-flash",
    },
    "CIO": {
        "default": "gpt-4o-mini",
        "security": "anthropic/claude-3.5-sonnet-20241022",
        "budget": "google/gemini-2.0-flash",
    },
    "CLO": {
        "default": "anthropic/claude-3.5-sonnet-20241022",
        "legal": "anthropic/claude-3-opus-20240229",
        "research": "anthropic/claude-3.5-sonnet-20241022",
        "budget": "anthropic/claude-3-haiku-20240307",
    },
    "CPO": {
        "default": "gpt-4o-mini",
        "roadmap": "anthropic/claude-3.5-sonnet-20241022",
        "budget": "google/gemini-2.0-flash",
    },
    "CTO": {
        "default": "anthropic/claude-3.5-sonnet-20241022",
        "code_review": "anthropic/claude-3.5-sonnet-20241022",
        "budget": "gpt-4o-mini",
    },
    "CXA": {
        "default": "gpt-4o-mini",
        "communication": "anthropic/claude-3.5-sonnet-20241022",
        "budget": "google/gemini-2.0-flash",
    },
}


@dataclass
class UsageInfo:
    """Token usage and cost information from an API call."""
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0
    duration_ms: float = 0.0
    model_used: str = ""
    provider: str = ""
    fallback_used: bool = False


@dataclass
class CompletionResult:
    """Result from a completion request with full metadata."""
    content: str
    usage: UsageInfo
    success: bool = True
    error: Optional[str] = None


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
    
    
# Default task routing (OpenRouter primary, OpenAI fallback)
DEFAULT_TASK_ROUTING = {
    "backstory_generation": TaskRouting(
        primary=ModelConfig(
            provider="openrouter",
            model="google/gemini-2.0-flash-exp:free",
            temperature=0.8,
            max_tokens=512
        ),
        fallback=ModelConfig(
            provider="openai",
            model="gpt-4o-mini",
            temperature=0.8,
            max_tokens=512
        )
    ),
    "image_generation": TaskRouting(
        primary=ModelConfig(
            provider="openai",
            model="dall-e-3",
            temperature=0.7,
            max_tokens=1024
        ),
        fallback=None  # DALL-E is the only image generation option
    ),
    "agent_reasoning": TaskRouting(
        primary=ModelConfig(
            provider="openrouter",
            model="google/gemini-2.0-flash-exp:free",
            temperature=0.5,
            max_tokens=2048
        ),
        fallback=ModelConfig(
            provider="openai",
            model="gpt-4o-mini",
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
        ),
        fallback=ModelConfig(
            provider="openai",
            model="gpt-4o-mini",
            temperature=0.3,
            max_tokens=256
        )
    ),
    "critical_decision": TaskRouting(
        primary=ModelConfig(
            provider="openrouter",
            model="anthropic/claude-3.5-sonnet-20241022",
            temperature=0.3,
            max_tokens=4096
        ),
        fallback=ModelConfig(
            provider="openai",
            model="gpt-4o",
            temperature=0.3,
            max_tokens=4096
        )
    ),
    "legal_review": TaskRouting(
        primary=ModelConfig(
            provider="openrouter",
            model="anthropic/claude-3-opus-20240229",
            temperature=0.2,
            max_tokens=4096
        ),
        fallback=ModelConfig(
            provider="openai",
            model="gpt-4o",
            temperature=0.2,
            max_tokens=4096
        )
    ),
    "content_generation": TaskRouting(
        primary=ModelConfig(
            provider="openrouter",
            model="anthropic/claude-3.5-sonnet-20241022",
            temperature=0.7,
            max_tokens=2048
        ),
        fallback=ModelConfig(
            provider="openai",
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=2048
        )
    ),
    "code_generation": TaskRouting(
        primary=ModelConfig(
            provider="openrouter",
            model="anthropic/claude-3.5-sonnet-20241022",
            temperature=0.3,
            max_tokens=4096
        ),
        fallback=ModelConfig(
            provider="openai",
            model="gpt-4o",
            temperature=0.3,
            max_tokens=4096
        )
    ),
    "default": TaskRouting(
        primary=ModelConfig(
            provider="openrouter",
            model="google/gemini-2.0-flash-exp:free",
            temperature=0.7,
            max_tokens=1024
        ),
        fallback=ModelConfig(
            provider="openai",
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=1024
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

    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost in USD for a request."""
        pricing = MODEL_PRICING.get(model, {"input": 0.003, "output": 0.015})
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        return round(input_cost + output_cost, 6)

    def _estimate_tokens(self, text: str) -> int:
        """Rough estimate of tokens (avg 4 chars per token)."""
        return len(text) // 4

    def get_model_for_agent(
        self,
        agent: str,
        task_type: str = "default",
        budget_status: Optional[Dict] = None
    ) -> str:
        """
        Get the appropriate model for an agent based on task and budget.

        Args:
            agent: Agent position (CEO, CFO, etc.)
            task_type: Type of task (default, critical, budget, etc.)
            budget_status: Optional budget info with 'remaining_percent' and 'emergency_pause'
        """
        config = AGENT_MODEL_CONFIG.get(agent, AGENT_MODEL_CONFIG.get("CEO", {}))

        # Emergency budget mode
        if budget_status and budget_status.get("emergency_pause"):
            return config.get("budget", "gpt-4o-mini")

        # Low budget (< 20% remaining)
        if budget_status and budget_status.get("remaining_percent", 1.0) < 0.20:
            return config.get("budget", "gpt-4o-mini")

        # Normal operation
        return config.get(task_type, config.get("default", "gpt-4o-mini"))

    def complete(
        self,
        task: str,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        use_fallback: bool = True,
        agent: Optional[str] = None
    ) -> Union[str, CompletionResult]:
        """
        Make a chat completion request.

        Args:
            task: Task type for routing (e.g., "backstory_generation")
            messages: Chat messages
            temperature: Override default temperature
            max_tokens: Override default max tokens
            use_fallback: Whether to try fallback on failure
            agent: Optional agent name for logging

        Returns:
            Response content string (for backward compatibility)
        """
        result = self.complete_with_usage(task, messages, temperature, max_tokens, use_fallback, agent)
        return result.content

    def complete_with_usage(
        self,
        task: str,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        use_fallback: bool = True,
        agent: Optional[str] = None
    ) -> CompletionResult:
        """
        Make a chat completion request with full usage tracking.

        Args:
            task: Task type for routing (e.g., "backstory_generation")
            messages: Chat messages
            temperature: Override default temperature
            max_tokens: Override default max tokens
            use_fallback: Whether to try fallback on failure
            agent: Optional agent name for logging

        Returns:
            CompletionResult with content and usage info
        """
        routing = self._get_routing(task)

        # Try primary
        result = self._make_request_with_usage(
            routing.primary,
            messages,
            temperature,
            max_tokens
        )

        # If primary succeeded, return it
        if result.success:
            result.usage.fallback_used = False
            return result

        # If primary failed and we have a fallback, try it
        if use_fallback and routing.fallback:
            print(f"Primary failed ({result.error}), trying fallback...")
            fallback_result = self._make_request_with_usage(
                routing.fallback,
                messages,
                temperature,
                max_tokens
            )
            fallback_result.usage.fallback_used = True
            return fallback_result

        # No fallback available, return the failed result
        return result

    def _make_request(
        self,
        config: ModelConfig,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Make request to specific provider (backward compatible)."""
        result = self._make_request_with_usage(config, messages, temperature, max_tokens)
        if not result.success:
            raise ValueError(result.error)
        return result.content

    def _make_request_with_usage(
        self,
        config: ModelConfig,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> CompletionResult:
        """Make request to specific provider with usage tracking."""
        start_time = time.time()

        if config.provider == "openrouter":
            return self._openrouter_request_with_usage(config, messages, temperature, max_tokens, start_time)
        elif config.provider == "openai":
            return self._openai_request_with_usage(config, messages, temperature, max_tokens, start_time)
        else:
            return CompletionResult(
                content="",
                usage=UsageInfo(),
                success=False,
                error=f"Unknown provider: {config.provider}"
            )
            
    def _openrouter_request(
        self,
        config: ModelConfig,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Make request to OpenRouter (backward compatible)."""
        result = self._openrouter_request_with_usage(config, messages, temperature, max_tokens, time.time())
        if not result.success:
            raise ValueError(result.error)
        return result.content

    def _openrouter_request_with_usage(
        self,
        config: ModelConfig,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        start_time: Optional[float] = None
    ) -> CompletionResult:
        """Make request to OpenRouter with usage tracking."""
        start_time = start_time or time.time()

        try:
            api_key = self._get_api_key("openrouter")

            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": os.getenv("OPENROUTER_REFERER", "https://ceopenspec.ai"),
                "X-Title": os.getenv("OPENROUTER_TITLE", "ceoOpenSpec"),
                "X-Factory-ID": self.factory_id
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

            duration_ms = (time.time() - start_time) * 1000

            if "choices" not in data or not data["choices"]:
                return CompletionResult(
                    content="",
                    usage=UsageInfo(duration_ms=duration_ms, model_used=config.model, provider="openrouter"),
                    success=False,
                    error=f"Unexpected OpenRouter response: {data}"
                )

            # Extract usage info
            usage_data = data.get("usage", {})
            input_tokens = usage_data.get("prompt_tokens", 0)
            output_tokens = usage_data.get("completion_tokens", 0)
            total_tokens = usage_data.get("total_tokens", input_tokens + output_tokens)

            usage = UsageInfo(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                cost_usd=self._calculate_cost(config.model, input_tokens, output_tokens),
                duration_ms=duration_ms,
                model_used=config.model,
                provider="openrouter"
            )

            return CompletionResult(
                content=data["choices"][0]["message"]["content"].strip(),
                usage=usage,
                success=True
            )

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            return CompletionResult(
                content="",
                usage=UsageInfo(duration_ms=duration_ms, model_used=config.model, provider="openrouter"),
                success=False,
                error=str(e)
            )

    def _openai_request(
        self,
        config: ModelConfig,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Make request to OpenAI (backward compatible)."""
        result = self._openai_request_with_usage(config, messages, temperature, max_tokens, time.time())
        if not result.success:
            raise ValueError(result.error)
        return result.content

    def _openai_request_with_usage(
        self,
        config: ModelConfig,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        start_time: Optional[float] = None
    ) -> CompletionResult:
        """Make request to OpenAI with usage tracking."""
        start_time = start_time or time.time()

        try:
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

            duration_ms = (time.time() - start_time) * 1000

            # Extract usage info
            usage_data = data.get("usage", {})
            input_tokens = usage_data.get("prompt_tokens", 0)
            output_tokens = usage_data.get("completion_tokens", 0)
            total_tokens = usage_data.get("total_tokens", input_tokens + output_tokens)

            usage = UsageInfo(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                cost_usd=self._calculate_cost(config.model, input_tokens, output_tokens),
                duration_ms=duration_ms,
                model_used=config.model,
                provider="openai"
            )

            return CompletionResult(
                content=data["choices"][0]["message"]["content"].strip(),
                usage=usage,
                success=True
            )

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            return CompletionResult(
                content="",
                usage=UsageInfo(duration_ms=duration_ms, model_used=config.model, provider="openai"),
                success=False,
                error=str(e)
            )
        
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

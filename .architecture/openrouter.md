# OpenRouter Configuration

OpenRouter is the primary LLM API router for all C-suite agents, enabling cost optimization and model flexibility.

---

## Why OpenRouter

1. **Single API, Multiple Models** - Access Claude, GPT, Gemini, and more
2. **Cost Optimization** - Choose best price/performance per task
3. **Fallback Routing** - Auto-fallback if primary model unavailable
4. **Unified Billing** - Single invoice, single credit card
5. **Usage Tracking** - Built-in token and cost tracking

---

## Configuration

### Environment Setup

```yaml
# config/openrouter.yaml
openrouter:
  base_url: https://openrouter.ai/api/v1
  secret_path: projects/{project}/secrets/openrouter-api-key/versions/latest
  
  # Headers for OpenRouter
  headers:
    HTTP-Referer: https://github.com/ceo4ced/ceoOpenSpec
    X-Title: CEO OpenSpec Business Factory
  
  # Default settings
  defaults:
    temperature: 0.7
    max_tokens: 4096
    
  # Fallback behavior
  fallback:
    enabled: true
    strategy: cost_optimized  # cost_optimized, quality_first, speed_first
```

### Secret Manager

```bash
# Store API key in GCP Secret Manager
echo -n "sk-or-v1-your-api-key" | \
  gcloud secrets create openrouter-api-key \
    --data-file=-
```

---

## Model Catalog

### Tier 1: Premium Quality (Critical Tasks)

| Model | Provider | Input/1M | Output/1M | Use Case |
|-------|----------|----------|-----------|----------|
| claude-3-opus-20240229 | Anthropic | $15.00 | $75.00 | Legal review, critical decisions |
| gpt-4-turbo | OpenAI | $10.00 | $30.00 | Complex analysis |

### Tier 2: Balanced (Default Operations)

| Model | Provider | Input/1M | Output/1M | Use Case |
|-------|----------|----------|-----------|----------|
| claude-3.5-sonnet-20241022 | Anthropic | $3.00 | $15.00 | General agent work |
| gpt-4o-2024-08-06 | OpenAI | $2.50 | $10.00 | General agent work |
| gemini-1.5-pro | Google | $1.25 | $5.00 | Long context tasks |

### Tier 3: Cost Optimized (High Volume)

| Model | Provider | Input/1M | Output/1M | Use Case |
|-------|----------|----------|-----------|----------|
| claude-3-haiku-20240307 | Anthropic | $0.25 | $1.25 | Quick classification |
| gpt-4o-mini | OpenAI | $0.15 | $0.60 | Bulk processing |
| gemini-2.0-flash | Google | $0.10 | $0.40 | High speed, high volume |

---

## Agent Model Assignments

### Default Configuration

```python
AGENT_MODEL_CONFIG = {
    'CEO': {
        'default': 'anthropic/claude-3.5-sonnet-20241022',
        'critical': 'anthropic/claude-3-opus-20240229',
        'budget': 'openai/gpt-4o-mini',
    },
    'CFO': {
        'default': 'anthropic/claude-3.5-sonnet-20241022',
        'analysis': 'anthropic/claude-3.5-sonnet-20241022',
        'budget': 'openai/gpt-4o-mini',
    },
    'CMO': {
        'default': 'anthropic/claude-3.5-sonnet-20241022',
        'content': 'anthropic/claude-3.5-sonnet-20241022',  # Quality for content
        'quick': 'openai/gpt-4o-mini',
        'budget': 'openai/gpt-4o-mini',
    },
    'COO': {
        'default': 'openai/gpt-4o-mini',  # Cost optimized
        'planning': 'anthropic/claude-3.5-sonnet-20241022',
        'budget': 'google/gemini-2.0-flash',
    },
    'CIO': {
        'default': 'openai/gpt-4o-mini',
        'security': 'anthropic/claude-3.5-sonnet-20241022',
        'budget': 'google/gemini-2.0-flash',
    },
    'CLO': {
        'default': 'anthropic/claude-3.5-sonnet-20241022',
        'legal': 'anthropic/claude-3-opus-20240229',  # Never compromise on legal
        'research': 'anthropic/claude-3.5-sonnet-20241022',
        'budget': 'anthropic/claude-3-haiku-20240307',
    },
    'CPO': {
        'default': 'openai/gpt-4o-mini',
        'roadmap': 'anthropic/claude-3.5-sonnet-20241022',
        'budget': 'google/gemini-2.0-flash',
    },
    'CTO': {
        'default': 'anthropic/claude-3.5-sonnet-20241022',  # Quality for code
        'code_review': 'anthropic/claude-3.5-sonnet-20241022',
        'budget': 'openai/gpt-4o-mini',
    },
}
```

---

## Model Selection Logic

```python
def select_model(
    agent: str,
    task_type: str,
    budget_status: dict,
    priority: str = 'normal'
) -> str:
    """
    Dynamically select model based on task, budget, and priority.
    """
    config = AGENT_MODEL_CONFIG.get(agent, {})
    
    # Priority override
    if priority == 'critical':
        return config.get('critical', config.get('default'))
    
    # Emergency budget mode
    if budget_status.get('emergency_pause'):
        return config.get('budget', 'google/gemini-2.0-flash')
    
    # Budget low (< 20% remaining)
    if budget_status.get('remaining_percent', 1.0) < 0.20:
        return config.get('budget', 'openai/gpt-4o-mini')
    
    # Normal operation
    return config.get(task_type, config.get('default'))
```

---

## API Integration

### Client Implementation

```python
import openai
from google.cloud import secretmanager

class OpenRouterClient:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.base_url = "https://openrouter.ai/api/v1"
        self._api_key = None
    
    @property
    def api_key(self) -> str:
        if not self._api_key:
            self._api_key = self._get_secret("openrouter-api-key")
        return self._api_key
    
    def _get_secret(self, secret_name: str) -> str:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{self.project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    
    async def chat(
        self,
        model: str,
        messages: list,
        agent: str,
        task_type: str = 'default',
        **kwargs
    ) -> dict:
        """
        Send chat request to OpenRouter.
        """
        client = openai.AsyncOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            default_headers={
                "HTTP-Referer": "https://github.com/ceo4ced/ceoOpenSpec",
                "X-Title": "CEO OpenSpec"
            }
        )
        
        start_time = time.time()
        
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        
        duration = time.time() - start_time
        
        # Calculate cost
        cost = self._calculate_cost(
            model,
            response.usage.prompt_tokens,
            response.usage.completion_tokens
        )
        
        # Log usage
        await self._log_usage(
            agent=agent,
            model=model,
            task_type=task_type,
            tokens=response.usage,
            cost=cost,
            duration=duration
        )
        
        return {
            'content': response.choices[0].message.content,
            'model': model,
            'usage': {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens
            },
            'cost': cost,
            'duration': duration
        }
    
    def _calculate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Calculate cost in USD."""
        pricing = MODEL_PRICING.get(model, {'input': 0.003, 'output': 0.015})
        input_cost = (input_tokens / 1_000_000) * pricing['input']
        output_cost = (output_tokens / 1_000_000) * pricing['output']
        return input_cost + output_cost


MODEL_PRICING = {
    'anthropic/claude-3-opus-20240229': {'input': 15.00, 'output': 75.00},
    'anthropic/claude-3.5-sonnet-20241022': {'input': 3.00, 'output': 15.00},
    'anthropic/claude-3-haiku-20240307': {'input': 0.25, 'output': 1.25},
    'openai/gpt-4o-2024-08-06': {'input': 2.50, 'output': 10.00},
    'openai/gpt-4o-mini': {'input': 0.15, 'output': 0.60},
    'google/gemini-2.0-flash': {'input': 0.10, 'output': 0.40},
    'google/gemini-1.5-pro': {'input': 1.25, 'output': 5.00},
}
```

---

## Cost Controls Integration

The OpenRouter client integrates with CFO budget controls:

```python
async def call_with_budget_check(
    agent: str,
    prompt: str,
    task_type: str = 'default'
) -> dict:
    """
    Call OpenRouter with budget verification.
    """
    # Get budget status
    budget_status = await get_budget_status(agent)
    
    # Check if budget allows
    if not budget_status['can_spend']:
        raise BudgetExceeded(
            f"{agent} has exceeded budget allocation. "
            f"Spent: ${budget_status['spent']:.2f} / "
            f"Limit: ${budget_status['limit']:.2f}"
        )
    
    # Select model based on budget
    model = select_model(agent, task_type, budget_status)
    
    # Estimate cost
    estimated_tokens = estimate_tokens(prompt)
    estimated_cost = estimate_cost(model, estimated_tokens)
    
    # Check if this specific call fits
    if budget_status['remaining'] < estimated_cost:
        # Try cheaper model
        model = get_fallback_model(agent)
        estimated_cost = estimate_cost(model, estimated_tokens)
        
        if budget_status['remaining'] < estimated_cost:
            raise BudgetExceeded(
                f"Insufficient budget for any model. "
                f"Remaining: ${budget_status['remaining']:.2f}"
            )
    
    # Make call
    result = await openrouter.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        agent=agent,
        task_type=task_type
    )
    
    # Update budget spent
    await update_budget_spent(agent, result['cost'])
    
    return result
```

---

## Fallback Strategy

If primary model fails:

```python
FALLBACK_CHAIN = {
    'anthropic/claude-3.5-sonnet-20241022': [
        'openai/gpt-4o-2024-08-06',
        'google/gemini-1.5-pro',
        'openai/gpt-4o-mini'
    ],
    'anthropic/claude-3-opus-20240229': [
        'anthropic/claude-3.5-sonnet-20241022',
        'openai/gpt-4o-2024-08-06',
    ],
    'openai/gpt-4o-mini': [
        'google/gemini-2.0-flash',
        'anthropic/claude-3-haiku-20240307'
    ]
}

async def call_with_fallback(model: str, **kwargs) -> dict:
    """Try primary model, then fallbacks."""
    try:
        return await openrouter.chat(model=model, **kwargs)
    except Exception as e:
        for fallback in FALLBACK_CHAIN.get(model, []):
            try:
                return await openrouter.chat(model=fallback, **kwargs)
            except:
                continue
        raise
```

---

## Usage Logging

Every OpenRouter call is logged to BigQuery:

```sql
INSERT INTO openrouter_calls (
    call_id,
    business_id,
    agent_position,
    
    -- Request
    model_requested,
    model_used,
    task_type,
    
    -- Tokens
    input_tokens,
    output_tokens,
    total_tokens,
    
    -- Cost
    cost_usd,
    
    -- Performance
    duration_ms,
    
    -- Status
    success,
    error_message,
    fallback_used,
    
    -- Time
    called_at TIMESTAMP
) VALUES (...);
```

---

*OpenRouter provides unified LLM access with full cost tracking and budget integration.*

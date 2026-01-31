# cfo.tokens

## Preamble

The CFO controls token budgets and can restrict spending based on runway and revenue.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CFO/.ethics/ethics.md`
3. `.architecture/observability.md`

---

## Overview

The CFO has **budget authority** over all AI spending:
- Set daily/weekly/monthly token limits
- Allocate budgets per agent
- Select cost-effective models via OpenRouter
- Pause non-essential operations when runway is low
- **Single credit card** - one funding source

---

## Command Types

```
cfo.tokens status                      # Current budget status
cfo.tokens allocate [agent] [amount]   # Set agent budget
cfo.tokens limit [daily|weekly|monthly] [amount]  # Set overall limits
cfo.tokens emergency [pause|resume]    # Emergency controls
cfo.tokens models                      # View/configure model selection
```

---

## Budget Structure

### Table: `token_budgets`

```sql
CREATE TABLE IF NOT EXISTS `{project}.{dataset}.token_budgets` (
  budget_id STRING NOT NULL,
  business_id STRING NOT NULL,
  
  -- Seed Capital
  initial_capital FLOAT64,          -- Starting budget (seed money)
  current_balance FLOAT64,          -- Remaining budget
  credit_card_last4 STRING,         -- Single card identifier
  
  -- Period Limits
  daily_limit FLOAT64,
  weekly_limit FLOAT64,
  monthly_limit FLOAT64,
  
  -- Alert Thresholds
  alert_at_percent FLOAT64 DEFAULT 0.80,  -- Alert at 80%
  pause_at_percent FLOAT64 DEFAULT 0.95,  -- Pause at 95%
  
  -- Per-Agent Allocations
  agent_allocations JSON,  -- {"CEO": 30, "CMO": 25, ...} percentages
  
  -- Emergency State
  emergency_pause BOOL DEFAULT FALSE,
  pause_reason STRING,
  paused_at TIMESTAMP,
  paused_by STRING,
  
  -- Meta
  updated_at TIMESTAMP,
  updated_by STRING
);
```

---

## Status: `cfo.tokens status`

### Output

```markdown
# 💰 Token Budget Status
Business: Nano Banana
As of: Jan 31, 2024 9:20 AM EST

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## SEED CAPITAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Initial Capital: $5,000.00
Spent to Date: $247.80
Remaining: $4,752.20 (95.0%)
Credit Card: •••• 4242 (Visa)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## PERIOD LIMITS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Period | Limit | Spent | Remaining | Status |
|--------|-------|-------|-----------|--------|
| Today | $50.00 | $12.40 | $37.60 | 🟢 25% |
| This Week | $250.00 | $89.40 | $160.60 | 🟢 36% |
| This Month | $500.00 | $247.80 | $252.20 | 🟡 50% |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## AGENT ALLOCATION (This Month)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Agent | Allocation | Spent | Remaining | % Used |
|-------|------------|-------|-----------|--------|
| CEO | $150 (30%) | $71.00 | $79.00 | 47% 🟢 |
| CMO | $125 (25%) | $112.50 | $12.50 | 90% 🔴 |
| CFO | $50 (10%) | $20.00 | $30.00 | 40% 🟢 |
| COO | $50 (10%) | $18.00 | $32.00 | 36% 🟢 |
| CIO | $50 (10%) | $12.00 | $38.00 | 24% 🟢 |
| CLO | $50 (10%) | $8.00 | $42.00 | 16% 🟢 |
| CPO | $25 (5%) | $6.30 | $18.70 | 25% 🟢 |
| CTO | $0 (0%) | $0 | $0 | N/A ⬜ |

⚠️ CMO approaching budget limit - may need reallocation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## RUNWAY ESTIMATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

At current burn rate ($^.40/day avg):
• Runway: 383 days
• Status: 🟢 Healthy

Revenue to date: $0.00
Break-even pace needed: N/A (pre-revenue)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## ALERTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• ⚠️ CMO at 90% of monthly allocation
• ℹ️ Consider reducing Nano Banana usage or reallocating
```

---

## Allocate: `cfo.tokens allocate`

Adjust per-agent budget allocation.

### Input
```yaml
agent: CMO
new_allocation: 35  # Percentage of monthly budget
source: CEO  # Take from which agent(s)
reason: "Increased content generation needs"
```

### Execution
```python
def reallocate_budget(agent: str, new_percent: float, source: str):
    """
    Reallocate budget from one agent to another.
    """
    current = get_allocations()
    
    # Calculate shift
    increase = new_percent - current[agent]
    decrease = increase
    
    # Take from source
    if current[source] < decrease:
        raise ValueError(f"{source} doesn't have enough to reallocate")
    
    current[source] -= decrease
    current[agent] = new_percent
    
    # Verify still 100%
    total = sum(current.values())
    if abs(total - 100) > 0.01:
        raise ValueError("Allocations must sum to 100%")
    
    # Log change
    log_budget_change(agent, new_percent, source, decrease)
    
    return current
```

---

## Limit: `cfo.tokens limit`

Set overall spending limits.

### Input
```yaml
period: daily
amount: 75.00  # USD
reason: "Increased operational needs"
```

### Constraints

```python
LIMIT_CONSTRAINTS = {
    'daily': {
        'min': 10.00,
        'max': 200.00,
        'requires_approval_above': 100.00
    },
    'weekly': {
        'min': 50.00,
        'max': 1000.00,
        'requires_approval_above': 500.00
    },
    'monthly': {
        'min': 100.00,
        'max': 5000.00,
        'requires_approval_above': 2000.00
    }
}
```

---

## Emergency: `cfo.tokens emergency`

Emergency budget controls.

### Pause All Non-Essential Operations

```yaml
action: pause
reason: "No revenue, conserving runway"
exceptions:
  - CEO  # Can still communicate with human
  - CFO  # Can still monitor finances
essential_only: true
```

### Effect When Paused

| Agent | Status | Allowed Actions |
|-------|--------|-----------------|
| CEO | Limited | Human communication only |
| CFO | Limited | Monitoring, reporting only |
| CMO | PAUSED | No content generation |
| COO | PAUSED | No operational planning |
| CIO | PAUSED | Emergency support only |
| CLO | LIMITED | Compliance concerns only |
| CPO | PAUSED | No product planning |
| CTO | PAUSED | Already gated |

### Resume

```yaml
action: resume
reason: "Revenue received, resuming operations"
```

---

## Models: `cfo.tokens models`

Configure OpenRouter model selection for cost optimization.

### Output

```markdown
# OpenRouter Model Configuration
Business: Nano Banana

## Current Model Selection

| Agent | Task Type | Model | Cost (per 1M) | Reason |
|-------|-----------|-------|---------------|--------|
| CEO | All | claude-3.5-sonnet | $18.00 | Quality for strategy |
| CFO | All | claude-3.5-sonnet | $18.00 | Accuracy for finance |
| CMO | Content | claude-3.5-sonnet | $18.00 | Creative quality |
| CMO | Quick tasks | gpt-4o-mini | $0.75 | Cost effective |
| COO | All | gpt-4o-mini | $0.75 | Cost effective |
| CIO | All | gpt-4o-mini | $0.75 | Cost effective |
| CLO | Legal | claude-3-opus | $90.00 | Maximum accuracy |
| CLO | Research | claude-3.5-sonnet | $18.00 | Good balance |
| CPO | All | gpt-4o-mini | $0.75 | Cost effective |

## Available Models (OpenRouter)

| Model | Input/1M | Output/1M | Quality | Speed | Best For |
|-------|----------|-----------|---------|-------|----------|
| claude-3-opus | $15.00 | $75.00 | ⭐⭐⭐⭐⭐ | 🐢 | Critical decisions |
| claude-3.5-sonnet | $3.00 | $15.00 | ⭐⭐⭐⭐ | 🐇 | General use |
| claude-3-haiku | $0.25 | $1.25 | ⭐⭐⭐ | ⚡ | Quick tasks |
| gpt-4o | $2.50 | $10.00 | ⭐⭐⭐⭐ | 🐇 | General use |
| gpt-4o-mini | $0.15 | $0.60 | ⭐⭐⭐ | ⚡ | Cost optimized |
| gemini-2.0-flash | $0.10 | $0.40 | ⭐⭐⭐ | ⚡ | Ultra fast |
| gemini-1.5-pro | $1.25 | $5.00 | ⭐⭐⭐⭐ | 🐇 | Long context |

## Recommended Changes (Based on Budget)

Current monthly burn: $247.80
Could save ~45% by:
1. Move COO to gemini-2.0-flash → Save $15/mo
2. Use haiku for CLO research → Save $8/mo
3. Use gpt-4o-mini for CMO quick tasks → Already done

**Proceed with optimizations?** (Requires human approval)
```

---

## Model Selection Logic

```python
def select_model(agent: str, task_type: str, budget_status: dict) -> str:
    """
    Select optimal model based on task and budget.
    """
    # Emergency mode: Use cheapest
    if budget_status['emergency_pause']:
        return 'gemini-2.0-flash'
    
    # Running low: Use cost-effective
    if budget_status['remaining_percent'] < 0.20:
        return get_budget_model(agent, task_type)
    
    # Normal operation: Use quality model
    return get_quality_model(agent, task_type)


MODEL_SELECTION = {
    'CEO': {
        'default': 'claude-3.5-sonnet',
        'budget': 'gpt-4o-mini',
        'critical': 'claude-3-opus'
    },
    'CFO': {
        'default': 'claude-3.5-sonnet',
        'budget': 'gpt-4o-mini',
        'analysis': 'claude-3.5-sonnet'
    },
    'CMO': {
        'default': 'claude-3.5-sonnet',
        'budget': 'gpt-4o-mini',
        'content': 'claude-3.5-sonnet',
        'quick': 'gpt-4o-mini'
    },
    'CLO': {
        'default': 'claude-3.5-sonnet',
        'budget': 'claude-3-haiku',
        'legal': 'claude-3-opus'  # Never compromise on legal
    },
    # ... etc
}
```

---

## OpenRouter Integration

### API Configuration

```python
OPENROUTER_CONFIG = {
    'base_url': 'https://openrouter.ai/api/v1',
    'secret_path': 'openrouter-api-key',
    
    # Route preferences
    'route': 'fallback',  # Use fallback if primary fails
    
    # Headers
    'http_referer': 'https://github.com/ceo4ced/ceoOpenSpec',
    'x_title': 'CEO OpenSpec'
}

async def call_openrouter(
    prompt: str,
    model: str,
    agent: str,
    budget_status: dict
) -> dict:
    """
    Call OpenRouter with budget awareness.
    """
    # Check budget before call
    estimated_tokens = estimate_tokens(prompt)
    estimated_cost = estimate_cost(model, estimated_tokens)
    
    if not can_afford(agent, estimated_cost, budget_status):
        # Try cheaper model
        model = get_fallback_model(agent)
        estimated_cost = estimate_cost(model, estimated_tokens)
        
        if not can_afford(agent, estimated_cost, budget_status):
            raise BudgetExceeded(f"{agent} has exceeded budget")
    
    # Make call
    response = await openrouter_api.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Log usage
    actual_cost = calculate_cost(
        model,
        response['usage']['prompt_tokens'],
        response['usage']['completion_tokens']
    )
    
    log_usage(agent, model, actual_cost)
    
    return {
        'content': response['choices'][0]['message']['content'],
        'model': model,
        'tokens': response['usage'],
        'cost': actual_cost
    }
```

---

## Budget Enforcement

### Before Every LLM Call

```python
def check_budget_before_call(agent: str, estimated_cost: float) -> dict:
    """
    Check if agent can afford this call.
    """
    status = get_budget_status(agent)
    
    # Check 1: Emergency pause
    if status['emergency_pause'] and agent not in ['CEO', 'CFO']:
        return {
            'allowed': False,
            'reason': 'Emergency budget pause active',
            'alternative': 'Essential operations only'
        }
    
    # Check 2: Overall daily limit
    if status['daily_spent'] + estimated_cost > status['daily_limit']:
        return {
            'allowed': False,
            'reason': 'Daily limit would be exceeded',
            'alternative': 'Wait until tomorrow or request increase'
        }
    
    # Check 3: Agent allocation
    if status['agent_spent'] + estimated_cost > status['agent_limit']:
        return {
            'allowed': False,
            'reason': f'{agent} monthly allocation exceeded',
            'alternative': 'Request reallocation from CFO'
        }
    
    # Check 4: Seed capital
    if status['current_balance'] - estimated_cost < 0:
        return {
            'allowed': False,
            'reason': 'Insufficient seed capital',
            'alternative': '🔴 RED PHONE: Out of funds'
        }
    
    return {'allowed': True}
```

---

## Single Credit Card Enforcement

```python
# Only one payment method allowed
PAYMENT_CONFIG = {
    'method': 'credit_card',
    'card_last4': None,  # Set during business init
    'max_single_charge': 500.00,  # Require approval above
    'billing_alerts': [0.50, 0.75, 0.90],  # Alert at % of limit
}

def validate_payment_source(card_last4: str):
    """
    Ensure only approved card is used.
    """
    if PAYMENT_CONFIG['card_last4'] and \
       card_last4 != PAYMENT_CONFIG['card_last4']:
        raise PaymentError(
            "Only the registered business card may be used. "
            f"Expected: ****{PAYMENT_CONFIG['card_last4']}"
        )
```

---

## Logging

```sql
INSERT INTO budget_changes (
    change_id,
    business_id,
    
    -- What changed
    change_type,  -- allocation, limit, emergency
    old_value,
    new_value,
    
    -- Who/Why
    changed_by,
    reason,
    
    -- When
    changed_at TIMESTAMP
) VALUES (...);
```

---

*CFO controls the purse strings. All spending requires budget availability.*

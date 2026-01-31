# Agent Observability & Transparency Framework

This document defines the complete observability system for C-suite AI agents, ensuring full transparency on token usage, model selection, thinking process, and KPIs.

---

## Core Principles

1. **No Hidden Thinking** - All agent reasoning is logged and visible
2. **Token Accountability** - Every token spent is tracked and attributed
3. **Model Transparency** - Which LLM processed each request is recorded
4. **Full Audit Trail** - Complete history of all agent actions
5. **Real-Time Dashboards** - KPIs visible per position

---

## BigQuery Schema

### Table: `conversations`

Records every agent conversation with full metadata.

```sql
CREATE TABLE IF NOT EXISTS `{project}.{dataset}.conversations` (
  conversation_id STRING NOT NULL,
  business_id STRING NOT NULL,
  agent_position STRING NOT NULL,  -- CEO, CFO, CMO, etc.
  command STRING,                   -- e.g., cfo.budget, cmo.campaign
  
  -- Model Information
  model_provider STRING NOT NULL,   -- openai, anthropic, google, openrouter
  model_name STRING NOT NULL,       -- gpt-4o, claude-3-opus, gemini-2.0-flash
  model_version STRING,             -- Specific version if available
  
  -- Timing
  started_at TIMESTAMP NOT NULL,
  completed_at TIMESTAMP,
  duration_seconds FLOAT64,
  
  -- Token Usage
  input_tokens INT64,
  output_tokens INT64,
  total_tokens INT64,
  
  -- Cost (in USD)
  input_cost FLOAT64,
  output_cost FLOAT64,
  total_cost FLOAT64,
  
  -- Status
  status STRING,                    -- success, error, timeout, cancelled
  error_message STRING,
  
  -- Context
  triggered_by STRING,              -- user, agent, scheduled, webhook
  parent_conversation_id STRING,    -- If spawned by another conversation
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
```

### Table: `thinking_logs`

Captures the agent's reasoning process (chain of thought).

```sql
CREATE TABLE IF NOT EXISTS `{project}.{dataset}.thinking_logs` (
  log_id STRING NOT NULL,
  conversation_id STRING NOT NULL,
  business_id STRING NOT NULL,
  agent_position STRING NOT NULL,
  
  -- Thinking Content
  step_number INT64,
  thinking_type STRING,             -- analysis, decision, question, concern
  content STRING,                   -- The actual thinking/reasoning
  
  -- Context
  input_summary STRING,             -- What triggered this thought
  output_action STRING,             -- What action resulted
  
  -- Confidence
  confidence_score FLOAT64,         -- 0.0 to 1.0
  uncertainty_flags ARRAY<STRING>,  -- Areas of uncertainty
  
  -- Timing
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
```

### Table: `escalations`

Tracks all RED PHONE alerts and escalations.

```sql
CREATE TABLE IF NOT EXISTS `{project}.{dataset}.escalations` (
  escalation_id STRING NOT NULL,
  business_id STRING NOT NULL,
  
  -- Source
  from_position STRING NOT NULL,
  to_position STRING,               -- NULL if to human
  to_human BOOL DEFAULT FALSE,
  
  -- Type
  escalation_type STRING,           -- red_phone, concern, question, blocker
  priority STRING,                  -- critical, high, medium, low
  
  -- Content
  subject STRING,
  situation STRING,
  concern STRING,
  evidence STRING,                  -- JSON blob of supporting data
  recommended_action STRING,
  
  -- Status
  status STRING,                    -- open, acknowledged, resolved, dismissed
  resolution STRING,
  resolved_by STRING,
  resolved_at TIMESTAMP,
  
  -- Timing
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
```

### Table: `kpi_snapshots`

Periodic snapshots of KPIs per position.

```sql
CREATE TABLE IF NOT EXISTS `{project}.{dataset}.kpi_snapshots` (
  snapshot_id STRING NOT NULL,
  business_id STRING NOT NULL,
  agent_position STRING NOT NULL,
  snapshot_date DATE NOT NULL,
  
  -- KPIs (JSON for flexibility per position)
  kpis JSON,
  
  -- Examples of position-specific KPIs:
  -- CEO: vision_clarity_score, propagation_success_rate, greenlight_wait_time
  -- CFO: budget_accuracy, forecast_variance, compliance_score
  -- CMO: campaign_roi, brand_awareness, lead_cost
  -- COO: process_efficiency, quality_score, on_time_delivery
  -- CIO: security_score, uptime_percentage, data_quality
  -- CLO: compliance_rate, contract_cycle_time, risk_score
  -- CPO: roadmap_completion, feature_adoption, customer_satisfaction
  -- CTO: build_success_rate, code_quality, deploy_frequency
  
  -- Meta
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
```

### Table: `model_usage_summary`

Daily aggregation of model usage for cost tracking.

```sql
CREATE TABLE IF NOT EXISTS `{project}.{dataset}.model_usage_summary` (
  summary_id STRING NOT NULL,
  business_id STRING NOT NULL,
  summary_date DATE NOT NULL,
  
  -- Aggregates
  model_provider STRING NOT NULL,
  model_name STRING NOT NULL,
  
  conversation_count INT64,
  total_input_tokens INT64,
  total_output_tokens INT64,
  total_tokens INT64,
  
  total_cost FLOAT64,
  
  -- By Position
  position_breakdown JSON,  -- {"CEO": 1500, "CFO": 2300, ...}
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
```

---

## Model Pricing Reference

```python
MODEL_PRICING = {
    # OpenAI
    "gpt-4o": {"input": 2.50, "output": 10.00},        # per 1M tokens
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    
    # Anthropic
    "claude-3-opus": {"input": 15.00, "output": 75.00},
    "claude-3-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-haiku": {"input": 0.25, "output": 1.25},
    "claude-3.5-sonnet": {"input": 3.00, "output": 15.00},
    
    # Google
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
    "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    
    # OpenRouter passthrough
    # Uses API response for actual cost
}
```

---

## Dashboard Specifications

### Universal Dashboard Header

Every position dashboard shows:

```
┌─────────────────────────────────────────────────────────────────────┐
│ [LOGO] [Business Name]              [Position] Dashboard            │
├─────────────────────────────────────────────────────────────────────┤
│ Last Activity: [timestamp] | Model: [model_name] | Status: 🟢 ACTIVE │
├─────────────────────────────────────────────────────────────────────┤
│ Today's Tokens: [X] ($[X]) | This Month: [X] ($[X])                 │
└─────────────────────────────────────────────────────────────────────┘
```

### Position-Specific Dashboards

#### CEO Dashboard
```
┌─────────────────────────────────────────────────────────────────────┐
│                    CEO COMMAND CENTER                                │
├────────────────────┬────────────────────┬───────────────────────────┤
│ Vision Status      │ C-Suite Health     │ Pending Approvals         │
│ ▓▓▓▓▓▓▓░░ 78%     │ 🟢 CFO            │ • GREENLIGHT: BUILD       │
│ Last update: 2d    │ 🟢 CMO            │ • [Request details]       │
│                    │ 🟡 COO            │                           │
│                    │ 🟢 CIO            │ [APPROVE] [DISCUSS]       │
│                    │ 🟢 CLO            │                           │
│                    │ 🟢 CPO            │                           │
│                    │ 🟢 CTO            │                           │
├────────────────────┴────────────────────┴───────────────────────────┤
│ Recent Thinking                                                      │
│ ─────────────────────────────────────────────────────────────────── │
│ [timestamp] Analyzing market opportunity...                          │
│ [timestamp] Considered 3 approaches, selected option B because...    │
│ [timestamp] Escalating concern to CMO about targeting...             │
│ [Show More]                                                          │
├─────────────────────────────────────────────────────────────────────┤
│ KPIs                                                                 │
│ • Vision Propagation: 6/8 agents briefed                            │
│ • Avg Greenlight Wait: 4.2 hours                                    │
│ • Active Initiatives: 3                                             │
└─────────────────────────────────────────────────────────────────────┘
```

#### CFO Dashboard
```
┌─────────────────────────────────────────────────────────────────────┐
│                    CFO FINANCIAL DASHBOARD                           │
├────────────────────┬────────────────────┬───────────────────────────┤
│ Cash Position      │ Burn Rate          │ Runway                    │
│ $[Amount]          │ $[X]/month         │ [X] months                │
│ ↑ 12% this month   │ ↓ target: $[Y]/mo  │ 🟢 Healthy                │
├────────────────────┼────────────────────┼───────────────────────────┤
│ Budget Variance    │ Forecast Accuracy  │ Compliance                │
│ +3.2% over         │ 94% accurate       │ 🟢 13/14 items            │
│ 🟡 Watch           │ 🟢 Good            │                           │
├────────────────────┴────────────────────┴───────────────────────────┤
│ Recent Thinking                                                      │
│ ─────────────────────────────────────────────────────────────────── │
│ [timestamp] Reviewed Q1 expenses, flagged marketing overspend...     │
│ [timestamp] Calculated runway at current burn: 8.2 months           │
│ [timestamp] Tax deadline approaching - reminded CLO integration...   │
├─────────────────────────────────────────────────────────────────────┤
│ Alerts                                                               │
│ ⚠️ Q1 tax filing due in 14 days                                     │
│ 🔴 Marketing spend 23% over budget                                  │
└─────────────────────────────────────────────────────────────────────┘
```

#### CMO Dashboard
```
┌─────────────────────────────────────────────────────────────────────┐
│                    CMO MARKETING DASHBOARD                           │
├────────────────────┬────────────────────┬───────────────────────────┤
│ Active Campaigns   │ Total Reach        │ Conversion Rate           │
│ 3                  │ 45.2K              │ 2.3%                      │
│                    │ ↑ 34% vs last week │ ↓ 0.2% vs target          │
├────────────────────┼────────────────────┼───────────────────────────┤
│ TikTok Status      │ Content Pipeline   │ CAC                       │
│ 🟢 Posted today    │ 12 pieces ready    │ $14.20                    │
│ 2.1K views         │ 5 in production    │ 🟢 Under target           │
├────────────────────┴────────────────────┴───────────────────────────┤
│ Recent Thinking                                                      │
│ ─────────────────────────────────────────────────────────────────── │
│ [timestamp] Analyzed TikTok engagement: comedy > educational...      │
│ [timestamp] A/B test results: CTA "Try Free" +23% vs "Learn More"   │
│ [timestamp] Nano Banana content scheduled for 3pm EST peak...        │
├─────────────────────────────────────────────────────────────────────┤
│ Upcoming                                                             │
│ • TikTok post: 3:00 PM                                              │
│ • Campaign review: Tomorrow                                          │
└─────────────────────────────────────────────────────────────────────┘
```

### Similar dashboards for: COO, CIO, CLO, CPO, CTO

---

## Thinking Log Display

Each agent's "Recent Thinking" section shows:

```
┌─────────────────────────────────────────────────────────────────────┐
│ THINKING LOG: [Agent Position]                             [Expand] │
├─────────────────────────────────────────────────────────────────────┤
│ 🧠 Analysis                                          [09:15:23 EST] │
│ ─────────────────────────────────────────────────────────────────── │
│ Input: "Review campaign performance"                                │
│                                                                      │
│ Reasoning:                                                          │
│ 1. Pulled last 7 days of campaign data from BigQuery                │
│ 2. Noticed TikTok CTR dropped 18% on Tuesday                        │
│ 3. Cross-referenced with competitor posts - they launched sale      │
│ 4. Considered: pause campaign vs. adjust creative vs. wait          │
│                                                                      │
│ Decision: Recommend adjusting CTA to match urgency, not pausing     │
│ Confidence: 72%                                                      │
│ Uncertainty: Don't know if competitor sale is ongoing               │
│                                                                      │
│ Output: Generated campaign adjustment recommendation                 │
│ Model: claude-3.5-sonnet | Tokens: 1,847 | Cost: $0.032             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Logging Standards

Every agent interaction MUST log:

```python
{
    "conversation_id": str,
    "business_id": str,
    "agent_position": str,
    "command": str,
    
    # Model info
    "model": {
        "provider": str,       # "anthropic", "openai", "google"
        "name": str,           # "claude-3.5-sonnet"
        "version": str         # Optional specific version
    },
    
    # Tokens
    "tokens": {
        "input": int,
        "output": int,
        "total": int
    },
    
    # Cost
    "cost": {
        "input": float,
        "output": float,
        "total": float,
        "currency": "USD"
    },
    
    # Thinking
    "thinking": [
        {
            "step": int,
            "type": str,       # "analysis", "decision", "question"
            "content": str,
            "confidence": float,
            "uncertainties": [str]
        }
    ],
    
    # Timing
    "started_at": timestamp,
    "completed_at": timestamp,
    "duration_seconds": float,
    
    # Status
    "status": str,             # "success", "error"
    "error": str               # If applicable
}
```

---

## Implementation Checklist

- [ ] Create BigQuery tables
- [ ] Implement logging wrapper for all agent calls
- [ ] Build cost calculation utility
- [ ] Create dashboard frontend (Cloud Run)
- [ ] Implement real-time thinking stream
- [ ] Add model selection logging
- [ ] Build token budget alerts
- [ ] Create daily summary reports

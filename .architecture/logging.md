# Logging Architecture

## Core Principle

> **All logs go to BigQuery. Append-only. No overwrites. No deletions by agents.**

Markdown files in agent `logs/` directories are **summaries** that link to BigQuery.
The source of truth is ALWAYS BigQuery.

---

## Why BigQuery

1. **Immutable by agents** - Agents cannot delete or modify past entries
2. **Cost tracking** - Every token matters when we pay for them
3. **Full audit trail** - Required for compliance
4. **Query capability** - Find patterns, analyze performance
5. **No accidental overwrites** - Append-only semantics

---

## Logging Tables

### conversations

Every agent conversation logged:

```sql
CREATE TABLE IF NOT EXISTS `{project}.{dataset}.conversations` (
  conversation_id STRING NOT NULL,
  business_id STRING NOT NULL,
  agent_position STRING NOT NULL,
  
  -- Timing
  started_at TIMESTAMP NOT NULL,
  ended_at TIMESTAMP,
  duration_seconds INT64,
  
  -- Model
  model_provider STRING,  -- openrouter
  model_name STRING,      -- claude-3.5-sonnet
  model_version STRING,
  
  -- Tokens
  input_tokens INT64,
  output_tokens INT64,
  total_tokens INT64,
  
  -- Cost
  cost_usd FLOAT64,
  
  -- Content
  command_executed STRING,
  user_prompt_preview STRING,  -- First 500 chars
  response_preview STRING,     -- First 500 chars
  
  -- Status
  status STRING,  -- completed, error, timeout
  error_message STRING,
  
  -- Metadata
  ip_address STRING,
  user_agent STRING,
  
  -- Partition
  _PARTITIONTIME TIMESTAMP
);
```

### thinking_logs

Every agent's reasoning process:

```sql
CREATE TABLE IF NOT EXISTS `{project}.{dataset}.thinking_logs` (
  thinking_id STRING NOT NULL,
  conversation_id STRING NOT NULL,
  business_id STRING NOT NULL,
  agent_position STRING NOT NULL,
  
  -- Timing
  timestamp TIMESTAMP NOT NULL,
  step_number INT64,
  
  -- Thinking
  thinking_type STRING,  -- analysis, decision, planning, uncertainty
  thinking_content STRING,  -- The actual reasoning
  confidence_level FLOAT64,  -- 0.0 to 1.0
  
  -- Context
  context_summary STRING,
  options_considered ARRAY<STRING>,
  decision_made STRING,
  rationale STRING,
  
  -- Metadata
  token_count INT64,
  model_used STRING
);
```

### decision_logs

Explicit decisions with rationale:

```sql
CREATE TABLE IF NOT EXISTS `{project}.{dataset}.decision_logs` (
  decision_id STRING NOT NULL,
  business_id STRING NOT NULL,
  agent_position STRING NOT NULL,
  
  -- Decision
  decision_type STRING,  -- routing, approval, escalation, action
  decision_summary STRING,
  
  -- Context
  context STRING,
  options_evaluated ARRAY<STRUCT<
    option STRING,
    pros ARRAY<STRING>,
    cons ARRAY<STRING>,
    score FLOAT64
  >>,
  
  -- Outcome
  chosen_option STRING,
  rationale STRING,
  confidence FLOAT64,
  
  -- Impact
  affected_agents ARRAY<STRING>,
  affected_entities ARRAY<STRING>,
  
  -- Timing
  decided_at TIMESTAMP NOT NULL,
  
  -- Review
  requires_human_review BOOL,
  human_reviewed BOOL,
  human_reviewer STRING,
  human_review_at TIMESTAMP,
  human_override STRING
);
```

### action_logs

Every action taken by agents:

```sql
CREATE TABLE IF NOT EXISTS `{project}.{dataset}.action_logs` (
  action_id STRING NOT NULL,
  business_id STRING NOT NULL,
  agent_position STRING NOT NULL,
  conversation_id STRING,
  
  -- Action
  action_type STRING,  -- mcp_call, approval_request, escalation, file_write
  action_target STRING,  -- What was acted upon
  action_details JSON,
  
  -- Timing
  started_at TIMESTAMP NOT NULL,
  completed_at TIMESTAMP,
  duration_ms INT64,
  
  -- Result
  success BOOL,
  result_summary STRING,
  error_message STRING,
  
  -- Cost
  cost_usd FLOAT64
);
```

### escalation_logs

Every escalation to human or CEO:

```sql
CREATE TABLE IF NOT EXISTS `{project}.{dataset}.escalation_logs` (
  escalation_id STRING NOT NULL,
  business_id STRING NOT NULL,
  
  -- Source
  source_agent STRING NOT NULL,
  source_conversation_id STRING,
  
  -- Escalation
  escalation_type STRING,  -- red_phone, greenlight, question, alert
  urgency STRING,  -- critical, high, normal
  subject STRING,
  description STRING,
  
  -- Target
  target STRING,  -- HUMAN, CEO, specific agent
  
  -- Timing
  escalated_at TIMESTAMP NOT NULL,
  acknowledged_at TIMESTAMP,
  resolved_at TIMESTAMP,
  
  -- Resolution
  resolution STRING,
  resolved_by STRING,
  
  -- SLA
  sla_target TIMESTAMP,
  sla_met BOOL
);
```

### mcp_usage_logs

Every MCP tool call:

```sql
CREATE TABLE IF NOT EXISTS `{project}.{dataset}.mcp_usage_logs` (
  usage_id STRING NOT NULL,
  business_id STRING NOT NULL,
  
  -- Context
  agent_position STRING NOT NULL,
  conversation_id STRING,
  
  -- MCP
  server_name STRING NOT NULL,
  tool_name STRING NOT NULL,
  
  -- Call
  called_at TIMESTAMP NOT NULL,
  parameters JSON,
  
  -- Result
  duration_ms INT64,
  success BOOL,
  error_message STRING,
  result_summary STRING,
  
  -- Cost
  tokens_used INT64,
  cost_usd FLOAT64
);
```

---

## Append-Only Guarantees

### IAM Permissions

Agents have ONLY these BigQuery permissions:
```yaml
bigquery:
  roles:
    - bigquery.dataEditor  # INSERT only, no DELETE/UPDATE
  
  # Custom role for strict append-only
  custom_role: roles/agent.logWriter
  permissions:
    - bigquery.tables.get
    - bigquery.tables.getData
    - bigquery.jobs.create
    allowed_operations:
      - INSERT
    denied_operations:
      - UPDATE
      - DELETE
      - TRUNCATE
      - DROP
```

### Write Pattern

```python
async def log_to_bigquery(table: str, data: dict) -> str:
    """
    Append-only insert to BigQuery.
    No updates, no deletes.
    """
    # Generate unique ID
    data['log_id'] = generate_uuid()
    data['logged_at'] = datetime.utcnow()
    
    # Insert row (no UPDATE capability)
    client = bigquery.Client()
    table_ref = f"{PROJECT}.{DATASET}.{table}"
    
    errors = client.insert_rows_json(table_ref, [data])
    
    if errors:
        raise LoggingError(f"Failed to log: {errors}")
    
    return data['log_id']
```

---

## Markdown Summaries

Agent `logs/` directories contain **summaries only**:

```markdown
# Decision Log Summary

This is a summary view. Full details in BigQuery.

## Recent Decisions (Last 7 Days)

| Date | Decision | Agent | BigQuery ID |
|------|----------|-------|-------------|
| 2024-01-31 | CMO budget reallocation | CFO | dec_abc123 |
| 2024-01-30 | TikTok content approved | CMO | dec_def456 |

[Query BigQuery for Full Details]
```

---

## Retention Policy

| Table | Retention | Reason |
|-------|-----------|--------|
| conversations | 7 years | Audit compliance |
| thinking_logs | 2 years | Analysis |
| decision_logs | 7 years | Audit compliance |
| action_logs | 2 years | Analysis |
| escalation_logs | 7 years | Compliance |
| mcp_usage_logs | 1 year | Cost tracking |

---

## Data Integrity

### Checksums
Every log entry includes a hash:
```python
def compute_log_hash(entry: dict) -> str:
    """Compute integrity hash for log entry."""
    content = json.dumps(entry, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()
```

### Audit Trail
All log access is itself logged:
```sql
-- Who queried what, when
INSERT INTO log_access_audit (...);
```

---

*All logs in BigQuery. Agents can insert. Agents cannot delete or modify.*

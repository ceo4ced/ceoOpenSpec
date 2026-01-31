# Agent Collaboration Architecture

## Platform: GCP + BigQuery

### Infrastructure

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         GCP Cloud Platform                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                  │
│  │   Telegram  │    │  Cloud Pub/ │    │  Cloud      │                  │
│  │   Webhook   │───▶│  Sub Topics │───▶│  Functions  │                  │
│  └─────────────┘    └─────────────┘    └──────┬──────┘                  │
│                                               │                         │
│                     ┌─────────────────────────┘                         │
│                     ▼                                                   │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                        BigQuery                                   │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐     │  │
│  │  │   tasks    │ │   agents   │ │   memory   │ │    logs    │     │  │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘     │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                  │
│  │  GitHub     │    │  Dashboard  │    │  Secrets    │                  │
│  │  Repo Sync  │    │  (Cloud Run)│    │  Manager    │                  │
│  └─────────────┘    └─────────────┘    └─────────────┘                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## BigQuery Schema

### tasks table
```sql
CREATE TABLE tasks (
  task_id STRING,
  business_id STRING,
  created_at TIMESTAMP,
  status STRING,           -- PENDING, ASSIGNED, IN_PROGRESS, BLOCKED, COMPLETE
  assigned_to STRING,      -- Position: CEO, CFO, CMO, etc.
  depends_on ARRAY<STRING>,-- Task IDs this depends on
  input_data JSON,         -- Context from parent task
  output_data JSON,        -- Results when complete
  token_usage INT64,       -- Tokens consumed
  cost_usd FLOAT64         -- API cost
);
```

### agents table
```sql
CREATE TABLE agents (
  agent_id STRING,
  business_id STRING,
  position STRING,
  status STRING,           -- IDLE, WORKING, WAITING, BLOCKED
  current_task STRING,
  last_active TIMESTAMP,
  total_tokens INT64,
  daily_tokens INT64
);
```

### memory table (shared context)
```sql
CREATE TABLE memory (
  key STRING,
  business_id STRING,
  owner STRING,            -- Position that owns this
  visibility STRING,       -- PRIVATE, SHARED, PUBLIC
  content JSON,
  updated_at TIMESTAMP
);
```

---

## Task Routing Matrix

When an order comes in, who does what?

### Input → Owner Mapping

| Trigger/Input | Primary Owner | Supports | Consults |
|---------------|---------------|----------|----------|
| "Build an app for X" | **CEO** | All | Founder |
| "How much will this cost?" | **CFO** | CEO | - |
| "Who is our customer?" | **CMO** | CPO | CEO |
| "Can we do this legally?" | **CLO** | CIO | CEO |
| "How do we handle data?" | **CIO** | CLO | CTO |
| "What should we build first?" | **CPO** | CTO, CMO | CEO |
| "How will this work?" | **COO** | CTO | CEO |
| "Build this feature" | **CTO** | CPO | - |

---

## Collaboration Matrix

How each position works with others:

```
         │ CEO │ CFO │ CMO │ COO │ CIO │ CLO │ CPO │ CTO │
─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
CEO      │  -  │  D  │  D  │  D  │  D  │  D  │  D  │  G  │
CFO      │  R  │  -  │  C  │  C  │  I  │  C  │  I  │  I  │
CMO      │  R  │  I  │  -  │  C  │  I  │  C  │  S  │  I  │
COO      │  R  │  I  │  C  │  -  │  C  │  C  │  I  │  C  │
CIO      │  R  │  I  │  I  │  C  │  -  │  C  │  I  │  S  │
CLO      │  R  │  C  │  C  │  C  │  C  │  -  │  I  │  I  │
CPO      │  R  │  I  │  S  │  I  │  I  │  I  │  -  │  D  │
CTO      │  R  │  I  │  I  │  C  │  S  │  I  │  R  │  -  │
```

**Legend:**
- **D** = Directs (gives orders to)
- **R** = Reports to (receives orders from)
- **S** = Strong collaboration (frequent, bidirectional)
- **C** = Consults (as needed)
- **I** = Informs (one-way notification)
- **G** = Gate (requires approval)

---

## Workflow Patterns

### Pattern 1: Vision to Plan (CEO-led)

```
Founder → CEO
              │
              ├──▶ CFO: Budget constraints?
              ├──▶ CLO: Legal feasibility?
              ├──▶ CIO: Data considerations?
              │
              ◀── All respond
              │
              └──▶ Generate Business Plan
```

### Pattern 2: Priority Decision (CPO-led with CMO)

```
CEO assigns "define product"
              │
              ▼
            CPO
              │
              ├──▶ CMO: What does market want?
              ├──▶ CFO: What's the budget?
              │
              ◀── Both respond
              │
              └──▶ Generate Roadmap + One-Pager
```

### Pattern 3: Build Request (CTO-led, gated)

```
CPO: "Build feature X"
              │
              ▼
      ┌───────────────┐
      │ VALIDATION    │
      │ GATE CHECK    │◀── CMO validation passed?
      └───────┬───────┘    Human approved?
              │
              ▼
            CTO
              │
              ├──▶ CIO: Security requirements?
              ├──▶ CLO: Compliance needs?
              │
              ◀── Both respond
              │
              └──▶ SpecKit → Build
```

### Pattern 4: Legal/Compliance Review (CLO-led)

```
Any agent: "Is X legal?"
              │
              ▼
            CLO
              │
              ├──▶ CIO: Data implications?
              ├──▶ CFO: Financial exposure?
              │
              ◀── Both respond
              │
              └──▶ Risk Assessment
                        │
                        ▼
              [Escalate to human if high-risk]
```

---

## Token Budget Management

### Per-Position Limits

| Position | Per-Task Max | Daily Max | Monthly Max |
|----------|--------------|-----------|-------------|
| CEO | 15,000 | 75,000 | 1,500,000 |
| CFO | 10,000 | 40,000 | 800,000 |
| CMO | 12,000 | 50,000 | 1,000,000 |
| COO | 8,000 | 30,000 | 600,000 |
| CIO | 10,000 | 40,000 | 800,000 |
| CLO | 8,000 | 30,000 | 600,000 |
| CPO | 12,000 | 50,000 | 1,000,000 |
| CTO | 50,000 | 200,000 | 4,000,000 |

### Cost Tracking Query

```sql
SELECT 
  position,
  SUM(token_usage) as total_tokens,
  SUM(cost_usd) as total_cost
FROM tasks
WHERE business_id = @business_id
  AND DATE(created_at) = CURRENT_DATE()
GROUP BY position
```

---

## Inter-Agent Communication

### Message Format

```json
{
  "from": "CMO",
  "to": "CPO",
  "type": "INFORM | REQUEST | RESPONSE | ESCALATE",
  "task_id": "task-123",
  "subject": "Market validation results",
  "body": "...",
  "priority": "HIGH | NORMAL | LOW",
  "requires_response": true,
  "deadline": "2026-01-31T12:00:00Z"
}
```

### BigQuery: messages table

```sql
CREATE TABLE messages (
  message_id STRING,
  business_id STRING,
  from_agent STRING,
  to_agent STRING,
  message_type STRING,
  task_id STRING,
  content JSON,
  sent_at TIMESTAMP,
  read_at TIMESTAMP,
  responded_at TIMESTAMP
);
```

---

## Implementation Notes

1. **Cloud Functions** handle each agent's logic
2. **Pub/Sub** routes messages between agents
3. **BigQuery** provides shared memory and audit trail
4. **GitHub** stores governance files (source of truth)
5. **Secrets Manager** holds LLM API keys, per business

---

*Part of CEO OpenSpec Architecture*

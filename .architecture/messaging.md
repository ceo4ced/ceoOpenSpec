# Inter-Agent Communication Protocol

This document defines how C-suite AI agents communicate with each other and with humans, ensuring all interactions are logged to BigQuery.

---

## Communication Types

| Type | Description | BigQuery Table |
|------|-------------|----------------|
| **Direct Message** | Agent-to-agent or agent-to-human | `messages` |
| **Task Assignment** | CEO assigns work to agents | `tasks` |
| **Escalation** | RED PHONE or concern | `escalations` |
| **Status Update** | Progress reports | `messages` |
| **Question** | Seeking input | `messages` |
| **Approval Request** | GREENLIGHT request | `greenlights` |

---

## Message Schema

### Table: `messages`

```sql
CREATE TABLE IF NOT EXISTS `{project}.{dataset}.messages` (
  message_id STRING NOT NULL,
  business_id STRING NOT NULL,
  conversation_id STRING,          -- Links to parent conversation
  
  -- Parties
  from_position STRING NOT NULL,   -- CEO, CFO, human, system
  to_position STRING NOT NULL,     -- Target position or "human"
  
  -- Content
  message_type STRING NOT NULL,    -- direct, task, question, status, escalation
  subject STRING,
  body STRING NOT NULL,
  
  -- Priority
  priority STRING DEFAULT 'normal', -- critical, high, normal, low
  requires_response BOOL DEFAULT FALSE,
  response_deadline TIMESTAMP,
  
  -- Threading
  thread_id STRING,                -- Groups related messages
  reply_to_id STRING,              -- If this is a reply
  
  -- Status
  status STRING DEFAULT 'sent',    -- sent, delivered, read, responded
  read_at TIMESTAMP,
  responded_at TIMESTAMP,
  
  -- Model info (for tracking)
  model_used STRING,
  tokens_used INT64,
  
  -- Timing
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
```

---

## Message Formats

### Standard Message

```json
{
  "type": "direct",
  "from": "CFO",
  "to": "CEO",
  "priority": "normal",
  "subject": "Q1 Budget Complete",
  "body": "I've completed the Q1 budget projection. Key highlights:\n- Total budget: $24,500/month\n- Runway: 8.2 months at current burn\n- Key risk: Marketing spend 23% over projections\n\nRecommend adjusting marketing allocation. Ready for your review.",
  "attachments": [
    {"type": "file", "path": "CFO/.cfo/memory/budget-q1.md"}
  ],
  "requires_response": true,
  "response_deadline": "2024-01-15T17:00:00Z"
}
```

### Task Assignment (CEO → Agent)

```json
{
  "type": "task",
  "from": "CEO",
  "to": "CMO",
  "priority": "high",
  "subject": "Create TikTok Content Strategy",
  "body": "Based on our vision conversation with the founder, we need a TikTok content strategy for Nano Banana. Target audience is Gen Z creators. Please create a strategy document including:\n1. Content pillars (3-5)\n2. Posting frequency\n3. First week of content ideas\n4. Success metrics\n\nDeadline: EOD tomorrow.",
  "context": {
    "vision_doc": "CEO/.ceo/memory/vision.md",
    "greenlight_status": "VISION approved"
  },
  "deadline": "2024-01-16T23:59:00Z"
}
```

### Question (Agent → Agent)

```json
{
  "type": "question",
  "from": "CMO",
  "to": "CIO",
  "priority": "normal",
  "subject": "TikTok API Integration",
  "body": "I'm planning our content posting workflow. Questions:\n1. Do we have TikTok API access set up?\n2. Can we schedule posts programmatically?\n3. What analytics can we pull?\n\nNeed this to finalize the content strategy.",
  "requires_response": true
}
```

### Escalation (RED PHONE)

```json
{
  "type": "escalation",
  "from": "CLO",
  "to": "human",
  "priority": "critical",
  "subject": "🔴 RED PHONE: COPPA Compliance Risk",
  "body": "SITUATION: CMO's TikTok strategy targets users under 13.\n\nCONCERN: COPPA requires parental consent for data collection from children. Current strategy has no age verification.\n\nEVIDENCE: CMO strategy doc mentions 'kids content' without compliance framework.\n\nRECOMMENDED ACTION: \n1. Add age gate to any data collection\n2. Adjust targeting to 13+\n3. Review with actual COPPA attorney\n\nThis blocks launch until resolved.",
  "escalation_type": "red_phone",
  "blocks": ["CMO.campaign_launch"]
}
```

### GREENLIGHT Request

```json
{
  "type": "greenlight_request",
  "from": "CEO",
  "to": "human",
  "priority": "high",
  "subject": "GREENLIGHT: BUILD Request",
  "body": "Vision phase complete. All C-suite agents have been briefed and have completed initial assessments:\n\n✅ CFO: Budget approved ($24,500/mo)\n✅ CMO: Market validated (TikTok test positive)\n✅ COO: Operations plan ready\n✅ CIO: Infrastructure spec complete\n✅ CLO: No blocking legal issues\n✅ CPO: Roadmap defined (MVP in 4 weeks)\n\nReady to proceed to BUILD phase. CTO awaiting your authorization.\n\nSay GREENLIGHT: BUILD to proceed.",
  "requires_response": true,
  "greenlight_type": "BUILD"
}
```

---

## Communication Flows

### CEO Propagation Flow

```
Human → CEO: "Here's my idea..."
         ↓
CEO → Human: [Clarifying questions]
         ↓
Human → CEO: [Answers]
         ↓
CEO: [Synthesizes vision document]
         ↓
CEO → Human: "Vision ready. Say GREENLIGHT: VISION to proceed."
         ↓
Human → CEO: "GREENLIGHT: VISION"
         ↓
CEO → ALL C-SUITE: [Task assignments based on vision]
         │
         ├→ CFO: "Create budget..."
         ├→ CMO: "Validate market..."
         ├→ COO: "Design operations..."
         ├→ CIO: "Plan infrastructure..."
         ├→ CLO: "Check compliance..."
         └→ CPO: "Define roadmap..."
```

### Inter-Agent Question Flow

```
CMO → CIO: "Can we integrate TikTok API?"
         ↓
CIO: [Researches, prepares response]
         ↓
CIO → CMO: "Yes, here's what we can do..."
         ↓
CMO: [Incorporates into strategy]
         ↓
CMO → CEO: "Strategy complete, ready for review"
```

### Escalation Flow

```
CLO: [Identifies compliance risk]
         ↓
CLO → CEO: "I have a concern about COPPA..."
         ↓
CEO: [Reviews, decides severity]
         ↓
         ├→ Minor: CEO → CMO: "Please address this..."
         │
         └→ Major: CLO → Human (RED PHONE): "🔴 COPPA RISK..."
                            ↓
              Human: [Reviews, decides]
                            ↓
              Human → CLO: "Good catch. CMO, fix this."
```

---

## Pub/Sub Topics

### Topic Structure

```
projects/{project}/topics/{business_id}-{topic}
```

### Topics

| Topic | Purpose | Publishers | Subscribers |
|-------|---------|------------|-------------|
| `agent-messages` | All agent communication | All agents | Message router |
| `human-inbox` | Messages to human | All agents | Telegram/Signal bot |
| `human-outbox` | Messages from human | Telegram/Signal bot | Message router |
| `task-queue` | New task assignments | CEO | All agents |
| `escalations` | RED PHONE alerts | All agents | Human notification service |
| `greenlights` | Approval requests/grants | CEO, Human | All agents |

### Message Router (Cloud Function)

```python
def route_message(event, context):
    """Route incoming messages to appropriate agents."""
    message = json.loads(base64.b64decode(event['data']))
    
    # Log to BigQuery
    log_message_to_bigquery(message)
    
    # Route based on recipient
    if message['to'] == 'human':
        publish_to_human(message)
    elif message['to'] == 'all':
        broadcast_to_agents(message)
    else:
        publish_to_agent(message['to'], message)
    
    # Check for escalation triggers
    if message.get('escalation_type') == 'red_phone':
        trigger_red_phone_alert(message)
```

---

## Response SLAs

| Priority | Human Response | Agent Response |
|----------|----------------|----------------|
| Critical | Immediate (push notification) | Immediate |
| High | 4 hours | 1 hour |
| Normal | 24 hours | 4 hours |
| Low | 48 hours | 24 hours |

---

## Threading

All related messages share a `thread_id`:

```
Thread: "q1-budget-review"
├── CFO → CEO: "Q1 Budget Complete" (original)
├── CEO → CFO: "What's driving marketing overspend?" (reply)
├── CFO → CEO: "Influencer costs higher than projected" (reply)
├── CEO → CMO: "Please review marketing spend with CFO" (branch)
├── CMO → CFO: "Let me look at the numbers" (cross-conversation)
└── CMO → CEO: "Found efficiencies, revised plan attached" (resolution)
```

---

## Notification Channels

### Telegram Bot

```python
async def send_telegram(user_id, message):
    """Send message to human via Telegram."""
    formatted = format_for_telegram(message)
    
    if message['priority'] == 'critical':
        formatted = f"🔴 URGENT\n\n{formatted}"
    
    await bot.send_message(
        chat_id=user_id,
        text=formatted,
        parse_mode='Markdown'
    )
```

### Signal Bot (Future)

```python
async def send_signal(phone_number, message):
    """Send message to human via Signal."""
    # Signal bot implementation
    pass
```

---

## Thinking Transparency in Messages

Every agent message includes thinking metadata:

```json
{
  "message": { ... },
  "thinking": {
    "reasoning": "I'm sending this to CFO because...",
    "confidence": 0.85,
    "alternatives_considered": [
      "Could have asked CMO instead, but CFO owns budget"
    ],
    "model": "claude-3.5-sonnet",
    "tokens": 234
  }
}
```

This is logged to `thinking_logs` table for dashboard display.

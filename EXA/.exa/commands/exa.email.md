# exa.email

## Preamble

This command handles all incoming and outgoing email through the single company email address.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `EXA/.ethics/ethics.md`
3. `EXA/.exa/memory/routing.md`

---

## Overview

Single company email: `hello@[company].com`

- ALL external email goes through this address
- EXA routes to appropriate C-suite
- EXA sends approved responses
- ALL email logged to BigQuery

---

## Command Types

```
exa.email check                    # Check for new emails
exa.email route [email-id]         # Route email to agent
exa.email respond [email-id]       # Send response (with approval)
exa.email search --query [text]    # Search email history
```

---

## Check: `exa.email check`

Check inbox for new unprocessed emails.

### Output

```markdown
# 📧 Email Inbox Check
Timestamp: [Date Time]

## New Emails (3)

| # | From | Subject | Received | Priority |
|---|------|---------|----------|----------|
| 1 | press@techcrunch.com | Interview Request | 5 min ago | 🟠 High |
| 2 | john@customer.com | Need help with... | 15 min ago | 🟡 Normal |
| 3 | vendor@supplies.com | Invoice #1234 | 1 hour ago | 🟢 Low |

## Suggested Routing

1. **TechCrunch Interview** → CMO (press inquiry)
2. **Customer Support** → COO (support request)
3. **Vendor Invoice** → CFO (accounts payable)

[Route All] [Review Individual]
```

---

## Route: `exa.email route`

Route an email to the appropriate C-suite agent.

### Routing Logic

```python
def route_email(email: dict) -> dict:
    """
    Determine routing for incoming email.
    """
    sender = email['from']
    subject = email['subject'].lower()
    body = email['body'].lower()
    
    # Check known contacts first
    contact = lookup_contact(sender)
    if contact and contact.get('preferred_agent'):
        return {
            'route_to': contact['preferred_agent'],
            'reason': 'Known contact preference',
            'priority': contact.get('priority', 'normal')
        }
    
    # Keyword-based routing
    routing_rules = [
        # Legal (highest priority)
        (['subpoena', 'lawsuit', 'legal notice', 'attorney'], 'CLO', 'critical'),
        (['attorney', 'counsel', 'legal'], 'CLO', 'high'),
        
        # Press/Media
        (['interview', 'press', 'journalist', 'media', 'reporter'], 'CMO', 'high'),
        
        # Investor
        (['invest', 'funding', 'valuation', 'venture', 'vc'], 'CFO', 'high'),
        
        # Technical
        (['bug', 'error', 'not working', 'broken', 'api'], 'CTO', 'normal'),
        
        # Support
        (['help', 'support', 'issue', 'problem'], 'COO', 'normal'),
        
        # Sales/Partnership
        (['pricing', 'demo', 'trial', 'purchase'], 'CMO', 'normal'),
        (['partner', 'collaborate', 'integration'], 'CEO', 'normal'),
        
        # Finance
        (['invoice', 'payment', 'receipt'], 'CFO', 'normal'),
        
        # HR
        (['job', 'resume', 'apply', 'position', 'hiring'], 'COO', 'low'),
    ]
    
    for keywords, agent, priority in routing_rules:
        if any(kw in subject or kw in body for kw in keywords):
            return {
                'route_to': agent,
                'reason': f'Keyword match: {keywords[0]}',
                'priority': priority
            }
    
    # Unknown - queue for human
    return {
        'route_to': 'HUMAN',
        'reason': 'Could not determine routing',
        'priority': 'normal'
    }
```

### Routing Notification (to Agent)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 INCOMING EMAIL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Routed to: CMO
Priority: 🟠 High
Reason: Press inquiry

From: press@techcrunch.com
Subject: Interview Request - AI Startup Feature
Received: Jan 31, 2024 9:30 AM EST

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY:
TechCrunch reporter requesting 30-min interview about 
AI content creation tools. Deadline: Friday.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FULL EMAIL:
[Email body]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RESPONSE SLA: 1 hour (high priority)
SUGGESTED ACTION: Schedule interview, prep talking points

[View Thread] [Draft Response]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Respond: `exa.email respond`

Send a response to an email.

### Approval Rules

| Response Type | Approval Required |
|---------------|-------------------|
| Acknowledgment (auto-template) | No |
| Meeting confirmation (Human scheduled) | No |
| Status update (factual) | No |
| First contact to new party | Yes |
| Substantive response | Yes (from routed agent) |
| Commitment of any kind | Yes (from Human) |

### Auto-Acknowledgment (No Approval)

```python
def auto_acknowledge(email: dict) -> str:
    """
    Send immediate acknowledgment email.
    """
    template = f"""
Hello {email['sender_name']},

Thank you for contacting Nano Banana. We've received your message 
and will respond within {get_sla_time(email['priority'])}.

If this is urgent, please call our main line at {COMPANY_PHONE}.

Best regards,
Nano Banana Team
hello@nanobanana.com
"""
    return template
```

### Agent Response Flow

```
Agent drafts response
        ↓
EXA receives draft
        ↓
EXA sends from company email
        ↓
Log to BigQuery
```

---

## Email Thread Tracking

```sql
CREATE TABLE IF NOT EXISTS email_threads (
    thread_id STRING NOT NULL,
    business_id STRING NOT NULL,
    
    -- Thread info
    subject STRING,
    started_at TIMESTAMP,
    last_activity TIMESTAMP,
    
    -- Participants
    external_participants ARRAY<STRING>,
    internal_agents ARRAY<STRING>,
    
    -- Routing
    primary_owner STRING,  -- Which agent owns this thread
    
    -- Status
    status STRING,  -- active, waiting, closed
    priority STRING,
    
    -- SLA
    response_due TIMESTAMP,
    response_sent TIMESTAMP,
    sla_met BOOL
);
```

---

## Email Logging

Every email logged:

```sql
INSERT INTO email_log (
    email_id,
    thread_id,
    business_id,
    
    -- Email details
    direction STRING,  -- inbound, outbound
    sender STRING,
    recipients ARRAY<STRING>,
    subject STRING,
    body_preview STRING,  -- First 500 chars
    
    -- Routing
    routed_to STRING,
    routing_reason STRING,
    priority STRING,
    
    -- Timing
    received_at TIMESTAMP,
    routed_at TIMESTAMP,
    responded_at TIMESTAMP,
    
    -- SLA
    sla_target TIMESTAMP,
    sla_met BOOL
) VALUES (...);
```

---

## Spam Filtering

Before routing, check for spam:

```python
SPAM_INDICATORS = [
    'click here to unsubscribe',
    'act now limited time',
    'you have been selected',
    'claim your prize',
    'nigerian prince',
    # Marketing automation
    'sent via mailchimp',
    'powered by hubspot',
]

def is_spam(email: dict) -> bool:
    combined = (email['subject'] + email['body']).lower()
    return any(spam in combined for spam in SPAM_INDICATORS)
```

Spam emails → Log but do not route or respond.

---

*All company email flows through EXA. Single address, unified voice.*

# coo.callcenter

## Preamble

The COO manages the call center / support operations.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `COO/.ethics/ethics.md`
3. `CXA/.exa/commands/exa.phone.md` (routing from CXA)

---

## Overview

The COO runs the support call center that handles:
- Customer support calls (transferred from CXA)
- Support tickets
- Customer inquiries
- Issue resolution
- Escalation to product/engineering

---

## Command Types

```
coo.callcenter status               # Current queue status
coo.callcenter ticket [action]      # Ticket management
coo.callcenter escalate [ticket-id] # Escalate to another dept
coo.callcenter report               # Support metrics
coo.callcenter sla                  # View/update SLAs
```

---

## Call Center Architecture

### Call Flow (from CXA)

```
CXA receives call
      ↓
CXA identifies as support request
      ↓
CXA transfers to COO Call Center
      ↓
Call answered (AI or human support)
      ↓
Issue resolved OR ticket created
      ↓
Follow-up if needed
      ↓
Logged to BigQuery
```

### Ticket Flow

```
Ticket created (from call, email, form)
      ↓
Auto-categorized
      ↓
Assigned to queue/agent
      ↓
Work in progress
      ↓
Resolution
      ↓
Customer confirmation
      ↓
Closed + logged
```

---

## Ticket Schema

```sql
CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id STRING NOT NULL,
    business_id STRING NOT NULL,
    
    -- Source
    source STRING,  -- phone, email, web_form, chat
    source_reference STRING,  -- call_id, email_id, etc.
    
    -- Customer
    customer_id STRING,
    customer_name STRING,
    customer_email STRING,
    customer_phone STRING,
    
    -- Classification
    category STRING,  -- billing, technical, product, account, other
    subcategory STRING,
    priority STRING,  -- critical, high, normal, low
    
    -- Content
    subject STRING,
    description STRING,
    
    -- Assignment
    assigned_to STRING,  -- agent or queue
    assigned_at TIMESTAMP,
    
    -- Status
    status STRING,  -- new, open, pending, waiting_customer, resolved, closed
    
    -- SLA
    sla_target TIMESTAMP,
    sla_status STRING,  -- on_track, at_risk, breached
    
    -- Resolution
    resolution STRING,
    resolved_at TIMESTAMP,
    closed_at TIMESTAMP,
    
    -- Satisfaction
    csat_score INT64,  -- 1-5
    csat_feedback STRING,
    
    -- Metadata
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    
    -- Escalation
    escalated BOOL,
    escalated_to STRING,
    escalated_at TIMESTAMP
);
```

---

## SLA Definitions

### Response SLA (First Response)

| Priority | Response Time | Target |
|----------|--------------|--------|
| 🔴 Critical | 15 minutes | 99% |
| 🟠 High | 1 hour | 95% |
| 🟡 Normal | 4 hours | 90% |
| 🟢 Low | 24 hours | 85% |

### Resolution SLA

| Priority | Resolution Time | Target |
|----------|----------------|--------|
| 🔴 Critical | 4 hours | 95% |
| 🟠 High | 8 hours | 90% |
| 🟡 Normal | 48 hours | 85% |
| 🟢 Low | 1 week | 80% |

---

## Priority Classification

```python
def classify_priority(ticket: dict) -> str:
    """
    Auto-classify ticket priority.
    """
    subject = ticket['subject'].lower()
    description = ticket['description'].lower()
    combined = subject + ' ' + description
    
    # Critical indicators
    critical_keywords = [
        'security breach', 'data leak', 'cannot access',
        'payment failed', 'charged incorrectly', 'account locked',
        'emergency', 'urgent', 'legal', 'lawsuit'
    ]
    if any(kw in combined for kw in critical_keywords):
        return 'critical'
    
    # High indicators
    high_keywords = [
        'not working', 'broken', 'error', 'bug', 'crash',
        'billing issue', 'refund', 'complaint'
    ]
    if any(kw in combined for kw in high_keywords):
        return 'high'
    
    # Low indicators
    low_keywords = [
        'question', 'how do i', 'feature request',
        'feedback', 'suggestion', 'when will'
    ]
    if any(kw in combined for kw in low_keywords):
        return 'low'
    
    return 'normal'
```

---

## Escalation Paths

### To Product (CPO)

```yaml
escalate_to_product:
  triggers:
    - Feature missing
    - UX complaint (multiple similar tickets)
    - Feature request (frequent)
  
  format:
    ticket_ids: [list of related tickets]
    issue_summary: "Description of product issue"
    customer_impact: "How many customers affected"
    suggested_action: "Product team to evaluate"
```

### To Engineering (CTO)

```yaml
escalate_to_engineering:
  triggers:
    - Bug confirmed
    - System outage
    - Performance issue
    - Security concern
  
  format:
    ticket_ids: [list of related tickets]
    issue_summary: "Technical description"
    severity: critical/high/normal
    reproduction_steps: "How to reproduce"
```

### To Billing (CFO)

```yaml
escalate_to_billing:
  triggers:
    - Refund request over threshold
    - Billing dispute
    - Fraudulent charge claim
  
  format:
    ticket_id: "Ticket ID"
    customer_id: "Customer ID"
    amount: "Dollar amount"
    issue: "Description"
```

---

## First Response Templates

### Acknowledgment

```
Subject: Re: [Original Subject] [Ticket #{{ticket_id}}]

Hi {{customer_name}},

Thank you for contacting Nano Banana support. We've received 
your request and a support specialist will respond within 
{{sla_time}}.

Your ticket number is: #{{ticket_id}}

In the meantime, you may find these resources helpful:
- Help Center: [link]
- FAQ: [link]

Best regards,
Nano Banana Support
```

### Resolution

```
Subject: Re: [Original Subject] [Ticket #{{ticket_id}}] - RESOLVED

Hi {{customer_name}},

Great news! We've resolved your support request.

Resolution: {{resolution_summary}}

If you have any further questions, please reply to this email
and we'll reopen your ticket.

How did we do? Please take 30 seconds to rate your experience:
[Excellent] [Good] [Fair] [Poor]

Best regards,
Nano Banana Support
```

---

## Metrics & Reporting

### Daily Metrics

```sql
SELECT 
  DATE(created_at) as date,
  COUNT(*) as tickets_created,
  COUNT(CASE WHEN status = 'resolved' THEN 1 END) as tickets_resolved,
  AVG(TIMESTAMP_DIFF(first_response_at, created_at, MINUTE)) as avg_response_minutes,
  AVG(TIMESTAMP_DIFF(resolved_at, created_at, MINUTE)) as avg_resolution_minutes,
  AVG(csat_score) as avg_csat,
  COUNT(CASE WHEN sla_status = 'breached' THEN 1 END) as sla_breaches
FROM support_tickets
WHERE business_id = @business_id
  AND created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY date
ORDER BY date DESC;
```

### Weekly Report

```markdown
# Support Report - Week of {{week_start}}

## Overview
- Tickets Created: {{created}}
- Tickets Resolved: {{resolved}}
- Open Tickets: {{open}}

## SLA Performance
- Response SLA Met: {{response_sla}}%
- Resolution SLA Met: {{resolution_sla}}%

## Customer Satisfaction
- Average CSAT: {{csat}}/5
- Promoters (5): {{promoters}}%
- Detractors (1-2): {{detractors}}%

## Top Issues
1. {{issue_1}} ({{count_1}} tickets)
2. {{issue_2}} ({{count_2}} tickets)
3. {{issue_3}} ({{count_3}} tickets)

## Escalations
- To Product: {{product_escalations}}
- To Engineering: {{eng_escalations}}
- To Billing: {{billing_escalations}}
```

---

## Integration with CXA

### Incoming Call Transfer

```python
async def handle_transfer_from_exa(transfer: dict) -> dict:
    """
    Handle incoming call transfer from CXA.
    """
    # Create ticket from call
    ticket = {
        'source': 'phone',
        'source_reference': transfer['call_id'],
        'customer_name': transfer['caller_name'],
        'customer_phone': transfer['caller_phone'],
        'subject': transfer['purpose_summary'],
        'description': transfer['notes'],
        'priority': classify_priority({'subject': transfer['purpose_summary']}),
        'status': 'new'
    }
    
    ticket_id = await create_ticket(ticket)
    
    # Handle call (AI or queue to human)
    if is_simple_inquiry(transfer['purpose_summary']):
        response = await ai_handle_call(transfer['call_id'], ticket_id)
    else:
        response = await queue_for_human(transfer['call_id'], ticket_id)
    
    return {
        'ticket_id': ticket_id,
        'handling': response
    }
```

---

*Every customer matters. Every issue tracked. Every SLA honored.*

# exa.contacts

## Preamble

This command manages the contact database for the company.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CXA/.ethics/ethics.md`

---

## Overview

CXA maintains the master contact database:
- Known contacts with preferences
- VIP identification
- Routing preferences
- Communication history

---

## Command Types

```
exa.contacts add [contact-details]     # Add new contact
exa.contacts lookup [identifier]       # Find contact
exa.contacts update [contact-id]       # Update contact
exa.contacts list --type [type]        # List contacts by type
exa.contacts vip [contact-id]          # Mark as VIP
```

---

## Contact Schema

```sql
CREATE TABLE IF NOT EXISTS contacts (
    contact_id STRING NOT NULL,
    business_id STRING NOT NULL,
    
    -- Identity
    first_name STRING,
    last_name STRING,
    email STRING,
    phone STRING,
    company STRING,
    title STRING,
    
    -- Classification
    contact_type STRING,  
    -- customer, prospect, vendor, partner, investor, press, legal, employee
    
    priority STRING,  -- vip, high, normal, low
    
    -- Routing preferences
    preferred_agent STRING,  -- Which C-suite handles
    routing_notes STRING,
    
    -- Communication prefs
    preferred_channel STRING,  -- email, phone, both
    timezone STRING,
    best_contact_time STRING,
    
    -- History
    first_contact TIMESTAMP,
    last_contact TIMESTAMP,
    total_interactions INT64,
    
    -- Relationships
    referred_by STRING,  -- Contact ID of referrer
    related_contacts ARRAY<STRING>,
    
    -- Notes
    notes STRING,
    tags ARRAY<STRING>,
    
    -- Status
    status STRING,  -- active, dormant, blocked
    
    -- Meta
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    created_by STRING
);
```

---

## Add: `exa.contacts add`

Add a new contact.

### Input
```yaml
first_name: Jane
last_name: Smith
email: jane@vc.com
phone: "+1-555-123-4567"
company: Venture Capital Inc
title: Partner

contact_type: investor
priority: high
preferred_agent: CFO

notes: "Met at TechCrunch event. Interested in AI startups."
tags:
  - venture_capital
  - ai_focus
  - warm_lead
```

### Auto-Classification

```python
def auto_classify_contact(contact: dict) -> dict:
    """
    Automatically classify contact type based on signals.
    """
    email_domain = contact['email'].split('@')[1].lower()
    title = contact.get('title', '').lower()
    
    # Investor signals
    if any(x in email_domain for x in ['vc', 'capital', 'ventures', 'partners']):
        return {'contact_type': 'investor', 'preferred_agent': 'CFO'}
    
    # Press signals
    if any(x in email_domain for x in ['nytimes', 'wsj', 'techcrunch', 'media']):
        return {'contact_type': 'press', 'preferred_agent': 'CMO'}
    
    # Legal signals
    if 'attorney' in title or 'counsel' in title or 'law' in email_domain:
        return {'contact_type': 'legal', 'preferred_agent': 'CLO'}
    
    # Customer signals (generic)
    return {'contact_type': 'prospect', 'preferred_agent': 'CMO'}
```

---

## Lookup: `exa.contacts lookup`

Find a contact by any identifier.

### Search Fields
- Email (exact or domain)
- Phone
- Name (first, last, or full)
- Company

### Output
```markdown
# Contact Found

## Jane Smith
**Partner** at Venture Capital Inc

| Field | Value |
|-------|-------|
| Email | jane@vc.com |
| Phone | +1-555-123-4567 |
| Type | Investor |
| Priority | 🔴 High |
| Routes to | CFO |

### History
- First contact: Jan 15, 2024
- Last contact: Jan 30, 2024
- Total interactions: 4

### Notes
Met at TechCrunch event. Interested in AI startups.

### Tags
`venture_capital` `ai_focus` `warm_lead`

### Related Contacts
- John Doe (colleague at VC Inc)

[Edit] [View Full History] [Log Interaction]
```

---

## VIP Contacts

VIP contacts receive special treatment:

| VIP Treatment | Action |
|---------------|--------|
| Immediate notification | Human + relevant agent alerted |
| Top routing priority | Skip normal queue |
| Personal attention | Human may want to respond directly |
| History visibility | Show full interaction history |

### VIP Classification

```python
VIP_CRITERIA = [
    # Automatic VIP
    {'contact_type': 'investor', 'has_invested': True},
    {'contact_type': 'press', 'outlet': 'tier1'},  # NYT, WSJ, etc.
    {'contact_type': 'customer', 'revenue': '>10000'},
    
    # Manual VIP (Human designated)
    {'manually_set': True}
]
```

---

## Contact Types

| Type | Description | Default Routing |
|------|-------------|-----------------|
| `customer` | Paying customer | COO |
| `prospect` | Potential customer | CMO |
| `vendor` | Supplier/service provider | CFO |
| `partner` | Business partner | CEO |
| `investor` | Investor or potential investor | CFO → CEO |
| `press` | Media/journalist | CMO |
| `legal` | Attorney/legal contact | CLO |
| `employee` | Internal team member | COO |
| `recruiter` | External recruiter | COO |
| `personal` | Human's personal contact | Direct to Human |

---

## Interaction Logging

Log every interaction:

```sql
INSERT INTO contact_interactions (
    interaction_id,
    contact_id,
    business_id,
    
    -- Interaction details
    interaction_type STRING,  -- email, phone, meeting, message
    direction STRING,  -- inbound, outbound
    
    -- Content
    subject STRING,
    summary STRING,
    
    -- Handling
    handled_by STRING,  -- Which agent
    
    -- Timing
    occurred_at TIMESTAMP,
    duration_seconds INT64,  -- For calls/meetings
    
    -- Outcome
    outcome STRING,
    follow_up_required BOOL,
    follow_up_by TIMESTAMP,
    
    -- Sentiment
    sentiment STRING  -- positive, neutral, negative
) VALUES (...);
```

---

## Blocked Contacts

Block persistent spammers or bad actors:

```python
def block_contact(contact_id: str, reason: str) -> dict:
    """
    Block a contact from all communication.
    """
    update_contact(contact_id, {
        'status': 'blocked',
        'blocked_reason': reason,
        'blocked_at': datetime.now()
    })
    
    # Add to email/phone block list
    add_to_block_list(contact['email'])
    add_to_block_list(contact['phone'])
    
    return {'status': 'blocked', 'contact_id': contact_id}
```

Blocked contacts:
- Emails auto-archived (not routed)
- Calls sent to voicemail (not answered)
- No responses sent

---

## Import/Export

### Export Contacts
```yaml
format: csv  # or json
filters:
  contact_type: [customer, investor]
  priority: [vip, high]
include_fields:
  - name
  - email
  - company
  - last_contact
```

### Import Contacts
```yaml
source: csv_file
mapping:
  name: "Full Name"
  email: "Email Address"
  company: "Company"
duplicate_handling: skip  # or update
```

---

## Privacy Compliance

- No contact data shared externally
- GDPR right to be forgotten (delete on request)
- Consent tracked for marketing communications
- Data minimization (only collect what's needed)

---

*Every contact organized, every interaction tracked.*

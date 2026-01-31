# CXA Routing Rules

This file defines the routing logic for incoming communications.

---

## Email Routing

### Priority Keywords (Route Immediately)

| Keywords | Routes To | Priority |
|----------|-----------|----------|
| subpoena, lawsuit, legal notice, court, attorney | CLO | 🔴 Critical |
| urgent, emergency, asap, critical | Queue for classification | 🔴 Critical |
| hack, breach, security incident | CIO | 🔴 Critical |

### Standard Routing

| Keywords/Signals | Routes To | Priority |
|------------------|-----------|----------|
| interview, press, journalist, reporter, media | CMO | 🟠 High |
| invest, funding, valuation, vc, venture | CFO → CEO | 🟠 High |
| pricing, demo, trial, purchase, buy | CMO | 🟡 Normal |
| partner, collaborate, integration, api | CEO | 🟡 Normal |
| help, support, problem, not working, bug | COO → CTO | 🟡 Normal |
| invoice, payment, receipt, bill | CFO | 🟡 Normal |
| job, resume, apply, position, hiring, career | COO | 🟢 Low |
| unsubscribe, opt out | Auto-process | 🟢 Low |

### Domain-Based Routing

| Domain Pattern | Routes To | Notes |
|----------------|-----------|-------|
| *.gov | CLO | Government inquiry |
| *.law.* | CLO | Legal firm |
| *capital*, *ventures*, *partners* | CFO | Likely investor |
| *media*, *news*, *times*, *post* | CMO | Likely press |

---

## Phone Routing

### Transfer Destinations

| Caller Type | Action | Destination |
|-------------|--------|-------------|
| Known VIP | Warm transfer | Preferred agent or Human |
| Customer support | Transfer | COO Call Center |
| Sales inquiry | Take message | CMO callback |
| Press/media | Take message | CMO callback (urgent) |
| Legal | Transfer or urgent message | CLO |
| Personal for Human | Transfer | Human direct |
| Unknown business | Take message | Review queue |
| Solicitor/spam | Politely decline | Block |

### COO Call Center Number
```
Primary: +1-XXX-XXX-XXXX (support line)
Fallback: Voicemail → COO review
```

---

## Override Rules

### Human Override
```
Any contact flagged as "HUMAN_ONLY" routes directly to Human.
Bypass all agent routing.
```

### VIP Override
```
VIP contacts:
1. Route as normal to agent
2. ALSO notify Human
3. ALSO notify CEO
```

### Escalation Override
```
If agent doesn't respond within SLA:
1. 50% SLA: Reminder to agent
2. 100% SLA: Escalate to CEO
3. 150% SLA: RED PHONE to Human
```

---

## Agent Availability

| Agent | Primary Domain | Backup If Unavailable |
|-------|----------------|----------------------|
| CEO | Strategic, partnerships | Human |
| CFO | Financial, investor | CEO |
| CMO | Marketing, press, sales | CEO |
| COO | Operations, support, HR | CEO |
| CIO | Technical, security | CTO |
| CLO | Legal, compliance | CEO → Human |
| CPO | Product | CEO |
| CTO | Engineering | CIO |

---

## Logging

Every routing decision logged with:
- Timestamp
- Communication type
- Sender info
- Keywords matched
- Routing decision
- Confidence level
- Handling agent

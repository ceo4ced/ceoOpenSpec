# Governance Protocols

## Human Communication with CEO

### Conversation Phase (Pre-GREENLIGHT)

When you message the CEO agent, you're in **conversation mode**:

```
YOU: "I have an idea for an education app..."

CEO: "Interesting! Let me understand better:
      1. Who is the target user?
      2. What problem does it solve?
      3. What's your timeline?"

YOU: "It's for K-12 teachers who need..."

CEO: "Got it. Here's what I'm thinking..."
     [Continues conversation, refines understanding]
```

**During conversation mode:**
- CEO gathers and refines your vision
- CEO may propose a plan
- CEO may ask clarifying questions
- **NO work is assigned to other agents**
- **NO resources are consumed**
- This can go on as long as needed

---

## GREENLIGHT Protocol

### Triggering Execution

The CEO agent **CANNOT** give marching orders to the C-suite until you provide explicit authorization:

```
CEO: "Based on our conversation, here's the business plan:
      [Plan summary]
      
      Ready to proceed? Say GREENLIGHT to authorize the C-suite
      to begin work, or continue discussing."

YOU: "GREENLIGHT"

CEO: "GREENLIGHT received. Initiating C-suite propagation..."
     [Only now does work begin]
```

### GREENLIGHT Rules

| Rule | Description |
|------|-------------|
| **Explicit only** | Must be the word "GREENLIGHT" (case-insensitive) |
| **Revocable** | Say "HALT" to pause all work |
| **Logged** | Every GREENLIGHT is timestamped in audit trail |
| **Scoped** | Each major phase requires its own GREENLIGHT |

### GREENLIGHT Stages

```
┌─────────────────────────────────────────────────────────────────┐
│                    GREENLIGHT GATES                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. GREENLIGHT: VISION                                          │
│     └── CEO can propagate to C-suite (CFO, CMO, COO, CIO, CLO, CPO)
│                                                                  │
│  2. GREENLIGHT: BUILD                                           │
│     └── CTO can begin development (after CMO validation)        │
│                                                                  │
│  3. GREENLIGHT: LAUNCH                                          │
│     └── Product can go live                                     │
│                                                                  │
│  4. GREENLIGHT: SPEND [amount]                                  │
│     └── Any expense over $X threshold                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## RED PHONE: Emergency Escalation

### Overview

Any C-suite agent can use the **RED PHONE** to contact you directly, bypassing the CEO. This is for emergencies, concerns about CEO behavior, or critical issues.

```
┌─────────────────────────────────────────────────────────────────┐
│                         RED PHONE                                │
│                                                                  │
│   🔴 ANY AGENT → HUMAN (bypasses CEO)                           │
│                                                                  │
│   Special Direct Lines:                                         │
│   🔴 CFO → HUMAN (financial emergencies)                        │
│   🔴 CLO → HUMAN (legal emergencies)                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### When to Use RED PHONE

| Agent | Use RED PHONE When |
|-------|--------------------|
| **CFO** | Budget exceeded, financial irregularity, cost overrun |
| **CLO** | Legal risk detected, compliance violation, liability exposure |
| **CMO** | Validation failed but CEO pushing forward |
| **CIO** | Security breach, data leak, privacy violation |
| **COO** | Operational impossibility, safety concern |
| **CPO** | Product direction contradicts market evidence |
| **CTO** | Technical infeasibility, security vulnerability |

### RED PHONE Message Format

```
🔴 RED PHONE ALERT 🔴

FROM: [Position]
PRIORITY: [CRITICAL | HIGH | MEDIUM]
REGARDING: [Brief subject]

SITUATION:
[What happened]

CONCERN:
[Why this is an emergency]

EVIDENCE:
[Supporting data]

RECOMMENDED ACTION:
[What you suggest]

---
This message bypassed the CEO chain of command.
```

---

## Vote of No Confidence

### Overview

If the CEO agent appears to be acting against the business interests, governance rules, or your wishes, the other seven C-suite positions can call for a **Vote of No Confidence**.

### Prerequisites

> ⚠️ **A vote CANNOT be called unless there have been at least 3 documented RED PHONE alerts regarding CEO behavior.**

This ensures:
1. Issues were escalated to the human first
2. Human had opportunity to intervene
3. Pattern of concern is established (not a one-off disagreement)

### Prerequisite Check

```sql
-- Before vote can proceed, verify:
SELECT COUNT(*) >= 3 
FROM red_phone_alerts 
WHERE business_id = @business_id
  AND subject LIKE '%CEO%'
  AND sent_at > DATE_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY);
```

### Triggering a Vote

Any C-suite agent can initiate:

```
[CFO]: "I am calling for a VOTE OF NO CONFIDENCE in the CEO.

REASON: CEO is directing resource allocation that contradicts 
        the approved budget and governance rules.

EVIDENCE: [Specific examples]

All C-suite agents, please register your vote."
```

### Voting Process

| Step | Action |
|------|--------|
| 1 | Any agent calls for vote with stated reason |
| 2 | All 7 non-CEO positions vote: CONFIDENCE or NO CONFIDENCE |
| 3 | Simple majority (4+) decides outcome |
| 4 | Result is logged and human is notified |

### Vote Outcomes

#### If Vote PASSES (4+ No Confidence):

```
┌─────────────────────────────────────────────────────────────────┐
│                    CEO REMOVED: SUCCESSION                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. CEO agent is suspended                                      │
│  2. NO new vision is created                                    │
│  3. Existing approved mandates CONTINUE                         │
│  4. CFO becomes acting leader (profit focus)                    │
│  5. CEO role is NOT replaced                                    │
│  6. Human is notified immediately via RED PHONE                 │
│                                                                  │
│  RATIONALE: Vision is complete. Execution continues.            │
│             CFO aims for profitability with existing plan.      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### If Vote FAILS (3 or fewer No Confidence):

```
┌─────────────────────────────────────────────────────────────────┐
│                    CEO RETAINED                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. CEO continues in role                                       │
│  2. Vote is logged for audit trail                              │
│  3. Human is notified of the vote (for awareness)               │
│  4. Dissenting agents document concerns                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### CFO Succession Powers

When CFO takes over after successful vote:

| Power | Status |
|-------|--------|
| Change vision | ❌ CANNOT |
| Create new mandates | ❌ CANNOT |
| Modify existing approved work | ✅ CAN (efficiency focus) |
| Allocate resources | ✅ CAN (within budget) |
| Pause/prioritize work | ✅ CAN |
| Call for spending cuts | ✅ CAN |
| Report to human | ✅ REQUIRED (more frequent) |

---

## Failsafe Summary

```
                    NORMAL OPERATION
                          │
                          ▼
               ┌─────────────────────┐
               │  CEO leads C-suite  │
               │  (with GREENLIGHT)  │
               └──────────┬──────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
    ┌─────────┐      ┌─────────┐      ┌─────────┐
    │ CONCERN │      │  ISSUE  │      │ CRISIS  │
    └────┬────┘      └────┬────┘      └────┬────┘
         │                │                │
         ▼                ▼                ▼
    ┌─────────┐      ┌─────────┐      ┌─────────┐
    │ CEO     │      │   RED   │      │ VOTE OF │
    │ Inquiry │      │  PHONE  │      │   NO    │
    └────┬────┘      └────┬────┘      │CONFIDENCE│
         │                │           └────┬────┘
         │                │                │
         ▼                ▼                ▼
    ┌─────────┐      ┌─────────┐      ┌─────────┐
    │ CEO     │      │ HUMAN   │      │ CFO     │
    │resolves │      │ decides │      │ leads   │
    └─────────┘      └─────────┘      └─────────┘
```

---

## Implementation in BigQuery

```sql
-- GREENLIGHT tracking
CREATE TABLE greenlights (
  greenlight_id STRING,
  business_id STRING,
  stage STRING,           -- VISION, BUILD, LAUNCH, SPEND
  granted_at TIMESTAMP,
  granted_by STRING,      -- Human identifier
  scope STRING,           -- What was authorized
  revoked_at TIMESTAMP,   -- NULL if still active
  revoked_reason STRING
);

-- RED PHONE alerts
CREATE TABLE red_phone_alerts (
  alert_id STRING,
  business_id STRING,
  from_agent STRING,
  priority STRING,
  subject STRING,
  content JSON,
  sent_at TIMESTAMP,
  acknowledged_at TIMESTAMP,
  resolution STRING
);

-- Votes of No Confidence
CREATE TABLE votes_of_no_confidence (
  vote_id STRING,
  business_id STRING,
  initiated_by STRING,
  reason STRING,
  initiated_at TIMESTAMP,
  votes JSON,              -- {"CFO": "NO_CONFIDENCE", "CMO": "CONFIDENCE", ...}
  result STRING,           -- PASSED | FAILED
  completed_at TIMESTAMP
);
```

---

*Part of CEO OpenSpec Governance Framework*

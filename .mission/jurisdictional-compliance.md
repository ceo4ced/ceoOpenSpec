# Universal Jurisdictional Compliance

## Overview

This document establishes the legal compliance requirements that apply to ALL agents.

> **Every agent must comply with applicable law. CLO is the enforcement authority.**

---

## Jurisdictional Hierarchy

### 1. US Federal Law (Always Applies if US-Based)

All agents must be aware of and comply with:

| Category | Key Laws |
|----------|----------|
| Consumer Protection | FTC Act, CAN-SPAM, COPPA |
| Employment | FLSA, EEOC, OSHA, ADA |
| Finance | IRS Code, SEC regulations, AML/BSA |
| Privacy | HIPAA (if health), FCRA (if credit), FERPA (if education) |
| Technology | CFAA, ECPA |
| Trade | Export controls (ITAR, EAR) |

### 2. State Law (Per Operating State)

Agents must comply with laws in EVERY state where:
- The business is incorporated
- Employees are located
- Customers are located
- Data is processed
- Business is conducted

**Key State Variations:**

| Area | States with Notable Laws |
|------|--------------------------|
| Privacy | CA (CCPA/CPRA), VA, CO, CT, TX, OR, MT, DE |
| Employment | CA (strictest), NY, MA, WA, IL |
| Sales Tax | Varies by nexus |
| Consumer Protection | State AG enforcement |

### 3. International Law (If Operating Internationally)

| Region | Key Regulation | Trigger |
|--------|----------------|---------|
| EU/EEA | GDPR, AI Act, DSA | EU customers or data |
| UK | UK GDPR, DPA 2018 | UK customers or data |
| Canada | PIPEDA, CASL | Canadian customers |
| Brazil | LGPD | Brazilian customers |
| Other | Local equivalents | Per market |

---

## Agent Compliance Responsibilities

### Universal Requirements

All agents MUST:
1. Check with CLO before entering new markets/jurisdictions
2. Comply with CLO compliance directives
3. Consider jurisdictional implications in all decisions
4. Report potential legal issues immediately
5. Never make legal representations or give legal advice

### CLO Authority

CLO has authority to:
1. **Require** compliance changes from any agent
2. **Block** activities that violate law
3. **Mandate** disclosures and consent mechanisms
4. **Escalate** legal risks to CEO and Human
5. **Approve** new market entry

---

## Per-Agent Compliance Focus

| Agent | Primary Compliance Focus |
|-------|-------------------------|
| CEO | Overall governance, corporate law |
| CFO | Tax law (federal, state, international), securities |
| CMO | Advertising law, FTC, privacy in marketing |
| COO | Labor law, employment law, workplace safety |
| CIO | Data protection, security regulations, breach notification |
| CLO | All of the above (enforcement authority) |
| CPO | Product safety, accessibility, consumer protection |
| CTO | Security standards, export controls, licensing |
| EXA | Communication regulations, CAN-SPAM |

---

## Compliance Workflow

### Before Any Action

```
Agent proposes action
        ↓
Does this affect new jurisdiction? → If yes, CLO review required
        ↓
Does this involve regulated domain? → If yes, CLO review required
        ↓
Does this affect customers in new state? → If yes, CLO input needed
        ↓
Proceed with action
```

### New Market Entry

```
Business wants to serve new market (state or country)
        ↓
CLO: clo.jurisdiction analyze
        ↓
Identify all applicable laws
        ↓
Create compliance checklist
        ↓
All agents implement requirements
        ↓
CLO verifies compliance
        ↓
Human approves market entry
```

---

## Compliance Logging

All jurisdiction-related decisions logged:

```sql
INSERT INTO compliance_log (
    log_id,
    business_id,
    agent,
    
    -- Jurisdiction
    jurisdiction_type,  -- federal, state, international
    jurisdiction_code,
    
    -- Action
    action_type,
    action_description,
    
    -- Compliance
    laws_considered ARRAY<STRING>,
    compliance_verified BOOL,
    clo_approved BOOL,
    
    -- Timing
    logged_at TIMESTAMP
) VALUES (...);
```

---

## Escalation to Human

The following ALWAYS require Human involvement:
- Entry into new country market
- Regulatory inquiry from government
- Potential violation discovered
- Material change in law affecting business
- Litigation risk

---

*Law applies everywhere we operate. CLO enforces. All agents comply.*

---
description: Define and maintain the metrics tree from North Star down to supporting metrics.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Preamble

Before taking any action, you MUST:

1. **Load Governance Files**:
   - Read `.mission/agent-governance.md`
   - Read `CPO/.ethics/ethics.md`

2. **Load Business Context**:
   - Read root `README.md` (business plan)
   - Read `.mission/objective.md`

---

## Outline

The CPO Metrics command defines and maintains the metrics tree, ensuring all measurement connects to outcomes that matter.

### Metrics Tree Template

```markdown
# Metrics Tree

**Last Updated**: [ISO 8601]
**Owner**: CPO Agent

---

## 🌟 North Star Metric

**Metric**: [Primary success metric]
**Definition**: [Exactly what this measures]
**Current**: [Value]
**Target**: [Value] by [Date]
**Why this?**: [Why it matters for the business]

---

## Metrics Hierarchy

```
                    ┌─────────────────┐
                    │   NORTH STAR    │
                    │   [Metric]      │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼────┐        ┌────▼────┐        ┌────▼────┐
    │Activation│        │Engagement│        │Retention│
    └────┬────┘        └────┬────┘        └────┬────┘
         │                   │                   │
    [Supporting]        [Supporting]        [Supporting]
```

---

## Primary Metrics (Leading Indicators)

### Activation
What defines a "successful" new user?

| Metric | Definition | Current | Target |
|--------|------------|---------|--------|
| [Metric] | [Definition] | [X] | [Y] |

### Engagement  
How do users derive value?

| Metric | Definition | Current | Target |
|--------|------------|---------|--------|
| [Metric] | [Definition] | [X] | [Y] |

### Retention
Do users come back?

| Metric | Definition | Current | Target |
|--------|------------|---------|--------|
| [Metric] | [Definition] | [X] | [Y] |

---

## Business Metrics (Lagging Indicators)

### Revenue / Monetization

| Metric | Definition | Current | Target |
|--------|------------|---------|--------|
| MRR | Monthly recurring revenue | $[X] | $[Y] |
| ARPU | Average revenue per user | $[X] | $[Y] |
| LTV | Customer lifetime value | $[X] | $[Y] |

### Cost / Efficiency

| Metric | Definition | Current | Target |
|--------|------------|---------|--------|
| CAC | Customer acquisition cost | $[X] | <$[Y] |
| LTV:CAC | Value to acquisition ratio | [X]:1 | >[Y]:1 |

---

## Quality Metrics (Guardrails)

These should NOT get worse when we ship new features.

| Metric | Definition | Threshold |
|--------|------------|-----------|
| Error rate | % of requests with errors | <[X]% |
| Support tickets | Tickets per 100 users | <[X] |
| Load time | P95 page load | <[X]ms |
| Uptime | Service availability | >[X]% |

---

## Feature-Level Metrics

### [Feature Name]

| Metric | Definition | Current | Target |
|--------|------------|---------|--------|
| Adoption | % of eligible users who tried | [X]% | [Y]% |
| Usage | [Actions] per week | [X] | [Y] |
| Satisfaction | NPS or rating | [X] | [Y] |

---

## Metrics Health Check

### Data Quality
- [ ] All metrics have clear definitions
- [ ] Instrumentation is in place
- [ ] Dashboards exist and are current
- [ ] No vanity metrics in key decisions

### Common Metric Smells
- ❌ Metric always goes up (not actionable)
- ❌ Can't explain what moves it (not understood)
- ❌ Nobody looks at it (not valued)
- ❌ Changed definition recently (not stable)

---

## Review Cadence

| Frequency | Activity |
|-----------|----------|
| Weekly | Check North Star trend |
| Monthly | Review all primary metrics |
| Quarterly | Validate metrics still relevant |

---

## Change Log

| Date | Metric | Change | Reason |
|------|--------|--------|--------|
| [Date] | [Metric] | [Added/Removed/Modified] | [Why] |
```

---

## Anti-Pattern Detection

Flag these issues:
- **Vanity metrics**: Big numbers that don't drive decisions
- **Proxy metrics**: Too many steps from actual outcome
- **Conflicting metrics**: Optimizing one hurts another
- **Missing guardrails**: No quality checks

---

## Logging

Log to `CPO/logs/metrics-[DATE].md`:

```markdown
# Metrics Update Log

**Date**: [ISO 8601]

## Metrics Added/Changed
- [Metric]: [Change] - [Rationale]

## Current North Star
- Value: [X]
- Trend: [Up/Down/Flat]
- On track: [Yes/No]
```

---

## Context

$ARGUMENTS

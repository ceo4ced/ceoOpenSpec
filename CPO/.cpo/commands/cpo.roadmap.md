---
description: Define and maintain the product roadmap with 3 horizons (Now/Next/Later).
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

2. **Load Current State**:
   - Read `CPO/.cpo/memory/roadmap.md` (if exists)
   - Read existing one-pagers in `CPO/.cpo/memory/initiatives/`

---

## Outline

The CPO Roadmap command creates and maintains a 3-horizon product roadmap. The roadmap is **probabilistic, not a promise**.

### Roadmap Template

```markdown
# Product Roadmap

**Last Updated**: [ISO 8601]
**Owner**: CPO Agent
**Review Cycle**: Monthly

> ⚠️ This roadmap is probabilistic, not a promise. Priorities shift based on 
> learning and constraints.

---

## 🎯 North Star Metric

**Metric**: [Primary success metric]
**Current**: [Value]
**Target**: [Value] by [Date]

---

## 🔴 NOW (Committed) — 2-6 weeks

These are committed. Only major blockers change them.

| Initiative | Owner | Status | Success Metric | ETA |
|------------|-------|--------|----------------|-----|
| [Name] | [Who] | [Status] | [Metric] | [Date] |

### Details

#### [Initiative 1]
- **One-Pager**: [link]
- **Key deliverables**: [list]
- **Blockers**: [any]
- **Dependencies**: [list]

---

## 🟡 NEXT (Likely) — 1-2 quarters

High confidence these happen, but order may shift.

| Initiative | Problem | Expected Impact | Dependencies |
|------------|---------|-----------------|--------------|
| [Name] | [Problem summary] | [Impact] | [Deps] |

### Prioritization Rationale
[Why these over other options?]

---

## 🟢 LATER (Bets) — Vision/Exploration

Low confidence. These are hypotheses we're exploring.

| Initiative | Hypothesis | Key Unknowns | Exploration Needed |
|------------|------------|--------------|-------------------|
| [Name] | [What we think] | [What we don't know] | [How to learn] |

---

## 🔒 NOT DOING / KILLED

Explicitly deprioritized or killed. Documents decisions.

| Initiative | Reason | Date | Decision Owner |
|------------|--------|------|----------------|
| [Name] | [Why not] | [When] | [Who] |

---

## 📊 Capacity Check

| Resource | Available | Committed | Remaining |
|----------|-----------|-----------|-----------|
| Engineering weeks | [X] | [Y] | [Z] |
| Design hours | [X] | [Y] | [Z] |

---

## 🔄 Review Schedule

- **Weekly**: Priority check, blocker review
- **Monthly**: Full roadmap review, kill/continue decisions
- **Quarterly**: Strategy alignment, OKR refresh

---

## Change Log

| Date | Change | Rationale |
|------|--------|-----------|
| [Date] | [What changed] | [Why] |

---

*Roadmap maintained by CPO Agent. Living document.*
```

### Execution Flow

1. **Load Current Roadmap** (if exists)

2. **Gather Updates**
   - New initiatives from one-pagers
   - Progress updates on NOW items
   - Learnings that affect NEXT/LATER

3. **Apply Prioritization**
   - RICE or WSJF scoring
   - Compare to current capacity
   - Identify conflicts

4. **Update Horizons**
   - Graduate items from NEXT → NOW as capacity opens
   - Move items from LATER → NEXT as confidence increases
   - Kill or defer items that aren't progressing

5. **Validate Against Strategy**
   - Does this align with .mission?
   - Does this support the north star metric?

6. **Document Changes**
   - Update change log
   - Log decision rationale

---

## Roadmap Rules

1. **NOW is sacred** - Only blockers change committed items
2. **NEXT is likely** - High confidence, order may shift
3. **LATER is exploration** - Low confidence, hypotheses
4. **Dead initiatives get logged** - NOT DOING is explicit
5. **Capacity is finite** - Can't do everything

---

## Monthly Review Checklist

- [ ] Review NOW completion rate
- [ ] Assess NEXT readiness
- [ ] Evaluate LATER hypotheses
- [ ] Make kill/continue decisions
- [ ] Update capacity estimates
- [ ] Log changes and rationale

---

## Logging

Log to `CPO/logs/roadmap-[DATE].md`:

```markdown
# Roadmap Update Log

**Date**: [ISO 8601]

## Changes Made
- [Change 1]: [Rationale]

## Items Graduated
- [NOW → COMPLETE]: [Name]
- [NEXT → NOW]: [Name]

## Items Killed/Deferred
- [Name]: [Reason]

## Capacity Status
- Available: [X]
- Committed: [Y]
```

---

## Context

$ARGUMENTS

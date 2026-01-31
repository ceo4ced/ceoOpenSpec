---
description: Record decisions with rationale, tradeoffs, and follow-up metrics to prevent re-litigating.
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

2. **Load Current Decision Log**:
   - Read `CPO/.cpo/memory/decision-log.md` (if exists)

---

## Outline

The CPO Decide command records significant decisions with full context, rationale, and tradeoffs. This prevents re-litigating decisions and creates accountability.

### Decision Log Entry Template

```markdown
## Decision #[N]: [SHORT_TITLE]

**Date**: [ISO 8601]
**Decision Owner**: [Who made/approved this]
**Status**: ACTIVE | SUPERSEDED | REVERSED

---

### Context
[What situation prompted this decision?]

### Decision
[What was decided?]

### Options Considered

| Option | Pros | Cons | Why Not? |
|--------|------|------|----------|
| Chosen: [X] | [Pros] | [Cons] | ✅ Selected |
| [Option B] | [Pros] | [Cons] | [Why rejected] |
| [Option C] | [Pros] | [Cons] | [Why rejected] |

### Rationale
[Why this option over others?]

### Tradeoffs Accepted
- ✅ We gain: [benefit]
- ❌ We lose: [cost]
- ⚠️ We risk: [risk]

### Stakeholders Consulted
- [Person/Role]: [Input given]

### Follow-up Metric
- **What we'll measure**: [Metric]
- **Expected outcome**: [Target]
- **Review date**: [When]

### Reversibility
[Easy / Moderate / Hard] to reverse

### Related Decisions
- [Link to related decision]

---
```

### Execution Flow

1. **Capture Decision Details**
   - What was decided?
   - Who made the decision?
   - What triggered it?

2. **Document Options Considered**
   - What alternatives existed?
   - Why were they rejected?
   - What tradeoffs were made?

3. **Define Success Metric**
   - How will we know if this was right?
   - When will we review?

4. **Assess Reversibility**
   - How hard is it to undo?
   - What's the blast radius if wrong?

5. **Cross-Reference**
   - Link to related decisions
   - Update roadmap if applicable
   - Notify relevant stakeholders

---

## When to Log a Decision

Log decisions when:
- Prioritization changes (what gets done)
- Scope changes (what's in/out)
- Architecture choices (build/buy/integrate)
- Policy changes (how things work)
- Kill decisions (sunsetting features)
- Pricing/packaging changes
- Launch/rollback decisions

---

## Decision Review Process

### Weekly
- Review recent decisions for completeness
- Check for decisions missing from log

### Monthly  
- Review follow-up metrics for past decisions
- Identify patterns in decision-making
- Flag decisions that may need revisiting

### Quarterly
- Audit decision log for superseded entries
- Update status of long-term decisions

---

## Decision Log File

Maintain at `CPO/.cpo/memory/decision-log.md`:

```markdown
# Product Decision Log

**Last Updated**: [ISO 8601]

## Active Decisions

[Most recent first]

---

## Superseded/Reversed Decisions

[Historical record]

---

## Pending Review

| Decision | Review Date | Status |
|----------|-------------|--------|
| [Name] | [Date] | [Due/Overdue] |
```

---

## Logging

Log to `CPO/logs/decisions-[DATE].md`:

```markdown
# Decision Log Update

**Date**: [ISO 8601]

## New Decisions Recorded
- Decision #[N]: [Title]

## Reviews Conducted
- Decision #[N]: [Outcome]

## Status Changes
- Decision #[N]: [Old status] → [New status]
```

---

## Context

$ARGUMENTS

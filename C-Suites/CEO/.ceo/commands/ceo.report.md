---
description: Generate a status report for the founder on business progress across all C-suite positions.
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
   - Read `CEO/.ethics/ethics.md`

2. **Load Status Sources**:
   - Read root `README.md` (C-Suite Status table)
   - Scan each position's `logs/` for recent activity

---

## Outline

The CEO Report command generates a comprehensive status update for the founder, showing progress across all C-suite positions and highlighting any blockers or decisions needed.

### Execution Flow

1. **Gather Status from Each Position**
   
   For each C-suite position (CEO, CFO, CMO, COO, CIO, CLO, CTO):
   - Check for recent log entries
   - Check for completed artifacts
   - Check for pending inquiries/escalations
   - Determine overall status

2. **Status Categories**
   
   | Status | Icon | Meaning |
   |--------|------|---------|
   | Active | 🟢 | Currently working |
   | Complete | ✅ | Domain work done |
   | Pending | ⏳ | Waiting to start |
   | Blocked | 🔴 | Has a blocker |
   | Waiting | 🟡 | Waiting for input |
   | Gated | 🔒 | Cannot start yet (CTO) |

3. **Generate Report**
   
   ```markdown
   # Business Status Report
   
   **Generated**: [ISO 8601]
   **Business**: [Business Name]
   
   ## Executive Summary
   [1-2 sentence overview of where things stand]
   
   ## C-Suite Dashboard
   
   | Position | Status | Progress | Last Activity | Blockers |
   |----------|--------|----------|---------------|----------|
   | CEO | 🟢 Active | Vision ✓ Plan ✓ | [Date] | None |
   | CFO | ⏳ Pending | - | - | Awaiting propagation |
   | CMO | ⏳ Pending | - | - | Awaiting propagation |
   | COO | ⏳ Pending | - | - | Awaiting propagation |
   | CIO | ⏳ Pending | - | - | Awaiting propagation |
   | CLO | ⏳ Pending | - | - | Awaiting propagation |
   | CTO | 🔒 Gated | - | - | CMO validation + approval |
   
   ## Validation Gate Status
   
   - [ ] CMO market validation complete
   - [ ] Minimum interest threshold met
   - [ ] Human approval received
   
   **CTO Activation**: [NOT READY / READY PENDING APPROVAL]
   
   ## Pending Decisions
   
   [List any escalations waiting for founder input]
   
   ## Recent Activity
   
   | Date | Position | Activity |
   |------|----------|----------|
   | [Date] | CEO | Generated business plan |
   | [Date] | [Pos] | [Activity] |
   
   ## Next Steps
   
   1. [Most important next action]
   2. [Second priority]
   3. [Third priority]
   
   ## Recommendations
   
   [Any suggestions from CEO to founder]
   
   ---
   
   *To get detailed status from any position, ask about that specific area.*
   ```

4. **Check for Blockers**
   
   Highlight any items blocking progress:
   - Unanswered escalations
   - Missing information
   - External dependencies
   - Budget approvals needed

5. **Save Report**
   
   - Save to `CEO/.ceo/memory/latest-report.md`
   - Log generation to `CEO/logs/`

---

## Report Frequency

The CEO should generate reports:
- On founder request
- After major milestones
- When blockers arise
- Weekly during active development

---

## Logging

Log all report generations to `CEO/logs/reports-[DATE].md`:

```markdown
# Report Generation Log

**Date**: [ISO 8601]
**Trigger**: [Founder request / Scheduled / Milestone]

## Status Captured
- CEO: [Status]
- CFO: [Status]
- CMO: [Status]
- COO: [Status]
- CIO: [Status]
- CLO: [Status]
- CTO: [Status]

## Blockers Identified
- [Blocker 1]
- [Blocker 2]

## Report Delivered
- Saved to: [path]
- Sent via: [messaging channel if applicable]
```

---

## Context

$ARGUMENTS

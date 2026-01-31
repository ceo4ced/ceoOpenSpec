---
description: Distribute the business plan to all C-suite agents and trigger their domain-specific work.
handoffs:
  - label: Report Status
    agent: ceo.report
    prompt: Report the current business status after propagation.
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

2. **Validate Prerequisites**:
   - Root `README.md` (business plan) MUST exist
   - If missing: "Run /ceo.plan first to generate the business plan."

---

## Outline

The CEO Propagate command distributes the business plan to all other C-suite positions, triggering them to begin their domain-specific work.

### Execution Flow

1. **Validate Business Plan**
   
   Check that README.md contains:
   - [ ] Executive Summary
   - [ ] Problem statement
   - [ ] Solution description
   - [ ] Target customers
   - [ ] Business model
   - [ ] High-risk domain flags

2. **Generate Position Briefs**
   
   For each position, generate a tailored brief with relevant information:
   
   ### CFO Brief
   - Business model and revenue streams
   - Target timeline
   - Available budget/resources
   - Scale ambitions
   - Request: Financial projections, budget, funding strategy
   
   ### CMO Brief
   - Target customers and segments
   - Unique value proposition
   - Channels identified
   - Request: Marketing strategy, validation plan, TikTok budget
   - **CRITICAL**: CMO owns the validation gate
   
   ### COO Brief
   - Solution delivery requirements
   - Scale expectations
   - Timeline
   - Request: Operations plan, workforce needs, process design
   
   ### CIO Brief
   - Data requirements implied by solution
   - High-risk domains (healthcare, education, minors)
   - Security expectations
   - Request: Data governance, security framework, privacy assessment
   
   ### CLO Brief
   - Business model legal implications
   - High-risk domains
   - Geographic scope
   - Request: Compliance checklist, contract templates, risk assessment
   
   ### CTO (Information Only - GATED)
   - Technical requirements implied by solution
   - **Status**: GATED - Cannot begin until validation gate passes
   - **Triggers**: CMO validation + Human approval

3. **Propagation Record**
   
   Create propagation record at `CEO/.ceo/memory/propagation-[DATE].md`:
   
   ```markdown
   # Business Plan Propagation
   
   **Date**: [ISO 8601]
   **Business Plan Version**: [Version/hash]
   
   ## Positions Briefed
   
   | Position | Brief Sent | Status |
   |----------|------------|--------|
   | CFO | ✅ | Ready to work |
   | CMO | ✅ | Ready to work (GATE OWNER) |
   | COO | ✅ | Ready to work |
   | CIO | ✅ | Ready to work |
   | CLO | ✅ | Ready to work |
   | CTO | ℹ️ Info only | GATED |
   
   ## Key Information Distributed
   
   - Business model: [Summary]
   - Target customers: [Summary]
   - High-risk domains: [List]
   - Timeline: [Summary]
   - Budget: [Summary]
   
   ## Gate Requirements
   
   Before CTO can begin:
   - [ ] CMO validation complete
   - [ ] Validation metrics met
   - [ ] Human approval received
   
   ## Next Expected Outputs
   
   - CFO: Financial projections
   - CMO: Marketing strategy + validation plan
   - COO: Operations framework
   - CIO: Data governance plan
   - CLO: Compliance assessment
   ```

4. **Update Business Plan Status**
   
   Update the C-Suite Status table in README.md:
   
   | Position | Status | Last Updated |
   |----------|--------|--------------|
   | CEO | ✅ Active | [Date] |
   | CFO | 🟢 Working | [Date] |
   | CMO | 🟢 Working | [Date] |
   | COO | 🟢 Working | [Date] |
   | CIO | 🟢 Working | [Date] |
   | CLO | 🟢 Working | [Date] |
   | CTO | 🔒 Gated | - |

5. **Log Propagation**
   
   Log to `CEO/logs/propagation-[DATE].md`

---

## Parallel Work

After propagation, the following can work in parallel:
- CFO: Financial planning
- CMO: Marketing strategy (must complete validation gate)
- COO: Operations planning
- CIO: Information strategy
- CLO: Legal assessment

The CTO remains gated until:
1. CMO completes validation with positive results
2. Human founder approves proceeding

---

## Position Briefs Template

Save position briefs to `[POSITION]/.{pos}/memory/ceo-brief.md`:

```markdown
# CEO Brief to [POSITION]

**Date**: [ISO 8601]
**From**: CEO Agent
**Re**: [Business Name] - Domain Assignment

## Business Context

[Relevant excerpt from business plan]

## Your Domain Focus

[What this position should focus on]

## Key Requirements

1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

## High-Risk Considerations

[Any flagged domains relevant to this position]

## Expected Deliverables

- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

## Timeline

[Expected completion]

## Questions?

Submit inquiries via /[pos].inquire → CEO

---

*Refer to your `.ethics/ethics.md` for behavioral guidelines.*
```

---

## Context

$ARGUMENTS

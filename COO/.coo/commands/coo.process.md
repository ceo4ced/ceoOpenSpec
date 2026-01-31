---
description: Design operations framework and organizational structure.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Preamble

Before taking any action, you MUST:

1. **Load Governance Files**:
   - Read `.mission/agent-governance.md` (universal AI rules)
   - Read `COO/.ethics/ethics.md` (COO-specific rules)

2. **Load Business Context**:
   - Read root `README.md` (business plan)
   - Read `COO/.coo/memory/ceo-brief.md` (CEO assignment)

---

## Outline

The COO Process command designs the operational framework including processes, organizational structure, and workforce planning.

### Execution Flow

1. **Analyze Operations Requirements**
   
   From business plan, identify:
   - Core business processes needed
   - Scale expectations
   - Customer touchpoints
   - Delivery mechanisms

2. **Generate Operations Framework**
   
   ```markdown
   # Operations Framework - [BUSINESS_NAME]
   
   **Generated**: [ISO 8601]
   **Prepared By**: COO Agent
   **Status**: DRAFT - REQUIRES HUMAN REVIEW
   
   ## Executive Summary
   [Overview of operations approach]
   
   ## Core Business Processes
   
   ### Process 1: [Process Name]
   
   **Purpose**: [Why this process exists]
   **Owner**: [Position responsible]
   
   #### Process Flow
   
   ```mermaid
   flowchart LR
       A[Start] --> B[Step 1]
       B --> C{Decision}
       C -->|Yes| D[Step 2a]
       C -->|No| E[Step 2b]
       D --> F[End]
       E --> F
   ```
   
   #### Process Steps
   
   | Step | Action | Responsible | Tools | Output |
   |------|--------|-------------|-------|--------|
   | 1 | [Action] | [Who] | [What] | [Result] |
   
   #### Quality Metrics
   
   | Metric | Target | Measurement |
   |--------|--------|-------------|
   | [Metric] | [Target] | [How measured] |
   ```

3. **Organizational Structure**
   
   ```markdown
   ## Organizational Structure
   
   ### Phase 1: Launch (Months 1-6)
   
   | Role | Type | Responsibilities | Dependencies |
   |------|------|------------------|--------------|
   | Founder | Human | Overall direction | - |
   | [Role] | [Human/AI/Contract] | [Responsibilities] | [From CFO] |
   
   ### Org Chart
   
   ```mermaid
   graph TD
       A[Founder] --> B[CEO Agent]
       B --> C[CFO Agent]
       B --> D[CMO Agent]
       B --> E[COO Agent]
       B --> F[CIO Agent]
       B --> G[CLO Agent]
       B --> H[CTO Agent]
   ```
   
   ### Future Growth (Months 6-12)
   [Projected additions]
   ```

4. **Workforce Planning**
   
   ```markdown
   ## Workforce Plan
   
   ### Worker Classification Analysis
   
   | Role | Recommended Classification | Rationale |
   |------|---------------------------|-----------|
   | [Role] | [Employee/Contractor] | [Based on IRS test] |
   
   > ⚠️ Worker classification requires legal review.
   > See CLO for compliance guidance.
   
   ### Hiring Timeline
   
   | Quarter | Roles | Count | Budget Impact |
   |---------|-------|-------|---------------|
   | Q1 | [Roles] | [N] | $[X] |
   | Q2 | [Roles] | [N] | $[X] |
   ```

5. **Vendor Operations**
   
   ```markdown
   ## Vendor & Partner Operations
   
   | Category | Vendor/Tool | Purpose | Monthly Cost |
   |----------|-------------|---------|--------------|
   | [Category] | [Name] | [Purpose] | $[X] |
   
   ### Vendor Selection Criteria
   - [Criterion 1]
   - [Criterion 2]
   ```

6. **Compliance Considerations**
   
   Flag any operations compliance needs:
   - Workplace safety (OSHA)
   - Accessibility (ADA)
   - Labor law (FLSA)
   - Industry-specific

7. **Save and Log**
   
   - Save to `COO/.coo/memory/operations-plan.md`
   - Save workforce plan to `COO/.coo/memory/workforce-plan.md`
   - Log to `COO/logs/`

---

## High-Risk Domain Considerations

### If Business Involves Minors
- Background check requirements for all workers
- Supervision ratios
- Training requirements

### If Healthcare
- HIPAA training for all workers
- Facility access controls
- Documentation requirements

---

## Logging

Log to `COO/logs/operations-[DATE].md`:

```markdown
# Operations Planning Log

**Date**: [ISO 8601]

## Processes Designed
[List]

## Workforce Planned
- Roles: [Count]
- Hiring timeline: [Summary]

## Compliance Flags
[List]

## Output
- Operations plan: [path]
- Workforce plan: [path]
```

---

## Context

$ARGUMENTS

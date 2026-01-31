# cpo.prd

## Preamble

This command creates a Product Requirements Document (PRD) for a feature or initiative.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CPO/.ethics/ethics.md`
3. Related `cpo.onepager` for context

---

## Overview

> **A PRD is a contract between Product, Engineering, and Design.**

PRDs are created for complex features that require detailed specification beyond a one-pager.

---

## Command Types

```
cpo.prd create [feature-name]     # Create new PRD
cpo.prd update [prd-id]           # Update existing PRD
cpo.prd review [prd-id]           # Request review
cpo.prd status                    # List all PRDs and status
```

---

## PRD Template

### Header

```markdown
# PRD: [Feature Name]

| Field | Value |
|-------|-------|
| PRD ID | PRD-[YYYYMMDD]-[SEQ] |
| Version | 1.0 |
| Author | CPO |
| Status | Draft / Review / Approved / Archived |
| One-Pager | [Link to one-pager] |
| Jira/Issue | [Link] |

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | CPO | Initial draft |
```

### Problem Statement

```markdown
## Problem Statement

### Current State
[Describe how things work today]

### Problem
[What specific problem are we solving?]

### Users Affected
[Who experiences this problem? How many?]

### Evidence
[Data, quotes, research supporting this is a real problem]
- Usage data: [metrics]
- Customer feedback: [quotes, ticket counts]
- Research: [study references]

### Impact of Not Solving
[What happens if we do nothing?]
```

### Goals & Success Metrics

```markdown
## Goals

### Primary Goal
[Single most important outcome]

### Secondary Goals
[Other outcomes we care about]

### Non-Goals
[Explicitly what we are NOT doing]

## Success Metrics

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| [Primary metric] | [X] | [Y] | [How measured] |
| [Secondary metric] | [X] | [Y] | [How measured] |

### Instrumentation Plan
[How will we track these metrics? What events/logging needed?]
```

### User Stories & Requirements

```markdown
## User Stories

### Core User Stories

**As a** [user type]
**I want to** [action]
**So that** [outcome]

Acceptance Criteria:
- [ ] [Specific testable criterion]
- [ ] [Another criterion]

### Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| [Edge case] | [What should happen] |
```

### Detailed Requirements

```markdown
## Functional Requirements

### [Feature Area 1]

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-001 | [Requirement] | P0/P1/P2 | [Notes] |

### [Feature Area 2]

[Continue for each area]

## Non-Functional Requirements

| ID | Category | Requirement |
|----|----------|-------------|
| NFR-001 | Performance | [Response time < X ms] |
| NFR-002 | Scalability | [Handle X concurrent users] |
| NFR-003 | Security | [Specific security requirement] |
| NFR-004 | Accessibility | [WCAG level] |
| NFR-005 | Privacy | [Data handling requirement] |
```

### Technical Considerations

```markdown
## Technical Considerations

### Architecture Impact
[How does this affect system architecture?]

### Data Model Changes
[New tables, fields, relationships]

### API Changes
[New endpoints, breaking changes]

### Third-Party Dependencies
[External services, APIs needed]

### Security Considerations
[Authentication, authorization, data protection]

### CTO Handoff Notes
[Specific guidance for engineering]
```

### Dependencies & Risks

```markdown
## Dependencies

| Dependency | Owner | Status | Impact if Delayed |
|------------|-------|--------|-------------------|
| [Dependency] | [Owner] | [Status] | [Impact] |

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | H/M/L | H/M/L | [Plan] |
```

### Launch & Rollout

```markdown
## Launch Plan

### Rollout Strategy
- [ ] Feature flag setup
- [ ] Canary/staged rollout plan
- [ ] Rollback plan

### Training Required
| Audience | Training Type | Owner |
|----------|---------------|-------|
| [Audience] | [Training] | [Owner] |

### Go-to-Market (if customer-facing)
[Coordinate with CMO on: announcement, help docs, etc.]

### Support Readiness
[Coordinate with COO on: FAQ, known issues, support scripts]
```

### Timeline

```markdown
## Timeline

| Phase | Start | End | Deliverable |
|-------|-------|-----|-------------|
| Design | [Date] | [Date] | Mockups approved |
| Development | [Date] | [Date] | Feature complete |
| Testing | [Date] | [Date] | QA passed |
| Rollout | [Date] | [Date] | 100% deployed |
| Measurement | [Date] | [Date] | Success metrics reviewed |
```

### Appendix

```markdown
## Appendix

### Mockups/Designs
[Embed or link to designs]

### Research
[Links to research docs]

### Competitive Analysis
[If applicable]

### Decision Log
[Major decisions made during PRD creation]
```

---

## PRD Workflow

```
One-Pager approved by CEO
        ↓
CPO creates PRD
        ↓
CTO reviews technical feasibility
        ↓
CLO reviews compliance (if applicable)
        ↓
CEO approves or requests changes
        ↓
PRD finalized
        ↓
Handoff to CTO for implementation
```

---

## Review Checklist

Before marking PRD as "Review":

- [ ] Problem statement is clear and evidence-based
- [ ] Success metrics are defined and measurable
- [ ] User stories have acceptance criteria
- [ ] All P0 requirements documented
- [ ] Technical considerations addressed
- [ ] Risks identified with mitigations
- [ ] Dependencies documented
- [ ] Timeline is realistic
- [ ] CLO reviewed (if legal/compliance implications)
- [ ] One-pager linked

---

## Logging

Log to BigQuery:

```sql
INSERT INTO prd_log (
    prd_id,
    business_id,
    
    feature_name,
    onepager_id,
    
    status,
    version,
    
    created_at,
    updated_at,
    approved_at,
    
    approved_by,
    
    requirements_count,
    priority_p0_count,
    
    estimated_effort_days,
    
    handoff_to_cto BOOL,
    handoff_at TIMESTAMP
) VALUES (...);
```

---

*PRDs are contracts. Be specific. Be measurable. Be realistic.*

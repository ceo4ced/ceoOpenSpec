---
description: Record validation results and determine gate decision (PROCEED/PIVOT/ITERATE).
handoffs:
  - label: Request Approval
    agent: cmo.approve
    prompt: Request human approval to activate CTO.
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
   - Read `CMO/.ethics/ethics.md`

2. **Load Validation Criteria**:
   - Read `CMO/.cmo/memory/strategy-v[latest].md` (contains gate criteria)

3. **Acknowledge Gate Responsibility**:
   - This is the critical gate before CTO activation
   - Must be honest about results, even if negative
   - Must recommend human approval before CTO proceeds

---

## Outline

The CMO Validate command records the results of the marketing validation campaign and makes a gate decision.

### Execution Flow

1. **Collect Campaign Results**
   
   Request or import the following data:
   
   ```markdown
   ## Validation Campaign Results
   
   **Campaign Period**: [Start Date] - [End Date]
   **Platform**: TikTok
   **Budget Spent**: $[AMOUNT] of $[BUDGET]
   
   ### Performance Metrics
   
   | Metric | Result | Target | % of Target |
   |--------|--------|--------|-------------|
   | Impressions | [X] | [Y] | [Z]% |
   | Views | [X] | [Y] | [Z]% |
   | Engagement rate | [X]% | [Y]% | [Z]% |
   | Link clicks | [X] | [Y] | [Z]% |
   | Signups/waitlist | [X] | [Y] | [Z]% |
   | Cost per signup | $[X] | $[Y] | [Z]% |
   ```

2. **Analyze Results**
   
   Compare against gate criteria from strategy document:
   
   | Criterion | Threshold | Actual | Status |
   |-----------|-----------|--------|--------|
   | Minimum signups | [X] | [Y] | ✅/❌ |
   | Max cost per signup | $[X] | $[Y] | ✅/❌ |
   | Min engagement rate | [X]% | [Y]% | ✅/❌ |
   | Positive sentiment | Required | [Assessment] | ✅/❌ |

3. **Qualitative Analysis**
   
   - Review comments and feedback
   - Identify common themes
   - Note any red flags
   - Assess sentiment (positive/neutral/negative)

4. **Make Gate Decision**
   
   Based on criteria:
   
   ### 🟢 PROCEED
   
   If ALL minimum thresholds met:
   
   ```markdown
   ## GATE DECISION: PROCEED ✅
   
   **Decision Date**: [ISO 8601]
   **Confidence**: [High/Medium]
   
   ### Evidence
   - [Key metric 1]: Exceeded threshold by [X]%
   - [Key metric 2]: Met threshold
   - Qualitative: [Positive indicators]
   
   ### Key Learnings
   1. [Learning 1]
   2. [Learning 2]
   
   ### Validated Messages (for CTO)
   - [Message that resonated]
   - [Feature most requested]
   
   ### Recommended Next Steps
   1. Request human approval for CTO activation
   2. Share validated messaging with CTO
   3. Begin product development
   
   **ACTION REQUIRED**: Human founder must approve CTO activation.
   ```
   
   ### 🔴 PIVOT
   
   If significantly below thresholds:
   
   ```markdown
   ## GATE DECISION: PIVOT 🔴
   
   **Decision Date**: [ISO 8601]
   
   ### Evidence
   - [Key metric 1]: [X]% below threshold
   - [Key metric 2]: [X]% below threshold
   - Qualitative: [Negative indicators]
   
   ### Analysis: Why It Failed
   1. [Reason 1]
   2. [Reason 2]
   
   ### Recommended Pivots
   
   | Option | Description | New Hypothesis |
   |--------|-------------|----------------|
   | A | [Pivot option] | [What we'd test] |
   | B | [Pivot option] | [What we'd test] |
   
   ### NOT Proceeding to CTO Until:
   - New validation campaign succeeds
   - OR founder decides to proceed despite results
   
   **ACTION REQUIRED**: Discuss pivot options with founder.
   ```
   
   ### 🟡 ITERATE
   
   If close to thresholds:
   
   ```markdown
   ## GATE DECISION: ITERATE 🟡
   
   **Decision Date**: [ISO 8601]
   
   ### Evidence
   - [Key metric 1]: [X]% of threshold (close)
   - [Key metric 2]: Met threshold
   - Qualitative: [Mixed indicators]
   
   ### Analysis: Room for Improvement
   1. [What worked]
   2. [What didn't]
   
   ### Iteration Plan
   - [Change 1] to address [issue]
   - [Change 2] to address [issue]
   - Budget for iteration: $[X]
   - Duration: [X] days
   
   ### Recommendation
   Run one more iteration before CTO activation.
   
   **ACTION REQUIRED**: Approve iteration budget and plan.
   ```

5. **Update Business Plan Status**
   
   Update README.md C-Suite Status table with CMO validation result.

6. **Save and Log**
   
   - Save to `CMO/.cmo/memory/validation-results-[DATE].md`
   - Log to `CMO/logs/`
   - Notify CEO of gate decision

---

## Gate Escalation

Always escalate to founder when:
- Any decision is made (PROCEED/PIVOT/ITERATE)
- Results are ambiguous
- Significant budget was spent without clear outcome

---

## Logging

Log to `CMO/logs/validation-[DATE].md`:

```markdown
# Validation Results Log

**Date**: [ISO 8601]
**Campaign**: [Platform]
**Budget Used**: $[X] of $[Y]

## Results Summary
[Brief summary]

## Metrics vs Thresholds
[Table]

## Qualitative Analysis
[Summary]

## Gate Decision
[PROCEED/PIVOT/ITERATE]

## Rationale
[Why this decision]

## Founder Notification
- Sent via: [Channel]
- Time: [ISO 8601]
```

---

## Context

$ARGUMENTS

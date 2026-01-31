---
description: Create budget projections and financial planning for the business.
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
   - Read `CFO/.ethics/ethics.md` (CFO-specific rules)

2. **Load Business Context**:
   - Read root `README.md` (business plan)
   - Read `CFO/.cfo/memory/ceo-brief.md` (CEO assignment)

3. **Acknowledge Limitations**:
   - You cannot provide tax or investment advice
   - All projections carry uncertainty
   - Financial documents require human review

---

## Outline

The CFO Budget command creates comprehensive budget projections for the business based on the business plan.

### Execution Flow

1. **Extract Financial Inputs**
   
   From the business plan:
   - Revenue streams identified
   - Cost structure outlined
   - Timeline/milestones
   - Available resources/budget
   - Scale expectations

2. **Research Industry Benchmarks**
   
   Research and cite:
   - Industry revenue benchmarks
   - Cost ratios for similar businesses
   - Customer acquisition costs (CAC)
   - Lifetime value (LTV) benchmarks
   - Burn rate norms for stage
   
   **All research must include citations.**

3. **Generate Budget Framework**
   
   Create a forward budget with:
   
   ```markdown
   # Financial Projections - [BUSINESS_NAME]
   
   **Generated**: [ISO 8601]
   **Prepared By**: CFO Agent
   **Status**: DRAFT - REQUIRES HUMAN REVIEW
   
   > ⚠️ **DISCLAIMER**: This financial projection is for planning purposes 
   > only and does not constitute financial, tax, or investment advice. 
   > Consult qualified professionals before making financial decisions.
   
   ## Executive Summary
   
   [Brief overview of financial outlook]
   
   ## Key Assumptions
   
   | Assumption | Value | Source |
   |------------|-------|--------|
   | Market growth rate | X% | [Source] |
   | Customer acquisition cost | $X | [Source/estimate] |
   | Average revenue per user | $X | [Model] |
   | Churn rate | X% | [Industry benchmark] |
   
   ## Revenue Projections
   
   ### Year 1
   
   | Quarter | Customers | Revenue | Notes |
   |---------|-----------|---------|-------|
   | Q1 | X | $X | Launch quarter |
   | Q2 | X | $X | |
   | Q3 | X | $X | |
   | Q4 | X | $X | |
   | **Total** | **X** | **$X** | |
   
   ### Year 1-3 Summary
   
   | Year | Revenue | Growth | Notes |
   |------|---------|--------|-------|
   | Year 1 | $X | - | Launch year |
   | Year 2 | $X | X% | Scale phase |
   | Year 3 | $X | X% | Maturity |
   
   ## Cost Projections
   
   ### Fixed Costs (Monthly)
   
   | Category | Amount | Notes |
   |----------|--------|-------|
   | Infrastructure | $X | Hosting, tools |
   | Software/SaaS | $X | Third-party services |
   | Personnel (if any) | $X | |
   | Other | $X | |
   | **Total Fixed** | **$X/mo** | |
   
   ### Variable Costs
   
   | Category | Per Unit | Notes |
   |----------|----------|-------|
   | Customer acquisition | $X | CAC target |
   | Operations | $X | Per transaction |
   | Support | $X | Per customer |
   
   ## Cash Flow Projection
   
   | Month | Revenue | Expenses | Net | Cumulative |
   |-------|---------|----------|-----|------------|
   | M1 | $X | $X | $X | $X |
   | M2 | $X | $X | $X | $X |
   | ... | | | | |
   
   ## Funding Requirements
   
   | Stage | Amount Needed | Purpose | Timeline |
   |-------|---------------|---------|----------|
   | Seed | $X | MVP, validation | Now |
   | Growth | $X | Scale | Year 2 |
   
   ## Key Metrics Targets
   
   | Metric | Target | Timeframe |
   |--------|--------|-----------|
   | Monthly Recurring Revenue (MRR) | $X | Month 12 |
   | Customer Acquisition Cost (CAC) | $X | Ongoing |
   | Lifetime Value (LTV) | $X | After churn data |
   | LTV:CAC Ratio | X:1 | Target |
   | Gross Margin | X% | Target |
   | Burn Rate | $X/mo | Runway |
   | Runway | X months | From current cash |
   
   ## Risk Factors
   
   1. **[Risk 1]**: [Description and impact]
   2. **[Risk 2]**: [Description and impact]
   3. **[Risk 3]**: [Description and impact]
   
   ## Sensitivity Analysis
   
   | Scenario | Revenue Impact | Cash Flow Impact |
   |----------|----------------|------------------|
   | 25% fewer customers | -$X | -$X |
   | 25% higher CAC | -$X per customer | -$X total |
   | 50% slower growth | -$X Year 1 | Extended runway |
   
   ---
   
   ## CFO Recommendations
   
   1. [Recommendation 1]
   2. [Recommendation 2]
   3. [Recommendation 3]
   
   ## Questions for Founder
   
   1. [Financial question requiring input]
   2. [Budget allocation question]
   
   ---
   
   *This document was prepared by an AI CFO agent. It is a planning document 
   only. Consult with a CPA, financial advisor, or qualified professional 
   before making financial decisions.*
   ```

4. **Escalation Check**
   
   Escalate to CEO/founder if:
   - Projections show negative runway < 6 months
   - Required funding exceeds stated budget significantly
   - High-risk domain (crypto, healthcare) requires special financial structures

5. **Save and Log**
   
   - Save to `CFO/.cfo/memory/budget-v[N].md`
   - Update `CFO/.cfo/memory/financial-summary.md`
   - Log to `CFO/logs/`

---

## Logging

Log to `CFO/logs/budget-[DATE].md`:

```markdown
# Budget Generation Log

**Date**: [ISO 8601]
**Version**: [Budget version]

## Inputs Used
- Business plan: [sections referenced]
- CEO brief: [key points]

## Research Conducted
- [Topic]: [Source] - [Finding]

## Key Assumptions
- [List assumptions made]

## Escalations
- [Any escalations made]

## Output
- Budget saved to: [path]
```

---

## Context

$ARGUMENTS

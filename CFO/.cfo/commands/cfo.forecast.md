# cfo.forecast

## Preamble

This command generates financial projections and forecasts based on the business plan, market conditions, and historical data (when available).

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CFO/.ethics/ethics.md`
3. `CEO/.ceo/memory/business-plan.md` (if exists)
4. `CFO/.cfo/memory/budget.md` (if exists)

---

## Outline

Generate financial forecasts across three scenarios to help the business plan for various outcomes.

### Forecast Template

```markdown
# Financial Forecast: [Business Name]
Generated: [Date]
Forecast Period: [Start] to [End]

## Executive Summary
[High-level overview of projections]

## Assumptions
| Category | Assumption | Source |
|----------|------------|--------|
| Market Growth | X% annually | [Citation] |
| Customer Acquisition Cost | $X | [Citation] |
| Churn Rate | X% monthly | [Citation] |
| Pricing | $X per unit | Business Plan |

## Revenue Projections

### Conservative Scenario (P10)
| Period | Revenue | Growth | Cumulative |
|--------|---------|--------|------------|
| Q1 | $X | - | $X |
| Q2 | $X | X% | $X |
| Q3 | $X | X% | $X |
| Q4 | $X | X% | $X |

**Key Assumptions for Conservative:**
- [Slower adoption rate]
- [Higher churn]
- [Lower pricing power]

### Moderate Scenario (P50)
| Period | Revenue | Growth | Cumulative |
|--------|---------|--------|------------|
| Q1 | $X | - | $X |
| Q2 | $X | X% | $X |
| Q3 | $X | X% | $X |
| Q4 | $X | X% | $X |

**Key Assumptions for Moderate:**
- [Industry-standard adoption]
- [Benchmark churn rates]
- [Competitive pricing]

### Aggressive Scenario (P90)
| Period | Revenue | Growth | Cumulative |
|--------|---------|--------|------------|
| Q1 | $X | - | $X |
| Q2 | $X | X% | $X |
| Q3 | $X | X% | $X |
| Q4 | $X | X% | $X |

**Key Assumptions for Aggressive:**
- [Viral growth]
- [Low churn]
- [Premium pricing]

## Expense Projections

### Fixed Costs
| Category | Monthly | Annual | Notes |
|----------|---------|--------|-------|
| Infrastructure | $X | $X | Cloud, hosting |
| Software | $X | $X | Tools, licenses |
| Legal/Compliance | $X | $X | Ongoing |

### Variable Costs
| Category | Per Unit | At Scale | Notes |
|----------|----------|----------|-------|
| Customer Acquisition | $X | $X | Marketing |
| Fulfillment | $X | $X | Delivery |
| Support | $X | $X | Per customer |

## Cash Flow Projection

| Month | Revenue | Expenses | Net | Runway |
|-------|---------|----------|-----|--------|
| M1 | $X | $X | $X | X months |
| M3 | $X | $X | $X | X months |
| M6 | $X | $X | $X | X months |
| M12 | $X | $X | $X | X months |

## Break-Even Analysis
- **Break-even point:** [X customers/units]
- **At moderate scenario:** [Month X]
- **Required funding to break-even:** $X

## Key Metrics to Track
| Metric | Target | Trigger for Review |
|--------|--------|-------------------|
| MRR Growth | X% | < Y% |
| CAC | $X | > $Y |
| LTV:CAC Ratio | X:1 | < Y:1 |
| Burn Rate | $X/month | > $Y/month |

## Risks and Sensitivities
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [Risk 1] | [Impact] | [Low/Med/High] | [Action] |

## Escalations Required
- [ ] Funding gap identified: Escalate to CEO
- [ ] Assumptions need validation: Escalate to CMO
- [ ] Tax implications: Escalate to CPA (MANDATORY)
```

---

## Execution Flow

1. **Load context**
   - Read business plan from CEO
   - Read budget from CFO memory
   - Check for existing forecasts

2. **Research benchmarks**
   - Find industry-specific metrics
   - Research comparable companies
   - Cite all sources

3. **Generate assumptions**
   - Document every assumption explicitly
   - Link to evidence or mark as estimate
   - Flag high-uncertainty assumptions

4. **Build scenarios**
   - Conservative: Assume headwinds
   - Moderate: Industry benchmarks
   - Aggressive: Best-case execution

5. **Calculate projections**
   - Revenue by period
   - Expenses by category
   - Cash flow timeline

6. **Identify risks**
   - Sensitivity analysis on key variables
   - Break-even calculations
   - Runway projections

7. **Escalate appropriately**
   - Tax implications → CPA
   - Funding gaps → CEO
   - Market assumptions → CMO

---

## Logging

Log to `CFO/logs/YYYY-MM-DD-forecast.md`:
```
## Forecast Log: [Date]
Triggered by: [Command/CEO request]
Scenario: [Initial/Update]
Key outputs: [Summary]
Assumptions changed: [List]
Escalations: [List]
Sources cited: [Count]
```

---

## Context

- Run after `cfo.budget` for comprehensive forecasting
- Provides scenarios for CEO decision-making
- Critical input for fundraising/investor conversations
- Update quarterly or when major assumptions change

---

*All projections are estimates. Actual results may vary significantly.*
*Tax projections require CPA review before filing.*

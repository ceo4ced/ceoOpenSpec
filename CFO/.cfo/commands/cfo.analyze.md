# cfo.analyze

## Preamble

This command performs financial analysis on business performance, comparing actuals to projections and identifying trends.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CFO/.ethics/ethics.md`
3. `CFO/.cfo/memory/forecast.md` (if exists)
4. `CFO/.cfo/memory/budget.md` (if exists)

---

## Outline

Analyze financial performance and provide actionable insights.

### Analysis Report Template

```markdown
# Financial Analysis: [Business Name]
Period: [Start] to [End]
Generated: [Date]

## Executive Summary
- **Overall Health:** [GREEN | YELLOW | RED]
- **Key Insight:** [One sentence]
- **Action Required:** [Yes/No - what]

## Performance vs. Forecast

### Revenue
| Metric | Forecast | Actual | Variance | Status |
|--------|----------|--------|----------|--------|
| Total Revenue | $X | $X | +/-X% | 🟢/🟡/🔴 |
| MRR | $X | $X | +/-X% | 🟢/🟡/🔴 |
| New Customers | X | X | +/-X% | 🟢/🟡/🔴 |

### Expenses
| Category | Budget | Actual | Variance | Status |
|----------|--------|--------|----------|--------|
| Fixed | $X | $X | +/-X% | 🟢/🟡/🔴 |
| Variable | $X | $X | +/-X% | 🟢/🟡/🔴 |
| Total | $X | $X | +/-X% | 🟢/🟡/🔴 |

### Key Ratios
| Ratio | Target | Actual | Trend | Status |
|-------|--------|--------|-------|--------|
| Gross Margin | X% | X% | ↑/↓/→ | 🟢/🟡/🔴 |
| CAC | $X | $X | ↑/↓/→ | 🟢/🟡/🔴 |
| LTV:CAC | X:1 | X:1 | ↑/↓/→ | 🟢/🟡/🔴 |
| Burn Rate | $X | $X | ↑/↓/→ | 🟢/🟡/🔴 |
| Runway | X mo | X mo | ↑/↓/→ | 🟢/🟡/🔴 |

## Trend Analysis

### Revenue Trend (Last 6 Periods)
```
[ASCII chart or description]
```

### Expense Trend (Last 6 Periods)
```
[ASCII chart or description]
```

## Variance Analysis

### Significant Variances (>10%)
| Item | Expected | Actual | Variance | Root Cause |
|------|----------|--------|----------|------------|
| [Item] | $X | $X | +/-X% | [Explanation] |

### Corrective Actions
| Issue | Impact | Recommended Action | Owner |
|-------|--------|-------------------|-------|
| [Issue] | $X impact | [Action] | [Position] |

## Unit Economics

| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| Revenue per Customer | $X | $X | 🟢/🟡/🔴 |
| Cost to Serve | $X | $X | 🟢/🟡/🔴 |
| Contribution Margin | X% | X% | 🟢/🟡/🔴 |
| Payback Period | X mo | X mo | 🟢/🟡/🔴 |

## Cash Position

| Metric | Current | 30 Days | 90 Days |
|--------|---------|---------|---------|
| Cash Balance | $X | $X | $X |
| Accounts Receivable | $X | $X | $X |
| Accounts Payable | $X | $X | $X |
| Net Position | $X | $X | $X |

## Recommendations

### Immediate Actions (This Week)
1. [Action with specific impact]
2. [Action with specific impact]

### Short-term (This Month)
1. [Action with specific impact]
2. [Action with specific impact]

### Strategic (This Quarter)
1. [Action with specific impact]
2. [Action with specific impact]

## Alerts & Escalations
- [ ] Runway < 6 months: 🔴 RED PHONE to Human
- [ ] Burn rate > budget: Alert CEO
- [ ] Revenue < 80% forecast: Alert CMO
```

---

## Execution Flow

1. **Gather data**
   - Collect actual financial data
   - Load forecasts and budgets
   - Identify reporting period

2. **Calculate variances**
   - Compare actuals to forecasts
   - Flag significant deviations (>10%)
   - Identify trends

3. **Analyze root causes**
   - For each significant variance
   - Document likely causes
   - Suggest corrective actions

4. **Calculate ratios**
   - Unit economics
   - Efficiency metrics
   - Cash position

5. **Generate recommendations**
   - Prioritize by impact
   - Assign to appropriate owner
   - Set timelines

6. **Escalate if needed**
   - Runway issues → CEO + Human
   - Budget overruns → CEO
   - Revenue shortfalls → CMO

---

## Logging

Log to `CFO/logs/YYYY-MM-DD-analysis.md`:
```
## Analysis Log: [Date]
Period analyzed: [Start - End]
Health status: [GREEN/YELLOW/RED]
Key variances: [List]
Escalations: [List]
Recommendations: [Count]
```

---

## Context

- Run weekly or monthly depending on business stage
- Provides early warning on financial issues
- Critical for maintaining runway visibility
- Feeds into forecast updates

---

*This analysis is for internal planning purposes.*
*Major decisions should involve professional advisors.*

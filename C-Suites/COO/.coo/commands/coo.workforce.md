# coo.workforce

## Preamble

This command creates workforce planning documentation including role definitions, hiring timelines, and compliance considerations.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `COO/.ethics/ethics.md`
3. `CEO/.ceo/memory/business-plan.md` (if exists)
4. `CFO/.cfo/memory/budget.md` (if exists)

---

## Outline

Design workforce structure aligned with business goals and regulatory requirements.

### Workforce Plan Template

```markdown
# Workforce Plan: [Business Name]
Generated: [Date]
Planning Horizon: [X months]

## ⚠️ DISCLAIMER
This is a planning document only. All hiring decisions, 
classifications, and employment practices must be reviewed 
by qualified HR professionals and/or employment attorneys.

---

## Workforce Summary

| Category | Current | +3 Months | +6 Months | +12 Months |
|----------|---------|-----------|-----------|------------|
| Full-time | X | X | X | X |
| Part-time | X | X | X | X |
| Contractors | X | X | X | X |
| Total | X | X | X | X |

---

## Organization Structure

```
[CEO/Founder]
├── [Role 1]
│   ├── [Sub-role]
│   └── [Sub-role]
├── [Role 2]
└── [Role 3]
```

---

## Role Definitions

### [Role Title]
| Attribute | Details |
|-----------|---------|
| **Department** | [Department] |
| **Reports To** | [Manager] |
| **Classification** | [Employee/Contractor - see analysis below] |
| **Type** | [Full-time/Part-time] |
| **Location** | [Remote/Hybrid/On-site] |
| **Compensation Range** | $X - $Y |
| **Target Start** | [Date] |

**Responsibilities:**
1. [Primary responsibility]
2. [Secondary responsibility]
3. [Additional duties]

**Requirements:**
- [Required skill/experience]
- [Required skill/experience]

**Nice-to-Haves:**
- [Preferred qualification]

---

## Employee vs. Contractor Analysis

⚠️ **Misclassification is a serious legal and financial risk.**

### Classification Factors (IRS Guidelines)

| Factor | Employee | Contractor |
|--------|----------|------------|
| Behavioral Control | Company directs work | Worker controls methods |
| Financial Control | Company provides tools/expenses | Worker invests in own tools |
| Relationship Type | Ongoing, exclusive | Project-based, multiple clients |
| Benefits | Eligible | Not eligible |
| Training | Company provides | Worker brings expertise |

### Classification Assessment: [Role]

| Factor | This Role | Lean Toward |
|--------|-----------|-------------|
| Who controls when/where? | [Answer] | Employee/Contractor |
| Who provides equipment? | [Answer] | Employee/Contractor |
| Ongoing or project? | [Answer] | Employee/Contractor |
| Exclusive relationship? | [Answer] | Employee/Contractor |
| **RECOMMENDATION** | | **[Final recommendation]** |

⚠️ **If unclear, escalate to CLO for legal review.**

---

## Hiring Timeline

| Role | Priority | Start Recruiting | Target Hire | Dependencies |
|------|----------|------------------|-------------|--------------|
| [Role 1] | P0 | [Date] | [Date] | None |
| [Role 2] | P1 | [Date] | [Date] | [Role 1] |
| [Role 3] | P2 | [Date] | [Date] | Funding |

---

## Compensation Framework

### Salary Bands
| Level | Range | Notes |
|-------|-------|-------|
| Entry | $X - $Y | [Market research citation] |
| Mid | $X - $Y | [Market research citation] |
| Senior | $X - $Y | [Market research citation] |

### Benefits (If Applicable)
| Benefit | Offering | Cost/Employee |
|---------|----------|---------------|
| Health Insurance | [Yes/No] | $X/month |
| Dental/Vision | [Yes/No] | $X/month |
| 401(k) | [Yes/No] | X% match |
| PTO | [X days] | N/A |
| Remote Stipend | [Yes/No] | $X/month |

---

## Compliance Requirements

### Federal
| Requirement | Applicability | Status |
|-------------|---------------|--------|
| I-9 Verification | All employees | [ ] |
| E-Verify | [If required] | [ ] |
| FLSA Compliance | All employees | [ ] |
| ADA Compliance | 15+ employees | [ ] |
| FMLA | 50+ employees | [ ] |

### State: [State Name]
| Requirement | Applicability | Status |
|-------------|---------------|--------|
| State New Hire Reporting | All employees | [ ] |
| Workers' Compensation | All employees | [ ] |
| Unemployment Insurance | All employees | [ ] |
| [State-specific] | [Condition] | [ ] |

---

## Onboarding Checklist

### Before Day 1
- [ ] Offer letter signed
- [ ] Background check complete (if applicable)
- [ ] Equipment ordered
- [ ] Accounts provisioned (CIO)
- [ ] Calendar invites sent

### Day 1
- [ ] I-9 completed (within 3 days)
- [ ] W-4 completed
- [ ] Direct deposit setup
- [ ] Employee handbook acknowledgment
- [ ] Benefits enrollment started

### Week 1
- [ ] Team introductions
- [ ] Systems training
- [ ] Role-specific training
- [ ] 1:1 with manager

---

## Budget Impact

| Category | Monthly | Annual | Notes |
|----------|---------|--------|-------|
| Salaries | $X | $X | [Details] |
| Benefits | $X | $X | X% of salary |
| Payroll Taxes | $X | $X | ~7.65% employer |
| Recruiting | $X | $X | One-time costs |
| Training | $X | $X | Ongoing |
| **Total** | **$X** | **$X** | |

→ Escalate to CFO for budget approval

---

## Escalations

- [ ] Classification unclear → CLO
- [ ] Budget not approved → CEO + CFO
- [ ] High-risk domain (minors, healthcare) → Additional compliance review
- [ ] International hiring → CLO + tax professional
```

---

## Execution Flow

1. **Understand requirements**
   - Business plan needs
   - Timeline constraints
   - Budget limits

2. **Design structure**
   - Org chart
   - Reporting lines
   - Growth projections

3. **Define roles**
   - Responsibilities
   - Requirements
   - Classification analysis

4. **Plan timeline**
   - Priority-based sequencing
   - Dependencies
   - Recruiting lead time

5. **Estimate costs**
   - Compensation research
   - Benefits costs
   - Overhead

6. **Compliance check**
   - Federal requirements
   - State requirements
   - Industry-specific

---

## Logging

Log to `COO/logs/YYYY-MM-DD-workforce.md`:
```
## Workforce Log: [Date]
Planning horizon: [Months]
Roles defined: [Count]
Classification concerns: [List]
Budget estimate: $X
Escalations: [List]
```

---

## Context

- Run during business formation
- Update when adding roles or changing structure
- Coordinate with CFO for budget
- Coordinate with CLO for compliance

---

*This is planning documentation only. Employment decisions require professional HR and legal review.*

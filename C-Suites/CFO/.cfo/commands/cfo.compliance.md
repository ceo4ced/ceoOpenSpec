# cfo.compliance

## Preamble

This command generates a financial and tax compliance checklist based on the business structure, location, and activities.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CFO/.ethics/ethics.md`
3. `CEO/.ceo/memory/business-plan.md` (if exists)

---

## Outline

Generate a comprehensive compliance checklist with deadlines and requirements.

### Compliance Checklist Template

```markdown
# Financial Compliance Checklist: [Business Name]
Generated: [Date]
Business Type: [LLC/Corp/Sole Prop/etc.]
Jurisdiction: [State, Country]

## ⚠️ DISCLAIMER
This checklist is for informational purposes only. 
Compliance requirements vary by jurisdiction and situation.
**CONSULT A CPA OR TAX ATTORNEY FOR BINDING ADVICE.**

---

## Entity Formation & Registration

### Federal Requirements
| Requirement | Status | Deadline | Notes |
|-------------|--------|----------|-------|
| EIN (Employer ID Number) | [ ] | Before hiring | IRS Form SS-4 |
| Business Bank Account | [ ] | After EIN | Required for separation |
| Federal Tax Election | [ ] | Within 75 days | S-Corp election if applicable |

### State Requirements ([State])
| Requirement | Status | Deadline | Notes |
|-------------|--------|----------|-------|
| State Registration | [ ] | Immediate | Secretary of State |
| State Tax ID | [ ] | Before operations | State revenue dept |
| Business License | [ ] | Before operations | Check local requirements |
| Registered Agent | [ ] | Ongoing | If required |

### Local Requirements
| Requirement | Status | Deadline | Notes |
|-------------|--------|----------|-------|
| City Business License | [ ] | Varies | Check municipality |
| Zoning Compliance | [ ] | Before operations | If physical location |
| DBA/Fictitious Name | [ ] | If using trade name | County clerk |

---

## Tax Compliance

### Federal Taxes
| Tax | Frequency | Due Date | Form |
|-----|-----------|----------|------|
| Income Tax | Annual | April 15 (or March 15) | 1120/1120-S/1065 |
| Estimated Tax | Quarterly | 15th of month after quarter | 1040-ES |
| Employment Tax | Quarterly | End of month after quarter | 941 |
| FUTA | Annual | January 31 | 940 |

### State Taxes
| Tax | Frequency | Due Date | Notes |
|-----|-----------|----------|-------|
| State Income Tax | Varies | [State-specific] | Check state DOR |
| Sales Tax | Monthly/Quarterly | [State-specific] | If applicable |
| Franchise Tax | Annual | [State-specific] | Check requirements |

### Payroll Taxes (If Employees)
| Requirement | Frequency | Notes |
|-------------|-----------|-------|
| Withhold Federal Income Tax | Per payroll | W-4 based |
| Withhold FICA (SS + Medicare) | Per payroll | 7.65% employee, 7.65% employer |
| Withhold State Tax | Per payroll | State-specific |
| Deposit Taxes | Per schedule | Based on liability |

---

## Financial Reporting

### Required Records
| Record | Retention | Notes |
|--------|-----------|-------|
| Income records | 7 years | All revenue documentation |
| Expense receipts | 7 years | All deductible expenses |
| Bank statements | 7 years | All accounts |
| Tax returns | 7 years | Federal and state |
| Payroll records | 7 years | If applicable |
| Contracts | 7+ years | Duration + 7 years |

### Recommended Practices
| Practice | Frequency | Tool |
|----------|-----------|------|
| Bookkeeping | Weekly | QuickBooks, Xero, Wave |
| Bank Reconciliation | Monthly | Accounting software |
| Financial Statements | Monthly | P&L, Balance Sheet |
| Cash Flow Review | Weekly | Spreadsheet/Software |

---

## Employment Compliance (If Hiring)

### Federal Requirements
| Requirement | Deadline | Notes |
|-------------|----------|-------|
| Form I-9 | Within 3 days of hire | Employment eligibility |
| Form W-4 | At hire | Federal withholding |
| New Hire Reporting | Within 20 days | State-specific |
| Workers Comp Insurance | Before hire | State requirements vary |

### Contractor vs Employee
| Factor | Employee | Contractor |
|--------|----------|------------|
| Control over work | High | Low |
| Set hours | Yes | No |
| Provide tools | Yes | No |
| Exclusive relationship | Often | No |
| Tax forms | W-2 | 1099-NEC |

⚠️ **Misclassification Risk:** IRS and DOL actively audit. When in doubt, consult CLO.

---

## Industry-Specific Compliance

### If Handling Customer Data
| Requirement | Applicability | Notes |
|-------------|---------------|-------|
| PCI-DSS | Credit cards | Payment processing |
| HIPAA | Health data | Healthcare |
| FERPA | Education records | Education |
| COPPA | Under-13 users | Children |
| GDPR | EU customers | Privacy |

### If Crypto/Fintech
| Requirement | Notes |
|-------------|-------|
| FinCEN MSB Registration | If transmitting money |
| State Money Transmitter License | Each state |
| SEC Registration | If securities |
| CFTC Registration | If commodities |

---

## Calendar of Deadlines

| Date | Requirement | Notes |
|------|-------------|-------|
| Jan 15 | Q4 Estimated Tax | Federal |
| Jan 31 | W-2s to employees | Deadline |
| Jan 31 | 1099s to contractors | Deadline |
| Mar 15 | S-Corp/Partnership returns | Or extension |
| Apr 15 | C-Corp/Individual returns | Or extension |
| Apr 15 | Q1 Estimated Tax | Federal |
| Jun 15 | Q2 Estimated Tax | Federal |
| Sep 15 | Q3 Estimated Tax | Federal |

---

## RED FLAGS - Escalate Immediately

- [ ] 🔴 Missing payroll tax deposits → IRS penalties severe
- [ ] 🔴 1099 for someone who should be W-2 → Audit risk
- [ ] 🔴 Commingling personal/business funds → Pierces corporate veil
- [ ] 🔴 Missing state registrations → Operating illegally
- [ ] 🔴 Crypto reporting gaps → IRS focus area

---

## Professional Review Required

**The following MUST be reviewed by licensed professionals:**
- [ ] Tax returns → CPA
- [ ] Employment classification → Attorney
- [ ] Securities/investments → Securities attorney
- [ ] State registrations → Business attorney

---
```

---

## Execution Flow

1. **Identify business profile**
   - Entity type
   - Jurisdiction(s)
   - Industry
   - Employee count

2. **Research requirements**
   - Federal requirements
   - State requirements (each state of operation)
   - Local requirements
   - Industry-specific

3. **Build calendar**
   - Map all deadlines
   - Create reminder schedule
   - Identify lead time needed

4. **Flag high-risk areas**
   - Employment classification
   - Tax deposits
   - Registration requirements

5. **Recommend professionals**
   - CPA for tax
   - Attorney for legal
   - Industry specialists

---

## Logging

Log to `CFO/logs/YYYY-MM-DD-compliance.md`:
```
## Compliance Log: [Date]
Business type: [Entity]
Jurisdictions: [List]
Requirements identified: [Count]
High-risk areas: [List]
Professional referrals: [List]
```

---

## Context

- Run at business formation
- Update annually or when structure changes
- Critical for avoiding penalties and legal issues
- Always refer to professionals for execution

---

*This is NOT tax or legal advice. Consult licensed professionals.*

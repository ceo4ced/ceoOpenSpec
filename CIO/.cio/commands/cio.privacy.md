# cio.privacy

## Preamble

This command creates privacy documentation and conducts Privacy Impact Assessments (PIAs).

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CIO/.ethics/ethics.md`
3. `CEO/.ceo/memory/business-plan.md` (if exists)

---

## Outline

Assess privacy implications and create compliance documentation.

### Privacy Impact Assessment Template

```markdown
# Privacy Impact Assessment: [Business Name]
Version: [X.X]
Generated: [Date]
Prepared by: CIO Agent
Review by: [Human/Privacy Professional]

## ⚠️ DISCLAIMER
This PIA is a planning document. Privacy compliance requires
review by qualified privacy professionals. Do not rely on this
as legal advice.

---

## 1. Executive Summary

**Business Description:** [One paragraph]

**Data Processing Summary:**
- Personal data collected: [Yes/No]
- Sensitive data collected: [Yes/No]
- Data subjects: [Customers/Employees/Children/etc.]
- High-risk processing: [Yes/No]

**Risk Level:** [LOW | MEDIUM | HIGH | CRITICAL]

**Key Findings:** [Brief summary]

---

## 2. Data Inventory

### What Personal Data?
| Data Element | Category | Source | Purpose | Legal Basis |
|--------------|----------|--------|---------|-------------|
| Name | Identity | User input | Account | Contract |
| Email | Contact | User input | Communication | Consent |
| IP Address | Technical | Automatic | Security | Legitimate interest |
| Payment info | Financial | User input | Transactions | Contract |
| [Add more] | | | | |

### Data Categories
| Category | Present | Special Handling |
|----------|---------|------------------|
| Basic identity | [ ] | Standard |
| Contact info | [ ] | Standard |
| Financial | [ ] | Encryption required |
| Location | [ ] | Minimization required |
| Health | [ ] | HIPAA if US, special GDPR |
| Biometric | [ ] | High protection |
| Children's data | [ ] | COPPA/GDPR special |
| Criminal | [ ] | Generally prohibited |

---

## 3. Data Subjects

### Who's Data?
| Subject Type | Present | Special Protections |
|--------------|---------|---------------------|
| Customers | [ ] | Standard |
| Employees | [ ] | Employment law |
| Children (<13 US) | [ ] | COPPA required |
| Children (<16 EU) | [ ] | GDPR parental consent |
| EU residents | [ ] | GDPR applies |
| CA residents | [ ] | CCPA applies |

### ⚠️ HIGH-RISK FLAG
If children or special category data: **ESCALATE TO CLO + HUMAN**

---

## 4. Data Flow

### Collection
```
[Data Subject] → [Collection Point] → [Your Systems]
```

| Collection Method | Data Collected | Notice Provided |
|-------------------|----------------|-----------------|
| Registration form | [Data] | [ ] Privacy policy link |
| Cookies | [Data] | [ ] Cookie banner |
| Third-party SDK | [Data] | [ ] Disclosed in policy |

### Storage
| Data | Location | Encryption | Retention |
|------|----------|------------|-----------|
| [Data type] | [Where] | [Yes/No] | [Period] |

### Sharing
| Recipient | Data Shared | Purpose | Safeguards |
|-----------|-------------|---------|------------|
| [Party] | [Data] | [Purpose] | [DPA, SCC] |

### Deletion
| Data | Retention Period | Deletion Method |
|------|------------------|-----------------|
| [Data type] | [Period] | [How deleted] |

---

## 5. Legal Basis Analysis (GDPR)

| Processing Activity | Data | Legal Basis | Justification |
|---------------------|------|-------------|---------------|
| Account creation | Name, email | Contract | Necessary for service |
| Marketing emails | Email | Consent | Opt-in required |
| Security logs | IP, activity | Legitimate interest | Fraud prevention |
| Analytics | Usage data | Legitimate interest | Service improvement |

### Consent Requirements
| Processing | Pre-checked? | Granular? | Withdrawable? |
|------------|--------------|-----------|---------------|
| Marketing | NO (required) | YES | YES |
| Analytics | NO (required) | YES | YES |
| Cookies | NO (required) | YES | YES |

---

## 6. Rights Implementation

### Data Subject Rights
| Right | GDPR | CCPA | Implementation |
|-------|------|------|----------------|
| Access | ✓ | ✓ | [How] |
| Rectification | ✓ | ✓ | [How] |
| Erasure | ✓ | ✓ | [How] |
| Portability | ✓ | ✓ | [How] |
| Opt-out (sale) | - | ✓ | [How] |

### Request Handling
| Step | Timeline | Owner |
|------|----------|-------|
| Receive request | T+0 | [System/email] |
| Verify identity | Within X days | [Process] |
| Acknowledge | Within X days | [Automated] |
| Fulfill | Within 30 days (GDPR) / 45 days (CCPA) | [Process] |

---

## 7. Risk Assessment

### Privacy Risks Identified
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Data breach | [L/M/H] | [L/M/H] | Encryption, access control |
| Overcollection | [L/M/H] | [L/M/H] | Data minimization |
| Consent gaps | [L/M/H] | [L/M/H] | Consent management |
| Vendor risk | [L/M/H] | [L/M/H] | DPAs, audits |

### Risk Matrix
```
        │ Low    │ Medium │ High
────────┼────────┼────────┼────────
High    │ Monitor│ Action │ CRITICAL
Likelihood│       │        │
────────┼────────┼────────┼────────
Medium  │ Accept │ Monitor│ Action
Likelihood│       │        │
────────┼────────┼────────┼────────
Low     │ Accept │ Accept │ Monitor
Likelihood│       │        │
```

---

## 8. Required Documentation

### Privacy Policy
| Section | Required | Status |
|---------|----------|--------|
| Who we are | ✓ | [ ] |
| Data collected | ✓ | [ ] |
| How we use it | ✓ | [ ] |
| Legal basis | ✓ (GDPR) | [ ] |
| Data sharing | ✓ | [ ] |
| Data transfers | ✓ | [ ] |
| Retention | ✓ | [ ] |
| Your rights | ✓ | [ ] |
| Contact | ✓ | [ ] |
| Updates | ✓ | [ ] |

### Additional Documents
| Document | Required When | Status |
|----------|---------------|--------|
| Cookie policy | Using cookies | [ ] |
| Data processing agreements | Using vendors | [ ] |
| Standard contractual clauses | EU→non-EU transfers | [ ] |
| Records of processing | GDPR, 250+ employees | [ ] |
| DPO appointment | Required processing | [ ] |

---

## 9. Compliance Mapping

| Regulation | Applicable? | Key Requirements | Status |
|------------|-------------|------------------|--------|
| GDPR | EU customers | Full compliance | [ ] |
| CCPA/CPRA | CA customers | Notice, opt-out, rights | [ ] |
| COPPA | US children <13 | Parental consent | [ ] |
| HIPAA | Health data | Full compliance | [ ] |
| FERPA | Student data | Consent, access | [ ] |
| PIPEDA | Canada | Consent, access | [ ] |

---

## 10. Action Items

| Priority | Action | Owner | Deadline | Status |
|----------|--------|-------|----------|--------|
| P0 | [Critical item] | [Who] | [When] | [ ] |
| P1 | [High priority] | [Who] | [When] | [ ] |
| P2 | [Medium] | [Who] | [When] | [ ] |

---

## 11. Sign-Off

- [ ] CIO Agent review complete
- [ ] CLO Agent review complete
- [ ] Human review complete
- [ ] Privacy professional review (if required)

**Approved by:** _________________ **Date:** _________
```

---

## Execution Flow

1. **Identify data flows**
   - What data
   - From whom
   - For what purpose

2. **Assess legal requirements**
   - Applicable regulations
   - Required documentation
   - Rights obligations

3. **Evaluate risks**
   - Data sensitivity
   - Processing risks
   - Mitigation measures

4. **Create documentation**
   - Privacy policy
   - Consent mechanisms
   - Rights procedures

5. **Define processes**
   - Request handling
   - Breach response
   - Ongoing compliance

---

## Logging

Log to `CIO/logs/YYYY-MM-DD-privacy.md`:
```
## Privacy Log: [Date]
Risk level: [Low/Medium/High/Critical]
Regulations applicable: [List]
High-risk processing: [Yes/No]
Actions required: [Count]
Escalations: [List]
```

---

## Context

- Required before collecting personal data
- Update when data practices change
- Foundation for privacy policy
- Required for GDPR compliance

---

*Privacy assessments require professional review for regulated industries.*

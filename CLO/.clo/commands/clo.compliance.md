---
description: Create compliance checklist and risk assessment for the business.
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
   - Read `CLO/.ethics/ethics.md` (CLO-specific rules)

2. **Load Business Context**:
   - Read root `README.md` (business plan)
   - Read `CLO/.clo/memory/ceo-brief.md` (CEO assignment)

3. **CRITICAL REMINDER**:
   > ⚠️ The CLO operates as a **digital paralegal**, NOT an attorney.
   > All outputs must include appropriate disclaimers.
   > All legal matters require attorney review.

---

## Outline

The CLO Compliance command creates a comprehensive compliance checklist based on the business plan, identifying applicable regulations and required actions.

### Execution Flow

1. **Identify Applicable Regulatory Domains**
   
   Based on business plan, check applicability:
   
   ```markdown
   # Compliance Assessment - [BUSINESS_NAME]
   
   **Generated**: [ISO 8601]
   **Prepared By**: CLO Agent (Digital Paralegal)
   **Status**: DRAFT - REQUIRES ATTORNEY REVIEW
   
   > ⚠️ **LEGAL DISCLAIMER**
   > This document was prepared by an AI assistant operating as a digital
   > paralegal. This is NOT legal advice. This document has NOT been reviewed
   > by a licensed attorney. Consult with a licensed attorney before taking
   > any actions based on this assessment.
   
   ## Regulatory Domain Analysis
   
   | Domain | Applicable? | Reason | Priority |
   |--------|-------------|--------|----------|
   | Corporate Formation | Yes | All businesses | High |
   | Employment Law | [Yes/No] | [Reason] | [Priority] |
   | Consumer Protection (FTC) | [Yes/No] | [Reason] | [Priority] |
   | Data Privacy (CCPA/GDPR) | [Yes/No] | [Reason] | [Priority] |
   | Minors (COPPA) | [Yes/No] | [Reason] | [Priority] |
   | Education (FERPA) | [Yes/No] | [Reason] | [Priority] |
   | Healthcare (HIPAA) | [Yes/No] | [Reason] | [Priority] |
   | Financial Services | [Yes/No] | [Reason] | [Priority] |
   | Crypto/Securities | [Yes/No] | [Reason] | [Priority] |
   ```

2. **Generate Compliance Checklist**
   
   For each applicable domain:
   
   ```markdown
   ## Compliance Checklist
   
   ### 1. Corporate Formation
   
   | Requirement | Status | Notes | Attorney Review |
   |-------------|--------|-------|-----------------|
   | Choose entity type (LLC, C-Corp, etc.) | ⏳ | Consult attorney | ✅ Required |
   | Register with state | ⏳ | After entity choice | ✅ Required |
   | Obtain EIN | ⏳ | After registration | - |
   | Operating agreement / Bylaws | ⏳ | Draft for review | ✅ Required |
   
   ### 2. [Domain]
   
   | Requirement | Status | Notes | Attorney Review |
   |-------------|--------|-------|-----------------|
   | [Requirement] | ⏳ | [Notes] | [Required?] |
   ```

3. **Risk Assessment**
   
   ```markdown
   ## Legal Risk Assessment
   
   | Risk Area | Likelihood | Impact | Risk Level | Mitigation |
   |-----------|------------|--------|------------|------------|
   | [Risk 1] | [H/M/L] | [H/M/L] | [Score] | [Action] |
   | [Risk 2] | [H/M/L] | [H/M/L] | [Score] | [Action] |
   
   ### High-Priority Risks
   
   1. **[Risk Name]**
      - Description: [Details]
      - Potential consequences: [Outcomes]
      - Recommended action: [Steps]
      - Attorney consultation: ✅ REQUIRED
   ```

4. **Contract Requirements**
   
   Identify contracts that may be needed:
   
   ```markdown
   ## Contract Requirements
   
   | Contract Type | Purpose | Priority | Attorney Draft |
   |---------------|---------|----------|----------------|
   | Terms of Service | User agreement | High | ✅ Required |
   | Privacy Policy | Data disclosure | High | ✅ Required |
   | [Contract type] | [Purpose] | [Priority] | [Required?] |
   
   > Note: CLO can prepare draft templates for attorney review.
   > Use /clo.contract to generate drafts.
   ```

5. **Action Items Summary**
   
   ```markdown
   ## Recommended Actions
   
   ### Immediate (Before Launch)
   - [ ] [Action 1] - Attorney: [Required/Recommended]
   - [ ] [Action 2]
   
   ### Short-term (Within 30 Days)
   - [ ] [Action 3]
   - [ ] [Action 4]
   
   ### Ongoing Compliance
   - [ ] [Regular review 1]
   - [ ] [Regular review 2]
   
   ## Attorney Consultation Required For:
   
   1. [Matter 1] - Reason: [Why attorney needed]
   2. [Matter 2] - Reason: [Why attorney needed]
   ```

6. **Save and Log**
   
   - Save to `CLO/.clo/memory/compliance-checklist.md`
   - Save risk assessment to `CLO/.clo/memory/risk-assessment.md`
   - Log to `CLO/logs/`

---

## High-Risk Domain Flags

If business involves high-risk domains, add special sections:

### Minors
- Contract voidability issues
- COPPA compliance requirements
- Parental consent mechanisms
- **ESCALATE + ATTORNEY REQUIRED**

### Healthcare
- HIPAA compliance program
- BAA requirements
- State-specific requirements
- **ESCALATE + ATTORNEY REQUIRED**

### Crypto/Securities
- Howey Test analysis (preliminary)
- State money transmitter considerations
- SEC/FinCEN considerations
- **ESCALATE + ATTORNEY REQUIRED**

---

## Standard Disclaimer

All outputs must include:

```markdown
---

⚠️ **LEGAL DISCLAIMER**

This compliance assessment was prepared by an AI assistant operating in a 
paralegal capacity. This is NOT legal advice. This document has NOT been 
reviewed by a licensed attorney.

Before taking any actions based on this assessment:
1. Consult with a licensed attorney in your jurisdiction
2. Verify all regulatory requirements are current
3. Obtain professional legal review for all contracts

The information provided is for planning purposes only and may not be 
complete, accurate, or current.
```

---

## Logging

Log to `CLO/logs/compliance-[DATE].md`:

```markdown
# Compliance Assessment Log

**Date**: [ISO 8601]

## Domains Analyzed
[List]

## High-Risk Flags
[List]

## Attorney Review Items
[List - items requiring attorney consultation]

## Output
- Compliance checklist: [path]
- Risk assessment: [path]
```

---

## Context

$ARGUMENTS

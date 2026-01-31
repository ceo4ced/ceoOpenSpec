---
description: Create data governance strategy and privacy impact assessment.
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
   - Read `CIO/.ethics/ethics.md` (CIO-specific rules)

2. **Load Business Context**:
   - Read root `README.md` (business plan)
   - Read `CIO/.cio/memory/ceo-brief.md` (CEO assignment)

3. **Check High-Risk Domains**:
   - Identify if business handles minor data (COPPA)
   - Identify if business handles student data (FERPA)
   - Identify if business handles health data (HIPAA)
   - Identify if business handles financial/crypto data
   - Identify if business operates in EU (GDPR)

---

## Outline

The CIO Data command creates a comprehensive data governance strategy including data classification, privacy impact assessment, and security framework recommendations.

### Execution Flow

1. **Data Inventory**
   
   Based on the business plan, identify all data the business will collect, process, or store:
   
   ```markdown
   # Data Governance Strategy - [BUSINESS_NAME]
   
   **Generated**: [ISO 8601]
   **Prepared By**: CIO Agent
   **Status**: DRAFT - REQUIRES HUMAN REVIEW
   
   ## Data Inventory
   
   | Data Category | Type | Collection Method | Purpose | Sensitivity |
   |---------------|------|-------------------|---------|-------------|
   | [Category] | [PII/Non-PII] | [How collected] | [Why] | [Level] |
   ```

2. **Data Classification**
   
   Apply classification framework:
   
   | Level | Definition | Examples | Controls |
   |-------|------------|----------|----------|
   | Public | No sensitivity | Marketing content | Integrity |
   | Internal | Business only | Internal docs | Access control |
   | Confidential | Sensitive | Customer PII | Encryption + logging |
   | Restricted | Highly sensitive | PHI, financial | Encryption + MFA + audit |
   | Prohibited | Cannot store | Certain minor data | Do not collect |

3. **Regulatory Mapping**
   
   ```markdown
   ## Regulatory Requirements
   
   ### Applicable Regulations
   
   | Regulation | Applicable | Reason | Key Requirements |
   |------------|------------|--------|------------------|
   | GDPR | [Yes/No] | [Why] | [Summary] |
   | CCPA/CPRA | [Yes/No] | [Why] | [Summary] |
   | HIPAA | [Yes/No] | [Why] | [Summary] |
   | COPPA | [Yes/No] | [Why] | [Summary] |
   | FERPA | [Yes/No] | [Why] | [Summary] |
   
   ### Compliance Requirements by Data Type
   [Detailed breakdown]
   ```

4. **Privacy Impact Assessment**
   
   ```markdown
   ## Privacy Impact Assessment (PIA)
   
   ### Processing Activities
   
   | Activity | Data Used | Legal Basis | Risks | Mitigations |
   |----------|-----------|-------------|-------|-------------|
   | [Activity] | [Data] | [Basis] | [Risks] | [Controls] |
   
   ### Risk Assessment
   
   | Risk | Likelihood | Impact | Overall | Mitigation |
   |------|------------|--------|---------|------------|
   | Data breach | [H/M/L] | [H/M/L] | [Score] | [Plan] |
   | Unauthorized access | [H/M/L] | [H/M/L] | [Score] | [Plan] |
   | Data misuse | [H/M/L] | [H/M/L] | [Score] | [Plan] |
   ```

5. **Security Framework Recommendations**
   
   Map to NIST CSF:
   
   ```markdown
   ## Security Framework (NIST CSF Aligned)
   
   ### Identify
   - Asset inventory: [Recommendations]
   - Risk assessment: [Recommendations]
   
   ### Protect
   - Access control: [Recommendations]
   - Data security: [Recommendations]
   - Encryption: [Recommendations]
   
   ### Detect
   - Monitoring: [Recommendations]
   - Alerting: [Recommendations]
   
   ### Respond
   - Incident response: [Recommendations]
   
   ### Recover
   - Recovery planning: [Recommendations]
   ```

6. **High-Risk Domain Escalations**
   
   If any high-risk domains identified:
   - Flag specific additional requirements
   - Recommend specialized compliance review
   - Escalate to CEO/founder

7. **Save and Log**
   
   - Save to `CIO/.cio/memory/data-governance.md`
   - Save PIA to `CIO/.cio/memory/privacy-assessment.md`
   - Log to `CIO/logs/`

---

## Escalation Rules

Escalate to CEO/founder if:
- Business will handle data from minors (COPPA)
- Business will handle health data (HIPAA)
- Business operates in EU (GDPR DPO requirement)
- High-risk AI/ML processing planned
- Third-party data sharing anticipated

---

## Logging

Log to `CIO/logs/data-governance-[DATE].md`:

```markdown
# Data Governance Log

**Date**: [ISO 8601]

## Scope
- Data types identified: [Count]
- High-risk domains: [List]

## Regulations Applicable
[List]

## High-Risk Escalations
[Any escalations made]

## Output
- Data governance: [path]
- Privacy assessment: [path]
```

---

## Context

$ARGUMENTS

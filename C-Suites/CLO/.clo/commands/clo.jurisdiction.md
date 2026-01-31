# clo.jurisdiction

## Preamble

The CLO manages jurisdictional compliance across all operating territories.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CLO/.ethics/ethics.md`

---

## Overview

> **The law of the land applies. ALL lands we operate in.**

The CLO is responsible for understanding and enforcing applicable laws based on:
- Where the business is incorporated
- Where customers are located
- Where services are delivered
- Where data is processed/stored

---

## Command Types

```
clo.jurisdiction analyze [business-activity]   # Determine applicable laws
clo.jurisdiction lookup [location]             # Laws for specific jurisdiction
clo.jurisdiction compliance [department]       # Compliance requirements by dept
clo.jurisdiction update                        # Update jurisdiction data
```

---

## Jurisdiction Hierarchy

### Level 1: Federal/National

```yaml
united_states:
  incorporation: Delaware  # Common for US businesses
  applicable_always:
    - Federal Trade Commission Act
    - Securities laws (if applicable)
    - Federal tax code (IRS)
    - ADA (accessibility)
    - CAN-SPAM Act
    - COPPA (if minors are users)
    - HIPAA (if health data)
    - FCRA (if credit data)
    - CFAA (computer fraud)
    - Export controls (ITAR, EAR)
```

### Level 2: State/Regional

```yaml
operating_states:
  # Must track for EACH state where:
  # - We have employees
  # - We have customers
  # - We collect data
  # - We do business
  
  california:
    - CCPA/CPRA (privacy)
    - CalOPPA
    - California Labor Code
    - Prop 65 (if products)
    
  new_york:
    - NY SHIELD Act
    - NY Labor Law
    - NYC Human Rights Law
    
  texas:
    - Texas Data Privacy Act
    - Texas Business & Commerce Code
    
  # ... all 50 states as applicable
```

### Level 3: International

```yaml
international:
  european_union:
    - GDPR (data protection)
    - Digital Services Act
    - AI Act (if AI deployed)
    - ePrivacy Directive
    
  united_kingdom:
    - UK GDPR
    - Data Protection Act 2018
    
  canada:
    - PIPEDA
    - CASL (anti-spam)
    - Provincial laws (Quebec, BC, Alberta)
    
  # Add jurisdictions as business expands
```

---

## Geotargeting Integration

### Determine Applicable Jurisdictions

```python
def determine_jurisdictions(activity: dict) -> dict:
    """
    Determine all applicable jurisdictions for a business activity.
    """
    jurisdictions = {
        'federal': [],
        'state': [],
        'international': [],
        'requirements': []
    }
    
    # Always include incorporation state
    jurisdictions['state'].append(INCORPORATION_STATE)
    jurisdictions['federal'].append('US_FEDERAL')
    
    # Check customer locations
    for customer_location in activity.get('customer_locations', []):
        if customer_location['country'] == 'US':
            jurisdictions['state'].append(customer_location['state'])
        else:
            jurisdictions['international'].append(customer_location['country'])
    
    # Check data processing locations
    for data_location in activity.get('data_processing_locations', []):
        if data_location['country'] != 'US':
            jurisdictions['international'].append(data_location['country'])
    
    # Check employee locations
    for employee_location in activity.get('employee_locations', []):
        if employee_location['country'] == 'US':
            jurisdictions['state'].append(employee_location['state'])
        else:
            jurisdictions['international'].append(employee_location['country'])
    
    # De-duplicate
    jurisdictions['state'] = list(set(jurisdictions['state']))
    jurisdictions['international'] = list(set(jurisdictions['international']))
    
    # Get requirements for each
    for jur_type, locations in jurisdictions.items():
        if jur_type == 'requirements':
            continue
        for location in locations:
            reqs = get_requirements(jur_type, location)
            jurisdictions['requirements'].extend(reqs)
    
    return jurisdictions
```

### Track Operating Territories

```sql
CREATE TABLE IF NOT EXISTS operating_jurisdictions (
    jurisdiction_id STRING NOT NULL,
    business_id STRING NOT NULL,
    
    -- Location
    jurisdiction_type STRING,  -- federal, state, country
    jurisdiction_code STRING,  -- US, CA, GB, etc.
    jurisdiction_name STRING,
    
    -- Applicability
    reason STRING,  -- incorporation, customers, employees, data_processing
    
    -- Status
    active BOOL,
    first_active DATE,
    
    -- Compliance
    last_compliance_review DATE,
    compliance_status STRING,  -- compliant, review_needed, non_compliant
    
    -- Requirements
    applicable_laws ARRAY<STRING>,
    special_requirements ARRAY<STRING>
);
```

---

## Department Compliance Matrix

### CMO (Marketing)

```yaml
cmo_compliance:
  us_federal:
    - FTC Act: No deceptive advertising
    - CAN-SPAM: Email marketing rules
    - COPPA: No marketing to children without consent
    
  california:
    - CalOPPA: Privacy policy requirements
    - CCPA: Do not sell my info
    
  eu:
    - GDPR: Consent for marketing
    - ePrivacy: Cookie consent
```

### CFO (Finance)

```yaml
cfo_compliance:
  us_federal:
    - IRS: Tax reporting
    - SEC: Securities (if applicable)
    - FinCEN: AML/KYC (if applicable)
    
  states:
    - State tax nexus rules
    - Sales tax by state
    - Payroll tax by state
```

### COO (Operations)

```yaml
coo_compliance:
  us_federal:
    - DOL: Labor laws
    - OSHA: Safety (if applicable)
    - EEOC: Non-discrimination
    
  states:
    - Minimum wage by state
    - Employment classification
    - Leave requirements
```

### CIO (Data/Tech)

```yaml
cio_compliance:
  us_federal:
    - HIPAA: If health data
    - CFAA: Computer security
    - FCRA: If credit data
    
  california:
    - CCPA/CPRA: Privacy rights
    
  eu:
    - GDPR: Data protection
    - Data localization requirements
```

---

## Compliance Enforcement

### CLO as Compliance Authority

```yaml
clo_authority:
  can_require:
    - Policy changes from any department
    - Feature removal (if non-compliant)
    - Market exit (if cannot comply)
    - Disclosure statements
    - Consent mechanisms
    
  can_escalate:
    - Compliance violations to CEO
    - Legal risk to Human (RED PHONE)
    
  must_approve:
    - New market entry (geo expansion)
    - New data collection
    - Terms of service changes
    - Privacy policy changes
    - Marketing claims
```

### Compliance Workflow

```
New Activity Proposed (any department)
        ↓
CLO: clo.jurisdiction analyze [activity]
        ↓
Identify applicable jurisdictions
        ↓
Identify legal requirements
        ↓
Generate compliance checklist
        ↓
Department implements requirements
        ↓
CLO verifies compliance
        ↓
Activity approved or blocked
```

---

## State-by-State Quick Reference

### Privacy Laws

| State | Law | Key Requirement |
|-------|-----|-----------------|
| California | CCPA/CPRA | Right to delete, opt-out of sale |
| Virginia | VCDPA | Consumer rights similar to CCPA |
| Colorado | CPA | Privacy assessments required |
| Connecticut | CTDPA | Consent for sensitive data |
| Utah | UCPA | Narrower than CCPA |
| Iowa | Iowa Privacy Law | 2025 effective |
| Indiana | Indiana CDPA | 2026 effective |
| Tennessee | TIPA | 2025 effective |
| Montana | MCDPA | 2024 effective |
| Oregon | OCPA | 2024 effective |
| Texas | TDPSA | 2024 effective |
| Delaware | DPDPA | 2025 effective |

### Employment Laws

| State | Notable Requirement |
|-------|---------------------|
| California | Strictest classification, meal breaks |
| New York | NYC wage requirements |
| Massachusetts | Non-compete restrictions |
| Washington | Non-compete restrictions |
| Colorado | Pay transparency |
| Illinois | Biometric information protection |

---

## International Compliance

### GDPR (EU/EEA)

```yaml
gdpr_requirements:
  lawful_basis:
    - Consent OR
    - Contract OR
    - Legal obligation OR
    - Vital interests OR
    - Public task OR
    - Legitimate interests
    
  data_subject_rights:
    - Access
    - Rectification
    - Erasure ("right to be forgotten")
    - Restriction
    - Portability
    - Objection
    - Automated decision-making rights
    
  breaches:
    - Report within 72 hours
    - Document all breaches
    
  transfers:
    - Adequacy decisions OR
    - Standard contractual clauses OR
    - Binding corporate rules
```

### Other Key International

| Region | Regulation | Key Points |
|--------|------------|------------|
| UK | UK GDPR | Post-Brexit version |
| Canada | PIPEDA | Similar to GDPR |
| Brazil | LGPD | GDPR-like |
| Japan | APPI | Data protection |
| Australia | Privacy Act | Australian Privacy Principles |
| China | PIPL | Strict data localization |

---

## Logging

All jurisdiction determinations logged:

```sql
INSERT INTO jurisdiction_analysis_log (
    analysis_id,
    business_id,
    
    -- Request
    activity_analyzed STRING,
    requesting_agent STRING,
    
    -- Results
    jurisdictions_identified ARRAY<STRING>,
    requirements_identified ARRAY<STRING>,
    
    -- Decision
    compliance_possible BOOL,
    modifications_required ARRAY<STRING>,
    
    -- Timing
    analyzed_at TIMESTAMP
) VALUES (...);
```

---

*Know the law. Follow the law. Every jurisdiction. Every time.*

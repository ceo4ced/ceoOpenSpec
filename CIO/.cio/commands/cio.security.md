# cio.security

## Preamble

This command creates a security framework and policy documentation for the business.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CIO/.ethics/ethics.md`
3. `CEO/.ceo/memory/business-plan.md` (if exists)

---

## Outline

Establish security policies and controls appropriate for the business.

### Security Framework Template

```markdown
# Security Framework: [Business Name]
Generated: [Date]
Risk Level: [Low/Medium/High]

## ⚠️ DISCLAIMER
This framework provides security guidance. Implementation should 
be reviewed by qualified security professionals. Regulated industries
require additional compliance validation.

---

## Security Overview

### Asset Inventory
| Asset Type | Examples | Sensitivity | Owner |
|------------|----------|-------------|-------|
| Customer Data | Names, emails, payment | HIGH | CIO |
| Business Data | Financials, strategy | HIGH | CFO/CEO |
| Systems | Servers, applications | MEDIUM | CTO |
| Code | Source code, configs | HIGH | CTO |
| Credentials | Passwords, API keys | CRITICAL | CIO |

### Threat Model
| Threat | Likelihood | Impact | Priority |
|--------|------------|--------|----------|
| Phishing | High | High | P0 |
| Credential theft | Medium | Critical | P0 |
| Malware | Medium | High | P1 |
| Insider threat | Low | High | P2 |
| DDoS | Low | Medium | P3 |

---

## Access Control

### Identity Management
| Requirement | Implementation | Status |
|-------------|----------------|--------|
| Unique accounts | No shared accounts | [ ] |
| MFA required | All systems | [ ] |
| Password policy | 12+ chars, complexity | [ ] |
| SSO | Google/Microsoft SSO | [ ] |

### Privilege Management
| Level | Access | Who |
|-------|--------|-----|
| Admin | Full access | Owner only |
| Manager | Read/write team data | Role-based |
| User | Read/write own data | Default |
| Guest | Read-only limited | External |

### Access Review
| Review Type | Frequency | Owner |
|-------------|-----------|-------|
| User access audit | Quarterly | CIO |
| Privilege review | Monthly | CIO |
| Termination checklist | Immediately | COO + CIO |

---

## Data Protection

### Data Classification
| Level | Examples | Handling |
|-------|----------|----------|
| PUBLIC | Marketing materials | No restrictions |
| INTERNAL | Policies, procedures | Company access only |
| CONFIDENTIAL | Customer data, financials | Need-to-know |
| RESTRICTED | Secrets, keys, PII | Encrypted, logged |

### Encryption Standards
| Data State | Encryption | Standard |
|------------|------------|----------|
| At rest | Required | AES-256 |
| In transit | Required | TLS 1.3 |
| Backups | Required | AES-256 |
| Secrets | Required | Vault/KMS |

### Data Handling
| Action | Policy |
|--------|--------|
| Storage | Approved systems only |
| Transmission | Encrypted channels only |
| Sharing | Least privilege, logged |
| Deletion | Secure wipe, verified |

---

## System Security

### Endpoint Security
| Control | Requirement | Status |
|---------|-------------|--------|
| Antivirus/EDR | All devices | [ ] |
| Disk encryption | All devices | [ ] |
| Auto-updates | Enabled | [ ] |
| Screen lock | 5 min timeout | [ ] |

### Network Security
| Control | Requirement | Status |
|---------|-------------|--------|
| Firewall | Configured | [ ] |
| VPN | For sensitive access | [ ] |
| Network segmentation | Prod/Dev/Corp | [ ] |
| DNS filtering | Enabled | [ ] |

### Application Security
| Control | Requirement | Status |
|---------|-------------|--------|
| HTTPS only | All apps | [ ] |
| WAF | Production apps | [ ] |
| Input validation | All user inputs | [ ] |
| Dependency scanning | CI/CD pipeline | [ ] |

---

## Incident Response

### Incident Severity
| Severity | Definition | Response Time |
|----------|------------|---------------|
| Critical | Active breach, data loss | Immediate |
| High | Potential breach, major vulnerability | 4 hours |
| Medium | Minor vulnerability, policy violation | 24 hours |
| Low | Security improvement needed | 1 week |

### Incident Response Plan
```
DETECTION
    ↓
CONTAINMENT (stop the bleeding)
    ↓
ERADICATION (remove the threat)
    ↓
RECOVERY (restore operations)
    ↓
LESSONS LEARNED (prevent recurrence)
```

### Escalation Path
| Severity | Notify | RED PHONE |
|----------|--------|-----------|
| Critical | CEO + Human | YES |
| High | CEO | If data breach |
| Medium | CTO | No |
| Low | Log only | No |

### Breach Notification
| Requirement | Timeframe | Notes |
|-------------|-----------|-------|
| GDPR | 72 hours | EU customers |
| CCPA | "Expeditiously" | CA customers |
| State laws | Varies | Check by state |
| Customers | ASAP | If affected |

---

## Security Operations

### Monitoring
| What | How | Frequency |
|------|-----|-----------|
| Failed logins | Alert threshold | Real-time |
| Privilege changes | Audit log | Daily review |
| Data exports | Logging | Weekly review |
| External access | Geo-anomaly | Real-time |

### Vulnerability Management
| Activity | Frequency | Owner |
|----------|-----------|-------|
| Dependency updates | Weekly | CTO |
| Vulnerability scan | Monthly | CIO |
| Penetration test | Annually | External |
| Security review | Quarterly | CIO |

### Backup & Recovery
| Data | Frequency | Retention | Recovery Test |
|------|-----------|-----------|---------------|
| Database | Daily | 30 days | Monthly |
| Files | Daily | 30 days | Monthly |
| Config | On change | 90 days | Quarterly |

---

## Compliance Mapping

### Frameworks (Check Applicable)
| Framework | Applicable | Status |
|-----------|------------|--------|
| NIST CSF | All | [ ] |
| SOC 2 | SaaS | [ ] |
| ISO 27001 | Enterprise | [ ] |
| HIPAA | Healthcare | [ ] |
| PCI-DSS | Payment data | [ ] |
| GDPR | EU customers | [ ] |

---

## Security Awareness

### Training Requirements
| Topic | Audience | Frequency |
|-------|----------|-----------|
| Phishing awareness | All | Quarterly |
| Data handling | All | Annual |
| Secure coding | Developers | Annual |
| Incident response | IT/Security | Annual |

### Acceptable Use Policy
- [ ] Business use of company systems
- [ ] Personal use limitations
- [ ] Social media guidelines
- [ ] BYOD policy
- [ ] Remote work security

---

## Vendor Security

### Third-Party Risk
| Vendor | Data Access | Risk Level | Review |
|--------|-------------|------------|--------|
| [Vendor 1] | [What data] | [H/M/L] | [Date] |

### Vendor Requirements
| Requirement | Critical Vendors | All Vendors |
|-------------|------------------|-------------|
| Security questionnaire | Required | Recommended |
| SOC 2 report | Required | Preferred |
| Encryption | Required | Required |
| Incident notification | Required | Required |
```

---

## Execution Flow

1. **Assess risk profile**
   - Business type
   - Data handled
   - Regulatory requirements

2. **Identify assets**
   - Data inventory
   - System inventory
   - Threat modeling

3. **Define controls**
   - Access management
   - Data protection
   - System security

4. **Create policies**
   - Document requirements
   - Define procedures
   - Training materials

5. **Plan operations**
   - Monitoring
   - Incident response
   - Compliance

---

## Logging

Log to `CIO/logs/YYYY-MM-DD-security.md`:
```
## Security Log: [Date]
Risk level assessed: [Low/Medium/High]
Controls defined: [Count]
Policies created: [List]
Compliance requirements: [List]
Escalations: [List]
```

---

## Context

- Foundation for any business handling data
- Required before handling sensitive data
- Prerequisite for enterprise sales
- Regular updates required

---

*Security frameworks require professional review for implementation.*

# cio.infrastructure

## Preamble

This command creates IT infrastructure planning and architecture documentation.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CIO/.ethics/ethics.md`
3. `CEO/.ceo/memory/business-plan.md` (if exists)
4. `CTO/.specify/memory/constitution.md` (if exists)

---

## Outline

Design IT infrastructure strategy aligned with business needs.

### Infrastructure Plan Template

```markdown
# IT Infrastructure Plan: [Business Name]
Generated: [Date]
Stage: [Startup/Growth/Scale]

## Executive Summary
[Overview of infrastructure strategy]

---

## Current State Assessment

### Existing Infrastructure
| Component | Current | Status | Notes |
|-----------|---------|--------|-------|
| Cloud provider | [None/AWS/GCP/Azure] | [Status] | |
| Hosting | [None/Shared/VPS/Dedicated] | [Status] | |
| Domain/DNS | [Registrar] | [Status] | |
| Email | [Provider] | [Status] | |
| Storage | [Provider] | [Status] | |
| Productivity | [Suite] | [Status] | |

### Pain Points
| Issue | Impact | Priority |
|-------|--------|----------|
| [Issue 1] | [Impact] | P0/P1/P2 |

---

## Recommended Architecture

### Cloud Platform
| Option | Pros | Cons | Cost Estimate |
|--------|------|------|---------------|
| AWS | Most services, enterprise | Complexity, cost | $X/mo |
| GCP | AI/ML, pricing, BigQuery | Smaller ecosystem | $X/mo |
| Azure | Microsoft integration | Complexity | $X/mo |
| Vercel/Netlify | Simple, fast | Limited backend | $X/mo |

**Recommendation:** [Platform]
**Rationale:** [Why this fits]

### Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                        CDN / Edge                            │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      Load Balancer                           │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
         ┌─────────┐    ┌─────────┐    ┌─────────┐
         │ App 1   │    │ App 2   │    │ App N   │
         └─────────┘    └─────────┘    └─────────┘
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                    ┌─────────────────┐
                    │    Database     │
                    └─────────────────┘
                              │
                    ┌─────────────────┐
                    │   Blob Storage  │
                    └─────────────────┘
```

---

## Component Specifications

### Compute
| Workload | Service | Size | Quantity | Cost/mo |
|----------|---------|------|----------|---------|
| Web app | [Service] | [Size] | [Count] | $X |
| API | [Service] | [Size] | [Count] | $X |
| Workers | [Service] | [Size] | [Count] | $X |

### Database
| Use Case | Service | Size | Cost/mo |
|----------|---------|------|---------|
| Primary DB | [Service] | [Size] | $X |
| Cache | [Redis/Memcached] | [Size] | $X |
| Search | [Elasticsearch/Algolia] | [Size] | $X |

### Storage
| Use Case | Service | Est. Size | Cost/mo |
|----------|---------|-----------|---------|
| User uploads | [Service] | [X GB] | $X |
| Backups | [Service] | [X GB] | $X |
| Logs | [Service] | [X GB] | $X |

### Networking
| Component | Service | Cost/mo |
|-----------|---------|---------|
| DNS | [Service] | $X |
| CDN | [Service] | $X |
| VPN | [If needed] | $X |
| Load balancer | [Service] | $X |

---

## Business Applications

### Productivity Suite
| Need | Recommended | Alternative | Cost/user/mo |
|------|-------------|-------------|--------------|
| Email | Google Workspace | Microsoft 365 | $6-18 |
| Docs/Sheets | Google Workspace | Microsoft 365 | Included |
| Calendar | Google Workspace | Microsoft 365 | Included |
| Video calls | Google Meet | Zoom | Included/$15 |

### Communication
| Need | Recommended | Alternative | Cost |
|------|-------------|-------------|------|
| Team chat | Slack | Discord/Teams | $0-8/user |
| External chat | [As needed] | | Varies |

### Development Tools
| Need | Recommended | Alternative | Cost |
|------|-------------|-------------|------|
| Version control | GitHub | GitLab | $0-19/user |
| CI/CD | GitHub Actions | CircleCI | Minutes-based |
| Project mgmt | Linear | Jira | $0-10/user |
| Monitoring | Datadog | New Relic | Usage-based |

---

## Cost Summary

### Monthly Recurring
| Category | Low Est. | High Est. |
|----------|----------|-----------|
| Cloud infrastructure | $X | $X |
| SaaS tools | $X | $X |
| Domains/DNS | $X | $X |
| Security tools | $X | $X |
| **Total** | **$X** | **$X** |

### One-Time Costs
| Item | Cost | Notes |
|------|------|-------|
| Migration | $X | If applicable |
| Setup | $X | Professional services |

→ Escalate to CFO for budget approval

---

## Scalability Plan

### Traffic Tiers
| Tier | Users | Infra Changes | Est. Cost |
|------|-------|---------------|-----------|
| Launch | <1K | Minimal | $X/mo |
| Growth | 1K-10K | Add capacity | $X/mo |
| Scale | 10K-100K | Architecture review | $X/mo |
| Enterprise | 100K+ | Significant investment | $X/mo |

### Auto-Scaling Configuration
| Metric | Scale Up When | Scale Down When | Limits |
|--------|---------------|-----------------|--------|
| CPU | >70% for 5 min | <30% for 10 min | 1-10 instances |
| Memory | >80% | <40% | 1-10 instances |
| Queue depth | >100 items | <10 items | 1-20 workers |

---

## Disaster Recovery

### RTO/RPO Targets
| System | RTO | RPO | Cost Impact |
|--------|-----|-----|-------------|
| Production app | X hours | X hours | $$$ |
| Database | X hours | X minutes | $$$$ |
| File storage | X hours | X hours | $$ |

### Backup Strategy
| Data | Frequency | Retention | Location |
|------|-----------|-----------|----------|
| Database | Daily | 30 days | Cross-region |
| Files | Daily | 30 days | Cross-region |
| Configs | On change | 90 days | Version control |

### Recovery Procedures
1. [Step 1]
2. [Step 2]
3. [Step 3]

---

## Security Requirements

→ See CIO security framework for details

| Requirement | Implementation |
|-------------|----------------|
| Encryption at rest | [Provider default] |
| Encryption in transit | TLS 1.3 |
| Network isolation | VPC/Private networking |
| Access control | IAM + MFA |
| Audit logging | Cloud logging |

---

## Compliance Considerations

| Regulation | Infrastructure Impact |
|------------|----------------------|
| GDPR | Data residency, encryption |
| HIPAA | BAA required, encryption, logging |
| SOC 2 | Logging, access control, backups |
| PCI-DSS | Network segmentation, encryption |

---

## Implementation Roadmap

| Phase | Tasks | Timeline | Dependencies |
|-------|-------|----------|--------------|
| 1 | Domain, email, basic hosting | Week 1 | None |
| 2 | Development environment | Week 2 | Phase 1 |
| 3 | Production infrastructure | Week 3-4 | Phase 2 |
| 4 | Monitoring, backups | Week 4 | Phase 3 |
| 5 | Security hardening | Week 5 | Phase 4 |

---

## Vendor Selection

### Primary Vendors
| Category | Vendor | Contract | Renewal |
|----------|--------|----------|---------|
| Cloud | [Vendor] | [Term] | [Date] |
| Email | [Vendor] | [Term] | [Date] |
| Monitoring | [Vendor] | [Term] | [Date] |

### Evaluation Criteria
| Criterion | Weight |
|-----------|--------|
| Cost | 25% |
| Reliability (SLA) | 25% |
| Features | 20% |
| Support | 15% |
| Security/Compliance | 15% |
```

---

## Execution Flow

1. **Assess needs**
   - Business requirements
   - Technical requirements
   - Scale expectations

2. **Evaluate options**
   - Cloud providers
   - Services
   - Vendors

3. **Design architecture**
   - System diagram
   - Component specs
   - Security requirements

4. **Plan implementation**
   - Phased approach
   - Dependencies
   - Timeline

5. **Estimate costs**
   - Monthly recurring
   - One-time
   - Scale projections

---

## Logging

Log to `CIO/logs/YYYY-MM-DD-infrastructure.md`:
```
## Infrastructure Log: [Date]
Platform selected: [Provider]
Monthly cost estimate: $X - $X
Components planned: [Count]
Phase: [Current phase]
Escalations: [List]
```

---

## Context

- Coordinate with CTO for technical requirements
- Coordinate with CFO for budget
- Foundation for development and operations
- Regular review as business scales

---

*Infrastructure decisions should be validated by qualified professionals.*

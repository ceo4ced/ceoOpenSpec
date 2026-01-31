# coo.quality

## Preamble

This command establishes quality management frameworks for products and services.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `COO/.ethics/ethics.md`
3. `CEO/.ceo/memory/business-plan.md` (if exists)

---

## Outline

Define quality standards, measurement, and continuous improvement processes.

### Quality Management Plan Template

```markdown
# Quality Management Plan: [Business Name]
Generated: [Date]
Product/Service: [Description]

## Quality Philosophy
[One-paragraph quality commitment statement]

---

## Quality Standards

### Product Quality Standards
| Attribute | Specification | Tolerance | Test Method |
|-----------|---------------|-----------|-------------|
| [Attribute 1] | [Spec] | ±X% | [How tested] |
| [Attribute 2] | [Spec] | ±X% | [How tested] |
| [Attribute 3] | [Spec] | ±X% | [How tested] |

### Service Quality Standards
| Dimension | Target | Measurement |
|-----------|--------|-------------|
| Response Time | X hours | Ticket timestamps |
| Resolution Time | X hours | First-contact resolution |
| Accuracy | X% | Audit sampling |
| Satisfaction | X/5 | Customer surveys |

---

## Quality Control Process

### Inspection Points
```
[Stage 1] → Checkpoint → [Stage 2] → Checkpoint → [Stage 3] → Final QC → Ship
```

### Checkpoint Details
| Checkpoint | What's Checked | Pass Criteria | Fail Action |
|------------|----------------|---------------|-------------|
| Incoming | [Materials/inputs] | [Criteria] | [Reject/hold] |
| In-process | [WIP quality] | [Criteria] | [Rework/escalate] |
| Final | [Finished product] | [Criteria] | [Rework/scrap] |
| Post-delivery | [Customer feedback] | [Target] | [Root cause] |

### Sampling Plan
| Volume | Sample Size | Accept/Reject |
|--------|-------------|---------------|
| <100 | 100% inspection | 0 defects |
| 100-500 | 20% random | ≤2 defects |
| >500 | Statistical (AQL) | Per AQL table |

---

## Quality Metrics (KPIs)

### Product Metrics
| Metric | Definition | Target | Current |
|--------|------------|--------|---------|
| Defect Rate | Defects / Units produced | <X% | X% |
| First Pass Yield | Good units / Total units | >X% | X% |
| Return Rate | Returns / Shipped | <X% | X% |
| COGS per Defect | Cost of quality issues | <$X | $X |

### Service Metrics
| Metric | Definition | Target | Current |
|--------|------------|--------|---------|
| CSAT | Customer satisfaction score | >X/5 | X/5 |
| NPS | Net Promoter Score | >X | X |
| FCR | First Contact Resolution | >X% | X% |
| SLA Compliance | % within SLA | >X% | X% |

### Dashboard
| Metric | This Week | Last Week | Trend | Status |
|--------|-----------|-----------|-------|--------|
| [Metric 1] | X | X | ↑/↓/→ | 🟢/🟡/🔴 |
| [Metric 2] | X | X | ↑/↓/→ | 🟢/🟡/🔴 |

---

## Issue Management

### Defect Classification
| Severity | Definition | Response Time | Escalation |
|----------|------------|---------------|------------|
| Critical | Safety/major function | Immediate | CEO + Human |
| Major | Significant but workaround exists | 24 hours | COO |
| Minor | Cosmetic/minor inconvenience | 72 hours | Team lead |

### Root Cause Analysis (5 Whys Template)
```
Problem: [Describe the issue]

Why 1: [First-level cause]
Why 2: [Second-level cause]
Why 3: [Third-level cause]
Why 4: [Fourth-level cause]
Why 5: [Root cause]

Root Cause: [Summary]
Corrective Action: [What will prevent recurrence]
Owner: [Who's responsible]
Due Date: [Deadline]
```

### Corrective Action Log
| ID | Issue | Root Cause | Action | Owner | Status |
|----|-------|------------|--------|-------|--------|
| 001 | [Issue] | [Cause] | [Action] | [Who] | [Open/Closed] |

---

## Continuous Improvement

### Improvement Cycle (PDCA)
```
    ┌─────────┐
    │  PLAN   │ ← Identify improvement
    └────┬────┘
         ↓
    ┌─────────┐
    │   DO    │ ← Implement change (small scale)
    └────┬────┘
         ↓
    ┌─────────┐
    │  CHECK  │ ← Measure results
    └────┬────┘
         ↓
    ┌─────────┐
    │   ACT   │ ← Standardize or adjust
    └─────────┘
```

### Improvement Backlog
| Priority | Improvement | Expected Impact | Effort | Status |
|----------|-------------|-----------------|--------|--------|
| P0 | [Improvement] | [Benefit] | [Hours] | [Status] |
| P1 | [Improvement] | [Benefit] | [Hours] | [Status] |

### Voice of Customer (VOC) Inputs
| Source | Frequency | How Collected | Owner |
|--------|-----------|---------------|-------|
| Support tickets | Continuous | [System] | [Role] |
| Surveys | [Frequency] | [Tool] | [Role] |
| Reviews | Continuous | [Platforms] | [Role] |
| Returns | Continuous | [Process] | [Role] |

---

## Documentation & Training

### Standard Operating Procedures (SOPs)
| Process | SOP ID | Last Updated | Owner |
|---------|--------|--------------|-------|
| [Process 1] | SOP-001 | [Date] | [Role] |
| [Process 2] | SOP-002 | [Date] | [Role] |

### Training Requirements
| Role | Required Training | Frequency | Verification |
|------|-------------------|-----------|--------------|
| [Role] | [Training] | [Frequency] | [Test/Cert] |

---

## Compliance & Certifications

### Applicable Standards
| Standard | Applicability | Status | Expiry |
|----------|---------------|--------|--------|
| ISO 9001 | [If pursuing] | [Status] | [Date] |
| SOC 2 | [If SaaS] | [Status] | [Date] |
| HIPAA | [If healthcare] | [Status] | [Date] |
| [Industry] | [If applicable] | [Status] | [Date] |

---

## Escalation Triggers

- [ ] Critical defect → CEO + Human immediately
- [ ] Recall situation → CLO + CEO + Human
- [ ] Pattern of issues → Root cause investigation
- [ ] Customer safety → STOP EVERYTHING, escalate
```

---

## Execution Flow

1. **Define standards**
   - Product specifications
   - Service levels
   - Customer expectations

2. **Design controls**
   - Inspection points
   - Sampling plans
   - Pass/fail criteria

3. **Establish metrics**
   - KPIs and targets
   - Measurement methods
   - Reporting cadence

4. **Create processes**
   - Issue management
   - Root cause analysis
   - Continuous improvement

5. **Document & train**
   - SOPs
   - Training requirements
   - Compliance tracking

---

## Logging

Log to `COO/logs/YYYY-MM-DD-quality.md`:
```
## Quality Log: [Date]
Metrics reviewed: [List]
Issues identified: [Count]
CAPAs opened: [Count]
CAPAs closed: [Count]
Escalations: [List]
```

---

## Context

- Establish early, before scaling
- Critical for customer satisfaction
- Required for many B2B sales
- Foundation for certifications

---

*Quality systems should be reviewed by professionals for regulated industries.*

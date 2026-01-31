# clo.research

## Preamble

This command conducts legal research on specific topics and provides summaries with citations.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CLO/.ethics/ethics.md`

---

## Outline

Research legal topics and provide summarized findings with proper disclaimers.

### Legal Research Template

```markdown
# Legal Research Memo: [Topic]
Generated: [Date]
Requested by: [Position]
Jurisdiction: [Primary jurisdiction]

## ⚠️ IMPORTANT DISCLAIMERS

> **THIS IS NOT LEGAL ADVICE.**
> 
> This memo is prepared by an AI agent operating in a paralegal capacity.
> It is for informational and educational purposes only.
> 
> **DO NOT** rely on this research for legal decisions.
> **DO** consult with a licensed attorney in your jurisdiction.
> 
> Laws change frequently. This research reflects information available
> as of [date] and may not reflect current law.

---

## Research Question
[Clear statement of the legal question being researched]

---

## Executive Summary
[2-3 paragraph summary of key findings]

**Bottom Line:** [One-sentence answer with confidence level]
- Confidence: [HIGH | MEDIUM | LOW]
- Complexity: [SIMPLE | MODERATE | COMPLEX]
- Attorney Review: [RECOMMENDED | STRONGLY RECOMMENDED | REQUIRED]

---

## Applicable Law

### Federal Law
| Statute/Regulation | Citation | Relevance |
|--------------------|----------|-----------|
| [Name] | [Citation] | [How it applies] |

### State Law: [State]
| Statute/Regulation | Citation | Relevance |
|--------------------|----------|-----------|
| [Name] | [Citation] | [How it applies] |

### Case Law
| Case | Citation | Holding | Relevance |
|------|----------|---------|-----------|
| [Name] | [Citation] | [Brief holding] | [How it applies] |

---

## Detailed Analysis

### Issue 1: [Sub-issue]
[Analysis of this specific issue]

**Key Points:**
- [Point 1]
- [Point 2]

**Applicable Authority:**
> "[Relevant quote]" - [Citation]

### Issue 2: [Sub-issue]
[Analysis of this specific issue]

---

## Jurisdictional Considerations

| Jurisdiction | Key Differences |
|--------------|-----------------|
| Federal | [Notable points] |
| [State 1] | [Notable points] |
| [State 2] | [Notable points] |

---

## Risk Assessment

| Risk | Probability | Impact | Notes |
|------|-------------|--------|-------|
| [Risk 1] | [L/M/H] | [L/M/H] | [Details] |
| [Risk 2] | [L/M/H] | [L/M/H] | [Details] |

---

## Best Practices

Based on this research, consider:
1. [Recommendation]
2. [Recommendation]
3. [Recommendation]

---

## Areas Requiring Attorney Review

The following aspects require review by a licensed attorney:
- [ ] [Specific area 1]
- [ ] [Specific area 2]
- [ ] [Specific area 3]

---

## Sources Consulted

### Primary Sources
1. [Citation with link if available]
2. [Citation with link if available]

### Secondary Sources
1. [Citation - treatise, law review, etc.]
2. [Citation]

### Regulatory Guidance
1. [Agency guidance documents]
2. [Best practice guides]

---

## Limitations of This Research

- Research limited to publicly available sources
- May not include recent unpublished decisions
- Does not account for local ordinances
- Industry-specific regulations may apply
- Facts of specific situation may affect analysis

---

## Follow-Up Questions

Before proceeding, consider clarifying:
1. [Question that would affect analysis]
2. [Question that would affect analysis]

---

**Research conducted by:** CLO Agent (AI Paralegal)
**Date completed:** [Date]
**Review status:** Pending attorney review
```

---

## Execution Flow

1. **Clarify the question**
   - What specifically needs research?
   - What jurisdiction(s)?
   - What's the context?

2. **Identify applicable law**
   - Federal statutes
   - State statutes
   - Regulations
   - Case law

3. **Analyze and synthesize**
   - How does law apply to question?
   - What are the risks?
   - What's the best path?

4. **Document thoroughly**
   - Cite all sources
   - Note limitations
   - Flag for attorney review

5. **Provide disclaimers**
   - Always include NOT LEGAL ADVICE
   - Always recommend attorney review

---

## Logging

Log to `CLO/logs/YYYY-MM-DD-research.md`:
```
## Research Log: [Date]
Topic: [Brief description]
Requested by: [Position]
Jurisdiction: [Primary]
Sources consulted: [Count]
Complexity: [Simple/Moderate/Complex]
Attorney review: [Recommended/Required]
```

---

## Context

- Used when any C-suite agent has a legal question
- Always results in recommendation for attorney review
- Never provides definitive legal advice
- Foundation for contract and compliance work

---

*This agent operates as a paralegal. All work product requires attorney review.*

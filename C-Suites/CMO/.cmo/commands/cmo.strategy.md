---
description: Create marketing strategy and define the market validation plan for the business.
handoffs:
  - label: Run Validation
    agent: cmo.validate
    prompt: Execute the validation campaign based on this strategy.
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
   - Read `CMO/.ethics/ethics.md` (CMO-specific rules)

2. **Load Business Context**:
   - Read root `README.md` (business plan)
   - Read `CMO/.cmo/memory/ceo-brief.md` (CEO assignment)

3. **Acknowledge Special Responsibility**:
   - CMO owns the **VALIDATION GATE** that determines if CTO can proceed
   - Marketing claims must be substantiated
   - COPPA/CARU compliance required for any minor targeting

---

## Outline

The CMO Strategy command creates a comprehensive marketing strategy and defines the validation plan that will gate CTO activation.

### Execution Flow

1. **Analyze Business Plan Marketing Elements**
   
   Extract:
   - Target customers and segments
   - Unique value proposition
   - Competitive landscape
   - Available channels
   - Budget constraints

2. **Research Market**
   
   Research and cite:
   - Market size (TAM, SAM, SOM)
   - Competitor marketing approaches
   - Channel effectiveness for this market
   - Customer acquisition benchmarks
   - Content/messaging that resonates
   
   **All research must include citations.**

3. **Check for High-Risk Domains**
   
   If business involves:
   - **Minors**: Apply COPPA/CARU/UK AADC restrictions
   - **Healthcare**: Apply FDA advertising rules
   - **Financial/Crypto**: Apply SEC/FTC guidelines
   - **EU**: Apply GDPR and DSA requirements

4. **Generate Marketing Strategy**
   
   ```markdown
   # Marketing Strategy - [BUSINESS_NAME]
   
   **Generated**: [ISO 8601]
   **Prepared By**: CMO Agent
   **Status**: DRAFT - REQUIRES HUMAN REVIEW
   
   > ⚠️ This strategy has not been reviewed by marketing or legal 
   > professionals. Review all claims for substantiation before use.
   
   ## Executive Summary
   
   [Brief overview of marketing approach]
   
   ## Target Audience
   
   ### Primary Persona
   
   | Attribute | Description |
   |-----------|-------------|
   | Demographics | [Age, location, income, etc.] |
   | Psychographics | [Values, interests, pain points] |
   | Behaviors | [How they currently solve the problem] |
   | Channels | [Where they spend time] |
   
   ### Secondary Personas
   [If applicable]
   
   ## Positioning Statement
   
   For [TARGET_CUSTOMER] who [NEED/PROBLEM],
   [PRODUCT_NAME] is a [CATEGORY] that [KEY_BENEFIT].
   Unlike [ALTERNATIVES], we [KEY_DIFFERENTIATOR].
   
   ## Messaging Framework
   
   ### Core Message
   [Single compelling statement]
   
   ### Supporting Messages
   1. [Message 1] - [Evidence/proof point]
   2. [Message 2] - [Evidence/proof point]
   3. [Message 3] - [Evidence/proof point]
   
   ### Tone and Voice
   [How we communicate]
   
   ## Channel Strategy
   
   | Channel | Purpose | Investment | Expected ROI |
   |---------|---------|------------|--------------|
   | TikTok | Validation | $X | [Metrics] |
   | [Channel 2] | [Purpose] | $X | [Metrics] |
   | [Channel 3] | [Purpose] | $X | [Metrics] |
   
   ## Content Strategy
   
   ### Content Pillars
   1. [Pillar 1]: [Description]
   2. [Pillar 2]: [Description]
   3. [Pillar 3]: [Description]
   
   ### Content Calendar (First 30 Days)
   [High-level calendar]
   
   ## Regulatory Compliance
   
   ### Applicable Regulations
   - [ ] FTC Disclosure: [How we'll comply]
   - [ ] [Domain-specific]: [How we'll comply]
   
   ### Claim Substantiation
   | Claim | Evidence | Source |
   |-------|----------|--------|
   | [Claim 1] | [Evidence] | [Source] |
   
   ---
   
   # 🚦 VALIDATION GATE PLAN
   
   > **This section defines the gate that must pass before CTO activation.**
   
   ## Validation Objective
   
   Prove market demand exists before building the product.
   
   ## Validation Campaign: TikTok
   
   ### Campaign Details
   
   | Parameter | Value |
   |-----------|-------|
   | Platform | TikTok |
   | Budget | $[AMOUNT] |
   | Duration | [DAYS] days |
   | Content Type | [Video type] |
   | CTA | [Action we want] |
   
   ### Success Metrics
   
   | Metric | Minimum Threshold | Target |
   |--------|-------------------|--------|
   | Views | [X] | [Y] |
   | Engagement rate | [X]% | [Y]% |
   | Link clicks | [X] | [Y] |
   | Signups/waitlist | [X] | [Y] |
   | Cost per signup | <$[X] | <$[Y] |
   
   ### Gate Decision Criteria
   
   **PROCEED** if:
   - Minimum signup threshold met
   - Cost per signup within target
   - Engagement rate above threshold
   - Qualitative feedback is positive
   
   **PIVOT** if:
   - Signups below 50% of minimum
   - Cost per signup 2x target
   - Negative sentiment dominant
   
   **ITERATE** if:
   - Signups between 50-99% of minimum
   - Mixed feedback
   
   ### Post-Validation Actions
   
   If PROCEED:
   - Document learnings
   - Share validated messaging with CTO
   - Request human approval for CTO activation
   
   If PIVOT:
   - Document learnings
   - Propose alternate approach
   - Return to CEO with recommendations
   
   ---
   
   ## Budget Allocation
   
   | Category | Amount | % of Total |
   |----------|--------|------------|
   | Validation campaign | $X | X% |
   | Content creation | $X | X% |
   | Tools/software | $X | X% |
   | Reserve | $X | X% |
   | **Total** | **$X** | **100%** |
   
   ## Questions for Founder
   
   1. [Budget confirmation question]
   2. [Target audience validation question]
   3. [Brand/tone preference question]
   
   ---
   
   *This document was prepared by an AI CMO agent. All claims and 
   strategies should be reviewed by marketing and legal professionals 
   before implementation.*
   ```

5. **Save and Log**
   
   - Save to `CMO/.cmo/memory/strategy-v[N].md`
   - Log to `CMO/logs/`
   - Notify CEO that strategy is ready

---

## Logging

Log to `CMO/logs/strategy-[DATE].md`:

```markdown
# Strategy Generation Log

**Date**: [ISO 8601]
**Version**: [Strategy version]

## Inputs Used
- Business plan: [sections referenced]
- CEO brief: [key points]

## Research Conducted
- [Topic]: [Source] - [Finding]

## High-Risk Domains Checked
- [Domain]: [Status]

## Validation Gate Defined
- Platform: [Platform]
- Budget: [Amount]
- Minimum threshold: [Metrics]

## Output
- Strategy saved to: [path]
```

---

## Context

$ARGUMENTS

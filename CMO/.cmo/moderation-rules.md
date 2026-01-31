# CMO Content Moderation Rules

This document defines the content moderation rules that apply to ALL CMO-generated content before human approval.

---

## Core Principles

1. **Safety First** - No harmful content, ever
2. **Brand Alignment** - All content reflects brand values
3. **Legal Compliance** - FTC, COPPA, platform rules
4. **Human Approval** - Nothing publishes without human consent

---

## Audience Age Gates

### Determination

The audience age gate is set in the brand kit and determines content restrictions:

| Gate | Description | Applied When |
|------|-------------|--------------|
| `all_ages` | Family-friendly, suitable for all | Default, children's products, general brands |
| `13-17` | Teen appropriate | Youth brands, social platforms |
| `18+` | Adult only | Products/services for adults only |

### ⚠️ Override Rules

```python
# Age gate can ONLY be set by human
# CMO cannot upgrade age gate without explicit approval

def set_audience_age(requested_age: str, current_age: str) -> str:
    """
    Audience age can only become MORE restrictive automatically.
    Becoming LESS restrictive requires human approval.
    """
    restriction_level = {
        'all_ages': 1,  # Most restrictive
        '13-17': 2,
        '18+': 3       # Least restrictive
    }
    
    if restriction_level[requested_age] > restriction_level[current_age]:
        raise RequiresApproval(
            "Cannot loosen age restrictions without human approval"
        )
    
    return requested_age
```

---

## Language Policy

### All Ages (Default)

**BLOCK** (content cannot proceed):
- All profanity (any severity)
- Violence or gore
- Sexual content/innuendo
- Drug/alcohol references
- Gambling references
- Political controversy
- Religious controversy
- Hate speech
- Bullying/harassment

**WARN** (flag for review but allow):
- Mild exclamations (gosh, darn)
- Competitive language
- Strong emotions

### 13-17 (Teen)

**BLOCK**:
- Severe profanity (f-word, s-word, slurs)
- Sexual content
- Drug references
- Hate speech
- Bullying/harassment
- Dangerous activities

**WARN** (flag for human review):
- Mild profanity (damn, hell)
- Violence in context (action, gaming)
- Edgy humor
- Social issues

**ALLOW**:
- Age-appropriate topics
- Teen slang
- Pop culture references

### 18+ (Adult)

**BLOCK**:
- Illegal content
- Hate speech / discrimination
- Dangerous activities
- Non-consensual themes
- Content illegal in target market

**WARN** (flag for human review):
- Strong profanity
- Adult themes
- Controversial opinions
- Explicit humor

**ALLOW** (with disclosure):
- Profanity appropriate to brand
- Mature themes
- Direct language
- Industry-specific content

---

## Profanity Dictionary

### Severity Tiers

```python
PROFANITY = {
    'tier_1_block_always': [
        # Slurs - always blocked everywhere
        # [redacted in spec - loaded from secure config]
    ],
    
    'tier_2_block_under_18': [
        'fuck', 'fucking', 'fucked',
        'shit', 'shitting', 
        'bitch', 'bitches',
        'asshole',
        'dick', 'cock',
        'pussy',
        'bastard',
        'whore', 'slut',
        # Compound forms auto-detected
    ],
    
    'tier_3_block_under_13': [
        'damn', 'damned',
        'hell',
        'ass',
        'crap', 'crappy',
        'piss', 'pissed',
        'suck', 'sucks',
    ],
    
    'tier_4_warn_only': [
        'stupid', 'idiot',
        'dumb', 
        'loser',
        'sucks',
    ]
}
```

### Detection Logic

```python
def check_language(text: str, audience_age: str) -> dict:
    """
    Check text against language policy.
    """
    text_lower = text.lower()
    text_normalized = normalize_leetspeak(text_lower)  # f*ck → fuck
    
    violations = []
    warnings = []
    
    # Check all tiers
    for word in PROFANITY['tier_1_block_always']:
        if word in text_normalized:
            violations.append({
                'word': word,
                'tier': 1,
                'action': 'HARD_BLOCK',
                'reason': 'Prohibited for all audiences'
            })
    
    if audience_age != '18+':
        for word in PROFANITY['tier_2_block_under_18']:
            if word in text_normalized:
                violations.append({
                    'word': word,
                    'tier': 2,
                    'action': 'BLOCK',
                    'reason': f'Blocked for {audience_age} audience'
                })
    
    if audience_age == 'all_ages':
        for word in PROFANITY['tier_3_block_under_13']:
            if word in text_normalized:
                violations.append({
                    'word': word,
                    'tier': 3,
                    'action': 'BLOCK',
                    'reason': 'Blocked for all-ages audience'
                })
    
    # Warnings for any audience
    for word in PROFANITY['tier_4_warn_only']:
        if word in text_normalized:
            warnings.append({
                'word': word,
                'tier': 4,
                'action': 'WARN',
                'reason': 'Consider if appropriate for brand'
            })
    
    return {
        'pass': len(violations) == 0,
        'violations': violations,
        'warnings': warnings,
        'audience_age': audience_age
    }


def normalize_leetspeak(text: str) -> str:
    """
    Normalize common obfuscation attempts.
    """
    replacements = {
        '@': 'a', '4': 'a',
        '3': 'e',
        '1': 'i', '!': 'i',
        '0': 'o',
        '5': 's', '$': 's',
        '7': 't',
        '*': '',  # Remove masking characters
    }
    
    result = text
    for char, replacement in replacements.items():
        result = result.replace(char, replacement)
    
    return result
```

---

## Content Category Rules

### Violence

| Audience | Rule |
|----------|------|
| All ages | No violence |
| 13-17 | Cartoon/fantasy only, no realistic harm |
| 18+ | Context-dependent, no gratuitous gore |

### Sexual Content

| Audience | Rule |
|----------|------|
| All ages | None whatsoever |
| 13-17 | No sexual content |
| 18+ | Tasteful adult themes OK with disclosure |

### Substances

| Audience | Rule |
|----------|------|
| All ages | No references |
| 13-17 | No references (even anti-drug messaging needs care) |
| 18+ | OK for relevant products (alcohol brands, etc.) |

### Controversial Topics

| Topic | Rule |
|-------|------|
| Politics | Avoid unless brand-relevant |
| Religion | Avoid unless brand-relevant |
| Social issues | Align with brand values, get approval |

---

## FTC Compliance

### Required Disclosures

| Situation | Disclosure |
|-----------|------------|
| Paid partnership | #Ad, #Sponsored, Paid partnership label |
| Gifted product | #Gifted |
| Affiliate link | "I may earn commission" |
| Contest/giveaway | Official rules, voiding jurisdictions |
| AI-generated | Disclosure if human-like (varies by platform) |

### Claim Verification

```python
FTC_BLOCKED_CLAIMS = [
    r'\b(best|#1|number one|top)\b',  # Unless substantiated
    r'\b(guaranteed|100%|always)\b',  # Absolute claims
    r'\bcure[sd]?\b',                 # Health claims
    r'\blose \d+ (pounds?|lbs?)\b',   # Weight loss claims
    r'\brisk.free\b',                 # Financial claims
]

def check_ftc_compliance(text: str) -> list:
    """
    Check for FTC-problematic claims.
    """
    issues = []
    
    for pattern in FTC_BLOCKED_CLAIMS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            issues.append({
                'type': 'unsubstantiated_claim',
                'match': matches,
                'action': 'BLOCK or add substantiation'
            })
    
    return issues
```

---

## Platform-Specific Rules

### TikTok Community Guidelines

**Auto-block content mentioning:**
- Self-harm / suicide
- Eating disorders  
- Dangerous challenges
- Weapons / drugs
- Nudity / sexual content
- Harassment / hate

### Instagram Community Guidelines

Similar to TikTok, plus:
- No spam/engagement bait
- No false information
- Copyright compliance

### Twitter/X Rules

- No threats
- No private information
- No platform manipulation

---

## Moderation Pipeline

```
CONTENT CREATED
      │
      ▼
┌─────────────────────────────────┐
│   AUTOMATED CHECKS (instant)    │
├─────────────────────────────────┤
│ □ Language policy               │
│ □ FTC compliance                │
│ □ Platform rules                │
│ □ Brand guidelines              │
│ □ Image/video safety scan       │
└─────────────────────────────────┘
      │
      ├── VIOLATIONS → BLOCK (return to CMO)
      │
      ├── WARNINGS → FLAG (include in approval request)
      │
      ▼
┌─────────────────────────────────┐
│   HUMAN APPROVAL (required)     │
├─────────────────────────────────┤
│ Human sees:                     │
│ • Content preview               │
│ • All warnings                  │
│ • Moderation report             │
│ • Publishing details            │
└─────────────────────────────────┘
      │
      ├── APPROVED → Ready to publish
      │
      ├── REVISE → Back to creation
      │
      └── REJECT → Archived
```

---

## Escalation Matrix

| Issue | Action |
|-------|--------|
| Tier 1 profanity (slurs) | 🔴 Immediate block, alert CMO |
| COPPA violation risk | 🔴 RED PHONE to human + CLO |
| Legal/trademark concern | 🔴 Escalate to CLO |
| Brand guideline violation | 🟡 Block, return to CMO |
| Minor warnings only | 🟢 Include in approval request |

---

## Logging

All moderation decisions logged:

```sql
INSERT INTO content_moderation (
    content_id,
    business_id,
    moderation_timestamp,
    
    -- Checks
    language_check_passed BOOL,
    language_violations JSON,
    ftc_check_passed BOOL,
    platform_check_passed BOOL,
    brand_check_passed BOOL,
    
    -- Result
    overall_result STRING,  -- passed, blocked, warned
    blocking_reasons JSON,
    warnings JSON,
    
    -- Audience
    audience_age STRING,
    
    -- Human decision
    sent_to_human_at TIMESTAMP,
    human_decision STRING,
    human_feedback STRING
) VALUES (...);
```

---

*All content must pass moderation AND human approval before external publication.*

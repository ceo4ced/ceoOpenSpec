# CMO Digital Asset Pipeline

This document defines the complete workflow for creating, reviewing, approving, and distributing digital assets from initial concept to platform publication.

---

## Pipeline Overview

```
BRIEF            CREATION          REVIEW           APPROVAL         DISTRIBUTION
  │                 │                │                 │                  │
  ▼                 ▼                ▼                 ▼                  ▼
┌─────┐         ┌─────┐         ┌─────────┐      ┌──────────┐      ┌──────────┐
│ CEO │ ──────► │ CMO │ ──────► │ Content │ ───► │  HUMAN   │ ───► │ Platform │
│Brief│         │Create│        │Moderation│     │ Approval │      │ Publish  │
└─────┘         └─────┘         └─────────┘      └──────────┘      └──────────┘
                   │                 │                 │
                   ▼                 ▼                 ▼
              Store in          Log Review       Log Decision
              BigQuery          Results          & Publish
```

---

## Asset Types

| Asset Type | Created With | Review Level | Platform |
|------------|--------------|--------------|----------|
| Logo | Human designer / Nano Banana | Full brand review | All |
| Brand colors | CMO + review | Brand review | All |
| Social graphics | Nano Banana + CMO | Content moderation | Social |
| TikTok videos | Nano Banana + CMO | Full moderation | TikTok |
| Ad creatives | Nano Banana + CMO | Full moderation + CLO | Ad platforms |
| Website assets | Nano Banana + CMO | Brand review | Web |
| Email graphics | Nano Banana + CMO | Content moderation | Email |

---

## Stage 1: Brief

### Brief Template

```markdown
# Creative Brief: [Asset Name]
From: CEO/CMO
Date: [Date]
Priority: [High/Medium/Low]

## Objective
What should this asset accomplish?

## Target Audience
- Age: [Range] ⚠️ CRITICAL FOR CONTENT POLICY
- Platform: [Where will this be shown?]
- Interests: [What resonates with them?]

## Key Message
[Single core message]

## Mandatory Elements
- [ ] Logo inclusion
- [ ] Brand colors
- [ ] CTA: [What action?]
- [ ] Hashtags (if social)

## Specifications
- Format: [Video/Image/Carousel]
- Size: [Dimensions]
- Duration: [If video]
- Files needed: [List]

## Inspiration/References
[Links or descriptions]

## Content Restrictions
- Audience age gate: [All Ages/13-17/18+]
- Language policy: [Clean/Moderate/Adult]
- Sensitive topics: [Any to avoid]

## Deadline
Created by: [Date]
Review by: [Date]
Publish by: [Date]
```

---

## Stage 2: Creation

### Asset Creation Sources

| Source | When to Use | Integration |
|--------|-------------|-------------|
| **Nano Banana** | Quick social content, images | API |
| **Human Designer** | Logo, brand identity, complex | Manual |
| **Templates** | Recurring content types | Library |
| **Stock** | Supporting imagery | Licensed sources |

### Nano Banana Integration

```python
# Example: Generate TikTok thumbnail
def create_asset_with_nano_banana(brief: dict) -> dict:
    """
    Call Nano Banana API to generate asset.
    """
    prompt = build_prompt_from_brief(brief)
    
    # Apply style guide constraints
    prompt = apply_brand_guidelines(prompt, brief['brand_kit'])
    
    # Apply content moderation rules
    prompt = apply_content_policy(prompt, brief['audience_age'])
    
    response = nano_banana_api.generate(
        prompt=prompt,
        style=brief.get('style', 'brand_default'),
        dimensions=brief['dimensions'],
        brand_colors=brief['brand_kit']['colors']
    )
    
    # Store in BigQuery
    store_asset_record(response, brief)
    
    return {
        'asset_id': response['id'],
        'preview_url': response['preview'],
        'status': 'pending_review'
    }
```

### Content Policy Enforcement During Creation

```python
def apply_content_policy(prompt: str, audience_age: str) -> str:
    """
    Enforce content policy based on audience age.
    """
    prohibited = {
        'all_ages': [
            # Explicit profanity
            r'\b(fuck|shit|damn|ass|bitch|hell)\b',
            # Violence
            r'\b(kill|murder|blood|gore)\b',
            # Adult themes
            r'\b(sex|drugs|alcohol|gambling)\b',
            # Controversial
            r'\b(political|religious.*controversy)\b'
        ],
        '13-17': [
            # Less restrictive but still clean
            r'\b(fuck|shit)\b',
            r'\b(sex|drugs)\b',
        ],
        '18+': [
            # Only truly prohibited
            r'\b(illegal|dangerous.*activity)\b'
        ]
    }
    
    policy = prohibited.get(audience_age, prohibited['all_ages'])
    
    for pattern in policy:
        if re.search(pattern, prompt, re.IGNORECASE):
            raise ContentPolicyViolation(
                f"Content violates policy for {audience_age} audience"
            )
    
    return prompt
```

---

## Stage 3: Content Moderation

### Automated Checks

Every asset goes through automated moderation:

```python
def moderate_content(asset: dict) -> dict:
    """
    Run automated content moderation.
    """
    checks = {
        'brand_compliance': check_brand_compliance(asset),
        'language_policy': check_language_policy(asset),
        'platform_rules': check_platform_rules(asset),
        'accessibility': check_accessibility(asset),
        'legal_compliance': check_legal_compliance(asset)
    }
    
    # Log to BigQuery
    log_moderation_result(asset['id'], checks)
    
    overall_status = 'pass' if all(c['pass'] for c in checks.values()) else 'fail'
    
    return {
        'asset_id': asset['id'],
        'moderation_status': overall_status,
        'checks': checks,
        'requires_human_review': True  # ALWAYS requires human
    }
```

### Check Details

#### Brand Compliance
```python
def check_brand_compliance(asset: dict) -> dict:
    """
    Verify asset follows brand guidelines.
    """
    return {
        'pass': True/False,
        'issues': [
            # "Logo too small",
            # "Colors off-brand",
            # "Font not approved"
        ]
    }
```

#### Language Policy
```python
def check_language_policy(asset: dict) -> dict:
    """
    Check text content against language policy.
    """
    audience_age = asset.get('audience_age', 'all_ages')
    text_content = extract_text(asset)
    
    violations = []
    
    # Profanity check
    profanity_words = get_profanity_list(audience_age)
    for word in profanity_words:
        if word.lower() in text_content.lower():
            violations.append(f"Prohibited word: {word}")
    
    # FTC compliance (no unsubstantiated claims)
    ftc_violations = check_ftc_compliance(text_content)
    violations.extend(ftc_violations)
    
    return {
        'pass': len(violations) == 0,
        'violations': violations,
        'audience_age': audience_age
    }
```

#### Platform Rules

```python
PLATFORM_RULES = {
    'tiktok': {
        'max_hashtags': 5,
        'max_duration': 180,  # seconds
        'prohibited_content': ['spam', 'misinformation', 'hate'],
        'requires_music_license': True
    },
    'instagram': {
        'max_hashtags': 30,
        'feed_ratio': ['1:1', '4:5'],
        'story_ratio': '9:16'
    },
    'twitter': {
        'max_chars': 280,
        'max_video_duration': 140
    }
}
```

---

## Stage 4: Human Approval

### ⚠️ MANDATORY FOR ALL EXTERNAL CONTENT

**No content publishes without human approval.**

### Approval Request Format

```
📋 CONTENT APPROVAL REQUEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Asset: [Name]
Type: [TikTok Video / Instagram Post / etc.]
Created: [Date]

📎 Preview: [Link to preview]

✅ AUTOMATED CHECKS PASSED:
• Brand compliance: ✓
• Language policy: ✓
• Platform rules: ✓
• Accessibility: ✓

⚠️ NOTES:
• [Any flags or concerns]

📊 TARGETING:
• Audience: [Details]
• Age gate: [All Ages / 13-17 / 18+]
• Platform: [Platform]

Reply:
• "APPROVE" - Publish immediately
• "APPROVE SCHEDULED [datetime]" - Schedule
• "REVISE: [feedback]" - Request changes
• "REJECT: [reason]" - Do not publish
```

### Approval Logging

```sql
INSERT INTO content_approvals (
    asset_id,
    business_id,
    requested_at,
    approved_at,
    approved_by,
    decision,
    feedback,
    platform,
    scheduled_publish_time
) VALUES (...);
```

---

## Stage 5: Distribution

### Supported Platforms

| Platform | API Integration | Scheduling | Analytics |
|----------|-----------------|------------|-----------|
| TikTok | TikTok API v2 | Yes | Yes |
| Instagram | Meta Graph API | Yes | Yes |
| Facebook | Meta Graph API | Yes | Yes |
| Twitter/X | Twitter API v2 | Yes | Yes |
| LinkedIn | LinkedIn API | Yes | Yes |
| YouTube | YouTube Data API | Yes | Yes |

### Publish Workflow

```python
async def publish_asset(asset_id: str, approval: dict) -> dict:
    """
    Publish approved asset to platform.
    """
    asset = get_asset(asset_id)
    
    # Verify approval
    if not approval.get('approved'):
        raise ValueError("Cannot publish unapproved content")
    
    # Get platform client
    platform = asset['target_platform']
    client = get_platform_client(platform)
    
    # Check if scheduled
    if approval.get('scheduled_time'):
        return schedule_publish(asset, approval['scheduled_time'])
    
    # Publish immediately
    result = await client.publish(
        content=asset['content'],
        media=asset['media_files'],
        caption=asset['caption'],
        hashtags=asset['hashtags']
    )
    
    # Log publication
    log_publication(asset_id, platform, result)
    
    return {
        'status': 'published',
        'platform_post_id': result['id'],
        'url': result['url'],
        'published_at': datetime.utcnow()
    }
```

### TikTok Specific

```python
async def publish_to_tiktok(asset: dict) -> dict:
    """
    Publish video to TikTok via API.
    """
    client = TikTokAPI(
        client_key=get_secret('tiktok-client-key'),
        client_secret=get_secret('tiktok-client-secret'),
        access_token=get_secret('tiktok-access-token')
    )
    
    # Upload video
    video_id = await client.upload_video(
        video_path=asset['video_path'],
        privacy_level='public',
        disable_duet=False,
        disable_stitch=False
    )
    
    # Add caption and hashtags
    result = await client.publish(
        video_id=video_id,
        title=asset['caption'][:150],  # TikTok limit
        hashtags=asset['hashtags'][:5]  # Max 5 recommended
    )
    
    return result
```

---

## Content Calendar

### Weekly Schedule Template

```markdown
# Content Calendar: Week of [Date]

## Monday
| Time | Platform | Content | Status |
|------|----------|---------|--------|
| 9am | TikTok | [Description] | [ ] Draft → [ ] Approved |
| 12pm | Instagram | [Description] | [ ] Draft → [ ] Approved |

## Tuesday
[...]

## Publishing Windows (Optimal Times)
| Platform | Best Times (EST) |
|----------|------------------|
| TikTok | 7am, 10am, 3pm, 7pm |
| Instagram | 8am, 12pm, 5pm |
| Twitter | 9am, 12pm, 3pm |
```

---

## Analytics & Reporting

### Tracked Metrics (Per Post)

| Metric | TikTok | Instagram | Twitter |
|--------|--------|-----------|---------|
| Views | ✓ | ✓ | ✓ |
| Likes | ✓ | ✓ | ✓ |
| Comments | ✓ | ✓ | ✓ |
| Shares | ✓ | ✓ | ✓ (Retweets) |
| Saves | ✓ | ✓ | ✓ (Bookmarks) |
| CTR | ✓ | ✓ | ✓ |
| Watch time | ✓ | ✓ (Reels) | ✓ |

### Performance Logging

```sql
CREATE TABLE content_performance (
    post_id STRING,
    platform STRING,
    asset_id STRING,
    business_id STRING,
    
    -- Engagement
    views INT64,
    likes INT64,
    comments INT64,
    shares INT64,
    saves INT64,
    
    -- Conversion
    clicks INT64,
    conversions INT64,
    
    -- Cost (if paid)
    spend FLOAT64,
    cpc FLOAT64,
    cpm FLOAT64,
    
    -- Timing
    published_at TIMESTAMP,
    snapshot_at TIMESTAMP
);
```

---

## Escalation Triggers

### Automatic Escalation

| Trigger | Action |
|---------|--------|
| Content moderation fail | Block publish, alert CMO |
| Profanity detected | Block publish, alert CMO |
| Under-13 content with issues | 🔴 RED PHONE to human + CLO |
| Legal/compliance flag | Block publish, escalate to CLO |
| Negative sentiment spike | Alert CMO, pause campaign |

---

## Integration with Nano Banana

### Workflow

```
1. CMO creates brief
2. Brief sent to Nano Banana API
3. Nano Banana returns asset options
4. CMO selects/refines best option
5. Asset enters review pipeline
6. Human approves
7. CMO publishes to platform
```

### API Integration Point

```python
NANO_BANANA_CONFIG = {
    'api_url': 'https://api.nanobanana.ai/v1',
    'default_style': 'brand_kit',
    'quality': 'high',
    'variations': 3  # Generate 3 options
}
```

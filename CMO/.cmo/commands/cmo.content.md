# cmo.content

## Preamble

This command generates content for social platforms using Nano Banana AI with brand guidelines and content moderation enforcement.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CMO/.ethics/ethics.md`
3. `CMO/.cmo/memory/brand-kit.md` (brand guidelines)
4. `CMO/.cmo/asset-pipeline.md` (workflow)

---

## Command Types

```
cmo.content create [type] --platform [platform]
cmo.content review [asset-id]
cmo.content schedule [asset-id] --time [datetime]
cmo.content publish [asset-id]  # Requires prior human approval
```

---

## Content Types

| Type | Description | Platforms |
|------|-------------|-----------|
| `video` | Short-form video (15-60s) | TikTok, Instagram Reels, YouTube Shorts |
| `image` | Static image post | Instagram, Twitter, LinkedIn |
| `carousel` | Multiple image post | Instagram, LinkedIn |
| `story` | Ephemeral content | Instagram, TikTok |
| `text` | Text-only post | Twitter, LinkedIn |
| `ad` | Paid advertisement | All (requires CLO review) |

---

## Create: `cmo.content create`

### Input

```yaml
type: video  # video, image, carousel, story, text, ad
platform: tiktok

# Content details
concept: "Unboxing our new product with funny reaction"
key_message: "Try Nano Banana for free"
cta: "Link in bio"

# Targeting
audience_age: 18+  # all_ages, 13-17, 18+
demographic: "Gen Z creators"

# Constraints
duration: 30  # seconds, for video
aspect_ratio: 9:16
music: trending  # trending, brand, none

# Nano Banana generation
style: energetic
variations: 3  # Number of options to generate
```

### Execution Flow

```
1. LOAD BRAND KIT
   └─ Read CMO/.cmo/memory/brand-kit.md
   └─ Extract: colors, fonts, voice, language policy

2. BUILD CREATIVE BRIEF
   └─ Apply brand constraints
   └─ Set content moderation level (based on audience_age)
   └─ Define visual requirements

3. GENERATE WITH NANO BANANA
   └─ Send brief to Nano Banana API
   └─ Request [variations] options
   └─ Apply brand color overlay

4. CONTENT MODERATION (AUTOMATED)
   └─ Check language policy compliance
   └─ Scan for prohibited content
   └─ Verify brand guideline adherence
   └─ Check platform-specific rules

5. STORE & QUEUE FOR REVIEW
   └─ Save to BigQuery asset table
   └─ Generate preview links
   └─ Create approval request

6. REQUEST HUMAN APPROVAL
   └─ Send to human via Telegram/Dashboard
   └─ BLOCK until approved

7. PUBLISH (only after approval)
```

### Content Moderation Rules

```python
MODERATION_RULES = {
    'all_ages': {
        'profanity': 'block',
        'violence': 'block',
        'adult_themes': 'block',
        'substance_references': 'block',
        'controversial_topics': 'block',
        'requires_disclaimer': []
    },
    '13-17': {
        'profanity': 'block',
        'violence': 'warn',
        'adult_themes': 'block',
        'substance_references': 'block',
        'controversial_topics': 'warn',
        'requires_disclaimer': ['sponsored']
    },
    '18+': {
        'profanity': 'allow_with_warning',  # Still flags for review
        'violence': 'warn',
        'adult_themes': 'allow_with_warning',
        'substance_references': 'allow_with_warning',
        'controversial_topics': 'warn',
        'requires_disclaimer': ['sponsored', 'adult_content']
    }
}
```

### Profanity Detection

```python
PROFANITY_TIERS = {
    'severe': [  # Always blocked
        'f*ck', 'sh*t', 'n-word', 'c-word'  # Redacted here
    ],
    'moderate': [  # Blocked unless 18+
        'damn', 'hell', 'ass', 'crap'
    ],
    'mild': [  # Warned, allow for 18+
        'sucks', 'stupid'
    ]
}

def check_profanity(text: str, audience_age: str) -> dict:
    """
    Check text for profanity based on audience age.
    """
    violations = []
    warnings = []
    
    text_lower = text.lower()
    
    for word in PROFANITY_TIERS['severe']:
        if word in text_lower:
            violations.append({
                'word': word,
                'severity': 'severe',
                'action': 'BLOCK'
            })
    
    for word in PROFANITY_TIERS['moderate']:
        if word in text_lower:
            if audience_age == '18+':
                warnings.append({'word': word, 'action': 'FLAG'})
            else:
                violations.append({
                    'word': word,
                    'severity': 'moderate',
                    'action': 'BLOCK'
                })
    
    return {
        'pass': len(violations) == 0,
        'violations': violations,
        'warnings': warnings
    }
```

---

## Output

### Approval Request (Sent to Human)

```
📱 CONTENT READY FOR REVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Asset ID: CNT-2024-0131-001
Type: TikTok Video (30s)
Created: Jan 31, 2024 9:15 AM

🎬 PREVIEW
[Preview Link]

📝 DETAILS
Caption: "When you finally try that thing everyone's talking about 😱 #NanoBanana #AICreator"
Hashtags: #NanoBanana #AICreator #ContentCreator #TikTok #Viral
Music: [Trending Sound Name]
CTA: Link in bio

✅ MODERATION PASSED
• Language: Clean ✓
• Brand: Compliant ✓
• Platform: TikTok rules ✓
• Legal: No disclaimers needed ✓

📊 TARGETING
• Audience: 18+
• Platform: TikTok
• Best time: 3:00 PM EST

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reply with:
✓ "APPROVE" → Publish now
✓ "SCHEDULE 3pm" → Schedule for 3:00 PM
✓ "REVISE [feedback]" → Request changes  
✗ "REJECT [reason]" → Discard

⚠️ No content publishes without your approval.
```

---

## Review: `cmo.content review`

Manually review an existing asset.

### Input
```yaml
asset_id: CNT-2024-0131-001
action: approve | reject | revise
feedback: "optional feedback"
schedule_time: "2024-01-31T15:00:00"  # If scheduling
```

### Actions

| Action | Result |
|--------|--------|
| `approve` | Asset cleared for immediate publish |
| `schedule` | Asset queued for scheduled time |
| `revise` | Asset returned to CMO with feedback |
| `reject` | Asset archived, not published |

---

## Schedule: `cmo.content schedule`

Schedule approved content for future publication.

### Input
```yaml
asset_id: CNT-2024-0131-001
platform: tiktok
publish_time: 2024-01-31T15:00:00-05:00  # Must include timezone
notify_on_publish: true
```

### Execution

1. Verify asset is approved
2. Add to publish queue
3. Cloud Scheduler triggers at time
4. Publish to platform
5. Log result
6. Notify human of publication

---

## Publish: `cmo.content publish`

Immediately publish an approved asset.

### Prerequisites

- [ ] Asset exists and is valid
- [ ] Content moderation passed
- [ ] **Human approval received** ⚠️ REQUIRED
- [ ] Platform credentials configured
- [ ] No active blocks or escalations

### Execution

```python
async def publish_content(asset_id: str) -> dict:
    """
    Publish content to platform.
    """
    asset = get_asset(asset_id)
    
    # CRITICAL: Verify human approval
    if not asset.get('human_approved'):
        raise ValueError("Cannot publish without human approval")
    
    if asset['human_approved_at'] < datetime.now() - timedelta(days=7):
        raise ValueError("Approval expired. Re-approval required.")
    
    # Get platform client
    platform = asset['platform']
    
    if platform == 'tiktok':
        result = await publish_to_tiktok(asset)
    elif platform == 'instagram':
        result = await publish_to_instagram(asset)
    elif platform == 'twitter':
        result = await publish_to_twitter(asset)
    else:
        raise ValueError(f"Unsupported platform: {platform}")
    
    # Log publication
    log_publication(asset_id, platform, result)
    
    # Notify human
    await notify_human(
        f"✅ Published to {platform}\n"
        f"URL: {result['url']}\n"
        f"Time: {datetime.now()}"
    )
    
    return result
```

---

## TikTok Publishing Details

### API Integration

```python
class TikTokPublisher:
    def __init__(self, credentials: dict):
        self.client_key = credentials['client_key']
        self.client_secret = credentials['client_secret']
        self.access_token = credentials['access_token']
    
    async def upload_video(self, video_path: str) -> str:
        """Upload video to TikTok."""
        # Step 1: Initialize upload
        init_response = await self._init_upload()
        upload_url = init_response['upload_url']
        
        # Step 2: Upload video file
        with open(video_path, 'rb') as f:
            await self._upload_file(upload_url, f)
        
        return init_response['video_id']
    
    async def publish(
        self,
        video_id: str,
        caption: str,
        privacy: str = 'public',
        allow_comments: bool = True,
        allow_duet: bool = True,
        allow_stitch: bool = True
    ) -> dict:
        """Publish uploaded video."""
        return await self._post('/publish/', {
            'video_id': video_id,
            'post_info': {
                'title': caption[:150],  # TikTok limit
                'privacy_level': privacy,
                'disable_comment': not allow_comments,
                'disable_duet': not allow_duet,
                'disable_stitch': not allow_stitch
            }
        })
```

### TikTok Content Requirements

| Requirement | Specification |
|-------------|---------------|
| Video format | MP4, MOV |
| Aspect ratio | 9:16 (vertical) |
| Resolution | 1080x1920 minimum |
| Duration | 5s - 3min (15-60s optimal) |
| File size | Max 287.6 MB |
| Caption | Max 150 chars |
| Hashtags | Max 5 recommended |

---

## Content Logging

### BigQuery Tables

```sql
-- Asset creation log
INSERT INTO content_assets (
    asset_id,
    business_id,
    content_type,
    platform,
    created_at,
    created_by,
    nano_banana_prompt,
    audience_age,
    moderation_passed,
    moderation_details
) VALUES (...);

-- Approval log
INSERT INTO content_approvals (
    asset_id,
    requested_at,
    decided_at,
    decision,
    decided_by,
    scheduled_time,
    feedback
) VALUES (...);

-- Publication log
INSERT INTO content_publications (
    asset_id,
    platform,
    platform_post_id,
    published_at,
    url,
    initial_views,
    error
) VALUES (...);
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Moderation fail | Block, return to CMO with violations |
| API rate limit | Retry with backoff |
| Upload fail | Retry 3x, then escalate |
| Approval expired | Request re-approval |
| Platform rejection | Log reason, notify CMO |

---

## Escalation Triggers

| Trigger | Escalation |
|---------|------------|
| Multiple moderation fails | Alert CMO, review process |
| Approval taking >24h | Reminder to human |
| Post removed by platform | 🔴 RED PHONE to CMO + CLO |
| Account restriction | 🔴 RED PHONE immediate |

---

## Integration Points

- **Nano Banana**: Content generation
- **BigQuery**: Asset/approval logging
- **Telegram/Dashboard**: Human approval
- **TikTok API**: Publishing
- **Cloud Scheduler**: Scheduled posts

---

*All content requires human approval before external publication.*

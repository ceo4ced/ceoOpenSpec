# cmo.approve

## Preamble

This command handles the human approval workflow for ALL content before external publication.

**CRITICAL: This is the human-in-the-loop gate. No content publishes without passing through this workflow.**

---

## Approval Types

| Type | When Required | Approver |
|------|---------------|----------|
| `GREENLIGHT: BRAND` | Brand kit, logo, style guide | Human |
| `GREENLIGHT: CONTENT` | Individual content pieces | Human |
| `GREENLIGHT: CAMPAIGN` | Multi-piece campaigns | Human |
| `GREENLIGHT: PAID` | Any paid advertising | Human + Budget check |

---

## Request: `cmo.approve request`

### Approval Request Format (Sent to Human via Telegram/Dashboard)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 CONTENT APPROVAL REQUEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 REQUEST ID: APR-2024-0131-001
📁 TYPE: [TikTok Video / Instagram Post / etc.]
⏰ SUBMITTED: [Date Time]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎬 PREVIEW
[Link to preview content]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 CONTENT DETAILS

Caption: "[Caption text]"

Hashtags: [List]

CTA: "[Call to action]"

Sound: [If TikTok/Reels]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ AUTOMATED CHECKS

• Language: ✓ PASSED (all_ages compliant)
• FTC: ✓ PASSED (no unsubstantiated claims)
• Brand: ✓ PASSED (colors, fonts, voice aligned)
• Platform: ✓ PASSED (TikTok rules compliant)

⚠️ WARNINGS (0)
[None OR list of flagged items]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 TARGETING

• Platform: TikTok
• Audience: 18+ [Age gate setting]
• Optimal post time: 3:00 PM EST
• Campaign: [None / Campaign name]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 SPEND (if paid)

• Budget: $0.00 (organic)
[Or budget details if paid]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 QUICK ACTIONS

Reply with:

✓ "APPROVE" → Publish at optimal time
✓ "APPROVE NOW" → Publish immediately  
✓ "SCHEDULE [datetime]" → Custom schedule
✓ "REVISE: [feedback]" → Request changes
✗ "REJECT: [reason]" → Do not publish

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Content will NOT publish without your response.
Request expires in 72 hours.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Response Processing

### Parse Human Response

```python
def parse_approval_response(message: str) -> dict:
    """
    Parse human's approval response.
    """
    message_upper = message.upper().strip()
    
    # Approve patterns
    if message_upper == 'APPROVE':
        return {
            'decision': 'approved',
            'publish_time': 'optimal',
            'feedback': None
        }
    
    if message_upper == 'APPROVE NOW':
        return {
            'decision': 'approved',
            'publish_time': 'immediate',
            'feedback': None
        }
    
    # Schedule pattern: SCHEDULE 3pm or SCHEDULE 2024-01-31 15:00
    schedule_match = re.match(r'SCHEDULE\s+(.+)', message_upper)
    if schedule_match:
        time_str = schedule_match.group(1)
        return {
            'decision': 'approved',
            'publish_time': parse_datetime(time_str),
            'feedback': None
        }
    
    # Revise pattern
    revise_match = re.match(r'REVISE[:\s]+(.+)', message, re.IGNORECASE)
    if revise_match:
        return {
            'decision': 'revise',
            'publish_time': None,
            'feedback': revise_match.group(1)
        }
    
    # Reject pattern
    reject_match = re.match(r'REJECT[:\s]+(.+)', message, re.IGNORECASE)
    if reject_match:
        return {
            'decision': 'rejected',
            'publish_time': None,
            'feedback': reject_match.group(1)
        }
    
    # Unclear response
    return {
        'decision': 'unclear',
        'publish_time': None,
        'feedback': message,
        'need_clarification': True
    }
```

---

## Approval States

```
┌─────────┐
│ CREATED │
└────┬────┘
     │
     ▼
┌─────────────┐
│ IN_REVIEW   │←─────────────────────┐
└──────┬──────┘                      │
       │                             │
       ▼                             │
┌─────────────────┐        ┌────────┴────────┐
│ PENDING_APPROVAL│───────►│    REVISE       │
└────────┬────────┘        └─────────────────┘
         │
    ┌────┴────┬──────────┐
    ▼         ▼          ▼
┌───────┐ ┌────────┐ ┌──────────┐
│APPROVED│ │REJECTED│ │ EXPIRED  │
└───┬───┘ └────────┘ └──────────┘
    │
    ▼
┌─────────┐
│PUBLISHED│
└─────────┘
```

---

## Batch Approval

For multiple content pieces (e.g., weekly calendar):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 BATCH APPROVAL: Week of Jan 31
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

7 pieces ready for approval:

1️⃣ Monday 9am - TikTok Video
   [Preview link] ✅ Checks passed

2️⃣ Monday 3pm - Instagram Reel  
   [Preview link] ✅ Checks passed

3️⃣ Tuesday 10am - TikTok Video
   [Preview link] ⚠️ 1 warning (mild language)

4️⃣ Wednesday 9am - Twitter Post
   [Preview link] ✅ Checks passed

5️⃣ Thursday 3pm - TikTok Video
   [Preview link] ✅ Checks passed

6️⃣ Friday 12pm - Instagram Carousel
   [Preview link] ✅ Checks passed

7️⃣ Saturday 7pm - TikTok Video
   [Preview link] ✅ Checks passed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reply:
• "APPROVE ALL" → Approve all 7 pieces
• "APPROVE 1,2,4,5,6,7" → Approve specific pieces
• "REVIEW 3" → Get details on piece #3
• "REJECT 3: [reason]" → Reject specific piece

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Approval SLAs

| Priority | Response Time | Auto-Action If No Response |
|----------|---------------|---------------------------|
| Critical | ASAP | Remind at 1h, 4h |
| High | 4 hours | Remind at 2h, escalate at 6h |
| Normal | 24 hours | Remind at 12h, expire at 72h |
| Low | 48 hours | Remind at 24h, expire at 7d |

### Reminder Flow

```
T+0:    Initial request sent
T+12h:  First reminder
T+24h:  Second reminder  
T+72h:  Request expires, content NOT published
```

---

## Audit Trail

Every approval decision logged:

```sql
INSERT INTO approval_log (
    approval_id,
    content_id,
    business_id,
    
    -- Request
    requested_at TIMESTAMP,
    requested_by STRING,  -- 'CMO' or agent
    content_type STRING,
    platform STRING,
    
    -- Content summary
    content_preview_url STRING,
    moderation_passed BOOL,
    warnings JSON,
    
    -- Decision
    decision STRING,  -- approved, rejected, revised, expired
    decided_at TIMESTAMP,
    decided_by STRING,  -- Human identifier
    feedback STRING,
    scheduled_time TIMESTAMP,
    
    -- Publication
    published_at TIMESTAMP,
    platform_post_id STRING,
    post_url STRING
) VALUES (...);
```

---

## Dashboard View

Human can review all pending approvals in dashboard:

```
┌──────────────────────────────────────────────────────────────────┐
│ 📋 PENDING APPROVALS                              [Filter ▼]     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌────────────────────────────────────────────────────────────┐  │
│ │ 🎬 TikTok Video                    Waiting 2h              │  │
│ │ Caption: "When you finally try..."                         │  │
│ │ ✅ All checks passed                                       │  │
│ │ [Preview] [Approve] [Revise] [Reject]                     │  │
│ └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│ ┌────────────────────────────────────────────────────────────┐  │
│ │ 📸 Instagram Carousel              Waiting 5h              │  │
│ │ Caption: "5 tips for better..."                            │  │
│ │ ⚠️ 1 warning: "Check FTC disclosure"                      │  │
│ │ [Preview] [Approve] [Revise] [Reject]                     │  │
│ └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│ ┌────────────────────────────────────────────────────────────┐  │
│ │ 🎨 Logo Concepts                   Waiting 1d              │  │
│ │ 5 concepts ready for selection                             │  │
│ │ 🔵 Requires GREENLIGHT: BRAND                              │  │
│ │ [Preview All] [Select] [Request More]                     │  │
│ └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│ [Approve All Checked] [Clear All]                               │
└──────────────────────────────────────────────────────────────────┘
```

---

## Emergency Override

If content must be published urgently:

**NOT SUPPORTED** - Human approval is mandatory.

The only exception is if human pre-approves a content type:
- "Approve all responses to comments for next 24h"
- "Approve scheduled content for this week"

These pre-approvals are logged and tracked.

---

## Integration Points

- **Telegram Bot**: Receives approval requests, sends decisions
- **Dashboard**: Visual approval interface
- **BigQuery**: Approval logging
- **Cloud Scheduler**: Scheduled publishing after approval
- **Platform APIs**: Actual publishing

---

*All external content requires explicit human approval before publication.*

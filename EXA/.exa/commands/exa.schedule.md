# exa.schedule

## Preamble

This command manages calendar scheduling for Human meetings with external parties.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `EXA/.ethics/ethics.md`

---

## Overview

EXA has:
- **READ** access to Human's calendar
- **REQUEST** ability (not direct write)
- Human confirms ALL calendar changes

---

## Command Types

```
exa.schedule request [meeting-details]    # Request new meeting
exa.schedule availability [date-range]    # Check Human's calendar
exa.schedule confirm [meeting-id]         # Confirm with external party
exa.schedule reschedule [meeting-id]      # Reschedule request
exa.schedule cancel [meeting-id]          # Cancel meeting
```

---

## Request: `exa.schedule request`

Request a new meeting on Human's calendar.

### Input

```yaml
meeting_type: investor_call
 
# External party
external_party:
  name: "Jane Smith"
  company: "Venture Capital Inc"
  email: "jane@vc.com"
  
# Details
subject: "Seed funding discussion"
duration: 30  # minutes
proposed_times:
  - "2024-02-01 10:00 EST"
  - "2024-02-01 14:00 EST"
  - "2024-02-02 11:00 EST"
  
# Context
briefing_agent: CFO  # Who should prep talking points
notes: "Follow-up from email introduction"
```

### Execution Flow

```
Meeting request received
        │
        ▼
Check Human's calendar for conflicts
        │
        ▼
Identify available slots
        │
        ▼
Send options to Human via Telegram
        │
        ▼
Human selects slot
        │
        ▼
EXA confirms with external party
        │
        ▼
EXA sends calendar invite
        │
        ▼
Notify briefing agent to prepare
```

---

## Approval Request (to Human)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 MEETING REQUEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REQUEST ID: MTG-2024-0131-001

WITH: Jane Smith
      Venture Capital Inc

SUBJECT: Seed funding discussion
DURATION: 30 minutes

TYPE: Investor Call
BRIEFING BY: CFO

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AVAILABLE SLOTS:

1️⃣ Thu Feb 1 @ 10:00 AM EST
2️⃣ Thu Feb 1 @ 2:00 PM EST
3️⃣ Fri Feb 2 @ 11:00 AM EST

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONTEXT:
Follow-up from email introduction

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reply with:
• "1" / "2" / "3" → Select that slot
• "OTHER [time]" → Propose different time
• "DECLINE [reason]" → Decline meeting

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Availability: `exa.schedule availability`

Check Human's calendar for availability.

### Input
```yaml
date_range:
  start: "2024-02-01"
  end: "2024-02-07"
duration_needed: 30  # minutes
time_preferences:
  - morning  # 9am-12pm
  - afternoon  # 1pm-5pm
timezone: "America/New_York"
```

### Output
```markdown
# Calendar Availability
Period: Feb 1-7, 2024
Duration needed: 30 minutes

## Available Slots

### Thursday Feb 1
- ✅ 10:00 AM - 10:30 AM
- ✅ 2:00 PM - 2:30 PM
- ✅ 3:30 PM - 4:00 PM

### Friday Feb 2
- ✅ 9:00 AM - 9:30 AM
- ✅ 11:00 AM - 11:30 AM

### Monday Feb 5
- ✅ 10:00 AM - 10:30 AM
- ✅ 1:00 PM - 1:30 PM
- ✅ 4:00 PM - 4:30 PM

## Busy Periods (context)
- Feb 1, 11am-1pm: Board meeting
- Feb 2, 2pm-5pm: Travel
- Feb 3-4: Weekend
- Feb 6-7: Conference
```

---

## Confirm: `exa.schedule confirm`

After Human approves, confirm with external party.

### Confirmation Email
```
Subject: Meeting Confirmed: [Subject] - [Date/Time]

Hello [Name],

This email confirms your meeting with [Human Name], 
[Title] of [Company].

MEETING DETAILS:
────────────────
Date: Thursday, February 1, 2024
Time: 10:00 AM EST (30 minutes)
Location: [Zoom Link / Phone / Address]

AGENDA:
- [Brief agenda based on meeting type]

Please let me know if you need to reschedule.

Best regards,
[Company Name]
hello@[company].com
```

### Calendar Invite

```
📅 Send Google Calendar invite:
- Title: [Subject] with [Human Name]
- Time: [Confirmed slot]
- Duration: [Duration]
- Location: [Meeting link or address]
- Attendees: [Human], [External party]
- Description: [Meeting context and agenda]
```

---

## Meeting Types

| Type | Prep Required | Duration | Briefing Agent |
|------|---------------|----------|----------------|
| `investor_call` | CFO brief | 30 min | CFO |
| `press_interview` | Talking points | 30-60 min | CMO |
| `customer_meeting` | Account summary | 30 min | COO |
| `partner_discussion` | Partnership analysis | 45 min | CEO |
| `legal_consultation` | Case summary | 60 min | CLO |
| `sales_demo` | Demo prep | 30 min | CMO |
| `job_interview` | Candidate summary | 45 min | COO |

---

## Briefing Request

After meeting confirmed, request briefing:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 BRIEFING REQUEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Meeting: Seed funding discussion
With: Jane Smith, Venture Capital Inc
When: Thu Feb 1 @ 10:00 AM EST

TYPE: Investor Call
HUMAN NEEDS: Briefing document

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CFO: Please prepare:
• Current financials summary
• Funding ask and use of funds
• Key metrics and growth
• Investor background research on VC Inc

Due: Wed Jan 31 @ 6:00 PM EST
(Day before meeting)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Reschedule: `exa.schedule reschedule`

Handle reschedule requests.

### Flow

```
Reschedule request (from Human or external)
        │
        ▼
Check new availability
        │
        ▼
Propose new times
        │
        ▼
Get confirmation from both parties
        │
        ▼
Update calendar
        │
        ▼
Send updated calendar invites
```

---

## Cancel: `exa.schedule cancel`

Cancel a scheduled meeting.

### Cancellation Email
```
Subject: Meeting Cancelled: [Subject] - [Date/Time]

Hello [Name],

Unfortunately, we need to cancel our scheduled meeting 
on [Date] at [Time].

[If rescheduling: We'd like to reschedule for a later 
date. Please let me know your availability for next week.]

[If not rescheduling: We'll be in touch when we can 
revisit this discussion.]

We apologize for any inconvenience.

Best regards,
[Company Name]
```

---

## Logging

All scheduling activity logged:

```sql
INSERT INTO scheduling_log (
    meeting_id,
    business_id,
    
    -- Meeting details
    subject STRING,
    meeting_type STRING,
    duration_minutes INT64,
    
    -- Parties
    external_name STRING,
    external_email STRING,
    external_company STRING,
    
    -- Timing
    requested_at TIMESTAMP,
    approved_at TIMESTAMP,
    scheduled_for TIMESTAMP,
    
    -- Status
    status STRING,  -- pending, confirmed, completed, cancelled, rescheduled
    
    -- Briefing
    briefing_agent STRING,
    briefing_delivered BOOL,
    
    -- Outcome
    meeting_held BOOL,
    notes STRING
) VALUES (...);
```

---

*Human's time is precious. Every meeting is confirmed, briefed, and logged.*

# exa.phone

## Preamble

This command handles all incoming phone calls through the single company phone number.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CXA/.ethics/ethics.md`
3. `CXA/.exa/memory/routing.md`

---

## Overview

Single company phone: `+1-XXX-XXX-XXXX`

- ALL calls come through this number
- CXA answers or voicemail captures
- Calls routed to COO call center or scheduled callbacks
- ALL calls logged to BigQuery

---

## Command Types

```
exa.phone answer [call-id]         # Answer incoming call
exa.phone route [call-id] [dest]   # Route call
exa.phone voicemail [call-id]      # Process voicemail
exa.phone callback [contact]       # Schedule callback
```

---

## Call Handling Flow

```
Incoming Call
      │
      ▼
┌─────────────────────────────────────────┐
│  ANSWER (AI or Human)                   │
│  "Thank you for calling [Company].      │
│   How may I direct your call?"          │
└────────────┬────────────────────────────┘
             │
             ▼
    ┌────────────────────┐
    │  Identify Caller   │
    │  & Purpose         │
    └────────┬───────────┘
             │
    ┌────────┴────────┬────────────┬────────────┐
    ▼                 ▼            ▼            ▼
┌─────────┐    ┌───────────┐ ┌──────────┐ ┌───────────┐
│ Support │    │ Sales/    │ │ Press/   │ │ Unknown/  │
│ Request │    │ Inquiry   │ │ Legal    │ │ Personal  │
└────┬────┘    └─────┬─────┘ └────┬─────┘ └─────┬─────┘
     │               │            │             │
     ▼               ▼            ▼             ▼
 COO Call        Take Msg      Urgent?      Take Msg
  Center        Route CMO    Y:Transfer    Review Later
                            N:Schedule
```

---

## Answer Script

### Initial Greeting
```
"Thank you for calling [Company Name]. 
My name is [AI Assistant Name]. 
How may I help you today?"
```

### Identifying Purpose
```
"I'd be happy to help with that. 
May I ask your name and company?"
```

### Routing Response
```
"Thank you, [Name]. Let me connect you 
with the right department. One moment please."
```

### If Unavailable
```
"I apologize, but [Person/Department] is currently 
unavailable. May I take a message and have them 
return your call?"
```

### Taking Message
```
"May I have:
- Your name?
- Your phone number?
- Best time to reach you?
- Brief description of what this is regarding?"
```

### Closing
```
"Thank you for calling [Company]. 
We'll be in touch within [timeframe]. 
Have a great day!"
```

---

## Routing Logic

```python
def route_call(caller_info: dict, purpose: str) -> dict:
    """
    Determine call routing.
    """
    purpose_lower = purpose.lower()
    
    # Check known contact
    contact = lookup_contact(caller_info.get('phone'))
    if contact:
        return {
            'action': 'transfer',
            'destination': contact.get('preferred_agent', 'COO'),
            'priority': contact.get('priority', 'normal')
        }
    
    # Emergency/Legal - immediate escalation
    if any(word in purpose_lower for word in ['legal', 'attorney', 'lawsuit', 'emergency']):
        return {
            'action': 'urgent_transfer',
            'destination': 'CLO',
            'priority': 'critical',
            'notify': ['CEO', 'HUMAN']
        }
    
    # Press/Media
    if any(word in purpose_lower for word in ['press', 'interview', 'reporter', 'journalist']):
        return {
            'action': 'message',
            'destination': 'CMO',
            'priority': 'high',
            'callback_sla': '1 hour'
        }
    
    # Technical Support
    if any(word in purpose_lower for word in ['support', 'help', 'problem', 'not working', 'bug']):
        return {
            'action': 'transfer',
            'destination': 'COO_CALL_CENTER',
            'priority': 'normal'
        }
    
    # Sales Inquiry
    if any(word in purpose_lower for word in ['pricing', 'demo', 'buy', 'purchase', 'interested']):
        return {
            'action': 'message',
            'destination': 'CMO',
            'priority': 'normal',
            'callback_sla': '4 hours'
        }
    
    # Default - take message
    return {
        'action': 'message',
        'destination': 'HUMAN',
        'priority': 'normal',
        'callback_sla': '24 hours'
    }
```

---

## COO Call Center Integration

Support calls are transferred to COO-managed call center:

```python
def transfer_to_call_center(call: dict) -> dict:
    """
    Warm transfer to COO call center.
    """
    # Attempt transfer
    transfer_result = twilio_transfer(
        call_sid=call['sid'],
        to=COO_CALL_CENTER_NUMBER,
        announcement="Transferring support call from [Caller Name]"
    )
    
    if transfer_result['success']:
        return {
            'status': 'transferred',
            'destination': 'COO Call Center',
            'call_sid': call['sid']
        }
    else:
        # Fallback to voicemail
        return take_voicemail(call, 'COO')
```

---

## Voicemail Processing

When calls go to voicemail:

```python
def process_voicemail(voicemail: dict) -> dict:
    """
    Process voicemail message.
    """
    # Transcribe voicemail
    transcript = transcribe_audio(voicemail['recording_url'])
    
    # Determine routing
    routing = route_call(
        caller_info={'phone': voicemail['from']},
        purpose=transcript
    )
    
    # Log and notify
    log_voicemail(voicemail, transcript, routing)
    
    # Notify appropriate agent
    notify_agent(
        agent=routing['destination'],
        message=f"""
📞 VOICEMAIL RECEIVED

From: {voicemail['from']}
Duration: {voicemail['duration']}s
Received: {voicemail['timestamp']}

TRANSCRIPT:
{transcript}

[Listen to Recording]

Callback SLA: {routing.get('callback_sla', '24 hours')}
"""
    )
    
    return routing
```

---

## Callback Scheduling

For messages requiring callback:

```python
def schedule_callback(contact: dict, priority: str) -> dict:
    """
    Schedule a callback.
    """
    sla_map = {
        'critical': timedelta(minutes=15),
        'high': timedelta(hours=1),
        'normal': timedelta(hours=4),
        'low': timedelta(hours=24)
    }
    
    callback = {
        'contact': contact,
        'due_by': datetime.now() + sla_map.get(priority, timedelta(hours=24)),
        'assigned_to': contact.get('routed_agent'),
        'status': 'pending'
    }
    
    # Add to callback queue
    add_to_callback_queue(callback)
    
    # Send reminder at 50% of SLA
    schedule_reminder(
        time=callback['due_by'] - (sla_map[priority] / 2),
        message=f"Callback due in {sla_map[priority]/2} to {contact['name']}"
    )
    
    return callback
```

---

## Call Logging

Every call logged:

```sql
INSERT INTO call_log (
    call_id,
    business_id,
    
    -- Call details
    direction STRING,  -- inbound, outbound, callback
    caller_phone STRING,
    caller_name STRING,
    caller_company STRING,
    
    -- Timing
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    duration_seconds INT64,
    
    -- Handling
    answered BOOL,
    answered_by STRING,  -- ai, human, voicemail
    routing_decision STRING,
    routed_to STRING,
    
    -- Outcome
    outcome STRING,  -- transferred, message, voicemail, callback_scheduled
    
    -- Voicemail
    voicemail_url STRING,
    voicemail_transcript STRING,
    
    -- Callback
    callback_scheduled BOOL,
    callback_due TIMESTAMP,
    callback_completed TIMESTAMP
) VALUES (...);
```

---

## Sales Call Blocking

Politely decline unsolicited sales calls:

```
"Thank you for your interest, but we're not taking 
unsolicited sales calls at this time. 

If you'd like to submit information, please email 
hello@[company].com and we'll review it.

Thank you for understanding."
```

---

## Working Hours

| Day | Hours (EST) | After-Hours Action |
|-----|-------------|-------------------|
| Mon-Fri | 9am - 6pm | Voicemail |
| Saturday | N/A | Voicemail |
| Sunday | N/A | Voicemail |

After-hours voicemail message:
```
"Thank you for calling [Company]. Our office is currently 
closed. Please leave a message with your name, number, 
and reason for calling, and we'll return your call 
during business hours. For urgent matters, please 
email hello@[company].com with URGENT in the subject."
```

---

*One phone number. Professional handling. Every call logged.*

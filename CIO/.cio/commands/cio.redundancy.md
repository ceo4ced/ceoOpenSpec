# cio.redundancy

## Preamble

The CIO ensures redundancy for all critical services.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CIO/.ethics/ethics.md`
3. `.architecture/observability.md`

---

## Overview

> **If a service can fail, it will fail. Plan for failure.**

The CIO is responsible for ensuring no single point of failure exists in the business infrastructure.

---

## Command Types

```
cio.redundancy audit                    # Audit all services for SPOF
cio.redundancy plan [service]           # Create redundancy plan
cio.redundancy failover test [service]  # Test failover
cio.redundancy status                   # Current redundancy status
```

---

## Redundancy Categories

### Tier 1: Critical (Zero Downtime)
Must have automatic failover with <1 minute RTO.

| Service | Primary | Secondary | Tertiary |
|---------|---------|-----------|----------|
| LLM API | OpenRouter | Direct Claude API | Direct GPT API |
| Database | Cloud SQL (Primary) | Cloud SQL (Read Replica) | Point-in-time recovery |
| Authentication | Google SSO | Emergency bypass tokens | Manual verification |
| Human Communication | Telegram | Email | SMS |

### Tier 2: Important (Minimal Downtime)
Should have failover with <15 minute RTO.

| Service | Primary | Failover |
|---------|---------|----------|
| BigQuery Logging | us-central1 | Multi-region dataset |
| Cloud Functions | us-central1 | us-east1 |
| Pub/Sub | GCP | Stored fallback queue |
| Email (CXA) | Gmail API | SMTP fallback |
| Phone (CXA) | Twilio | Backup provider |

### Tier 3: Standard (Recoverable)
Can tolerate temporary outage, <4 hour RTO.

| Service | Primary | Recovery Method |
|---------|---------|-----------------|
| Dashboard | Cloud Run | Redeploy from container |
| MCP Servers | Various | Restart/reconnect |
| Calendar | Google Calendar | Manual scheduling |

---

## Redundancy Audit

```python
def audit_redundancy() -> dict:
    """
    Audit all services for single points of failure.
    """
    services = get_all_services()
    results = []
    
    for service in services:
        redundancy = check_redundancy(service)
        
        result = {
            'service': service.name,
            'tier': service.tier,
            'has_failover': redundancy.has_failover,
            'failover_tested': redundancy.last_test_date,
            'rto_target': service.rto_target,
            'rto_achieved': redundancy.measured_rto,
            'spof_risk': not redundancy.has_failover,
            'issues': []
        }
        
        # Check for issues
        if not redundancy.has_failover:
            result['issues'].append('NO_FAILOVER')
        if redundancy.last_test_date < days_ago(90):
            result['issues'].append('TEST_OVERDUE')
        if redundancy.measured_rto > service.rto_target:
            result['issues'].append('RTO_EXCEEDED')
            
        results.append(result)
    
    return {
        'audit_date': datetime.now(),
        'services_audited': len(results),
        'spof_count': sum(1 for r in results if r['spof_risk']),
        'results': results
    }
```

### Audit Report Format

```markdown
# Redundancy Audit Report
Date: 2024-01-31

## Summary
- Services Audited: 15
- Single Points of Failure: 1 🔴
- Failover Tests Overdue: 2 🟡
- RTO Targets Met: 12/15

## Critical Issues (Tier 1)

### 🔴 LLM API Failover
Issue: Tertiary fallback not configured
Risk: If OpenRouter AND Direct Claude fail, no AI capability
Action: Configure GPT-4 as tertiary by Feb 5

## Warnings (Tier 2)

### 🟡 Email Service
Issue: Failover test overdue (120 days)
Action: Schedule SMTP failover test this week

## All Services Status

| Service | Tier | Failover | Last Test | RTO |
|---------|------|----------|-----------|-----|
| LLM API | 1 | ⚠️ Partial | Jan 15 | <1m |
| Database | 1 | ✅ Yes | Jan 20 | <1m |
| BigQuery | 2 | ✅ Yes | Dec 15 | <15m |
```

---

## Failover Configurations

### LLM API Failover

```yaml
llm_failover:
  primary:
    provider: openrouter
    endpoint: https://openrouter.ai/api/v1
    api_key_secret: openrouter-api-key
    
  secondary:
    provider: anthropic
    endpoint: https://api.anthropic.com/v1
    api_key_secret: anthropic-api-key
    
  tertiary:
    provider: openai
    endpoint: https://api.openai.com/v1
    api_key_secret: openai-api-key
    
  failover_rules:
    - condition: "response_time > 30s OR error_rate > 5%"
      action: switch_to_secondary
    - condition: "secondary_error_rate > 5%"
      action: switch_to_tertiary
    - condition: "primary_healthy for 5m"
      action: revert_to_primary
```

### Database Failover

```yaml
database_failover:
  primary:
    instance: prod-db-primary
    region: us-central1
    
  secondary:
    instance: prod-db-replica
    region: us-east1
    type: read_replica
    promotion_time: 60s  # To primary if needed
    
  backup:
    type: point_in_time
    retention: 30_days
    recovery_time: 15m
```

### Communication Failover

```yaml
communication_failover:
  human_channel:
    primary: telegram
    secondary: email
    tertiary: sms
    
    rules:
      - if: "telegram_unreachable for 5m"
        then: switch_to_email
      - if: "email_unreachable for 15m"
        then: switch_to_sms
      - if: "all_unreachable"
        then: hold_and_retry
```

---

## Failover Testing

### Monthly Tests

```python
def run_failover_test(service: str) -> dict:
    """
    Test failover for a service.
    ONLY in staging unless production test approved by Human.
    """
    test = {
        'service': service,
        'test_date': datetime.now(),
        'environment': 'staging',  # Default to staging
        'steps': [],
        'passed': True
    }
    
    # Step 1: Verify primary healthy
    test['steps'].append({
        'step': 'verify_primary_healthy',
        'result': check_health(service, 'primary')
    })
    
    # Step 2: Simulate primary failure
    test['steps'].append({
        'step': 'simulate_failure',
        'result': block_primary(service)
    })
    
    # Step 3: Verify automatic failover
    start = time.time()
    failover_result = wait_for_failover(service, timeout=60)
    failover_time = time.time() - start
    
    test['steps'].append({
        'step': 'verify_failover',
        'result': failover_result,
        'time_seconds': failover_time
    })
    
    # Step 4: Verify service continues
    test['steps'].append({
        'step': 'verify_continuity',
        'result': test_service_operation(service)
    })
    
    # Step 5: Restore primary
    test['steps'].append({
        'step': 'restore_primary',
        'result': unblock_primary(service)
    })
    
    # Step 6: Verify automatic failback
    test['steps'].append({
        'step': 'verify_failback',
        'result': wait_for_failback(service, timeout=300)
    })
    
    test['passed'] = all(s['result']['success'] for s in test['steps'])
    test['failover_time_seconds'] = failover_time
    
    # Log to BigQuery
    log_to_bigquery('failover_tests', test)
    
    return test
```

---

## Status Dashboard

```sql
-- Current redundancy status
SELECT 
  service_name,
  tier,
  has_failover,
  failover_type,
  last_test_date,
  last_test_passed,
  TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), last_test_date, DAY) as days_since_test,
  rto_target_seconds,
  last_measured_rto_seconds,
  CASE 
    WHEN last_measured_rto_seconds > rto_target_seconds THEN 'EXCEEDED'
    ELSE 'MET'
  END as rto_status
FROM redundancy_status
WHERE business_id = @business_id
ORDER BY tier, service_name;
```

---

## Escalation

| Condition | Action |
|-----------|--------|
| Tier 1 SPOF detected | 🔴 RED PHONE to Human |
| Failover test fails | Alert CIO + CEO |
| RTO exceeded in production | Alert CIO + CFO (cost impact) |
| Multiple Tier 2 failures | Escalate to CEO |

---

*No single point of failure. Test regularly. Trust but verify.*

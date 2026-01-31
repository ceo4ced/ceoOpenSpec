# cto.backups

## Preamble

The CTO ensures comprehensive backup coverage for all data and systems.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CTO/.ethics/ethics.md`
3. `.architecture/logging.md`

---

## Overview

> **Data not backed up doesn't exist. Backups not tested don't work.**

The CTO is responsible for ensuring all critical data has verified, recoverable backups.

---

## Command Types

```
cto.backups audit                     # Audit backup coverage
cto.backups status                    # Current backup status
cto.backups test [system]             # Test backup restoration
cto.backups schedule                  # View/modify backup schedule
cto.backups restore [backup-id]       # Initiate restoration
```

---

## Backup Categories

### Category A: Business Critical Data
Must have multiple backup copies with point-in-time recovery.

| Data | Backup Frequency | Retention | Recovery Test |
|------|------------------|-----------|---------------|
| BigQuery logs | Continuous + daily export | 7 years | Quarterly |
| Financial records | Real-time sync + daily | 7 years | Monthly |
| Contracts/legal | On change + daily | Permanent | Quarterly |
| User data | Hourly + daily | Per policy | Monthly |

### Category B: Operational Data
Daily backups with weekly verification.

| Data | Backup Frequency | Retention | Recovery Test |
|------|------------------|-----------|---------------|
| Configuration | On change | 90 days | Monthly |
| Agent memory files | Daily | 30 days | Monthly |
| Contact database | Hourly | 1 year | Weekly |
| Calendar data | On change | 1 year | Monthly |

### Category C: Development Assets
Regular backups with version control.

| Data | Backup Frequency | Retention | Recovery Test |
|------|------------------|-----------|---------------|
| Code repositories | Continuous (Git) | Permanent | N/A |
| Infrastructure config | On change | 1 year | Quarterly |
| Documentation | Daily | 1 year | Quarterly |

---

## Backup Architecture

### 3-2-1 Rule

```
3 copies of all critical data
2 different storage types
1 copy offsite (different region/provider)
```

### Implementation

```yaml
backup_architecture:
  primary_storage:
    provider: gcp
    region: us-central1
    type: cloud_storage
    
  secondary_storage:
    provider: gcp
    region: us-east1
    type: cloud_storage
    replication: cross_region
    
  tertiary_storage:
    provider: aws  # Different provider
    region: us-west-2
    type: s3
    sync: daily
    
  encryption:
    at_rest: AES-256
    in_transit: TLS 1.3
    key_management: cloud_kms
```

---

## Backup Schedules

### BigQuery Export

```python
def backup_bigquery_table(table: str) -> dict:
    """
    Export BigQuery table to Cloud Storage.
    Runs daily for all tables.
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    destination = f"gs://{BACKUP_BUCKET}/bigquery/{table}/{timestamp}/"
    
    job_config = bigquery.ExtractJobConfig(
        destination_format='AVRO',
        compression='SNAPPY'
    )
    
    job = client.extract_table(
        f"{PROJECT}.{DATASET}.{table}",
        destination,
        job_config=job_config
    )
    
    job.result()  # Wait for completion
    
    # Verify backup
    files = list_bucket_files(destination)
    size = sum(f.size for f in files)
    
    backup_record = {
        'backup_id': generate_uuid(),
        'table': table,
        'destination': destination,
        'timestamp': timestamp,
        'file_count': len(files),
        'total_size_bytes': size,
        'verified': True
    }
    
    log_to_bigquery('backup_logs', backup_record)
    return backup_record
```

### Database Backup

```yaml
cloud_sql_backup:
  automated_backups:
    enabled: true
    start_time: "02:00"  # 2 AM
    location: us-central1
    retention_days: 30
    
  point_in_time_recovery:
    enabled: true
    retention_days: 7
    
  on_demand_backup:
    trigger: before_major_changes
    retention: 90_days
```

### File System Backup

```yaml
cloud_storage_backup:
  versioning:
    enabled: true
    retention: 30_versions
    
  lifecycle:
    - action: delete
      condition:
        age: 365
        is_live: false
        
  cross_region_replication:
    enabled: true
    destination: us-east1
```

---

## Backup Testing

### Monthly Recovery Test

```python
def test_backup_recovery(backup_type: str) -> dict:
    """
    Test backup by restoring to staging environment.
    """
    test = {
        'test_id': generate_uuid(),
        'backup_type': backup_type,
        'test_date': datetime.now(),
        'steps': [],
        'passed': False
    }
    
    # Step 1: Select recent backup
    backup = get_latest_backup(backup_type)
    test['steps'].append({
        'step': 'select_backup',
        'backup_id': backup.id,
        'backup_date': backup.timestamp
    })
    
    # Step 2: Restore to staging
    staging_location = f"staging_{backup_type}_{test['test_id']}"
    restore_result = restore_backup(backup, staging_location)
    test['steps'].append({
        'step': 'restore',
        'location': staging_location,
        'success': restore_result.success,
        'duration_seconds': restore_result.duration
    })
    
    # Step 3: Verify data integrity
    verification = verify_restored_data(
        original=backup.source,
        restored=staging_location
    )
    test['steps'].append({
        'step': 'verify_integrity',
        'checksums_match': verification.checksums_match,
        'row_counts_match': verification.row_counts_match,
        'sample_data_valid': verification.sample_valid
    })
    
    # Step 4: Cleanup staging
    cleanup_result = delete_staging_restore(staging_location)
    test['steps'].append({
        'step': 'cleanup',
        'success': cleanup_result.success
    })
    
    test['passed'] = all(
        s.get('success', True) and 
        s.get('checksums_match', True) 
        for s in test['steps']
    )
    
    # Log result
    log_to_bigquery('backup_tests', test)
    
    # Alert if failed
    if not test['passed']:
        escalate('CEO', f"Backup test FAILED for {backup_type}")
    
    return test
```

---

## Backup Status Dashboard

```sql
-- Current backup status
SELECT 
  data_category,
  backup_type,
  last_backup_time,
  TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), last_backup_time, HOUR) as hours_since_backup,
  last_backup_size_bytes,
  last_test_date,
  last_test_passed,
  CASE 
    WHEN TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), last_backup_time, HOUR) > 24 THEN 'OVERDUE'
    WHEN last_test_passed = false THEN 'FAILED_TEST'
    ELSE 'HEALTHY'
  END as status
FROM backup_status
WHERE business_id = @business_id
ORDER BY data_category, backup_type;
```

---

## Disaster Recovery

### RPO (Recovery Point Objective)

| Category | RPO | Meaning |
|----------|-----|---------|
| A | 1 hour | Lose at most 1 hour of data |
| B | 24 hours | Lose at most 1 day of data |
| C | 7 days | Lose at most 1 week of data |

### RTO (Recovery Time Objective)

| Category | RTO | Meaning |
|----------|-----|---------|
| A | 4 hours | Restore within 4 hours |
| B | 24 hours | Restore within 1 day |
| C | 72 hours | Restore within 3 days |

### Disaster Recovery Runbook

```markdown
# DR Runbook

## Scenario: Complete Data Loss

1. **Assess impact**
   - Which systems affected?
   - Last known good backup?

2. **Notify stakeholders**
   - Human (RED PHONE)
   - All C-suite (CEO broadcasts)

3. **Begin recovery**
   - Start with Category A data
   - Use most recent verified backup

4. **Verify integrity**
   - Run checksums
   - Sample data verification

5. **Restore operations**
   - Bring systems online in priority order
   - Monitor for issues

6. **Post-incident review**
   - Document cause
   - Update procedures
```

---

## Escalation

| Condition | Action |
|-----------|--------|
| No backup for 24h (Cat A) | 🔴 RED PHONE |
| Backup test fails | Alert CTO + CEO |
| No backup for 48h (Cat B) | Alert CTO + CIO |
| Recovery takes longer than RTO | Escalate to CEO |

---

*Everything backed up. Everything tested. Everything recoverable.*

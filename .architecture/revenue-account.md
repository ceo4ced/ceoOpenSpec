# Revenue Account Access

## Overview

Agents have **READ-ONLY** access to the revenue account.

This allows visibility into deposits without any transfer or modification capability.

---

## Account Configuration

```yaml
revenue_account:
  name: "Business Operating Account"
  bank: "[Bank Name]"
  account_type: "Business Checking"
  
  # API Access (Read-Only)
  api_provider: plaid  # or bank-specific API
  access_level: READ_ONLY
  
  # Credentials (Secret Manager)
  secret_path: projects/{project}/secrets/bank-read-access/versions/latest
```

---

## What Agents Can See

| Data Point | Access |
|------------|--------|
| Current balance | ✅ Yes |
| Recent transactions | ✅ Yes |
| Deposit notifications | ✅ Yes |
| Transaction history | ✅ Yes |
| Account statements | ✅ Yes |

## What Agents CANNOT Do

| Action | Access |
|--------|--------|
| Transfer funds | ❌ No |
| Make payments | ❌ No |
| Modify account | ❌ No |
| Add payees | ❌ No |
| Request cards | ❌ No |
| Close account | ❌ No |

---

## Agent Access Matrix

| Agent | Revenue Visibility | Purpose |
|-------|-------------------|---------|
| CEO | Balance, trends | Strategic overview |
| CFO | Full access (read) | Financial reporting |
| CXA | Deposit notifications | Alert CFO of revenue |
| COO | None | Not needed |
| CMO | None | Not needed |
| CIO | None | Not needed |
| CLO | None | Not needed |
| CPO | None | Not needed |
| CTO | None | Not needed |

---

## Deposit Notification Flow

```
Bank receives deposit
        ↓
Bank API triggers webhook
        ↓
Cloud Function receives notification
        ↓
CXA logs deposit to BigQuery
        ↓
CXA notifies CFO
        ↓
CFO updates budget status
        ↓
Human receives daily summary
```

---

## BigQuery Logging

All revenue data logged:

```sql
CREATE TABLE IF NOT EXISTS revenue_transactions (
    transaction_id STRING NOT NULL,
    business_id STRING NOT NULL,
    
    -- Transaction
    transaction_date DATE,
    transaction_time TIMESTAMP,
    amount FLOAT64,
    type STRING,  -- deposit, refund, fee, etc.
    description STRING,
    
    -- Source
    payer_name STRING,
    payer_reference STRING,  -- Invoice #, etc.
    
    -- Balance
    balance_after FLOAT64,
    
    -- Notification
    notified_at TIMESTAMP,
    notified_to ARRAY<STRING>,  -- CFO, CEO, etc.
    
    -- Meta
    logged_at TIMESTAMP
);
```

---

## Security

### API Credentials
- Stored in GCP Secret Manager
- Read-only scoped tokens only
- Rotated every 90 days
- Audit logged

### Monitoring
- All API calls logged
- Unusual access patterns flagged
- Human notified of any anomalies

---

## Separation from Credit Card

The revenue account is **separate** from the credit card used for expenses.

| Account | Purpose | Owner |
|---------|---------|-------|
| Revenue Account | Deposit customer payments | READ-ONLY |
| Credit Card (****4242) | Business expenses | CFO spend control |

Funds do NOT automatically transfer from revenue to credit card.
Human controls when to pay credit card from revenue.

---

*Revenue visible for reporting. Spending controlled separately via CFO.*

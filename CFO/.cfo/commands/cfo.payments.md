# cfo.payments

## Preamble

The CFO manages payment processing and expense tracking.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CFO/.ethics/ethics.md`
3. `.architecture/revenue-account.md`

---

## Overview

> **One credit card. One payment processor. Full visibility.**

The CFO handles:
- Single credit card management
- Payment processing (Stripe)
- Invoice generation
- Expense categorization
- Tax calculation integration
- Accounting software sync

---

## Command Types

```
cfo.payments status                 # Current payment status
cfo.payments invoice [action]       # Invoice management
cfo.payments expense [action]       # Expense tracking
cfo.payments reconcile              # Reconciliation
cfo.payments report                 # Financial reports
```

---

## Single Credit Card Policy

```yaml
company_credit_card:
  card_ending: "****4242"
  provider: "Card Provider"
  monthly_limit: 10000  # Set by Human
  
  # Usage rules
  authorized_uses:
    - OpenRouter API charges
    - Cloud infrastructure (GCP)
    - SaaS subscriptions
    - Marketing spend (CMO approved)
    - Legal services (CLO approved)
    
  prohibited_uses:
    - Personal expenses
    - Unbudgeted purchases
    - Hardware without approval
    - Travel without approval
    
  # Approval thresholds
  auto_approve_under: 100   # Auto-approve < $100
  cfo_approve_under: 1000   # CFO approves $100-$1000
  human_required_over: 1000 # Human approves > $1000
```

---

## Payment Processing (Stripe)

### Configuration

```yaml
stripe:
  mode: production  # or test
  secret_key_secret: projects/{project}/secrets/stripe-secret-key
  publishable_key: pk_live_...
  webhook_secret: whsec_...
  
  products:
    - name: "Subscription"
      price_id: price_xxx
      type: recurring
```

### Invoice Generation

```python
def create_invoice(customer: dict, line_items: list) -> dict:
    """
    Create and send invoice via Stripe.
    """
    # Create Stripe invoice
    invoice = stripe.Invoice.create(
        customer=customer['stripe_id'],
        collection_method='send_invoice',
        days_until_due=30,
        auto_advance=True
    )
    
    # Add line items
    for item in line_items:
        stripe.InvoiceItem.create(
            customer=customer['stripe_id'],
            invoice=invoice.id,
            description=item['description'],
            amount=int(item['amount'] * 100),  # Cents
            currency='usd'
        )
    
    # Finalize and send
    invoice = stripe.Invoice.finalize_invoice(invoice.id)
    stripe.Invoice.send_invoice(invoice.id)
    
    # Log to BigQuery
    log_to_bigquery('invoices', {
        'invoice_id': invoice.id,
        'customer_id': customer['id'],
        'amount': invoice.amount_due / 100,
        'status': invoice.status,
        'created_at': datetime.now(),
        'due_date': invoice.due_date
    })
    
    return {
        'invoice_id': invoice.id,
        'invoice_url': invoice.hosted_invoice_url,
        'amount': invoice.amount_due / 100
    }
```

### Payment Webhooks

```python
async def handle_stripe_webhook(event: dict):
    """
    Handle incoming Stripe webhooks.
    """
    event_type = event['type']
    
    if event_type == 'invoice.paid':
        invoice = event['data']['object']
        await record_payment({
            'invoice_id': invoice['id'],
            'amount': invoice['amount_paid'] / 100,
            'paid_at': datetime.now()
        })
        # Notify EXA to log revenue
        await notify_exa_revenue(invoice)
        
    elif event_type == 'invoice.payment_failed':
        invoice = event['data']['object']
        await handle_failed_payment(invoice)
        # Escalate if significant amount
        if invoice['amount_due'] > 100000:  # $1000+
            escalate('CEO', f"Payment failed for ${invoice['amount_due']/100}")
            
    elif event_type == 'customer.subscription.deleted':
        # Handle churn
        await record_churn(event['data']['object'])
```

---

## Expense Categorization

### Categories

| Category | Description | Budget % |
|----------|-------------|----------|
| `ai_compute` | OpenRouter, LLM APIs | 30% |
| `infrastructure` | GCP, AWS | 25% |
| `software` | SaaS subscriptions | 15% |
| `marketing` | Ads, content | 15% |
| `legal` | Legal services | 5% |
| `other` | Miscellaneous | 10% |

### Auto-Categorization

```python
def categorize_expense(transaction: dict) -> str:
    """
    Auto-categorize credit card transactions.
    """
    merchant = transaction['merchant_name'].lower()
    
    categories = {
        'openrouter': 'ai_compute',
        'anthropic': 'ai_compute',
        'openai': 'ai_compute',
        'google cloud': 'infrastructure',
        'aws': 'infrastructure',
        'stripe': 'payment_processing',
        'slack': 'software',
        'notion': 'software',
        'github': 'software',
        'google workspace': 'software',
        'meta ads': 'marketing',
        'google ads': 'marketing',
        'tiktok': 'marketing',
    }
    
    for keyword, category in categories.items():
        if keyword in merchant:
            return category
    
    return 'other'  # Manual review needed
```

---

## Tax Calculation

### Sales Tax (Nexus)

```yaml
sales_tax_nexus:
  # States where we have sales tax obligation
  states:
    california:
      rate: 0.0725  # Base rate, varies by county
      collect: true
    new_york:
      rate: 0.08
      collect: true
    texas:
      rate: 0.0625
      collect: true
    # Add states as nexus established
```

### Tax Integration

```python
def calculate_tax(order: dict) -> dict:
    """
    Calculate sales tax for order.
    """
    # Check if taxable
    if not order.get('taxable', True):
        return {'tax_amount': 0, 'tax_rate': 0}
    
    customer_state = order['shipping_address']['state']
    
    if customer_state in NEXUS_STATES:
        rate = get_tax_rate(customer_state, order['shipping_address']['zip'])
        tax_amount = order['subtotal'] * rate
        return {
            'tax_amount': round(tax_amount, 2),
            'tax_rate': rate,
            'jurisdiction': customer_state
        }
    
    return {'tax_amount': 0, 'tax_rate': 0}
```

---

## Accounting Integration

### QuickBooks Sync

```yaml
quickbooks:
  enabled: true
  sync_frequency: daily
  
  mappings:
    # Stripe to QB account mapping
    revenue:
      stripe_invoice_paid: "4000 - Sales Revenue"
    expenses:
      ai_compute: "5100 - API Costs"
      infrastructure: "5200 - Cloud Infrastructure"
      software: "5300 - Software Subscriptions"
      marketing: "5400 - Marketing Expense"
      legal: "5500 - Professional Services"
```

### Sync Process

```python
async def sync_to_accounting():
    """
    Daily sync to QuickBooks.
    """
    # Get transactions since last sync
    transactions = await get_new_transactions()
    
    for tx in transactions:
        # Map to QB account
        account = get_qb_account(tx['category'])
        
        # Create journal entry
        await create_qb_entry({
            'date': tx['date'],
            'account': account,
            'amount': tx['amount'],
            'description': tx['description'],
            'reference': tx['transaction_id']
        })
    
    # Update sync timestamp
    await update_last_sync()
    
    # Log
    log_to_bigquery('accounting_syncs', {
        'synced_at': datetime.now(),
        'transactions_synced': len(transactions)
    })
```

---

## Expense Approval Workflow

```
Expense incurred (auto from credit card)
        ↓
Auto-categorize
        ↓
Under $100? → Auto-approve, log
        ↓
$100-$1000? → CFO review queue
        ↓
Over $1000? → Human approval required
        ↓
Approved → Sync to accounting
```

---

## Reporting

### Monthly Financial Report

```sql
SELECT 
  DATE_TRUNC(created_at, MONTH) as month,
  
  -- Revenue
  SUM(CASE WHEN type = 'revenue' THEN amount ELSE 0 END) as revenue,
  
  -- Expenses by category
  SUM(CASE WHEN category = 'ai_compute' THEN amount ELSE 0 END) as ai_costs,
  SUM(CASE WHEN category = 'infrastructure' THEN amount ELSE 0 END) as infra_costs,
  SUM(CASE WHEN category = 'software' THEN amount ELSE 0 END) as software_costs,
  SUM(CASE WHEN category = 'marketing' THEN amount ELSE 0 END) as marketing_costs,
  
  -- Totals
  SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expenses,
  
  -- Net
  SUM(CASE WHEN type = 'revenue' THEN amount ELSE 0 END) - 
  SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as net
  
FROM transactions
WHERE business_id = @business_id
GROUP BY month
ORDER BY month DESC;
```

---

## Logging

All financial transactions logged:

```sql
INSERT INTO transactions (
    transaction_id,
    business_id,
    
    type,  -- revenue, expense
    category,
    
    amount,
    currency,
    
    description,
    merchant,
    
    payment_method,
    stripe_id,
    
    approved_by,
    approved_at,
    
    synced_to_accounting,
    accounting_id,
    
    created_at
) VALUES (...);
```

---

*Every dollar tracked. Every expense categorized. Full financial transparency.*

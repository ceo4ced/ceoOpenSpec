# coo.logistics

## Preamble

This command creates logistics and supply chain planning for businesses that involve physical products or services.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `COO/.ethics/ethics.md`
3. `CEO/.ceo/memory/business-plan.md` (if exists)

---

## Outline

Design logistics framework for delivering products or services.

### Logistics Plan Template

```markdown
# Logistics Plan: [Business Name]
Generated: [Date]
Business Type: [Product/Service/Hybrid]

## Executive Summary
[Overview of logistics strategy]

---

## Product/Service Flow

### For Physical Products
```
[Supplier] → [Inventory] → [Fulfillment] → [Shipping] → [Customer]
                              ↓
                         [Returns]
```

### For Digital Products
```
[Development] → [Hosting] → [Delivery] → [Customer]
                               ↓
                          [Support]
```

### For Services
```
[Scheduling] → [Resource Allocation] → [Delivery] → [Customer]
                                          ↓
                                    [Follow-up]
```

---

## Supplier Management

### Key Suppliers
| Supplier | What They Provide | Lead Time | Alt Supplier |
|----------|-------------------|-----------|--------------|
| [Name] | [Product/Service] | X days | [Backup] |

### Supplier Criteria
| Criterion | Weight | [Supplier A] | [Supplier B] |
|-----------|--------|--------------|--------------|
| Quality | 30% | X/10 | X/10 |
| Price | 25% | X/10 | X/10 |
| Reliability | 25% | X/10 | X/10 |
| Lead Time | 20% | X/10 | X/10 |
| **Total** | 100% | X/10 | X/10 |

---

## Inventory Management

### Inventory Policy
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Reorder Point | X units | Based on lead time + safety stock |
| Safety Stock | X units | X days of average demand |
| Order Quantity | X units | Based on EOQ or supplier minimums |
| Max Inventory | X units | Storage/cash constraints |

### Inventory Tracking
| Method | Tool | Notes |
|--------|------|-------|
| Manual | Spreadsheet | Early stage |
| Barcode | [Tool name] | When scaling |
| RFID | [Tool name] | High volume |

---

## Fulfillment

### Fulfillment Options
| Option | Pros | Cons | Cost |
|--------|------|------|------|
| In-house | Control, speed | Space, staff | $X/order |
| 3PL | Scalable | Less control | $X/order |
| Dropship | No inventory | Margins | % of sale |

### Recommended: [Option]
**Rationale:** [Why this option fits]

### Fulfillment SLA
| Metric | Target | Measurement |
|--------|--------|-------------|
| Order to Ship | X hours | Timestamp difference |
| Shipping Time | X days | Carrier transit |
| Order Accuracy | X% | Orders correct / Total |
| Damage Rate | <X% | Damaged / Total |

---

## Shipping

### Carrier Options
| Carrier | Service | Cost | Speed | Tracking |
|---------|---------|------|-------|----------|
| USPS | Priority | $X | X days | Yes |
| UPS | Ground | $X | X days | Yes |
| FedEx | Express | $X | X days | Yes |
| [Regional] | [Service] | $X | X days | [Y/N] |

### Shipping Zones
| Zone | Coverage | Typical Transit | Cost |
|------|----------|-----------------|------|
| Local | [Radius] | X days | $X |
| Regional | [States] | X days | $X |
| National | USA | X days | $X |
| International | [Countries] | X days | $X |

---

## Returns & Reverse Logistics

### Return Policy
| Condition | Allowed | Timeframe | Refund Type |
|-----------|---------|-----------|-------------|
| Defective | Yes | X days | Full |
| Wrong item | Yes | X days | Full + shipping |
| Change of mind | [Y/N] | X days | [Full/Partial/Store credit] |

### Return Process
```
Customer requests return
         ↓
Return authorized (RMA)
         ↓
Customer ships item
         ↓
Item received and inspected
         ↓
Refund/replacement issued
```

---

## Capacity Planning

### Current Capacity
| Resource | Capacity | Current Use | Headroom |
|----------|----------|-------------|----------|
| Warehouse space | X sq ft | X sq ft | X% |
| Daily orders | X orders | X orders | X% |
| Staff hours | X hours | X hours | X% |

### Scale Triggers
| When we hit... | We need to... | Lead time |
|----------------|---------------|-----------|
| 80% warehouse | Expand/relocate | X months |
| 80% order capacity | Add staff or automate | X weeks |
| 50% margin erosion | Renegotiate suppliers | X months |

---

## Technology Stack

| Function | Tool | Cost | Integration |
|----------|------|------|-------------|
| Inventory | [Tool] | $X/mo | [Systems] |
| Order Management | [Tool] | $X/mo | [Systems] |
| Shipping | [Tool/API] | $X/mo | [Systems] |
| Analytics | [Tool] | $X/mo | [Systems] |

---

## Key Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Order Accuracy | >99% | X% | 🟢/🟡/🔴 |
| On-Time Delivery | >95% | X% | 🟢/🟡/🔴 |
| Inventory Turnover | X turns/year | X | 🟢/🟡/🔴 |
| Cost per Order | <$X | $X | 🟢/🟡/🔴 |
| Return Rate | <X% | X% | 🟢/🟡/🔴 |

---

## Risk Management

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Supplier failure | Low | High | Multiple suppliers |
| Shipping delays | Medium | Medium | Buffer stock |
| Demand spike | Medium | Medium | Flexible capacity |
| Quality issues | Low | High | QC process |

---

## Escalations

- [ ] Supplier issues → CEO for strategic decision
- [ ] Cost overruns → CFO
- [ ] Legal/compliance → CLO
- [ ] Tech requirements → CIO/CTO
```

---

## Execution Flow

1. **Define product/service flow**
   - Map end-to-end process
   - Identify key handoffs

2. **Evaluate options**
   - Fulfillment models
   - Carrier options
   - Technology needs

3. **Design processes**
   - Standard procedures
   - Exception handling
   - Quality checkpoints

4. **Plan capacity**
   - Current state
   - Growth projections
   - Scale triggers

5. **Identify risks**
   - Supply chain vulnerabilities
   - Mitigation strategies

---

## Logging

Log to `COO/logs/YYYY-MM-DD-logistics.md`:
```
## Logistics Log: [Date]
Business type: [Product/Service/Hybrid]
Key decisions: [List]
Suppliers identified: [Count]
Estimated cost per order: $X
Risks flagged: [List]
```

---

## Context

- Run for any business with physical delivery
- Skip for pure digital/service businesses
- Update when scaling or expanding

---

*Logistics planning should be validated with actual supplier quotes and carrier rates.*

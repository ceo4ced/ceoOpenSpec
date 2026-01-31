# cio.mcp

## Preamble

The CIO manages all Model Context Protocol (MCP) servers and tools used by the C-suite agents.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CIO/.ethics/ethics.md`
3. `.architecture/observability.md`

---

## Overview

The CIO is responsible for:
- **MCP server inventory** - What tools are available
- **MCP server health** - Are they operational
- **MCP usage tracking** - Who uses what
- **MCP security** - Access controls

The CFO is responsible for:
- **Token budgets** - How much can be spent
- **Cost allocation** - Who pays for what
- **Budget enforcement** - Stopping spend when limits hit

---

## Command Types

```
cio.mcp list                          # List all MCPs
cio.mcp status [server-name]          # Check server health
cio.mcp usage --period [7d|30d]       # Usage analytics
cio.mcp add [server-config]           # Add new MCP (requires human approval)
cio.mcp remove [server-name]          # Remove MCP (requires human approval)
```

---

## MCP Inventory

### Table: `mcp_servers`

```sql
CREATE TABLE IF NOT EXISTS `{project}.{dataset}.mcp_servers` (
  server_id STRING NOT NULL,
  business_id STRING NOT NULL,
  
  -- Server Info
  server_name STRING NOT NULL,
  server_type STRING,           -- local, remote, saas
  description STRING,
  
  -- Connection
  endpoint STRING,
  auth_method STRING,           -- api_key, oauth, none
  secret_reference STRING,      -- Secret Manager path
  
  -- Status
  status STRING DEFAULT 'active',  -- active, inactive, error
  last_health_check TIMESTAMP,
  health_status STRING,
  
  -- Access Control
  allowed_agents ARRAY<STRING>, -- Which agents can use
  requires_approval BOOL,       -- Human approval per use?
  
  -- Cost
  has_api_cost BOOL,
  cost_per_call FLOAT64,
  
  -- Meta
  added_at TIMESTAMP,
  added_by STRING,
  approved_by STRING
);
```

---

## List: `cio.mcp list`

### Output

```markdown
# MCP Server Inventory
Business: [Business Name]
Generated: [Date]

## Active Servers (7)

| Server | Type | Description | Agents | Cost | Status |
|--------|------|-------------|--------|------|--------|
| GitKraken | Local | Git operations | All | Free | 🟢 Active |
| OpenRouter | Remote | LLM routing | All | Per token | 🟢 Active |
| TikTok | Remote | Content publishing | CMO | Free* | 🟢 Active |
| BigQuery | GCP | Data warehouse | All | Usage | 🟢 Active |
| Secrets | GCP | Secret management | All | Free | 🟢 Active |
| Telegram | Remote | Human messaging | CEO, All | Free | 🟢 Active |
| NanoBanana | Remote | AI content gen | CMO | Per call | 🟢 Active |

*Platform costs separate from MCP

## Server Details

### GitKraken
- **Purpose**: Git operations (commit, push, branch)
- **Endpoint**: Local MCP
- **Auth**: None (local)
- **Tools Available**:
  - `git_status` - Check repo status
  - `git_add_or_commit` - Stage and commit
  - `git_push` - Push changes
  - `git_branch` - Branch management
  - `git_log_or_diff` - View history
- **Usage (7d)**: 145 calls
- **Cost**: Free

### OpenRouter
- **Purpose**: LLM API routing (cost optimization)
- **Endpoint**: https://openrouter.ai/api/v1
- **Auth**: API Key (Secret: openrouter-api-key)
- **Models Available**: [See model catalog]
- **Usage (7d)**: 847 calls, 2.3M tokens
- **Cost (7d)**: $47.20

### TikTok
- **Purpose**: Content publishing
- **Endpoint**: https://open.tiktokapis.com/v2
- **Auth**: OAuth 2.0
- **Tools Available**:
  - `upload_video` - Upload content
  - `publish` - Publish to feed
  - `analytics` - Get performance
- **Usage (7d)**: 12 posts
- **Cost**: Free (platform, not API)
- **Access**: CMO only

[... more servers ...]

## Inactive Servers (0)
None

## Pending Approval (1)
- Instagram Graph API - Awaiting human approval
```

---

## Status: `cio.mcp status`

Health check for specific MCP server.

### Input
```yaml
server_name: OpenRouter
include_latency_test: true
```

### Output
```markdown
# MCP Status: OpenRouter
Checked: [Timestamp]

## Health
| Check | Result | Details |
|-------|--------|---------|
| Connectivity | ✅ Pass | 45ms latency |
| Authentication | ✅ Pass | API key valid |
| Rate Limits | ✅ OK | 847/10000 requests used |
| Quota | ⚠️ Watch | $47.20 / $100.00 budget |

## Recent Errors (0)
None in last 24 hours

## Performance
| Metric | Value | Trend |
|--------|-------|-------|
| Avg Response | 1.2s | ↓ Improving |
| Success Rate | 99.8% | Stable |
| P95 Latency | 3.4s | Stable |

## Actions
- [ ] Rotate API key (recommended every 90d)
- [ ] Review rate limit allocation
```

---

## Usage: `cio.mcp usage`

Analytics on MCP usage.

### Output
```markdown
# MCP Usage Report
Period: Last 7 Days
Business: [Name]

## Summary
| Metric | Value | vs Previous |
|--------|-------|-------------|
| Total API Calls | 2,847 | +23% |
| Total Tokens | 4.2M | +18% |
| Total Cost | $89.40 | +15% |
| Unique MCPs Used | 6/7 | Same |

## Usage by Server
| Server | Calls | Tokens | Cost | Top User |
|--------|-------|--------|------|----------|
| OpenRouter | 847 | 2.3M | $47.20 | CEO (45%) |
| NanoBanana | 234 | N/A | $32.00 | CMO (100%) |
| BigQuery | 1,456 | N/A | $8.20 | All |
| TikTok | 12 | N/A | $0 | CMO |
| GitKraken | 145 | N/A | $0 | All |
| Telegram | 153 | N/A | $0 | CEO |

## Usage by Agent
| Agent | Calls | Tokens | Cost | % of Total |
|-------|-------|--------|------|------------|
| CEO | 423 | 1.1M | $28.40 | 32% |
| CMO | 312 | 890K | $45.00 | 50% |
| CFO | 156 | 432K | $8.00 | 9% |
| COO | 89 | 245K | $4.00 | 4% |
| CIO | 45 | 123K | $2.00 | 2% |
| CLO | 34 | 98K | $1.50 | 2% |
| CPO | 28 | 76K | $0.50 | 1% |
| CTO | 0 | 0 | $0 | 0% |

## Usage Trends (Daily)
```
$20 |           ▄▄
$15 |       ▄▄ ████
$10 |   ▄▄ ████████▄▄
$5  | ████████████████
    └─────────────────
      M  T  W  T  F  S  S
```

## Anomalies
- ⚠️ CMO usage spiked 150% on Wednesday (campaign generation)
- ✅ No unauthorized access detected
```

---

## Add: `cio.mcp add`

Add new MCP server (requires human approval).

### Input
```yaml
server_name: Instagram
server_type: remote
description: Instagram publishing and analytics
endpoint: https://graph.facebook.com/v18.0
auth_method: oauth
secret_reference: projects/[project]/secrets/instagram-token

allowed_agents:
  - CMO
  
has_api_cost: false
requires_approval: false  # Per-use approval
```

### Approval Required
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔌 NEW MCP SERVER REQUEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CIO requests adding new MCP server:

Server: Instagram Graph API
Type: Remote API
Purpose: Content publishing to Instagram

Access: CMO only
Cost: Free (platform costs separate)

Security:
• OAuth authentication
• Secret stored in GCP Secret Manager
• Read/write access to Instagram account

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reply:
• "APPROVE" - Add server
• "REJECT: [reason]" - Deny

⚠️ New integrations require your approval.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Security & Access Control

### Per-Server Access

```python
MCP_ACCESS_MATRIX = {
    'GitKraken': ['CEO', 'CFO', 'CMO', 'COO', 'CIO', 'CLO', 'CPO', 'CTO'],
    'OpenRouter': ['CEO', 'CFO', 'CMO', 'COO', 'CIO', 'CLO', 'CPO', 'CTO'],
    'TikTok': ['CMO'],  # Only CMO can post
    'Instagram': ['CMO'],
    'BigQuery': ['CEO', 'CFO', 'CMO', 'COO', 'CIO', 'CLO', 'CPO', 'CTO'],
    'Telegram': ['CEO'],  # CEO handles human communication
    'NanoBanana': ['CMO'],  # Content generation
}

def check_mcp_access(agent: str, server: str) -> bool:
    """Verify agent can use this MCP."""
    allowed = MCP_ACCESS_MATRIX.get(server, [])
    return agent in allowed
```

---

## Logging

All MCP operations logged:

```sql
INSERT INTO mcp_usage (
    usage_id,
    business_id,
    
    -- What
    server_name,
    tool_name,
    
    -- Who
    agent_position,
    conversation_id,
    
    -- When
    called_at TIMESTAMP,
    duration_ms INT64,
    
    -- Result
    success BOOL,
    error_message STRING,
    
    -- Cost
    tokens_used INT64,
    cost_usd FLOAT64
) VALUES (...);
```

---

*CIO manages MCP infrastructure. CFO controls the budget.*

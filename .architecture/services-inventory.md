# Services & API Inventory

## Overview

This document lists all external services and APIs required to operate a business spawned from this template.

> **⚠️ HUMAN-ONLY:** Only the Human may sign up for services, agree to terms, or enter payment information.

---

## Service Categories

### 🧠 AI / LLM Services

| Service | Purpose | API Key Required | Terms to Sign |
|---------|---------|------------------|---------------|
| **OpenRouter** | LLM routing (primary) | ✅ Yes | ⚠️ Human only |
| Anthropic (direct) | Fallback LLM | ✅ Yes | ⚠️ Human only |
| OpenAI (direct) | Fallback LLM | ✅ Yes | ⚠️ Human only |
| Google AI (Gemini) | Fallback LLM | ✅ Yes | ⚠️ Human only |

**Onboarding Input:**
```
OPENROUTER_API_KEY=sk-or-...
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_AI_API_KEY=...
```

---

### ☁️ Cloud Infrastructure

| Service | Purpose | API Key Required | Terms to Sign |
|---------|---------|------------------|---------------|
| **Google Cloud Platform** | Primary infrastructure | ✅ Service Account JSON | ⚠️ Human only |
| AWS (optional) | Backup/redundancy | ✅ Access Key + Secret | ⚠️ Human only |

**GCP Services Used:**
- BigQuery (logging, analytics)
- Cloud Functions (agent hosting)
- Pub/Sub (inter-agent messaging)
- Cloud Storage (file storage, backups)
- Secret Manager (credential storage)
- Cloud Run (dashboard hosting)

**Onboarding Input:**
```
GCP_PROJECT_ID=your-project-id
GCP_SERVICE_ACCOUNT_JSON=[paste JSON or path]
GCP_REGION=us-central1
```

---

### 💳 Payment Processing

| Service | Purpose | API Key Required | Terms to Sign |
|---------|---------|------------------|---------------|
| **Stripe** | Payment processing | ✅ Secret Key + Publishable Key | ⚠️ Human only |

**Onboarding Input:**
```
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

---

### 📧 Communication

| Service | Purpose | API Key Required | Terms to Sign |
|---------|---------|------------------|---------------|
| **Gmail / Google Workspace** | Company email | ✅ OAuth credentials | ⚠️ Human only |
| **Twilio** | Phone/SMS | ✅ Account SID + Auth Token | ⚠️ Human only |
| **Telegram** | Human-agent chat | ✅ Bot Token | ⚠️ Human only |
| Signal (optional) | Encrypted chat | Phone number | ⚠️ Human only |
| SendGrid (optional) | Transactional email | ✅ API Key | ⚠️ Human only |

**Onboarding Input:**
```
COMPANY_EMAIL=hello@yourcompany.com
GMAIL_OAUTH_CREDENTIALS=[OAuth JSON]

TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+1...

TELEGRAM_BOT_TOKEN=...
TELEGRAM_AUTHORIZED_USER_IDS=123456789,987654321
```

---

### 📱 Social Media APIs

| Platform | Purpose | API Key Required | Terms to Sign |
|----------|---------|------------------|---------------|
| **TikTok** | Content publishing | ✅ OAuth + App credentials | ⚠️ Human only |
| **Instagram** | Content publishing | ✅ Meta Business Suite | ⚠️ Human only |
| **X (Twitter)** | Content publishing | ✅ API Key + Secret | ⚠️ Human only |
| **YouTube** | Video publishing | ✅ OAuth credentials | ⚠️ Human only |
| **LinkedIn** | Business content | ✅ OAuth credentials | ⚠️ Human only |

**Onboarding Input:**
```
TIKTOK_CLIENT_KEY=...
TIKTOK_CLIENT_SECRET=...
TIKTOK_ACCESS_TOKEN=...

META_APP_ID=...
META_APP_SECRET=...
INSTAGRAM_ACCESS_TOKEN=...

TWITTER_API_KEY=...
TWITTER_API_SECRET=...
TWITTER_BEARER_TOKEN=...
TWITTER_ACCESS_TOKEN=...
TWITTER_ACCESS_TOKEN_SECRET=...

YOUTUBE_OAUTH_CREDENTIALS=[OAuth JSON]

LINKEDIN_CLIENT_ID=...
LINKEDIN_CLIENT_SECRET=...
LINKEDIN_ACCESS_TOKEN=...
```

---

### 📊 Analytics & Monitoring

| Service | Purpose | API Key Required | Terms to Sign |
|---------|---------|------------------|---------------|
| Google Analytics | Website analytics | ✅ Measurement ID | ⚠️ Human only |
| Mixpanel (optional) | Product analytics | ✅ API Key | ⚠️ Human only |
| Datadog (optional) | Infrastructure monitoring | ✅ API Key | ⚠️ Human only |

**Onboarding Input:**
```
GA_MEASUREMENT_ID=G-...
MIXPANEL_TOKEN=...
DATADOG_API_KEY=...
```

---

### 💼 Business Tools

| Service | Purpose | API Key Required | Terms to Sign |
|---------|---------|------------------|---------------|
| **QuickBooks** | Accounting | ✅ OAuth credentials | ⚠️ Human only |
| **Google Calendar** | Scheduling | ✅ OAuth credentials | ⚠️ Human only |
| Notion (optional) | Documentation | ✅ API Key | ⚠️ Human only |
| Slack (optional) | Team chat | ✅ Bot Token | ⚠️ Human only |
| GitHub | Code hosting | ✅ PAT or App | ⚠️ Human only |

**Onboarding Input:**
```
QUICKBOOKS_CLIENT_ID=...
QUICKBOOKS_CLIENT_SECRET=...
QUICKBOOKS_REALM_ID=...

GOOGLE_CALENDAR_OAUTH=[OAuth JSON]

NOTION_API_KEY=secret_...

GITHUB_PAT=ghp_...
```

---

### 🔒 Security & Identity

| Service | Purpose | API Key Required | Terms to Sign |
|---------|---------|------------------|---------------|
| Google SSO | Authentication | ✅ OAuth credentials | ⚠️ Human only |
| Auth0 (optional) | Identity management | ✅ Domain + Keys | ⚠️ Human only |

**Onboarding Input:**
```
GOOGLE_SSO_CLIENT_ID=...
GOOGLE_SSO_CLIENT_SECRET=...
```

---

### 🏦 Banking (READ ONLY)

| Service | Purpose | API Key Required | Terms to Sign |
|---------|---------|------------------|---------------|
| Plaid | Bank account read access | ✅ Client ID + Secret | ⚠️ Human only |
| Mercury API (if using) | Banking API | ✅ API Key | ⚠️ Human only |

> **⚠️ AGENTS HAVE READ-ONLY ACCESS.** No transfer capabilities.

**Onboarding Input:**
```
PLAID_CLIENT_ID=...
PLAID_SECRET=...
PLAID_ACCESS_TOKEN=...  # Per linked account

BANK_ACCOUNT_ID=...  # For display only
```

---

### 🎨 Content Generation

| Service | Purpose | API Key Required | Terms to Sign |
|---------|---------|------------------|---------------|
| Nano Banana | AI content generation | ✅ API Key | ⚠️ Human only |
| DALL-E / OpenAI Images | Image generation | ✅ (via OpenAI key) | ⚠️ Human only |
| ElevenLabs (optional) | Voice generation | ✅ API Key | ⚠️ Human only |
| Midjourney (optional) | Image generation | Discord-based | ⚠️ Human only |

**Onboarding Input:**
```
NANO_BANANA_API_KEY=...
ELEVENLABS_API_KEY=...
```

---

### 📋 Legal & Compliance

| Service | Purpose | API Key Required | Terms to Sign |
|---------|---------|------------------|---------------|
| DocuSign (optional) | Document signing | ✅ API Key | ⚠️ Human only |
| Ironclad (optional) | Contract management | ✅ API Key | ⚠️ Human only |

> **⚠️ AGENTS CANNOT SIGN.** These are for tracking and preparing documents for Human signature.

**Onboarding Input:**
```
DOCUSIGN_INTEGRATION_KEY=...
DOCUSIGN_USER_ID=...
DOCUSIGN_ACCOUNT_ID=...
```

---

### 🔍 Search & Data

| Service | Purpose | API Key Required | Terms to Sign |
|---------|---------|------------------|---------------|
| Google Search API | Web search | ✅ API Key + CSE ID | ⚠️ Human only |
| Clearbit (optional) | Company enrichment | ✅ API Key | ⚠️ Human only |
| ZoomInfo (optional) | Contact enrichment | ✅ API Key | ⚠️ Human only |

**Onboarding Input:**
```
GOOGLE_SEARCH_API_KEY=...
GOOGLE_CSE_ID=...
CLEARBIT_API_KEY=...
```

---

## Minimum Viable Setup

For a basic deployment, you need at minimum:

| Service | Why Essential |
|---------|---------------|
| OpenRouter | LLM access for all agents |
| GCP | Infrastructure (BigQuery, Functions, etc.) |
| Stripe | Payment processing |
| Gmail/Google Workspace | Company email |
| Twilio | Company phone |
| Telegram | Human-agent communication |
| GitHub | Code hosting |

**Minimum Credentials:**
```
# Essential
OPENROUTER_API_KEY=
GCP_PROJECT_ID=
GCP_SERVICE_ACCOUNT_JSON=
STRIPE_SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=
COMPANY_EMAIL=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
TELEGRAM_BOT_TOKEN=
TELEGRAM_AUTHORIZED_USER_IDS=
```

---

## Secret Manager Structure

All credentials stored in GCP Secret Manager:

```
projects/{project}/secrets/
├── openrouter-api-key
├── anthropic-api-key
├── openai-api-key
├── stripe-secret-key
├── stripe-publishable-key
├── stripe-webhook-secret
├── twilio-account-sid
├── twilio-auth-token
├── telegram-bot-token
├── telegram-authorized-ids
├── gmail-oauth-credentials
├── tiktok-credentials
├── instagram-credentials
├── twitter-credentials
├── youtube-credentials
├── linkedin-credentials
├── quickbooks-credentials
├── plaid-credentials
└── ...
```

---

## Binding Agreements

### ⚠️ HUMAN-ONLY ACTIONS

The following REQUIRE Human action:

| Action | Cannot Be Done By |
|--------|-------------------|
| Sign up for services | Any agent |
| Agree to Terms of Service | Any agent |
| Enter payment information | Any agent |
| Sign contracts | Any agent |
| Authorize bank connections | Any agent |
| Accept legal obligations | Any agent |

### Agent Capabilities

Agents CAN:
- Read data from connected services
- Make API calls (within approved scope)
- Prepare documents for Human review
- Queue items for Human approval

Agents CANNOT:
- Sign anything
- Agree to terms
- Make binding commitments
- Transfer funds
- Enter contracts

---

*All service agreements require Human signature. No exceptions.*

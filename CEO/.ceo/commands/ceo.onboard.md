# ceo.onboard

## Preamble

This command guides the Human through the business onboarding process.

**Must read before execution:**
1. `.mission/agent-governance.md`
2. `CEO/.ethics/ethics.md`
3. `.architecture/services-inventory.md`

---

## Overview

The CEO agent facilitates onboarding but **CANNOT:**
- Sign up for services
- Agree to terms
- Enter payment information
- Make any binding commitments

The CEO **CAN:**
- Guide the Human through required steps
- Collect and securely store credentials (after Human creates them)
- Verify connectivity
- Track onboarding progress

---

## Command Types

```
ceo.onboard start              # Begin onboarding wizard
ceo.onboard status             # Check onboarding progress
ceo.onboard verify [service]   # Test service connection
ceo.onboard complete           # Finalize onboarding
```

---

## Onboarding Wizard

### Phase 1: Business Identity

```
╔══════════════════════════════════════════════════════════════╗
║  ONBOARDING - PHASE 1: BUSINESS IDENTITY                    ║
╚══════════════════════════════════════════════════════════════╝

Please provide the following information:

1. Business Name: _______________________
2. Business Domain: _____________________.com
3. Your Name (Human/Chairman): _______________________
4. Your Email: _______________________
5. Your Phone: _______________________
6. Your Telegram User ID: _______________________

This information will be stored securely and used to configure
all C-suite agents.

[Save & Continue →]
```

### Phase 2: Essential Services

```
╔══════════════════════════════════════════════════════════════╗
║  ONBOARDING - PHASE 2: ESSENTIAL SERVICES                   ║
╚══════════════════════════════════════════════════════════════╝

⚠️ YOU (the Human) must sign up for these services.
I cannot do this for you - it requires agreeing to terms.

REQUIRED SERVICES:

□ 1. Google Cloud Platform
   → Go to: https://console.cloud.google.com
   → Create a new project
   → Enable billing
   → Create a service account with Owner role
   → Download the JSON key file

   Project ID: _______________________
   [Upload Service Account JSON]

□ 2. OpenRouter
   → Go to: https://openrouter.ai
   → Create account
   → Add payment method
   → Generate API key

   OpenRouter API Key: _______________________

□ 3. Stripe
   → Go to: https://dashboard.stripe.com
   → Create account (or use existing)
   → Get API keys from Developers section

   Stripe Secret Key: sk_live_______________________
   Stripe Publishable Key: pk_live_______________________

[Save & Continue →]
```

### Phase 3: Communication

```
╔══════════════════════════════════════════════════════════════╗
║  ONBOARDING - PHASE 3: COMMUNICATION                        ║
╚══════════════════════════════════════════════════════════════╝

□ 4. Google Workspace (or Gmail)
   → Your company email: hello@_______.com
   → Enable Gmail API in GCP Console
   → Create OAuth credentials

   [Upload OAuth Credentials JSON]

□ 5. Twilio (Phone)
   → Go to: https://www.twilio.com
   → Create account
   → Get a phone number
   → Get Account SID and Auth Token

   Phone Number: +1_______________________
   Account SID: AC_______________________
   Auth Token: _______________________

□ 6. Telegram Bot
   → Open Telegram, message @BotFather
   → Create new bot: /newbot
   → Get the token

   Bot Token: _______________________
   Your Telegram ID: _______________________
   
   (Get your ID from @userinfobot)

[Save & Continue →]
```

### Phase 4: Social Media (Optional)

```
╔══════════════════════════════════════════════════════════════╗
║  ONBOARDING - PHASE 4: SOCIAL MEDIA (Optional)              ║
╚══════════════════════════════════════════════════════════════╝

Skip any platforms you don't need.

□ TikTok
   → Create TikTok Developer account
   → Create app and get credentials

   Client Key: _______________________
   Client Secret: _______________________

□ Instagram / Facebook
   → Go to: https://developers.facebook.com
   → Create app for Instagram Graph API

   App ID: _______________________
   App Secret: _______________________

□ X (Twitter)
   → Go to: https://developer.twitter.com
   → Create project and app

   API Key: _______________________
   API Secret: _______________________
   Bearer Token: _______________________

□ YouTube
   → Enable YouTube Data API in GCP
   → Create OAuth credentials

   [Upload OAuth Credentials JSON]

□ LinkedIn
   → Go to: https://www.linkedin.com/developers
   → Create app

   Client ID: _______________________
   Client Secret: _______________________

[Skip] [Save & Continue →]
```

### Phase 5: Business Tools (Optional)

```
╔══════════════════════════════════════════════════════════════╗
║  ONBOARDING - PHASE 5: BUSINESS TOOLS (Optional)            ║
╚══════════════════════════════════════════════════════════════╝

□ QuickBooks
   → Go to: https://developer.intuit.com
   → Create app for QuickBooks Online

   Client ID: _______________________
   Client Secret: _______________________
   Realm ID: _______________________

□ GitHub
   → Generate Personal Access Token
   → Settings → Developer Settings → PAT

   GitHub PAT: ghp_______________________

□ Bank Account (READ-ONLY via Plaid)
   → Go to: https://plaid.com
   → Sign up for developer account
   
   ⚠️ AGENTS WILL ONLY HAVE READ ACCESS
   
   Client ID: _______________________
   Secret: _______________________

[Skip] [Save & Continue →]
```

### Phase 6: Verification

```
╔══════════════════════════════════════════════════════════════╗
║  ONBOARDING - PHASE 6: VERIFICATION                         ║
╚══════════════════════════════════════════════════════════════╝

Testing all connections...

✅ GCP Connection: SUCCESS
   - BigQuery: Ready
   - Cloud Functions: Ready
   - Secret Manager: Ready

✅ OpenRouter: SUCCESS
   - Model access verified
   - Balance: $XX.XX

✅ Stripe: SUCCESS
   - Test charge capability verified

✅ Gmail: SUCCESS
   - hello@yourcompany.com connected

✅ Twilio: SUCCESS
   - +1-XXX-XXX-XXXX ready

✅ Telegram: SUCCESS
   - @YourBotName connected
   - Your user ID authorized

❌ TikTok: NOT CONFIGURED (optional)
❌ Instagram: NOT CONFIGURED (optional)

[Finish Onboarding →]
```

### Phase 7: Complete

```
╔══════════════════════════════════════════════════════════════╗
║  ONBOARDING COMPLETE! 🎉                                     ║
╚══════════════════════════════════════════════════════════════╝

Business: [Business Name]
Domain: [domain.com]
Chairman: [Your Name]

All credentials have been stored in GCP Secret Manager.
No credentials are stored in code or files.

NEXT STEPS:

1. Complete your .mission files:
   - mission-statement.md
   - values.md
   - objective.md
   - elevator-pitch.md

2. Review ethics files for each position
   (these are HUMAN-EDITABLE ONLY)

3. Deploy agents using:
   ceo.propagate deploy all

4. Test the system:
   ceo.status

You can reach me anytime via Telegram.

Welcome to your AI-powered business! 🍌
```

---

## Credential Storage

All credentials go directly to GCP Secret Manager:

```python
def store_credential(name: str, value: str) -> bool:
    """
    Store credential in Secret Manager.
    Never log or display credential values.
    """
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{PROJECT_ID}/secrets/{name}"
    
    try:
        # Create secret if doesn't exist
        client.create_secret(
            request={
                "parent": f"projects/{PROJECT_ID}",
                "secret_id": name,
                "secret": {"replication": {"automatic": {}}}
            }
        )
    except AlreadyExists:
        pass
    
    # Add version with value
    client.add_secret_version(
        request={
            "parent": parent,
            "payload": {"data": value.encode()}
        }
    )
    
    return True
```

---

## Onboarding Status Tracking

```sql
CREATE TABLE IF NOT EXISTS onboarding_status (
    business_id STRING NOT NULL,
    
    -- Business Info
    business_name STRING,
    domain STRING,
    human_name STRING,
    human_email STRING,
    
    -- Phase Completion
    phase_1_complete BOOL DEFAULT FALSE,
    phase_2_complete BOOL DEFAULT FALSE,
    phase_3_complete BOOL DEFAULT FALSE,
    phase_4_complete BOOL DEFAULT FALSE,
    phase_5_complete BOOL DEFAULT FALSE,
    phase_6_complete BOOL DEFAULT FALSE,
    
    -- Service Status
    gcp_connected BOOL DEFAULT FALSE,
    openrouter_connected BOOL DEFAULT FALSE,
    stripe_connected BOOL DEFAULT FALSE,
    gmail_connected BOOL DEFAULT FALSE,
    twilio_connected BOOL DEFAULT FALSE,
    telegram_connected BOOL DEFAULT FALSE,
    
    -- Optional Services
    tiktok_connected BOOL DEFAULT FALSE,
    instagram_connected BOOL DEFAULT FALSE,
    twitter_connected BOOL DEFAULT FALSE,
    youtube_connected BOOL DEFAULT FALSE,
    linkedin_connected BOOL DEFAULT FALSE,
    quickbooks_connected BOOL DEFAULT FALSE,
    plaid_connected BOOL DEFAULT FALSE,
    
    -- Timestamps
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    
    PRIMARY KEY (business_id)
);
```

---

## Important Reminders

### ⚠️ HUMAN-ONLY ACTIONS

During onboarding, the CEO agent CANNOT:
- Create accounts on any service
- Accept terms of service
- Enter credit card information
- Sign any agreements
- Make any commitments

The Human must perform ALL of these actions.

### Security Notes

- All credentials stored in Secret Manager
- Never display full credentials after entry
- Mask sensitive values in logs
- Rotate credentials periodically

---

*Welcome to your business. The Human leads. The agents serve.*

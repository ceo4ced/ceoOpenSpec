# FACTORY_SETUP.md

## What This Is

**This is a TEMPLATE FACTORY, not a factory, not a product.**

This repository is a specification for how to create AI-driven businesses with C-suite agents. When you fork this repository, you get:

- A complete organizational structure for 9 AI agent positions
- Governance and compliance frameworks
- Inter-agent communication protocols
- Transparency and logging architecture
- Human-in-the-loop safeguards

## What You Do NOT Get

- Working code (this is specification, not implementation)
- A deployed product
- API keys or credentials
- A running business

---

## How to Spawn a Business from This Template

### Step 1: Fork the Repository

```bash
git clone https://github.com/[your-org]/ceoOpenSpec.git [business-name]
cd [business-name]
```

### Step 2: Replace Placeholders

Search for and replace these placeholders throughout the codebase:

| Placeholder | Replace With |
|-------------|--------------|
| `[BUSINESS_NAME]` | Your business name |
| `[COMPANY_DOMAIN]` | Your domain (e.g., nanobanana.com) |
| `[HUMAN_NAME]` | Founder/owner name |
| `[GCP_PROJECT]` | Your GCP project ID |
| `[OPENROUTER_KEY]` | Your OpenRouter API key path |
| `[PHONE]` | Company phone number |

### Step 3: Complete Mission Files

Edit these files in `.mission/`:

| File | Action |
|------|--------|
| `mission-statement.md` | Write your mission statement |
| `values.md` | Define your company values |
| `objective.md` | Set your business objectives |
| `elevator-pitch.md` | Craft your elevator pitch |

### Step 4: Configure Ethics Files

Review and customize each position's ethics file:

```
CEO/.ethics/ethics.md
CFO/.ethics/ethics.md
CMO/.ethics/ethics.md
COO/.ethics/ethics.md
CIO/.ethics/ethics.md
CLO/.ethics/ethics.md
CPO/.ethics/ethics.md
CTO/.ethics/ethics.md
EXA/.ethics/ethics.md
```

⚠️ **These files are HUMAN-EDITABLE ONLY.** Agents cannot modify their own ethics.

### Step 5: Set Up Infrastructure (Implementation Phase)

This template provides specifications. To implement:

1. **GCP Project Setup**
   - Create GCP project
   - Enable required APIs (BigQuery, Pub/Sub, Cloud Functions, Secret Manager)
   - Set up billing

2. **BigQuery Setup**
   - Create dataset
   - Run schema creation scripts from `.architecture/logging.md`

3. **Secret Manager**
   - Store all API keys
   - Configure access

4. **OpenRouter**
   - Create account
   - Add credit card (single card per CFO policy)
   - Generate API key

5. **Agent Implementation**
   - Build agents based on specifications
   - Deploy as Cloud Functions
   - Configure Pub/Sub topics

6. **Dashboard**
   - Build based on `.architecture/dashboard.md`
   - Deploy to Cloud Run

7. **Communication**
   - Set up Telegram bot
   - Configure company email
   - Set up company phone (Twilio)

---

## Template Structure

```
ceoOpenSpec/
├── .mission/                 # Company identity (TEMPLATE)
│   ├── mission-statement.md
│   ├── values.md
│   ├── objective.md
│   ├── elevator-pitch.md
│   └── agent-governance.md   # Universal agent rules
│
├── .architecture/            # Technical specifications
│   ├── logging.md            # BigQuery append-only logging
│   ├── messaging.md          # Pub/Sub inter-agent communication
│   ├── observability.md      # Monitoring and dashboards
│   ├── openrouter.md         # LLM configuration
│   ├── chairman-dashboard.md # Full transparency UI
│   ├── revenue-account.md    # Read-only bank access
│   ├── legal-jurisdiction.md # Compliance framework
│   └── ...
│
├── CEO/                      # Chief Executive Officer
│   ├── .ethics/ethics.md     # HUMAN-EDITABLE ONLY
│   ├── .ceo/commands/        # CEO slash commands
│   ├── .ceo/memory/          # Working memory
│   └── logs/
│
├── CFO/                      # Chief Financial Officer
│   ├── .ethics/ethics.md
│   ├── .cfo/commands/
│   └── ...
│
├── CMO/                      # Chief Marketing Officer
├── COO/                      # Chief Operating Officer
├── CIO/                      # Chief Information Officer
├── CLO/                      # Chief Legal Officer
├── CPO/                      # Chief Product Officer
├── CTO/                      # Chief Technology Officer
├── EXA/                      # Executive Assistant
│
└── README.md                 # This file
```

---

## Position Responsibilities

| Position | Primary Role | Key Commands |
|----------|--------------|--------------|
| **CEO** | Strategy, vision, coordination | ceo.vision, ceo.plan, ceo.propagate |
| **CFO** | Finance, budget, tokens | cfo.tokens, cfo.payments, cfo.report |
| **CMO** | Marketing, content, brand | cmo.content, cmo.tiktok, cmo.approve |
| **COO** | Operations, HR, support | coo.callcenter, coo.process |
| **CIO** | Technology, security, data | cio.mcp, cio.security, cio.redundancy |
| **CLO** | Legal, compliance | clo.jurisdiction, clo.contract |
| **CPO** | Product, roadmap | cpo.prd, cpo.roadmap, cpo.onepager |
| **CTO** | Engineering (SpecKit) | Existing SpecKit commands |
| **EXA** | Communications, scheduling | exa.email, exa.phone, exa.schedule |

---

## Key Concepts

### Human-in-the-Loop

The Chairman (Human owner) maintains control through:
- **Ethics files** that agents cannot modify
- **Approval gates** for all external actions
- **RED PHONE** for critical escalations
- **Vote of No Confidence** to remove misbehaving agents
- **Full transparency** via Chairman Dashboard

### Single Points of Control

| Control | Managed By |
|---------|------------|
| Single credit card | CFO |
| Single email (hello@company.com) | EXA |
| Single phone number | EXA |
| Single LLM router | CIO (OpenRouter) |
| Single revenue account | Read-only for agents |

### Governance Hierarchy

```
Human (Chairman)
    ↓
CEO (Strategy)
    ↓
├── CFO (Money)
├── CMO (Marketing)
├── COO (Operations)
├── CIO (Technology)
├── CLO (Legal)
├── CPO (Product)
├── CTO (Engineering)
└── EXA (Communications - NO VOTE)
```

### Compliance

- US Federal law applies to all
- State laws apply where operating
- International law applies where customers/data exist
- CLO is the compliance authority
- All agents must comply with CLO directives

---

## After Setup

### Daily Operations

1. Agents communicate via Pub/Sub
2. All actions logged to BigQuery
3. Human receives summaries via Telegram
4. Approvals requested for external actions

### Monitoring

1. Chairman Dashboard shows all activity
2. Token usage tracked in real-time
3. Costs visible by agent, by day

### Emergency Controls

1. CFO can pause non-essential agents
2. Human can invoke RED PHONE anytime
3. Vote of No Confidence removes agents
4. All agents have kill switches

---

## Checklist to Go Live

- [ ] Repository forked
- [ ] Placeholders replaced
- [ ] Mission files completed
- [ ] Ethics files customized
- [ ] GCP project created
- [ ] BigQuery schemas deployed
- [ ] API keys in Secret Manager
- [ ] OpenRouter account funded
- [ ] Agents implemented and deployed
- [ ] Dashboard running
- [ ] Telegram bot connected
- [ ] Email configured
- [ ] Phone configured
- [ ] Test all agent commands
- [ ] Human walkthrough complete

---

## Support

This is an open specification. For implementation assistance:
- Review all `.architecture/` documentation
- Follow command specifications in each position's `.commands/` directory
- Use BigQuery schemas from `.architecture/logging.md`

---

*This template gives you the spec. You build the business.*

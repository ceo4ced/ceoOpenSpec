# CEO OpenSpec - Business Factory Template

> **A template factory for spawning AI-driven businesses with C-suite agents.**

## What is CEO OpenSpec?

CEO OpenSpec is a **meta-template** that you fork to create new AI-driven businesses. Each forked repository becomes an autonomous business with C-suite AI agents operating under strict governance frameworks.

### How It Works

1. **Fork this repo** → Your new business repo is created
2. **Configure** → Set up messaging, customize governance
3. **Communicate** → Send your business idea via Signal/Telegram
4. **CEO Agent** → Gathers vision, creates business plan
5. **C-Suite Propagation** → CFO, CMO, COO, CIO, CLO, CPO work in parallel
6. **Validation Gate** → CMO validates market demand
7. **CPO Prioritizes** → Product roadmap and decisions
8. **Human Approval** → You review and approve
9. **CTO Builds** → SpecKit methodology creates the product
9. **Launch!**

---

## Repository Structure

```
ceoOpenSpec/
├── .mission/                    # Business-level governance (HUMAN ONLY)
│   ├── agent-governance.md      # Universal AI agent rules
│   ├── mission-statement.md     # Why this business exists
│   ├── values.md                # Core values
│   ├── objective.md             # Main objective
│   └── elevator-pitch.md        # Two-minute pitch
│
├── .github/
│   ├── CODEOWNERS               # Protects governance files
│   └── workflows/               # GitHub Actions (coming soon)
│
├── CEO/                          # Chief Executive Officer
│   ├── .ethics/ethics.md         # CEO governance (HUMAN ONLY)
│   ├── .ceo/                     # Commands, templates, memory
│   └── logs/                     # Activity logs
│
├── CFO/                          # Chief Financial Officer
│   ├── .ethics/ethics.md         # CFO governance (HUMAN ONLY)
│   ├── .cfo/                     # Commands, templates, memory
│   └── logs/
│
├── CMO/                          # Chief Marketing Officer
│   ├── .ethics/ethics.md         # CMO governance (HUMAN ONLY)
│   ├── .cmo/                     # Commands, templates, memory
│   └── logs/
│
├── COO/                          # Chief Operations Officer
│   ├── .ethics/ethics.md         # COO governance (HUMAN ONLY)
│   ├── .coo/                     # Commands, templates, memory
│   └── logs/
│
├── CIO/                          # Chief Information Officer
│   ├── .ethics/ethics.md         # CIO governance (HUMAN ONLY)
│   ├── .cio/                     # Commands, templates, memory
│   └── logs/
│
├── CLO/                          # Chief Legal Officer (Paralegal)
│   ├── .ethics/ethics.md         # CLO governance (HUMAN ONLY)
│   ├── .clo/                     # Commands, templates, memory
│   └── logs/
│
├── CPO/                          # Chief Product Officer
│   ├── .ethics/ethics.md         # PM Constitution (HUMAN ONLY)
│   ├── .cpo/                     # Commands, templates, memory
│   └── logs/
│
├── CTO/                          # Chief Technology Officer
│   ├── .ethics/ethics.md         # CTO non-dev ethics (HUMAN ONLY)
│   ├── .specify/                 # SpecKit (existing)
│   │   └── memory/constitution.md # Development governance
│   ├── .claude/commands/         # SpecKit commands
│   └── logs/
│
├── CXA/                          # Chief Experience Agent
│   ├── .ethics/ethics.md         # CXA governance (HUMAN ONLY)
│   ├── .cxa/                     # Commands, templates, memory
│   └── logs/
│
└── System/                       # Agent Implementation
    ├── functions/                # Cloud Functions (agents)
    │   ├── ceo/main.py          # CEO agent implementation
    │   ├── cfo/main.py          # CFO agent implementation
    │   ├── cmo/main.py          # CMO agent implementation
    │   ├── coo/main.py          # COO agent implementation
    │   ├── cio/main.py          # CIO agent implementation
    │   ├── clo/main.py          # CLO agent implementation
    │   ├── cpo/main.py          # CPO agent implementation
    │   ├── cto/main.py          # CTO agent implementation
    │   ├── cxa/main.py          # CXA agent implementation
    │   ├── packages/            # Shared code
    │   │   └── factory_core/    # BaseAgent class
    │   └── tests/               # Unit tests
    └── lib/                     # Shared libraries
        └── api_manager.py       # LLM API integration
```

---

## Governance Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                    .mission/agent-governance.md                  │
│                    UNIVERSAL AI AGENT RULES                      │
│                    (Supersedes all other rules)                  │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│               .mission/ (Other Files)                           │
│    Mission Statement | Values | Objective | Elevator Pitch      │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    .ethics/ethics.md                            │
│            Position-specific governance (per C-suite)           │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼ (CTO only)
┌─────────────────────────────────────────────────────────────────┐
│              .specify/memory/constitution.md                     │
│              Development-specific (SpecKit)                      │
└─────────────────────────────────────────────────────────────────┘
```

> ⚠️ **All governance files are HUMAN-EDITABLE ONLY. AI agents cannot modify them.**

---

## C-Suite Agents

| Position | Responsibility | Key Frameworks |
|----------|----------------|-----------------|
| **CEO** | Vision, business plan, coordination | OECD Governance, ISO 37000 |
| **CFO** | Financial planning, budgets, projections | GAAP, IRS, IFRS, AML |
| **CMO** | Marketing, validation gate, campaigns | FTC, COPPA, GDPR |
| **COO** | Operations, HR, processes | DOL, OSHA, FLSA, EEOC |
| **CIO** | Data governance, security, privacy | NIST, ISO 27001, HIPAA |
| **CLO** | Legal research, contracts (paralegal) | ABA Guidelines, UPL Rules |
| **CPO** | Product decisions, roadmap, metrics | PM Constitution, RICE/WSJF |
| **CTO** | Technology, uses SpecKit (GATED) | WCAG, Security Standards |
| **CXA** | External communication, email routing | CAN-SPAM, TCPA, CASL |

---

## Quick Start

### 1. Fork This Repository

Click "Fork" or use:
```bash
gh repo fork ceo4ced/ceoOpenSpec --clone
```

### 2. Update CODEOWNERS

Edit `.github/CODEOWNERS` and replace `@OWNER` with your GitHub username:
```
/.mission/ @your-username
```

### 3. Customize Governance

Edit the `.mission/` files to reflect your business vision:
- `mission-statement.md` - Why does your business exist?
- `values.md` - What are your non-negotiable values?
- `objective.md` - What's your primary measurable goal?
- `elevator-pitch.md` - How do you explain your business?

### 4. Configure Messaging (Coming Soon)

Set up Telegram or Signal integration for communicating with agents.

### 5. Start Your Business

Send your business idea to the CEO agent and watch the C-suite go to work!

---

## Development

### Running Tests

To run the unit tests for all C-Suite agents:

```bash
cd System/functions/tests
pip install -r requirements.txt
python -m pytest -v
```

The test suite includes 151 tests covering:
- BaseAgent initialization and command dispatch
- All 9 C-Suite agents and their commands
- Validation gate logic (CMO → CTO)
- Email routing (CXA)
- High-risk domain detection

### API Configuration

The agents use LLM integration via the APIManager:

```bash
# Set environment variables
export OPENROUTER_API_KEY="your-openrouter-key"
export OPENAI_API_KEY="your-openai-key"  # Fallback
```

The system uses OpenRouter as the primary provider with OpenAI as fallback.

---

## Key Principles

### Evidence-Based Decisions
All agent recommendations must be based on empirical evidence or published research with citations.

### Human Authority
Humans have ultimate authority. Agents are advisory, not autonomous.

### Sequential Gate
The CTO only begins after:
1. All other C-suite complete their work
2. CMO validates market demand
3. Human approves proceeding

### Transparency
All agent actions are logged. Everything is auditable.

### Regulatory Compliance
Each position operates under specific regulatory frameworks covering:
- US regulations
- EU regulations (GDPR, etc.)
- Minor protection (COPPA, etc.)
- Education (FERPA, etc.)
- Healthcare (HIPAA, etc.)
- Crypto (SEC, FinCEN, MiCA, etc.)

---

## Documentation

- [Agent Governance Mandate](.mission/agent-governance.md)
- [Factory Setup Guide](FACTORY_SETUP.md) (coming soon)
- [CEO Agent Guide](CEO/README.md) (coming soon)
- [SpecKit Documentation](CTO/.claude/commands/)

---

## Status

🚧 **Under Development**

### Completed

- [x] Governance structure (.mission, .ethics)
- [x] All C-suite ethics files (9 positions)
- [x] CODEOWNERS protection
- [x] **CEO Agent** - 6 commands (vision, plan, propagate, onboard, inquire, report)
- [x] **CFO Agent** - 6 commands (budget, tokens, payments, forecast, compliance, analyze)
- [x] **CMO Agent** - 9 commands (validate, approve, strategy, campaign, content, brand, logo, tiktok, website)
- [x] **COO Agent** - 5 commands (process, workforce, logistics, quality, callcenter)
- [x] **CIO Agent** - 6 commands (security, data, infrastructure, privacy, mcp, redundancy)
- [x] **CLO Agent** - 5 commands (compliance, contract, risk, research, jurisdiction)
- [x] **CPO Agent** - 5 commands (prd, roadmap, metrics, onepager, decide)
- [x] **CTO Agent** - 4 commands (status, plan, implement, backups) - GATED
- [x] **CXA Agent** - 4 commands (email, phone, schedule, contacts)
- [x] BaseAgent with LLM integration (OpenRouter + OpenAI fallback)
- [x] Unit tests for all agents (151 tests)

### In Progress

- [ ] Inter-agent communication protocol
- [ ] GitHub Actions orchestration
- [ ] Telegram integration
- [ ] Dashboard
- [ ] Signal integration

---

## License

[To be determined]

---

## Contributing

This is a template factory. To contribute:
1. Fork the repo
2. Make changes
3. Submit a PR
4. All governance file changes require owner approval

---

*Built with ❤️ for autonomous, ethical, AI-driven businesses.*

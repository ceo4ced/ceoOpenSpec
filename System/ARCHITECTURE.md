# System Architecture

## Overview

The CEO OpenSpec system implements a C-Suite of AI agents that collaborate to create and manage AI-driven businesses. Each agent has specific responsibilities and operates under governance frameworks.

## Core Components

### 1. BaseAgent (`packages/factory_core/agent.py`)

The foundation class for all C-Suite agents. Provides:

- **Command Dispatch**: Routes commands like `ceo.vision` to methods like `ceo_vision()`
- **LLM Integration**: `_think()` method for AI reasoning via APIManager
- **Usage Tracking**: Tracks token usage and costs per session
- **Governance Loading**: Loads ethics files from agent directories
- **JSON Logging**: Structured logging for Cloud Functions

```python
from factory_core.agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__("AGENT_ID", "Agent Role")

    def agent_command(self, payload):
        response = self._think("Analyze this...", task_type="agent_reasoning")
        return {"result": response}
```

### 2. APIManager (`lib/api_manager.py`)

Handles LLM API calls with fallback support:

- **Primary Provider**: OpenRouter (multiple model support)
- **Fallback Provider**: OpenAI
- **Task-Based Routing**: Different models for different task types
- **Usage Tracking**: Detailed token and cost tracking

Task types:
- `agent_reasoning`: Standard agent decisions
- `critical_decision`: High-stakes decisions requiring better models
- `content_generation`: Marketing/content creation
- `code_generation`: Technical implementation

## Agent Hierarchy

```
                    ┌─────────┐
                    │   CEO   │
                    └────┬────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
    │    CFO    │  │    CMO    │  │    COO    │
    └───────────┘  └─────┬─────┘  └───────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
    │    CIO    │  │    CLO    │  │    CPO    │
    └───────────┘  └───────────┘  └─────┬─────┘
                                        │
                                  ┌─────▼─────┐
                                  │    CTO    │ (GATED)
                                  └───────────┘
```

## Validation Gate

The CTO is **GATED** and cannot proceed until:

1. **CMO Validation**: `cmo.validate` returns `PROCEED` decision
2. **Human Approval**: Human creates approval file in CTO memory

The gate is checked by `CTO._check_gate_status()`:

```python
def _check_gate_status(self):
    cmo_validated = self._check_cmo_validation()  # Looks for PROCEED in CMO memory
    human_approved = self._check_human_approval()  # Looks for approval file

    return {
        "gate_open": cmo_validated and human_approved,
        "cmo_validated": cmo_validated,
        "human_approved": human_approved
    }
```

## Agent Commands

### CEO (Chief Executive Officer)
| Command | Description |
|---------|-------------|
| `ceo.vision` | Interactive vision gathering (8 questions) |
| `ceo.plan` | Generate business plan from vision |
| `ceo.propagate` | Create briefs for all C-Suite positions |
| `ceo.onboard` | Onboard human operators |
| `ceo.inquire` | Answer questions, detect escalations |
| `ceo.report` | Generate status reports |

### CFO (Chief Financial Officer)
| Command | Description |
|---------|-------------|
| `cfo.budget` | Generate budget from business plan |
| `cfo.tokens` | LLM token usage and cost report |
| `cfo.payments` | Payment integrations status |
| `cfo.forecast` | Financial projections |
| `cfo.compliance` | Financial compliance check |
| `cfo.analyze` | Custom financial analysis |

### CMO (Chief Marketing Officer)
| Command | Description |
|---------|-------------|
| `cmo.validate` | **CRITICAL GATE** - Market validation |
| `cmo.approve` | Approve proceeding after validation |
| `cmo.strategy` | Marketing strategy generation |
| `cmo.campaign` | Campaign creation and management |
| `cmo.content` | Content generation |
| `cmo.brand` | Brand guidelines |
| `cmo.logo` | Logo concept generation |
| `cmo.tiktok` | TikTok content creation |
| `cmo.website` | Website specifications |

### COO (Chief Operations Officer)
| Command | Description |
|---------|-------------|
| `coo.process` | Process documentation |
| `coo.workforce` | Workforce planning |
| `coo.logistics` | Logistics and fulfillment |
| `coo.quality` | Quality assurance framework |
| `coo.callcenter` | Call center setup |

### CIO (Chief Information Officer)
| Command | Description |
|---------|-------------|
| `cio.security` | Security framework |
| `cio.data` | Data governance |
| `cio.infrastructure` | Infrastructure recommendations |
| `cio.privacy` | Privacy assessment |
| `cio.mcp` | MCP server configuration |
| `cio.redundancy` | Redundancy planning |

### CLO (Chief Legal Officer - Digital Paralegal)
| Command | Description |
|---------|-------------|
| `clo.compliance` | Regulatory compliance assessment |
| `clo.contract` | Contract template generation |
| `clo.risk` | Legal risk assessment |
| `clo.research` | Legal topic research |
| `clo.jurisdiction` | Multi-jurisdiction analysis |

> Note: CLO operates as a digital paralegal, NOT an attorney. All output includes legal disclaimers.

### CPO (Chief Product Officer)
| Command | Description |
|---------|-------------|
| `cpo.prd` | Product Requirements Document |
| `cpo.roadmap` | Product roadmap |
| `cpo.metrics` | Product metrics framework |
| `cpo.onepager` | Feature one-pager |
| `cpo.decide` | Decision framework |

### CTO (Chief Technology Officer)
| Command | Description |
|---------|-------------|
| `cto.status` | Gate and implementation status |
| `cto.plan` | Technical plan (requires gate) |
| `cto.implement` | Implementation guidance (requires gate) |
| `cto.backups` | Backup status |

> Note: CTO is GATED until CMO validation passes AND human approves.

### CXA (Chief Experience Agent)
| Command | Description |
|---------|-------------|
| `cxa.email` | Email routing and management |
| `cxa.phone` | Phone/SMS capabilities |
| `cxa.schedule` | Calendar management |
| `cxa.contacts` | Contact management |

## File Storage

Each agent stores data in its C-Suite directory:

```
C-Suites/
└── CEO/
    ├── .ceo/
    │   ├── memory/          # Persistent memory (vision, plans)
    │   ├── commands/        # Command specifications
    │   └── templates/       # Output templates
    ├── .ethics/
    │   └── ethics.md        # Agent governance (HUMAN ONLY)
    └── logs/                # Activity logs
```

## High-Risk Domain Detection

Multiple agents detect high-risk business domains:

| Domain | Trigger Keywords | Required Actions |
|--------|------------------|------------------|
| Minors/Children | child, kid, minor, school, COPPA | CLO compliance review, CIO COPPA audit |
| Healthcare | health, medical, patient, HIPAA | CLO HIPAA review, CIO BAA requirements |
| Finance | bank, invest, crypto, trading | CLO SEC/FinCEN review, CFO AML checks |
| Education | student, teacher, FERPA, school | CLO FERPA review, CIO data handling |
| EU/GDPR | Europe, EU, GDPR, personal data | CLO GDPR review, CIO DPA requirements |

## Testing

Run unit tests:

```bash
cd System/functions/tests
pip install -r requirements.txt
python -m pytest -v
```

Current test coverage: 151 tests across all agents.

## Environment Variables

```bash
# Required
OPENROUTER_API_KEY=your-openrouter-key

# Optional (fallback)
OPENAI_API_KEY=your-openai-key

# Configuration
FACTORY_ID=your-factory-id  # Default: "development"
```

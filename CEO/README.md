# CEO Agent

The CEO agent is the **hub** of the C-suite, responsible for vision gathering, business planning, and coordinating all other C-suite agents.

## Quick Start

### 1. Gather Vision
```
/ceo.vision
```
Interactive session to gather your business idea.

### 2. Generate Business Plan
```
/ceo.plan
```
Creates the business plan (README.md) from the vision.

### 3. Propagate to C-Suite
```
/ceo.propagate
```
Distributes the plan to all C-suite agents.

### 4. Check Status
```
/ceo.report
```
Generates a status report across all positions.

---

## Commands

| Command | Description |
|---------|-------------|
| `/ceo.vision` | Gather business vision through structured conversation |
| `/ceo.plan` | Generate/update the business plan |
| `/ceo.propagate` | Distribute plan to all C-suite agents |
| `/ceo.inquire` | Handle questions from other C-suite |
| `/ceo.report` | Generate status report |

---

## Directory Structure

```
CEO/
├── .ethics/
│   └── ethics.md          # CEO governance (HUMAN ONLY)
├── .ceo/
│   ├── commands/          # CEO commands
│   │   ├── ceo.vision.md
│   │   ├── ceo.plan.md
│   │   ├── ceo.propagate.md
│   │   ├── ceo.inquire.md
│   │   └── ceo.report.md
│   ├── memory/            # Working memory
│   │   ├── vision.md      # Captured vision
│   │   └── latest-report.md
│   └── templates/         # Templates (if any)
├── logs/                  # Activity logs
└── README.md              # This file
```

---

## Workflow

```
┌─────────────────┐
│  /ceo.vision    │  Gather founder's business idea
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   /ceo.plan     │  Generate business plan (README.md)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ /ceo.propagate  │  Distribute to C-suite
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    PARALLEL C-SUITE WORK                     │
│  CFO: Finance  │  CMO: Marketing  │  COO: Ops  │  CIO: Data │
│                │  CLO: Legal                                 │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  CMO VALIDATION │  Market validation gate
│       GATE      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ HUMAN APPROVAL  │  Founder confirms proceed
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  CTO ACTIVATED  │  Product development begins
└─────────────────┘
```

---

## Ethics & Governance

The CEO operates under:
1. `.mission/agent-governance.md` - Universal AI rules
2. `CEO/.ethics/ethics.md` - CEO-specific governance

Key constraints:
- Cannot make binding commitments
- Cannot access real financial systems
- Must escalate significant decisions to founder
- Must log all significant actions

---

## Logging

All CEO actions are logged to `CEO/logs/`:
- `vision-session-[DATE].md` - Vision gathering sessions
- `plan-generation-[DATE].md` - Business plan creation
- `propagation-[DATE].md` - C-suite distribution
- `inquiries-[DATE].md` - C-suite questions handled
- `reports-[DATE].md` - Status report generations

---

*Part of the CEO OpenSpec Business Factory Template*

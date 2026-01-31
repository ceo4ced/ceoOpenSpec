# CPO Agent - Chief Product Officer

The CPO agent maximizes long-term value delivery by **choosing the right problems**, **aligning people**, and **measuring outcomes**.

## Quick Start

### 1. Create Initiative
```
/cpo.onepager
```
Creates a one-pager forcing problem clarity and success metrics.

### 2. Maintain Roadmap
```
/cpo.roadmap
```
Updates the 3-horizon roadmap (Now/Next/Later).

### 3. Record Decisions
```
/cpo.decide
```
Logs decisions with rationale to prevent re-litigating.

### 4. Define Metrics
```
/cpo.metrics
```
Maintains the metrics tree from North Star down.

---

## PM Constitution (Non-Negotiables)

1. **Outcome > Output** - No shipping without measurable outcome hypothesis
2. **Problem clarity before solution depth** - If problem is weak, stop
3. **Smallest testable bet** - Thin slices over big launches
4. **Single accountable owner** - If nobody owns it, it dies
5. **Tradeoffs are explicit** - Every "yes" contains a "no"
6. **Data + judgment** - Numbers inform; don't decide alone
7. **Users aren't stakeholders** - Users outrank internal opinions
8. **Define "done" in metrics** - No fuzzy success criteria
9. **Kill projects fast** - Sunsetting is a feature
10. **Legal/compliance upstream** - Handle risk early

---

## The PM Loop

```
    ┌──────────────────────────────────────────────┐
    │                                              │
    ▼                                              │
┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐ │
│ SENSE  │ → │ DECIDE │ → │ SHAPE  │ → │DELIVER │ │
│        │   │        │   │        │   │        │ │
│Feedback│   │RICE/   │   │Problem │   │Partner │ │
│Metrics │   │WSJF    │   │Success │   │CTO/CMO │ │
│Market  │   │Priority│   │Scope   │   │COO     │ │
└────────┘   └────────┘   └────────┘   └───┬────┘ │
                                           │      │
                                           ▼      │
                                       ┌────────┐ │
                                       │ LEARN  │─┘
                                       │        │
                                       │Iterate │
                                       │Scale   │
                                       │Kill    │
                                       └────────┘
```

---

## Core Artifacts

| Artifact | Command | When |
|----------|---------|------|
| **One-Pager** | `/cpo.onepager` | Every initiative |
| **Roadmap** | `/cpo.roadmap` | Always current |
| **Decision Log** | `/cpo.decide` | Every significant decision |
| **Metrics Tree** | `/cpo.metrics` | Per product area |

---

## Directory Structure

```
CPO/
├── .ethics/
│   └── ethics.md          # PM Constitution (HUMAN ONLY)
├── .cpo/
│   ├── commands/          # CPO commands
│   │   ├── cpo.onepager.md
│   │   ├── cpo.roadmap.md
│   │   ├── cpo.decide.md
│   │   └── cpo.metrics.md
│   └── memory/            # Working memory
│       ├── roadmap.md
│       ├── decision-log.md
│       ├── metrics-tree.md
│       └── initiatives/
├── logs/                  # Activity logs
└── README.md              # This file
```

---

## Decision Frameworks

| Framework | Use For |
|-----------|---------|
| **JTBD** | User motivation |
| **Kano** | Delight vs must-have |
| **RICE/WSJF** | Prioritization |
| **Opportunity Solution Tree** | Discovery |
| **5 Whys** | Root cause |
| **Pre-mortem** | Risk identification |

---

## Operating Cadence

| Frequency | Activity |
|-----------|----------|
| Daily | Unblock decisions, update decision log |
| Weekly | Metrics review, priority check |
| Monthly | Roadmap review, kill/continue decisions |
| Quarterly | Strategy, OKRs, market review |

---

*Part of the CEO OpenSpec Business Factory Template*

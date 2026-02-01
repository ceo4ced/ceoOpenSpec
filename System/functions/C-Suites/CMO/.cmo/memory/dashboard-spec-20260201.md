# C-Suite Dashboard Update Specification

**Generated**: 2026-02-01T01:14:57.548607Z
**Author**: CMO Agent
**Target**: All C-Suite Dashboards
**Status**: AWAITING APPROVAL

---

## Overview

This specification defines updates to the C-Suite dashboard to display:
1. **Plan Section** - Role's respective plan document with navigation
2. **Function Activity Section** - Real-time function execution tracking
3. **Agent Activity Console** - Always positioned at bottom

### Layout Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│ Header (Title, Refresh, Red Phone)                      │
├─────────────────────────────────────────────────────────┤
│ FLEXIBLE ZONE (scrollable)                              │
│  ├─ Plan Section (NEW)                                  │
│  └─ Function Activity Section (NEW)                     │
├─────────────────────────────────────────────────────────┤
│ FIXED ZONE (bottom, 200px)                              │
│  └─ Agent Activity Console (existing, repositioned)     │
└─────────────────────────────────────────────────────────┘
```

**Key Rule**: Activity Console ALWAYS stays at bottom. New sections insert above it.

---

## Component 1: Plan Section

### Purpose
Display the role's respective plan document with interactive navigation.

### Data Source
| Role | Plan Document | Title |
|------|---------------|-------|
| CEO | `C-Suites/CEO/README.md` | Business Plan |
| CFO | `C-Suites/CFO/README.md` | Financial Plan |
| CMO | `C-Suites/CMO/README.md` | Marketing Plan |
| COO | `C-Suites/COO/README.md` | Operations Plan |
| CIO | `C-Suites/CIO/README.md` | Information Plan |
| CLO | `C-Suites/CLO/README.md` | Legal Plan |
| CPO | `C-Suites/CPO/README.md` | Product Plan |
| CTO | `C-Suites/CTO/README.md` | Technical Plan |
| CXA | `C-Suites/CXA/README.md` | Experience Plan |

### Visual Design

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 📋 [ROLE] Plan                                    [Expand ↗] [Edit ✎]      │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────┬───────────────────────────────────────┐   │
│  │ Table of Contents            │ Plan Content Preview                  │   │
│  │ ──────────────────────       │ ────────────────────────────          │   │
│  │ ○ 1. Section One             │ ## 1. Section One                     │   │
│  │ ○ 2. Section Two        ───▶ │ Content preview here...               │   │
│  │ ○ 3. Section Three           │                                       │   │
│  │                              │ Status: ████████░░ 80%                │   │
│  │ Last Updated: [DATE]         │                                       │   │
│  └──────────────────────────────┴───────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Properties

| Property | Value |
|----------|-------|
| Height | 280px collapsed, expandable |
| Layout | 2-column: TOC (30%) + Content (70%) |
| Background | `#111827` |
| Border | `1px solid #1e293b` |
| Border Radius | 8px |

### Interactions
- Click TOC item → Scroll content to section
- Expand button → Full-screen modal with complete plan
- Edit button → Link to plan editor (if permitted)

---

## Component 2: Function Activity Section

### Purpose
Display real-time function execution with newest entries at top.

### Visual Design

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚡ Function Activity                              [Filter ▼] [Clear]        │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ ● NEW ENTRIES APPEAR HERE (Sorted: Newest First)                      │  │
│  ├───────────────────────────────────────────────────────────────────────┤  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │ ▼ ceo.decide()                              just now  ● RUN    │  │  │
│  │  │   ├─ Input: { decision_type: "strategic" }                    │  │  │
│  │  │   ├─ Processing: Evaluating options...                         │  │  │
│  │  │   └─ Status: ████████░░░░ 67%                                   │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │ ▶ ceo.plan()                                   2m ago  ✓ OK    │  │  │
│  │  │   Completed in 8.2s | Tokens: 1,247 | Cost: $0.024              │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Properties

| Property | Value |
|----------|-------|
| Height | 320px (scrollable) |
| Max Entries | 50 (oldest pruned) |
| Sort Order | Newest first (prepend) |
| Background | `#0f172a` |
| Border | `1px solid #1e293b` |

### Entry States

| State | Icon | Color | Badge |
|-------|------|-------|-------|
| Running | ● | `#10b981` | RUN |
| Success | ✓ | `#10b981` | OK |
| Error | ✕ | `#ef4444` | ERR |
| Pending | ○ | `#64748b` | WAIT |

---

## Component 3: Agent Activity Console (Repositioned)

### Changes from Current
- **Position**: Fixed at bottom (200px height, reduced from 400px)
- **Behavior**: New entries prepend (newest on top within console)
- **z-index**: Stays below flexible zone content

### CSS Updates

```css
.agent-activity-console {
  position: sticky;
  bottom: 0;
  height: 200px;
  flex-shrink: 0;
  z-index: 10;
}
```

---

## Layout CSS Specification

```css
/* Main content area */
.dashboard-content {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 64px); /* Account for header */
  overflow: hidden;
}

/* Flexible zone - scrollable content */
.flexible-zone {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 16px;
}

/* Fixed zone - always at bottom */
.fixed-zone {
  flex-shrink: 0;
  height: 200px;
  border-top: 1px solid #1e293b;
}

/* Plan Section */
.plan-section {
  background: #111827;
  border: 1px solid #1e293b;
  border-radius: 8px;
  height: 280px;
  display: grid;
  grid-template-columns: 30% 70%;
}

.plan-section.expanded {
  position: fixed;
  inset: 0;
  height: 100vh;
  z-index: 100;
}

/* Function Activity Section */
.function-activity {
  background: #0f172a;
  border: 1px solid #1e293b;
  border-radius: 8px;
  height: 320px;
  overflow-y: auto;
}

.function-entry {
  border: 1px solid #1e293b;
  border-radius: 4px;
  margin: 8px;
  padding: 12px;
  background: #111827;
}

.function-entry.running {
  border-color: #10b981;
  animation: pulse 2s infinite;
}

.function-entry.error {
  border-color: #ef4444;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
```

---

## Data Structures

### FunctionActivity Interface

```typescript
interface FunctionActivity {
  id: string;
  role: string;                    // CEO, CFO, etc.
  functionName: string;            // ceo.decide, cfo.budget
  status: 'running' | 'success' | 'error' | 'pending';
  timestamp: Date;
  input?: Record<string, any>;
  output?: Record<string, any>;
  error?: string;
  progress?: number;               // 0-100 if running
  estimatedRemaining?: number;     // Seconds
  duration?: number;               // Seconds if complete
  tokens?: number;
  cost?: number;                   // USD
}
```

### PlanSection Interface

```typescript
interface PlanSection {
  role: string;
  planPath: string;
  planTitle: string;
  content: string;                 // Markdown content
  lastUpdated: Date;
  sections: TableOfContentsItem[];
  completionStatus: {
    complete: number;
    inReview: number;
    draft: number;
  };
}

interface TableOfContentsItem {
  id: string;
  title: string;
  level: number;                   // 1, 2, 3 for h1, h2, h3
  anchor: string;
}
```

---

## Implementation Notes

1. **Plan Content Loading**
   - Parse markdown from `C-Suites/[ROLE]/README.md`
   - Extract headings for TOC generation
   - Render with syntax highlighting for code blocks

2. **Function Activity Updates**
   - New entries prepend to list (newest first)
   - Auto-prune when exceeding 50 entries
   - WebSocket or polling for real-time updates

3. **Activity Console Repositioning**
   - Reduce height from 400px to 200px
   - Add sticky positioning at bottom
   - Maintain existing functionality

4. **Responsive Design**
   - Mobile: Stack sections vertically
   - Tablet: Reduce plan section height to 200px
   - Desktop: Full layout as specified

---

## Approval Required

This specification requires **GREENLIGHT: DASHBOARD** from human before implementation.

---

*Generated by CMO Agent | Dashboard Specification v1.0*

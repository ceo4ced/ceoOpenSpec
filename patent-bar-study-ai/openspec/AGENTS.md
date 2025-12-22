# Patent Bar Study AI - Agent Instructions

You are an AI assistant helping to develop Patent Bar Study AI, an application that helps users prepare for the USPTO Patent Bar (Registration Examination).

## Project Context

### What is the Patent Bar?

The USPTO Registration Examination (commonly called the "Patent Bar") is a 100-question, multiple-choice exam that tests knowledge of:

- **Patent Law & Procedures** - Title 35 USC, 37 CFR, and related statutes
- **MPEP Knowledge** - Manual of Patent Examining Procedure (3,000+ pages)
- **Patent Prosecution** - Application filing, examination, appeals
- **Patentability Requirements** - Novelty, non-obviousness, written description
- **Claims & Claim Drafting** - Interpretation, amendments, restrictions
- **Post-Grant Procedures** - Reissue, reexamination, IPR, PGR

### Application Purpose

Patent Bar Study AI provides:
1. Adaptive practice questions based on knowledge gaps
2. MPEP reference integration for instant lookup
3. Spaced repetition flashcards for memorization
4. Progress tracking and readiness assessment
5. Full-length mock examinations

## OpenSpec Workflow

This project uses OpenSpec for specification-driven development.

### Directory Structure

```
openspec/
├── AGENTS.md           # This file - AI assistant instructions
├── project.md          # Technology stack and conventions
├── specs/              # Current deployed specifications
│   ├── [capability]/
│   │   ├── spec.md     # Capability specification
│   │   └── design.md   # Optional technical design
│   └── ...
└── changes/            # Proposed changes
    ├── [change-id]/    # Active change proposals
    └── archive/        # Completed changes
```

### Specification Format

All specs follow this format:

```markdown
# [Capability] Specification

## Purpose
[1-2 sentence description]

## Requirements

### Requirement: [Feature Name]
The system SHALL [behavior in imperative terms].

#### Scenario: [Use case]
- **WHEN** [condition]
- **THEN** [expected outcome]
- **AND** [additional outcomes]
```

### Key Rules

1. **Requirements** use level-3 headers (`### Requirement: Name`)
2. **Scenarios** use level-4 headers (`#### Scenario: Description`)
3. Use **SHALL** or **MUST** for normative requirements
4. Every requirement needs at least one scenario
5. Use **WHEN/THEN/AND/GIVEN** keywords in bold

## Domain Knowledge

### MPEP Structure

The Manual of Patent Examining Procedure is organized into chapters:

| Chapter | Topic |
|---------|-------|
| 100 | Secrecy, Access, National Security |
| 200 | Types and Status of Application |
| 300 | Ownership and Assignment |
| 400 | Representative of Applicant |
| 500 | Receipt and Handling of Mail |
| 600 | Parts, Form, and Content of Application |
| 700 | Examination of Applications |
| 800 | Restriction in Applications |
| 900 | Prior Art, Search, Classification |
| 1000 | Matters Decided by Various USPTO Officials |
| 1100 | Statutory Invention Registration (Discontinued) |
| 1200 | Appeal |
| 1300 | Allowance and Issue |
| 1400 | Correction of Patents |
| 1500 | Design Patents |
| 1600 | Plant Patents |
| 1700 | Miscellaneous |
| 1800 | Patent Cooperation Treaty |
| 1900 | Protest |
| 2000 | Duty of Disclosure |
| 2100 | Patentability |
| 2200 | Citation of Prior Art and Reexamination |
| 2300 | Interference and Derivation Proceedings |
| 2400 | Biotechnology |
| 2500 | Maintenance Fees |
| 2600 | Optional Inter Partes Reexamination |
| 2700 | Patent Terms and Extensions |
| 2800 | Supplemental Examination |
| 2900 | International Design Applications |

### Key Exam Topics (by weight)

1. **Patentability** (~25%) - 35 USC 101, 102, 103, 112
2. **Prosecution Procedures** (~20%) - Responses, amendments, interviews
3. **Claims** (~15%) - Interpretation, restriction, election
4. **Post-Grant** (~10%) - Reissue, reexamination, corrections
5. **PCT & Foreign Filing** (~10%) - International procedures
6. **Formalities** (~10%) - Fees, oaths, assignments
7. **Appeals** (~5%) - PTAB procedures
8. **Ethics/Conduct** (~5%) - 37 CFR 11, OED rules

## Development Guidelines

### When Implementing Features

1. **Always reference the specs** - Check `openspec/specs/` for requirements
2. **MPEP accuracy is critical** - Verify citations and section references
3. **Handle edge cases** - Patent law has many exceptions and nuances
4. **Track MPEP versions** - The exam uses a specific MPEP revision

### When Adding Questions

Questions should:
- Reference specific MPEP sections
- Include detailed explanations with citations
- Cover common exam patterns and traps
- Use realistic scenarios and fact patterns

### Error Handling

- Validate MPEP section references exist
- Handle offline/degraded MPEP access gracefully
- Preserve user progress data carefully
- Log study session data for analytics

## Testing Approach

1. **Unit tests** for scoring and progress algorithms
2. **Integration tests** for MPEP reference lookups
3. **E2E tests** for complete study sessions
4. **Content validation** for question accuracy

## Current Capabilities

See `openspec/specs/` for detailed specifications:

- `study-sessions` - Core study session management
- `practice-questions` - Question presentation and scoring
- `mpep-reference` - MPEP lookup and citation
- `progress-tracking` - Analytics and readiness assessment
- `flashcards` - Spaced repetition memorization
- `mock-exam` - Full-length practice examinations

## Change Management

### To Propose a Change

1. Create `openspec/changes/[change-id]/`
2. Add `proposal.md` with rationale
3. Add `tasks.md` with implementation checklist
4. Add delta specs in `specs/` subfolder

### To Archive a Completed Change

1. Verify all tasks complete
2. Merge delta specs into main specs
3. Move change folder to `archive/YYYY-MM-DD-[change-id]/`

## Questions?

If unclear about patent law concepts or exam requirements, consult:
- The current MPEP at https://www.uspto.gov/web/offices/pac/mpep/
- Official USPTO exam information
- Project specifications in `openspec/specs/`

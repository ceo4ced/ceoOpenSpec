# Flashcards Specification

## Purpose

Provide spaced repetition flashcard functionality for memorizing key patent law concepts, rules, deadlines, and procedures with scientifically-optimized review scheduling.

## Requirements

### Requirement: Flashcard Display

The system SHALL present flashcards in an intuitive, interactive format.

#### Scenario: Display flashcard front

- **WHEN** a flashcard is presented
- **THEN** the front (question/prompt) is displayed
- **AND** the card topic/category is shown
- **AND** a "Show Answer" action is available
- **AND** the card's due status is indicated

#### Scenario: Reveal flashcard back

- **WHEN** a user requests to see the answer
- **THEN** the back (answer) is revealed
- **AND** the front remains visible for reference
- **AND** MPEP section references are shown
- **AND** rating buttons appear for spaced repetition

#### Scenario: Display rich content

- **WHEN** a flashcard contains formatted content
- **THEN** lists, tables, and formatting are rendered
- **AND** legal citations are properly styled
- **AND** code/claim formatting is preserved

### Requirement: Spaced Repetition Algorithm

The system SHALL implement the SM-2 spaced repetition algorithm (or similar).

#### Scenario: Initial card scheduling

- **WHEN** a new flashcard is added to the user's deck
- **THEN** the ease factor is set to 2.5 (default)
- **AND** the interval is set to 1 day
- **AND** the card is immediately available for review

#### Scenario: Process review rating

- **WHEN** a user rates a card after review
- **THEN** the system accepts ratings:
  - **Again** (0) - Complete failure, reset interval
  - **Hard** (1) - Correct with difficulty, small interval increase
  - **Good** (2) - Correct with effort, normal interval increase
  - **Easy** (3) - Correct easily, large interval increase

#### Scenario: Calculate next interval (Again)

- **WHEN** a user rates "Again"
- **THEN** the interval resets to 1 day
- **AND** the ease factor decreases by 0.2 (minimum 1.3)
- **AND** the card enters "relearning" state

#### Scenario: Calculate next interval (Good)

- **WHEN** a user rates "Good"
- **THEN** the new interval = old interval × ease factor
- **AND** the ease factor remains unchanged
- **AND** intervals cap at 365 days maximum

#### Scenario: Calculate next interval (Easy)

- **WHEN** a user rates "Easy"
- **THEN** the new interval = old interval × ease factor × 1.3
- **AND** the ease factor increases by 0.15
- **AND** the card graduates faster

### Requirement: Review Session Management

The system SHALL organize flashcard reviews into effective sessions.

#### Scenario: Start review session

- **WHEN** a user starts a flashcard session
- **THEN** due cards are loaded (those with nextReview <= now)
- **AND** new cards are mixed in (configurable daily limit)
- **AND** the total session size is shown

#### Scenario: Prioritize overdue cards

- **WHEN** cards are queued for review
- **THEN** overdue cards appear first (oldest overdue first)
- **AND** new cards are interleaved
- **AND** learning/relearning cards take priority

#### Scenario: Complete review session

- **WHEN** all due cards are reviewed
- **THEN** the session summary is displayed
- **AND** cards reviewed, accuracy, and next due date are shown
- **AND** the option to continue with additional cards is offered

#### Scenario: Set daily new card limit

- **WHEN** a user configures their daily limit
- **THEN** no more than that many new cards are introduced per day
- **AND** the limit applies across all decks
- **AND** the setting persists in user preferences

### Requirement: Flashcard Deck Management

The system SHALL organize flashcards into manageable decks.

#### Scenario: Create deck

- **WHEN** a user creates a new deck
- **THEN** the deck is created with a name
- **AND** optional description and category are supported
- **AND** the deck appears in the user's deck list

#### Scenario: Organize by MPEP chapter

- **WHEN** viewing pre-built decks
- **THEN** decks are available for each major MPEP chapter
- **AND** users can select which chapters to study
- **AND** chapter decks can be combined for review

#### Scenario: Topic-based decks

- **WHEN** topic decks are available
- **THEN** decks cover major topics:
  - Patentability (101, 102, 103, 112)
  - Claims and Claim Drafting
  - Deadlines and Time Periods
  - Fees and Calculations
  - PCT Procedures
  - Appeals and PTAB
  - Post-Grant Procedures

#### Scenario: Merge decks for review

- **WHEN** a user wants combined review
- **THEN** cards from multiple decks can be reviewed together
- **AND** the source deck is indicated on each card
- **AND** statistics are tracked per deck

### Requirement: Flashcard Content

The system SHALL provide high-quality flashcard content.

#### Scenario: Display MPEP reference

- **WHEN** a flashcard has an MPEP reference
- **THEN** the section number is shown
- **AND** clicking opens the MPEP section
- **AND** the relevant text is highlighted

#### Scenario: Cover key deadlines

- **WHEN** reviewing deadline flashcards
- **THEN** cards cover critical time periods:
  - Response deadlines (1, 2, 3, 6 months)
  - Priority claim periods (12 months)
  - PCT deadlines (30/31 months)
  - Maintenance fee windows
  - Appeal periods

#### Scenario: Cover fee amounts

- **WHEN** reviewing fee flashcards
- **THEN** cards cover common fee types
- **AND** small/micro entity discounts are addressed
- **AND** fee calculation methods are explained

#### Scenario: Cover rules and procedures

- **WHEN** reviewing procedural flashcards
- **THEN** cards cover 37 CFR rules
- **AND** procedural steps are enumerated
- **AND** exceptions and special cases are noted

### Requirement: Custom Flashcards

The system SHALL allow users to create custom flashcards.

#### Scenario: Create custom card

- **WHEN** a user creates a flashcard
- **THEN** they enter front and back content
- **AND** they can add MPEP references
- **AND** they assign it to a deck
- **AND** they can add topic tags

#### Scenario: Create card from question

- **WHEN** a user wants to create a card from a missed question
- **THEN** the system suggests card content
- **AND** the question and correct answer are pre-populated
- **AND** the user can edit before saving

#### Scenario: Edit custom card

- **WHEN** a user edits their card
- **THEN** all content fields are editable
- **AND** the card's schedule is preserved
- **AND** changes are saved immediately

#### Scenario: Delete custom card

- **WHEN** a user deletes a card
- **THEN** confirmation is requested
- **AND** the card is removed from all decks
- **AND** review history is deleted

### Requirement: Flashcard Statistics

The system SHALL track detailed flashcard statistics.

#### Scenario: Track card-level stats

- **WHEN** a card is reviewed
- **THEN** the system tracks:
  - Total review count
  - Correct vs. incorrect responses
  - Current interval and ease factor
  - Last review date
  - Time to answer

#### Scenario: Track deck-level stats

- **WHEN** viewing deck statistics
- **THEN** the system shows:
  - Total cards in deck
  - Cards due today
  - Mature vs. learning cards
  - Average retention rate
  - Estimated daily review time

#### Scenario: Predict review workload

- **WHEN** viewing upcoming reviews
- **THEN** the system forecasts:
  - Cards due each day for next week
  - Estimated review time
  - Upcoming heavy review days

### Requirement: Flashcard Sync and Backup

The system SHALL reliably sync flashcard data.

#### Scenario: Sync across devices

- **WHEN** a user reviews on multiple devices
- **THEN** progress syncs in real-time
- **AND** conflicts are resolved (latest wins)
- **AND** no duplicate reviews occur

#### Scenario: Offline review

- **WHEN** a user is offline
- **THEN** due cards are available locally
- **AND** reviews are queued for sync
- **AND** syncing occurs when reconnected

#### Scenario: Export flashcard data

- **WHEN** a user exports flashcards
- **THEN** cards export in standard formats (CSV, Anki)
- **AND** review history is optionally included
- **AND** deck structure is preserved

### Requirement: Cram Mode

The system SHALL support intensive pre-exam cramming.

#### Scenario: Enable cram mode

- **WHEN** a user activates cram mode
- **THEN** normal scheduling is suspended
- **AND** cards are presented regardless of due date
- **AND** reviews don't affect long-term scheduling

#### Scenario: Cram specific topics

- **WHEN** cramming for specific topics
- **THEN** only cards from selected topics are shown
- **AND** cards can be filtered by mastery level
- **AND** weak cards are prioritized

#### Scenario: Exit cram mode

- **WHEN** a user exits cram mode
- **THEN** normal scheduling resumes
- **AND** cram session statistics are logged
- **AND** due cards are recalculated

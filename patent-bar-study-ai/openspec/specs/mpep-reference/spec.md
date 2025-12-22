# MPEP Reference Specification

## Purpose

Provide integrated access to the Manual of Patent Examining Procedure (MPEP), enabling quick lookups, semantic search, and contextual references during study sessions.

## Requirements

### Requirement: MPEP Section Lookup

The system SHALL provide direct access to MPEP sections by number.

#### Scenario: Lookup section by number

- **WHEN** a user enters an MPEP section number (e.g., "2106")
- **THEN** the system displays the full section content
- **AND** shows the section title and hierarchy
- **AND** indicates the MPEP version/revision date

#### Scenario: Lookup subsection

- **WHEN** a user enters a subsection reference (e.g., "2106.04(a)")
- **THEN** the system navigates directly to that subsection
- **AND** shows parent section context
- **AND** provides navigation to adjacent subsections

#### Scenario: Handle invalid section reference

- **WHEN** a user enters an invalid section number
- **THEN** the system indicates the section was not found
- **AND** suggests similar valid sections
- **AND** offers to search for related content

### Requirement: MPEP Search

The system SHALL provide full-text and semantic search across MPEP content.

#### Scenario: Keyword search

- **WHEN** a user searches for a keyword or phrase (e.g., "obviousness")
- **THEN** the system returns matching sections ranked by relevance
- **AND** highlights the matching terms in context
- **AND** shows the section number and title for each result

#### Scenario: Semantic search

- **WHEN** a user searches with a natural language query (e.g., "when can I combine references?")
- **THEN** the system interprets the intent
- **AND** returns conceptually relevant sections
- **AND** may not require exact keyword matches

#### Scenario: Filter search results

- **WHEN** search results are displayed
- **THEN** users can filter by MPEP chapter
- **AND** filter by content type (procedures, rules, examples)
- **AND** sort by relevance or section number

#### Scenario: Search within chapter

- **WHEN** a user searches within a specific chapter
- **THEN** results are limited to that chapter
- **AND** the search scope is clearly indicated
- **AND** option to expand to full MPEP is available

### Requirement: MPEP Navigation

The system SHALL provide intuitive navigation through MPEP structure.

#### Scenario: Browse table of contents

- **WHEN** a user opens MPEP navigation
- **THEN** the chapter-level table of contents is displayed
- **AND** chapters can be expanded to show sections
- **AND** current location is highlighted

#### Scenario: Navigate section hierarchy

- **WHEN** viewing an MPEP section
- **THEN** breadcrumb navigation shows the hierarchy
- **AND** parent and child sections are accessible
- **AND** previous/next section navigation is available

#### Scenario: Cross-reference navigation

- **WHEN** a section references another MPEP section
- **THEN** the reference is displayed as a clickable link
- **AND** hovering shows a preview of the referenced section
- **AND** clicking navigates to the full section

### Requirement: MPEP Content Display

The system SHALL display MPEP content in a readable, accessible format.

#### Scenario: Render formatted content

- **WHEN** MPEP content is displayed
- **THEN** headings, lists, and tables are properly formatted
- **AND** legal citations are clearly distinguished
- **AND** examples are visually separated from main text

#### Scenario: Display forms and figures

- **WHEN** a section includes USPTO forms or figures
- **THEN** forms are rendered with proper formatting
- **AND** figures are displayed at appropriate resolution
- **AND** form fields are labeled and explained

#### Scenario: Handle special content

- **WHEN** content includes flowcharts or decision trees
- **THEN** they are rendered as interactive elements when possible
- **AND** accessible text alternatives are provided
- **AND** zoom functionality is available

### Requirement: Contextual MPEP Access

The system SHALL provide contextual MPEP access from study features.

#### Scenario: Access from question explanation

- **WHEN** a question explanation references an MPEP section
- **THEN** the reference is a clickable link
- **AND** the relevant portion is highlighted when opened
- **AND** the user can easily return to the question

#### Scenario: Access from flashcard

- **WHEN** a flashcard references an MPEP section
- **THEN** the section can be viewed without leaving the flashcard
- **AND** the card context is preserved
- **AND** quick reference panel is available

#### Scenario: Quick reference during exam

- **WHEN** a user requests MPEP reference during a mock exam
- **THEN** access is provided consistent with exam rules
- **AND** time spent in MPEP is tracked
- **AND** usage pattern is logged for analytics

### Requirement: MPEP Bookmarks and Highlights

The system SHALL allow users to save and annotate MPEP content.

#### Scenario: Bookmark a section

- **WHEN** a user bookmarks an MPEP section
- **THEN** the bookmark is saved to their profile
- **AND** appears in their bookmarks list
- **AND** includes the section number, title, and date added

#### Scenario: Highlight text

- **WHEN** a user highlights text within MPEP content
- **THEN** the highlight is saved with position information
- **AND** appears when viewing the section again
- **AND** can be given a color or category

#### Scenario: Add annotation

- **WHEN** a user adds a note to MPEP content
- **THEN** the note is anchored to the specific location
- **AND** a visual indicator shows note presence
- **AND** the note is searchable in user's notes

### Requirement: MPEP Version Management

The system SHALL track and manage MPEP versions.

#### Scenario: Display current MPEP version

- **WHEN** viewing MPEP content
- **THEN** the revision date and version are displayed
- **AND** users are notified when updates are available
- **AND** the exam-relevant version is clearly indicated

#### Scenario: Compare versions

- **WHEN** a user wants to see what changed
- **THEN** the system can highlight differences between versions
- **AND** added, removed, and modified content is distinguished
- **AND** change summary is provided

#### Scenario: Use exam-specific version

- **WHEN** a user is preparing for a specific exam date
- **THEN** the system uses the MPEP version applicable to that exam
- **AND** warns if content may have changed
- **AND** allows toggling between versions

### Requirement: MPEP Analytics

The system SHALL track user interaction with MPEP content.

#### Scenario: Track section views

- **WHEN** a user views an MPEP section
- **THEN** the view is logged with timestamp and duration
- **AND** frequently viewed sections are identified
- **AND** this data informs study recommendations

#### Scenario: Identify knowledge gaps

- **WHEN** analyzing MPEP usage patterns
- **THEN** the system identifies sections rarely accessed
- **AND** correlates with question performance
- **AND** recommends review of under-studied sections

### Requirement: Offline MPEP Access

The system SHALL support offline access to MPEP content.

#### Scenario: Download MPEP for offline use

- **WHEN** a user requests offline access
- **THEN** the full MPEP is downloaded to local storage
- **AND** progress and storage usage are shown
- **AND** offline status is indicated in the UI

#### Scenario: Use MPEP offline

- **WHEN** the user is offline
- **THEN** all downloaded MPEP content is accessible
- **AND** search functions work on local content
- **AND** bookmarks and notes sync when reconnected

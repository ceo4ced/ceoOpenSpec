# Practice Questions Specification

## Purpose

Present practice questions to users, manage question selection algorithms, handle answer submission, and provide detailed explanations with MPEP references.

## Requirements

### Requirement: Question Display

The system SHALL present questions in a clear, exam-like format.

#### Scenario: Display multiple choice question

- **WHEN** a question is presented to the user
- **THEN** the system displays the question stem
- **AND** displays answer choices labeled A through D (or E if applicable)
- **AND** indicates the current question number and total questions
- **AND** shows session progress visually

#### Scenario: Display question with fact pattern

- **WHEN** a question includes a fact pattern or scenario
- **THEN** the system displays the fact pattern prominently
- **AND** clearly separates it from the question stem
- **AND** allows the fact pattern to be referenced while viewing answers

#### Scenario: Display questions with exhibits

- **WHEN** a question references a claim, specification, or figure
- **THEN** the system displays the exhibit inline or in a modal
- **AND** allows the exhibit to remain visible while answering
- **AND** properly formats claim text with proper indentation

### Requirement: Answer Selection and Submission

The system SHALL handle answer selection with clear feedback and confirmation.

#### Scenario: Select an answer

- **WHEN** a user clicks an answer choice
- **THEN** the choice is visually highlighted
- **AND** other choices are visually deemphasized
- **AND** the selection is saved immediately (auto-save)

#### Scenario: Change answer before submission

- **WHEN** a user selects a different answer before submitting
- **THEN** the new selection replaces the previous one
- **AND** the change is logged for analytics
- **AND** the UI updates to reflect the new selection

#### Scenario: Submit answer in practice mode

- **WHEN** a user submits an answer in practice mode
- **THEN** the system immediately reveals if the answer is correct
- **AND** displays the explanation
- **AND** shows the relevant MPEP reference
- **AND** provides a button to proceed to the next question

#### Scenario: Submit answer in timed mode

- **WHEN** a user submits an answer in timed mode
- **THEN** the system records the answer without feedback
- **AND** proceeds to the next question
- **AND** allows marking the question for review

### Requirement: Explanations and References

The system SHALL provide comprehensive explanations for all questions.

#### Scenario: Display explanation after answer

- **WHEN** an explanation is shown
- **THEN** it explains why the correct answer is correct
- **AND** explains why each incorrect answer is wrong
- **AND** includes the specific MPEP section reference
- **AND** provides a link to view the full MPEP section

#### Scenario: Explain with rule citations

- **WHEN** a question tests a specific rule or statute
- **THEN** the explanation cites the exact rule (e.g., 37 CFR 1.56)
- **AND** quotes the relevant portion
- **AND** explains how it applies to the question

#### Scenario: Handle questions with exceptions

- **WHEN** a question involves an exception to a general rule
- **THEN** the explanation clearly states the general rule
- **AND** identifies the applicable exception
- **AND** explains the conditions under which the exception applies

### Requirement: Question Selection Algorithm

The system SHALL intelligently select questions based on user performance and study goals.

#### Scenario: Select questions for new user

- **WHEN** a new user starts their first session
- **THEN** the system presents a mix of difficulty levels
- **AND** covers foundational topics first
- **AND** establishes a baseline performance profile

#### Scenario: Adaptive question selection

- **WHEN** selecting questions for an adaptive session
- **THEN** the system prioritizes topics with lowest mastery scores
- **AND** adjusts difficulty based on recent performance
- **AND** ensures coverage of all major exam topics over time

#### Scenario: Avoid question repetition

- **WHEN** selecting questions
- **THEN** recently answered questions are deprioritized
- **AND** incorrectly answered questions are scheduled for re-testing
- **AND** mastered questions appear less frequently

#### Scenario: Topic-focused selection

- **WHEN** a user requests questions on specific topics
- **THEN** all questions come from those topics
- **AND** subtopics within the selection are balanced
- **AND** difficulty progression is maintained

### Requirement: Question Flagging and Notes

The system SHALL allow users to flag questions and add personal notes.

#### Scenario: Flag question for review

- **WHEN** a user flags a question
- **THEN** the flag status is saved
- **AND** flagged questions appear in a dedicated review list
- **AND** the flag is visible when the question is encountered again

#### Scenario: Add note to question

- **WHEN** a user adds a note to a question
- **THEN** the note is saved and associated with the question
- **AND** the note appears when reviewing the question
- **AND** notes are searchable in the user's notes collection

#### Scenario: Review flagged questions

- **WHEN** a user views flagged questions
- **THEN** all flagged questions are listed with their topics
- **AND** the user can start a session with only flagged questions
- **AND** flags can be removed after review

### Requirement: Question Quality Metrics

The system SHALL track question performance metrics for quality assurance.

#### Scenario: Track question statistics

- **WHEN** a question is answered
- **THEN** the system updates:
  - Total times presented
  - Correct answer rate
  - Average time to answer
  - Skip rate

#### Scenario: Identify problematic questions

- **WHEN** a question has unusual statistics
- **THEN** the system flags it for review
- **AND** criteria include: correct rate < 20% or > 95%, high skip rate, or significantly longer answer time

### Requirement: Question Categories

The system SHALL organize questions by multiple categorization schemes.

#### Scenario: Categorize by MPEP chapter

- **WHEN** questions are organized
- **THEN** each question is tagged with primary MPEP chapter (e.g., 2100)
- **AND** secondary sections are also recorded (e.g., 2106)
- **AND** users can filter by chapter

#### Scenario: Categorize by topic

- **WHEN** questions are organized
- **THEN** each question has topic tags (e.g., "Obviousness", "Written Description")
- **AND** related topics are grouped
- **AND** topic coverage is tracked for balanced studying

#### Scenario: Categorize by difficulty

- **WHEN** questions are organized
- **THEN** each question has a difficulty rating (easy, medium, hard)
- **AND** difficulty is calibrated based on user performance data
- **AND** users can filter by difficulty level

### Requirement: Question Content Accuracy

The system SHALL ensure question content accuracy and currency.

#### Scenario: Track MPEP version

- **WHEN** a question is created or updated
- **THEN** the applicable MPEP version is recorded
- **AND** questions are flagged when the MPEP is updated
- **AND** outdated questions are reviewed for accuracy

#### Scenario: Handle rule changes

- **WHEN** a rule or procedure changes
- **THEN** affected questions are identified
- **AND** questions are updated or retired as appropriate
- **AND** historical questions are marked with effective dates
